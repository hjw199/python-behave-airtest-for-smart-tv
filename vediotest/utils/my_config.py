import os
import configparser

from vediotest.utils.my_logger import Logger

#load logger.ini
logger = Logger().getLogger(__name__)

fileDir = os.path.dirname(os.path.abspath(__file__))
mainDir = os.path.dirname(fileDir)
cfgPath = os.path.join(mainDir, 'config', 'config.ini')

class Config(object):
    def __init__(self, cfgPath=cfgPath):
        self.cfgPath = cfgPath
        assert os.path.exists(self.cfgPath), logger('config.ini not found: %s'%self.cfgPath)
        self.cfg = configparser.ConfigParser()
        self.cfg.read(cfgPath)

    def read(self, varCfgSection, varCfgName, varEnvName=None):
        if varEnvName:
            ret, var = read_environment_var(varEnvName)
            if not ret:
                 var = self.cfg.get(varCfgSection, varCfgName)
        else:
            var = self.cfg.get(varCfgSection, varCfgName)
        return var

    def readint(self, varCfgSection, varCfgName, varEnvName=None):
        var = self.read(varCfgSection, varCfgName, varEnvName)
        var = int(var)
        return var

    def readfloat(self, varCfgSection, varCfgName, varEnvName=None):
        var = self.read(varCfgSection, varCfgName, varEnvName)
        var = float(var)
        return var

    def readbool(self, varCfgSection, varCfgName, varEnvName=None):
        var = self.read(varCfgSection, varCfgName, varEnvName)
        if var.lower()=='false':
            var = False
        else:
            var = bool(var)
        return var



def read_environment_var(envName):
    try:
        var = os.environ[envName]
        logger.info('read environment-var success: %s=%s;'%(envName, var))
        ret = True
    except:
        ret = False
        var = None
        logger.warning('read environment-var failed: %s;'%envName)
    return ret, var
