from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco()
import os

# poco.adb_client.shell('input keyevent 3')
# os.system('adb shell input keyevent 3')

# home()
start_app('com.ruijie.whiteboard.lscreen')