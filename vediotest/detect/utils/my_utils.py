import cv2
import math
import numpy as np


def resizebox(img0, new_shape=(416,416), color=128):
    #img0—>img1—>img2
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)
    h0,w0,_=img0.shape
    h2,w2=new_shape
    r0, r2 = w0/h0, w2/h2
    if r0>=r2:
        w1=w2
        h1=max(round(w1/r0),1)
    else:
        h1=h2
        w1=max(round(h1*r0),1)
    dx = (w2-w1)//2
    dy = (h2-h1)//2
    img1 = cv2.resize(img0, (w1, h1), interpolation= cv2.INTER_AREA)
    
    canvas = np.full((h2, w2, 3), color).astype(np.uint8) 
    canvas[dy:dy+h1, dx:dx+w1, :]=img1
    return canvas
 
def rescale_coords(img2_shape, coords, img0_shape):
    # Rescale coords (xyxy) from img2_shape to img0_shape
    if isinstance(img0_shape, int):
        img0_shape = (img0_shape, img0_shape) 
    if isinstance(img2_shape, int):
        img2_shape = (img2_shape, img2_shape)
    h0,w0=img0_shape
    h2,w2=img2_shape
    r0, r2 = w0/h0, w2/h2
    if r0>=r2:
        w1=w2
        h1=max(round(w1/r0),1)
        scale=w1/w0
    else:
        h1=h2
        w1=max(round(h1*r0),1)
        scale=h1/h0
    dx = (w2-w1)//2
    dy = (h2-h1)//2
    coords[:, [0, 2]] -= dx
    coords[:, [1, 3]] -= dy
    coords[:,:4] /= scale
    coords[:,[0, 2]] = np.clip(coords[:,[0, 2]],a_min=0,a_max=w0)
    coords[:,[1, 3]] = np.clip(coords[:,[1, 3]],a_min=0,a_max=h0)
    return coords


def non_max_suppression(pred, conf_thres=0.5, iou_thres=0.5, method='or', multi_cls=True):
    """
    Removes detections with lower object confidence score than 'conf_thres'
    Non-Maximum Suppression to further filter detections.
    Returns detections with shape:
        (x1, y1, x2, y2, object_conf, conf, class)
    """
    # NMS methods https://github.com/ultralytics/yolov3/issues/679 'or', 'and', 'merge', 'vision', 'vision_batch'
    
    # Box constraints
    min_wh, max_wh = 2, 4096  # (pixels) minimum and maximum box width and height
    nc = pred.shape[1] - 5  # number of classes
    multi_cls = multi_cls and (nc > 1)  # allow multiple classes per anchor
    output=None
    
    pred = pred[pred[:, 4] > conf_thres]
        
    # Apply width-height constraint
    pred = pred[(pred[:, 2:4] > min_wh).all(1) & (pred[:, 2:4] < max_wh).all(1)]
    
    # If none remain process next image
    if len(pred) == 0:
        return output
    
    # Compute conf
    pred[..., 5:] *= pred[..., 4:5]  # conf = obj_conf * cls_conf

    # Box (center x, center y, width, height) to (x1, y1, x2, y2)
    box = xywh2xyxy(pred[:, :4])
    
    # Detections matrix nx6 (xyxy, conf, cls)
    if multi_cls:
        i, j = np.nonzero(pred[:, 5:] > conf_thres)
        pred = np.concatenate((box[i], np.expand_dims(pred[i, j + 5],axis=1), np.expand_dims(j.astype(np.float32),axis=1)), 1)
    else:  # best class only
        conf = pred[:, 5:].max(1)
        j = pred[:, 5:].argmax(1)
        box=box[conf>conf_thres]
        j=j[conf>conf_thres]
        conf=conf[conf>conf_thres]
        pred = np.concatenate((box, np.expand_dims(conf,axis=1), np.expand_dims(j.astype(np.float32),axis=1)), 1)

    # Filter by class
    #if classes:
        #pred = pred[(j == classes)]
    
    # Apply finite constraint(delete infinite data)
    if not np.isfinite(pred).all():
        pred = pred[np.isfinite(pred).all(1)]
        
    
    # Sort by confidence
    pred = pred[pred[:, 4].argsort()[::-1]]
    
    # All other NMS methods
    det_max = []
    cls = pred[:, -1]
    for c in np.unique(cls):
        dc = pred[cls == c]  # select class c        
        n = len(dc)
        if n == 1:
            det_max.append(dc)  # No NMS required if only 1 prediction
            continue
        elif n > 500:
            dc = dc[:500]  # limit to first 500 boxes: https://github.com/ultralytics/yolov3/issues/117

        if method == 'or':  # default
            while dc.shape[0]:
                det_max.append(dc[:1])  # save highest conf detection
                if len(dc) == 1:  # Stop if we're at the last detection
                    break
                iou = bbox_iou(dc[0], dc[1:])  # iou with other boxes
                dc = dc[1:][iou < iou_thres]  # remove ious > threshold

        elif method == 'and':  # requires overlap, single boxes erased
            while len(dc) > 1:         
                iou = bbox_iou(dc[0],dc[1:])  # iou with other boxes
                if iou.max() > 0.5:
                    det_max.append(dc[:1])
                dc = dc[1:][iou < iou_thres]  # remove ious > threshold

        elif method == 'merge':  # weighted mixture box
            while len(dc):
                if len(dc) == 1:
                    det_max.append(dc)
                    break
                i = bbox_iou(dc[0], dc) > iou_thres  # iou with other boxes   
                weights = dc[i, 4:5]
                dc[0, :4] = (weights * dc[i, :4]).sum(0) / weights.sum()
                det_max.append(dc[:1])
                dc = dc[i == 0]

        elif method == 'soft':  # soft-NMS https://arxiv.org/abs/1704.04503
            sigma = 0.5  # soft-nms sigma parameter
            while len(dc):
                if len(dc) == 1:
                    det_max.append(dc)
                    break
                det_max.append(dc[:1])
                iou = bbox_iou(dc[0], dc[1:])  # iou with other boxes
                dc = dc[1:]
                dc[:, 4] *= np.exp(-iou ** 2 / sigma)  # decay confidences
                dc = dc[dc[:, 4] > conf_thres]  # https://github.com/ultralytics/yolov3/issues/362

    if len(det_max):
        det_max = np.concatenate(det_max)  # concatenate
        output  = det_max[(-det_max[:, 4]).argsort()]  # sort

    return output

def xywh2xyxy(x):
    # Convert bounding box format from [x, y, w, h] to [x1, y1, x2, y2]
    y = np.zeros_like(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2
    y[:, 1] = x[:, 1] - x[:, 3] / 2
    y[:, 2] = x[:, 0] + x[:, 2] / 2
    y[:, 3] = x[:, 1] + x[:, 3] / 2
    return y

def bbox_iou(box1, box2, x1y1x2y2=True, GIoU=False, DIoU=False, CIoU=False):
    # Returns the IoU of box1 to box2. box1 is 4, box2 is nx4
    box2 = box2.T
    # Get the coordinates of bounding boxes
    if x1y1x2y2:  # x1, y1, x2, y2 = box1
        b1_x1, b1_y1, b1_x2, b1_y2 = box1[0], box1[1], box1[2], box1[3]
        b2_x1, b2_y1, b2_x2, b2_y2 = box2[0], box2[1], box2[2], box2[3]
    else:  # x, y, w, h = box1
        b1_x1, b1_x2 = box1[0] - box1[2] / 2, box1[0] + box1[2] / 2
        b1_y1, b1_y2 = box1[1] - box1[3] / 2, box1[1] + box1[3] / 2
        b2_x1, b2_x2 = box2[0] - box2[2] / 2, box2[0] + box2[2] / 2
        b2_y1, b2_y2 = box2[1] - box2[3] / 2, box2[1] + box2[3] / 2

    # Intersection area
    inter = np.clip((np.minimum(b1_x2, b2_x2) - np.maximum(b1_x1, b2_x1)),a_min=0,a_max=None)*\
            np.clip((np.minimum(b1_y2, b2_y2) - np.maximum(b1_y1, b2_y1)),a_min=0,a_max=None)
    
    # Union Area
    w1, h1 = b1_x2 - b1_x1, b1_y2 - b1_y1
    w2, h2 = b2_x2 - b2_x1, b2_y2 - b2_y1
    union = (w1 * h1 + 1e-16) + w2 * h2 - inter

    iou = inter / union  # iou
    if GIoU or DIoU or CIoU:
        cw = np.maximum(b1_x2, b2_x2) - np.minimum(b1_x1, b2_x1)  # convex (smallest enclosing box) width
        ch = np.maximum(b1_y2, b2_y2) - np.minimum(b1_y1, b2_y1)  # convex height
    if GIoU:  # Generalized IoU https://arxiv.org/pdf/1902.09630.pdf
        c_area = cw * ch + 1e-16  # convex area
        return iou - (c_area - union) / c_area  # GIoU
    if DIoU or CIoU:  # Distance or Complete IoU https://arxiv.org/abs/1911.08287v1
        # convex diagonal squared
        c2 = cw ** 2 + ch ** 2 + 1e-16
        # centerpoint distance squared
        rho2 = ((b2_x1 + b2_x2) - (b1_x1 + b1_x2)) ** 2 / 4 + ((b2_y1 + b2_y2) - (b1_y1 + b1_y2)) ** 2 / 4
        if DIoU:
            return iou - rho2 / c2  # DIoU
        elif CIoU:  # https://github.com/Zzh-tju/DIoU-SSD-pytorch/blob/master/utils/box/box_utils.py#L47
            v = (4 / math.pi ** 2) * np.power(np.arctan(w2 / h2) - np.arctan(w1 / h1), 2)
            alpha = v / (1 - iou + v)
            return iou - (rho2 / c2 + v * alpha)  # CIoU
    return iou

def load_classes(path):
    # Loads *.names file at 'path'
    with open(path, 'r') as f:
        names = f.read().split('\n')
    return list(filter(None, names))  # filter removes empty strings (such as last line)