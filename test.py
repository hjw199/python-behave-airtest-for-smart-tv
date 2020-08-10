from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco()
import os
from airtest.core.android.minitouch import *
from airtest.core.android.base_touch import *
import random
from mappings import *
from airtest.core.cv import Template, TargetPos
# poco.adb_client.shell('input keyevent 3')
# os.system('adb shell input keyevent 3')

# home()
# start_app('com.netease.nie.yosemite')
# stop_app('com.ruijie.whiteboard.cloudfile.screen')

# SOFT_DICT = {
#     # "登录软件" : 'adb shell am start -n com.ruijie.login.server/com.ruijie.login.server.ui.login.LoginActivity',
#     "登录软件" : 'com.ruijie.login.server',
#     "云资料夹" : 'com.ruijie.whiteboard.cloudfile.screen',
#     "云白板" : 'com.ruijie.whiteboard.lscreen',
# }

# for i in SOFT_DICT:
#     print(i)
# while True:
#     multitouch_event = []
#     x = random.randint(1,1920)
#     multitouch_event.append(DownEvent((x, 1080), 0))
#     multitouch_event.append(MoveEvent((x,850),0))
#     # multitouch_event.append(SleepEvent(1))
#     multitouch_event.append(UpEvent(0))
#     device().minitouch.perform(multitouch_event)
#     touch((100,100))
#     time.sleep(1.0)


# poco.adb_client.shell('am start -n com.ruijie.launcher20200520/com.ruijie.launcher20200520.launcher.LauncherActivity')
# # home()
# touch((100,100))
# time.sleep(0.5)
# multitouch_event = []
# multitouch_event.append(DownEvent((random.randint(1,1920), 1080), 0))
# multitouch_event.append(MoveEvent((random.randint(1,1920),900),0))
# multitouch_event.append(UpEvent(0))
# device().minitouch.perform(multitouch_event)

# img = location_img("关闭正在运行应用")
# resolution_x = poco.get_screen_size()[0]
# resolution_y = poco.get_screen_size()[1]
# while True:
#     try:
#         touch(Template(img, record_pos=None, resolution=(resolution_x, resolution_y)))
#     except:
#         break
# # touch(Template(img, record_pos=None, resolution=(resolution_x, resolution_y)))


# multitouch_event = []
# x = random.randint(1,1920)
# multitouch_event.append(DownEvent((x, 1080), 0))
# multitouch_event.append(MoveEvent((x,900),0))
# multitouch_event.append(UpEvent(0))
# device().minitouch.perform(multitouch_event)

# cmd = DownEvent((random.randint(1,1920), 1080), 0).getcmd
# print(cmd)



def existsimg(image_path):
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    query = Template(image_path, target_pos=TargetPos.MID, resolution=(resolution_x, resolution_y),rgb = True)
    try:
        pos = loop_find(query)
    except Exception as e:
        return False
    else:
        return pos


# img = location_img("快速登录图片")
# t = existsimg(img)
# print("111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
# print(t)

# multitouch_event = []
# multitouch_event.append(DownEvent((random.randint(1,1920), 1080), 0))
# multitouch_event.append(MoveEvent((random.randint(1,1920),900),0))
# multitouch_event.append(UpEvent(0))
# device().minitouch.perform(multitouch_event)
# img = location_img("关闭正在运行应用")
# resolution_x = poco.get_screen_size()[0]
# resolution_y = poco.get_screen_size()[1]
# while True:
#     if existsimg(img):
#         touch(Template(img, record_pos=None, resolution=(resolution_x, resolution_y)))
#     else:
#         break

# multitouch_event = []
# x = random.randint(1,1920)
# multitouch_event.append(DownEvent((x, 1080), 0))
# multitouch_event.append(MoveEvent((x,850),0))
# # multitouch_event.append(SleepEvent(1))
# multitouch_event.append(UpEvent(0))
# device().minitouch.perform(multitouch_event)

# multitouch_event = []
# multitouch_event.append(DownEvent((random.randint(1,1920), 1080), 0))
# multitouch_event.append(MoveEvent((random.randint(1,1920),900),0))
# multitouch_event.append(UpEvent(0))
# device().minitouch.perform(multitouch_event)
img = location_img("关闭正在运行应用")
resolution_x = poco.get_screen_size()[0]
resolution_y = poco.get_screen_size()[1]
while True:
    if existsimg(img):
        touch(Template(img, record_pos=None, resolution=(resolution_x, resolution_y)))
    else:
        break

multitouch_event = []
x = random.randint(1,1920)
multitouch_event.append(DownEvent((x, 1080), 0))
multitouch_event.append(MoveEvent((x,850),0))
# multitouch_event.append(SleepEvent(1))
multitouch_event.append(UpEvent(0))
device().minitouch.perform(multitouch_event)