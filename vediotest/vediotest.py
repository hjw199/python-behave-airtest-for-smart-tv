from vediotest.my_recorder import *
from moviepy.editor import *
import cv2
import numpy as np
from vediotest.detect.my_detector import YoloDetector
from vediotest.audio.my_detector import AudioDetector
import os
def vediotest(ip,savDir,recordTime):
    #录制视频
    vedioresult = 0
    voiceresult = 0
    reco=Recorder(ip,savDir,recordTime)
    reco.record()
    vet,videoPath,aet,audioPath = reco.read(audio=True)
    print ( vet,videoPath,aet,audioPath)
    if aet:
        ad =AudioDetector()
        reta, ra = ad.start(audioPath)
        if reta:
            if ra > 50 :
                print("检测到校验音频")
                voiceresult = 1
            else:
                print("未检测到校验音频")
                voiceresult = 0

        else:
            print("校验音频失败")
            voiceresult = -1
    else:
        print("录制音频失败")
        voiceresult = -2
    if vet:
        # 读取视频文件 
        videoCapture = cv2.VideoCapture(videoPath)
        #每秒读取一帧
        success, frame = videoCapture.read()
        i = 0
        timeF = 25
        j=0
        while success :
            i = i + 1
            if (i % timeF == 0):
                j = j + 1
                # save_image(frame,'./results/',j)
                imgPath = savDir+'/' +str(j)+ '.jpg'
                cv2.imwrite(imgPath,frame)
                yd = YoloDetector()
                img = cv2.imread(imgPath)
                results = yd.start(img)
                if results:
                    vedioresult=vedioresult+1
                    print("img test success, result: ", results)
                #print('save image:',j)
            success, frame = videoCapture.read()
        if vedioresult>0:
            print("检测到校验视频")
        else:
            print("未检测到校验视频")
    else:
        print("录制视频失败")
        vedioresult = -2
    assert vedioresult and voiceresult

def voicetest(ip,savDir,recordTime):
    #录制视频
    reco=Recorder(ip,savDir,recordTime)
    reco.record()
    vet,videoPath,aet,audioPath = reco.read(audio=True)
    if aet:
        ad =AudioDetector()
        reta, ra = ad.start(audioPath)
        if reta:
            if ra > 50 :
                print("检测到校验音频")
                assert True
            else:
                print("未检测到校验音频")
                assert False

        else:
            print("校验音频失败")
            assert False
    else:
        print("录制音频失败")
        assert False