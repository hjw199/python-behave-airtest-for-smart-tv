from airtest.core.api import *
from config.config import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

connect_device('android:///' + Android_Serial_No)

def before_all(context):
    # connect_device('android:///' + Android_Serial_No)
    # context.poco = AndroidUiautomationPoco()
    pass


def after_all(context):
    pass