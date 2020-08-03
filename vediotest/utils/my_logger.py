import os
import platform
import logging 
import logging.config
import configparser

fileDir = os.path.dirname(os.path.abspath(__file__))
mainDir = os.path.dirname(fileDir)
logCfgPath = os.path.join(mainDir, 'config', 'logger.ini')

class Logger(object):
    def __init__(self, logCfgPath=logCfgPath):
        self.logCfgPath = logCfgPath
        assert os.path.exists(self.logCfgPath), print('logger.ini not found: %s'%self.logCfgPath)
        self.set_logCfg()
        logging.config.fileConfig(self.logCfgPath)

    
    def set_logCfg(self):
        logname='run.log'
        logSavDir=os.path.join(mainDir, 'logs','logs')
        os.makedirs(logSavDir, exist_ok=True)

        cfg = configparser.ConfigParser()
        cfg.read(self.logCfgPath)
        args = cfg.get('handler_fileHandler','args')

        argsList = args.split(',')
        #logname=os.path.split(argsList[0][2:-1])[1]
        if platform.system()=='Windows':
            logPath = os.path.join(logSavDir, logname).replace('\\','\\\\')
        elif platform.system()=='Linux':
            logPath = os.path.join(logSavDir, logname)
        
        argsList[0]='(\''+logPath+'\''
        argsNew = ','.join(argsList)
        cfg.set('handler_fileHandler','args',argsNew)
        with open (self.logCfgPath,'w') as f:
            cfg.write(f)

    def getLogger(self, name):
        return logging.getLogger(name)
