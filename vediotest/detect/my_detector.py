import warnings
warnings.filterwarnings("ignore")

import os
import glob
import cv2
import numpy as np

# import onnxruntime

from vediotest.utils.my_config import Config
from vediotest.utils.my_logger import Logger
from vediotest.detect.utils.my_utils import *

fileDir = os.path.dirname(os.path.abspath(__file__))
mainDir = os.path.dirname(fileDir)
modelDir = os.path.join(mainDir, 'model', 'detect')

logger = Logger().getLogger(__name__)

#load config.ini
cfg = Config()
version = cfg.read('detect', 'version')
useHequ = cfg.readbool('detect', 'use_hequ')

class YoloDetector(object):
    def __init__(self, version=version, confThre=None, iouThre=None, info=True, useHequ=useHequ):
        self.version = version
        self.useHequ = useHequ
        self.fileDir = os.path.dirname(__file__)
        self.loadDir = os.path.join(modelDir,self.version)

        self.load_model()
        self.load_class()
        self.load_config(confThre, iouThre)
        logger.info('detect-info: version={0}, model-name={1}, confThre={2}, iouThre={3}, useHequ={4}'.format(self.version, self.modelname, self.conf_thres, self.iou_thres, self.useHequ))
        #self.info={'version'=}

    def load_model(self):
        assert len(glob.glob(os.path.join(self.loadDir,'*.onnx')))==1
        weightPath = glob.glob(os.path.join(self.loadDir,'*.onnx'))[0]
        
        # self.sess = onnxruntime.InferenceSession(weightPath, None)
        self.modelname=os.path.splitext(os.path.split(weightPath)[1])[0]
    
    def load_class(self):
        assert len(glob.glob(os.path.join(self.loadDir,'*.names')))==1
        namePath = glob.glob(os.path.join(self.loadDir,'*.names'))[0]

        self.classes = load_classes(namePath)

    def load_config(self, confThre, iouThre):
        assert len(glob.glob(os.path.join(self.loadDir,'*.ini')))==1
        cfgPath = glob.glob(os.path.join(self.loadDir,'*.ini'))[0]
        #print(cfgPath)
        cfg = Config(cfgPath)
        self.img_height = cfg.readint('params','img_height')
        self.img_width  = cfg.readint('params','img_width') 
        self.fill_color = cfg.readint('params','fill_color')
        self.nms_method = cfg.read('params','nms_method')
        if confThre==None:
            self.conf_thres = cfg.readfloat('params','conf_thres')
        else:
            self.conf_thres = confThre
        if iouThre==None:
            self.iou_thres  = cfg.readfloat('params','iou_thres')
        else:
            self.iou_thres = iouThre

        self.img_size = (self.img_height, self.img_width) 

    def preprocess(self, img0, useHequ=True):
        if useHequ:
            img0 = self.histogram_equalization(img0)
        # Padded resizez
        img = resizebox(img0, new_shape=self.img_size)
        
        # Normalize RGB
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, hwc to chw
        img = img[np.newaxis,:]
        img = np.ascontiguousarray(img, dtype=np.float32)  # uint8 to float32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        return img
    
    def histogram_equalization(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=200, tileGridSize=(10,10))
        equ = clahe.apply(img)
        equ = cv2.cvtColor(equ, cv2.COLOR_GRAY2BGR)
        return equ

    def predict(self, img, img0):
        _,_,h,w=img.shape
        # Get detections
        preds = self.sess.run([], {self.sess.get_inputs()[0].name: img})
        pred = np.concatenate((preds[1],np.ones((preds[0].shape[0],1)),preds[0]),axis=1)
        pred[:,[0,2]]*=w
        pred[:,[1,3]]*=h
        det = non_max_suppression(pred, conf_thres=self.conf_thres, iou_thres=self.iou_thres, method=self.nms_method, multi_cls=False)

        result=[]
        if det is not None and len(det) > 0:
            # Rescale boxes from 416 to true image size
            det[:,:4] = rescale_coords((h,w), det[:,:4], img0.shape[:2]).round()
            # Draw bounding boxes and labels of detections
            for xMin,yMin, xMax, yMax, cls_conf, cls_id in det:
                result.append({
                    'bbox': [int(xMin), int(yMin), int(xMax), int(yMax)], 
                    'class_score':cls_conf,
                    'class_id':int(cls_id),
                    'class_name':self.classes[int(cls_id)]
                })
        return result

    def start(self, img0):#img0 is BGR
        img = self.preprocess(img0, useHequ=self.useHequ)
        result = self.predict(img, img0)
        #if self.useHequ and len(result)==0:
            #img = self.preprocess(img0，useHequ=True)
            #result = self.predict(img, img0)
        return result
