from airtest.core.api import *
from config.config import *
# from poco.drivers.android.uiautomation import AndroidUiautomationPoco

connect_device('android:///' + Android_Serial_No)
# poco = AndroidUiautomationPoco()

def before_all(context):
    pass

def after_all(context):
    pass

def after_scenario(context,scenario):
    time.sleep(1)
