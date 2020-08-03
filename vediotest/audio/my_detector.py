#import warnings
#warnings.filterwarnings("ignore")

import os
import sys
import platform
import subprocess as sp

from vediotest.utils.my_logger import Logger
from vediotest.utils.my_config import Config

fileDir = os.path.dirname(os.path.abspath(__file__))

#load logger.ini
logger = Logger().getLogger(__name__)

class AudioDetector():
    def __init__(self):
        self.load_config()

    def load_config(self):
        #load config.ini
        cfg = Config().cfg
        self.audioModel = cfg.get('audio', 'model')
        if self.audioModel=='xf':
            if platform.system()=='Windows':
                self.analysis = self.analysis_xf_win
                self.ffmpegPath = os.path.join(fileDir,'ffmpeg.exe')
            elif platform.system()=='Linux':
                self.analysis = self.analysis_xf_linux
                self.ffmpegPath = 'ffmpeg'
            self.audioExt='pcm'
            self.cal_result=self.cal_result_xf

        elif self.audioModel=='hh':
            if platform.system()=='Windows':
                self.analysis = self.analysis_hh_win
                self.ffmpegPath = os.path.join(fileDir,'ffmpeg.exe')
            elif platform.system()=='Linux':
                self.analysis = self.analysis_hh_linux
                self.ffmpegPath = 'ffmpeg'
            self.audioExt='wav'
            self.cal_result=self.cal_result_hh

        else:
            logger.error('audioModel: %s is not supported'%self.audioModel)


    
    def audio_format_convert(self, audioPath, ext):
        pcmPath=os.path.splitext(audioPath)[0]+'.'+ext
        cmd_topcm=[self.ffmpegPath,
                         '-y',#
                         '-v', 'quiet',#不打印ffmpeg的log
                         '-i', audioPath,
                         '-ac',str(1),
                         '-ar', '16000',
                         '-acodec', 'pcm_s16le',
                         '-f', 's16le',
                         pcmPath,
                         ]
        
        try:
            sp.check_call(cmd_topcm,
                          shell=False,
                          stdin = sp.PIPE,
                          stdout = sp.PIPE
                          )
        except Exception as err:
            logger.error('convert to %s failed'%ext, exc_info=1)
            ret=False
        else:
            ret=True
            logger.info('convert to %s completed: %s'%(ext, audioPath))
        return ret, pcmPath

    def analysis_xf_linux(self, audioPath):
        exePath=os.path.join(fileDir, self.audioModel, 'linux', 'bin', 'scp_awake.sh')
        cmd=[exePath,
             audioPath,
            ]
        self.p=sp.Popen(cmd,
                        shell=Flase,
                        stdin = sp.PIPE,
                        stdout = sp.PIPE
                        )
        self.p.wait()
        output=self.p.stdout.read()
        self.p.kill()
        return str(output, encoding="utf-8")

    def analysis_xf_win(self, audioPath):
        exePath=os.path.join(fileDir, self.audioModel, 'windows', 'bin', 'src_hub.exe')
        awakePath=os.path.join(fileDir, self.audioModel, 'windows', 'bin', 'scp_awake.exe')
        cmd=[exePath,
             '-e', awakePath,
             audioPath,
            ]
        self.p=sp.Popen(cmd,
                        shell=False,
                        stdin = sp.PIPE,
                        stdout = sp.PIPE
                        )
        self.p.wait()
        output=self.p.stdout.read()
        self.p.kill()
        return str(output, encoding="utf-8")

    def analysis_hh_win(self, audioPath):
        exePath=os.path.join(fileDir, self.audioModel, 'windows', 'detect.exe')
        cmd=[exePath,
             audioPath,
            ]
        self.p=sp.Popen(cmd,
                        shell=False,
                        stdin = sp.PIPE,
                        stdout = sp.PIPE
                        )
        self.p.wait()
        output=self.p.stdout.read()
        self.p.kill()
        return str(output, encoding="utf-8").rstrip('\r\n')

    def analysis_hh_linux(self, audioPath):
        exePath=os.path.join(fileDir, self.audioModel, 'linux', 'detect')
        cmd=[exePath,
             audioPath,
            ]
        self.p=sp.Popen(cmd,
                        shell=False,
                        stdin = sp.PIPE,
                        stdout = sp.PIPE
                        )
        self.p.wait()
        output=self.p.stdout.read()
        self.p.kill()
        return str(output, encoding="utf-8").rstrip('\r\n')

    def cal_result_xf(self, result):
        result=int(float(result))
        if result<=3000 and result>=0 :
            result=int(result/30)
            ret=True
        elif result==-1:
            ret=True
        else:
            ret=False
        return ret, result

    def cal_result_hh(self, result):
        try:
            result=int(float(result))
            if result<=100 and result>=0 :
                ret=True
            else:
                ret=False
        except:
            ret = False
            logger.error('audio analysis failed: %s'%result, exc_info=1)
        return ret, result

    def start(self, audioPath):
        ext=os.path.splitext(audioPath)[1][1:]#分离文件与扩展名后取扩展名（例wav）
        if ext!=self.audioExt:
            ret, audioPath = self.audio_format_convert(audioPath, self.audioExt)
            if not ret:
                return ret, None
        try:
            result = self.analysis(audioPath)
            ret, result = self.cal_result(result)
        except:
            ret=False
            result=-17
            logger.error('audio analysis failed', exc_info=1)
        return ret, result

