from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco()
import os

# poco.adb_client.shell('input keyevent 3')
# os.system('adb shell input keyevent 3')

# home()
start_app('com.netease.nie.yosemite')
# stop_app('com.ruijie.whiteboard.cloudfile.screen')

# SOFT_DICT = {
#     # "登录软件" : 'adb shell am start -n com.ruijie.login.server/com.ruijie.login.server.ui.login.LoginActivity',
#     "登录软件" : 'com.ruijie.login.server',
#     "云资料夹" : 'com.ruijie.whiteboard.cloudfile.screen',
#     "云白板" : 'com.ruijie.whiteboard.lscreen',
# }

# for i in SOFT_DICT:
#     print(i)