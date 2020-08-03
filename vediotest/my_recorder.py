import os
import sys
import time
from threading import Thread
import subprocess as sp

# import the Queue class from Python 3
if sys.version_info >= (3, 0):
    from queue import Queue, LifoQueue
# otherwise, import the Queue class for Python 2.7
else:
    from Queue import Queue, LifoQueue

from vediotest.utils.my_logger import Logger
logger = Logger().getLogger(__name__)

fileDir = os.path.dirname(os.path.abspath(__file__))
mainDir = os.path.dirname(fileDir)
ttfPath = os.path.join(fileDir,'arial.ttf')

import platform
if platform.system()=='Windows':
    ffmpegPath = os.path.join(fileDir,'ffmpeg.exe')
elif platform.system()=='Linux':
    ffmpegPath = 'ffmpeg'
else:
    logger.error('%s is not supported'%platform.system())

class Recorder(object):
    def __init__(self, ip, savDir, recordTime, videoShape=None, timeStamp=False, recordMode=None, queueSize=256):
        self.savDir=savDir
        self.recordTime=recordTime
        self.recordMode=recordMode
        self.cmd=[ffmpegPath,
                  '-y',#
                  '-v', 'quiet',#不打印ffmpeg的log
                  '-rtsp_transport','tcp',
                  '-i',ip,
                  '-t',str(self.recordTime),
                  '-vcodec', 'copy', #'libx264',
                  '-acodec', 'copy',
                  '-f', 'mp4',
                 ]
        if videoShape is not None:
            self.cmd.append('-s')
            self.cmd.append('%d*%d'%(videoShape[0],videoShape[1]))
        if timeStamp:
            self.cmd.append('-vf')
            self.cmd.append('drawtext=expansion=strftime:fontcolor=yellow:fontsize=50:text=%Y-%m-%d %H-%M-%S')

        self.Q = Queue(maxsize=queueSize)

    def record(self):
        self.extraStop=False
        self.savPath = self.get_savPath()
        hour_start = self.savPath2hour(self.savPath)
        logger.info('record start: %s'%self.savPath)

        cmd_record = self.cmd.copy()
        cmd_record.append(self.savPath)

        
        self.p=sp.Popen(cmd_record,
                        shell=False,
                        stdin = sp.PIPE,
                        stdout = sp.PIPE,
                        stderr = sp.PIPE,
                        #universal_newlines=True, 
                       )

        tStart=time.time()
        timeout=self.recordTime+7
        while True:
            if self.p.poll() is not None:
                if os.path.exists(self.savPath):
                    self.Q.put([True, self.savPath])
                    logger.info('record completed: %s'%self.savPath)
                else:
                    self.Q.put([False, self.savPath])
                    logger.info('record failed: %s'%self.savPath)
                break
            if self.extraStop:
                break
            if self.recordMode=='sharp' and time.localtime().tm_sec == 0 and time.localtime().tm_min == 0 and time.localtime().tm_hour!=hour_start:
                self.stop()
                break
            if time.time()-tStart>timeout:
                logger.warning('record timeout: %s'%self.savPath)
                self.stop()
                break
        self.Q.task_done()
        return
    
    def stop(self):
        try:
            self.p.communicate(input=b'q', timeout=7)
        except Exception as err:
            logger.warning('quit ffmpeg failed', exc_info=1)
            self.Q.put([False, None])
        else:
            if os.path.exists(self.savPath):
                self.Q.put([True, self.savPath])
                logger.info('record completed: %s'%self.savPath)
            else:
                self.Q.put([False, self.savPath])
                logger.info('record failed: %s'%self.savPath)
        finally:
            self.p.kill()
        self.extraStop=True

    def split_audio(self, videoPath, audioExt='wav'):
        audioPath = os.path.splitext(videoPath)[0]+'.'+audioExt
        cmd_split_audio=[ffmpegPath,
                         '-y',#
                         '-v', 'quiet',#不打印ffmpeg的log
                         '-i',videoPath,
                         '-ac',str(1),
                         '-ar', '16000',
                         '-acodec', 'pcm_s16le',
                         ]
        if audioExt=='pcm':
            cmd_split_audio.append('-f')
            cmd_split_audio.append('s16le')

        cmd_split_audio.append(audioPath) 

        try:
            sp.check_call(cmd_split_audio,
                          shell=False,
                          stdin = sp.PIPE,
                          stdout = sp.PIPE
                          )
        except Exception as err:
            logger.error('split audio failed', exc_info=1)
            ret=False
        else:
            ret=True
            logger.info('split completed: %s'%audioPath)
        return ret, audioPath

    def get_savPath(self):
        os.makedirs(self.savDir, exist_ok=True)
        t=time.time()
        filename0=time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(t))
        filename1=(t-int(t))*1000
        filename = '%s-%03d.mp4'%(filename0,filename1)
        savPath=os.path.join(self.savDir, filename)
        return savPath

    def savPath2hour(self, savPath):
        videoname = os.path.split(savPath)[1]
        filename = os.path.splitext(videoname)[0]
        t=filename.split('-')
        return int(t[3])

    def start(self):
        t1=Thread(target=self.record, args=())
        t1.setDaemon(True)
        t1.start()
        return self
    
    def read(self, audio=False, audioExt='wav'):
        try:
            retV, videoPath = self.Q.get(timeout=self.recordTime+20)
        except Exception as err:
            logger.error('get record queue failed', exc_info=1)
            retV, videoPath = False, None

        if not audio:
            return retV, videoPath

        if retV:
           retA, audioPath = self.split_audio(videoPath, audioExt=audioExt)
        else:
           retA, audioPath=False, None

        return retV, videoPath, retA, audioPath

    def len(self):
        return self.Q.qsize()

