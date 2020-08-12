from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco()
import os
from airtest.core.android.minitouch import *
from airtest.core.android.base_touch import *
import random
from mappings import *
from airtest.core.cv import Template, TargetPos
import numpy as np, numpy.random
import math
from airtest.aircv import aircv
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



# def existsimg(image_path):
#     resolution_x = poco.get_screen_size()[0]
#     resolution_y = poco.get_screen_size()[1]
#     query = Template(image_path, target_pos=TargetPos.MID, resolution=(resolution_x, resolution_y),rgb = True)
#     try:
#         pos = loop_find(query)
#     except Exception as e:
#         return False
#     else:
#         return pos


# img = location_img("快速登录图片")
# t = existsimg(img)
# print("111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
# print(t)


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

# touch((1,1))
# # for i in POS_DICT:
# #     pos = location_pos(i)
# #     print(pos)


def existsimg(image_path,target_pos=TargetPos.MID):
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    query = Template(image_path, target_pos, resolution=(resolution_x, resolution_y),rgb = True)
    try:
        pos = loop_find(query)
    except Exception as e:
        return False
    else:
        return pos


def find_image(image_path, target_image=None, target_pos=TargetPos.MID, timeout=20, threshold=None, interval=0.5,rgb=False, intervalfunc=None):
    start_time = time.time()
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    query = Template(image_path, target_pos=target_pos, resolution=(resolution_x, resolution_y),rgb = rgb)
    while True:
        if target_image:
            screen = aircv.imread(target_image)
        else:
            imagepath = screenshotDir + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + ".png"
            screen = airtestG.DEVICE.snapshot(imagepath)
            print("----------------")
            print(screen is None)
            print("----------------")
        if screen is None:
            print("Screen is None, may be locked")
        else:
            if threshold:
                query.threshold = threshold
            match_pos = query.match_in(screen)
            if match_pos:
                return match_pos

        if intervalfunc is not None:
            intervalfunc()

        # 超时则raise，未超时则进行下次循环:
        if (time.time() - start_time) > timeout:
            raise Exception('Picture %s not found in screen' % query)
        else:
            time.sleep(interval)


touch((1,1))

# ratio = 0.8
# multitouch_event = []
# x = random.randint(1,1920)
# y = random.randint(1,1080)
# y1 = y*random.uniform(0.95,1.05)
# y2 = y*random.uniform(0.95,1.05)
# y3 = y*random.uniform(0.95,1.05)
# y4 = y*random.uniform(0.95,1.05)
# multitouch_event.append(DownEvent((960, y1), 0))
# multitouch_event.append(DownEvent((930, y2), 1))
# multitouch_event.append(DownEvent((900, y3), 2))
# multitouch_event.append(DownEvent((990, y4), 3))
# multitouch_event.append(MoveEvent((960,(1080-y1)*(1-ratio)+y1),0))
# multitouch_event.append(MoveEvent((960,(1080-y2)*(1-ratio)+y2),1))
# multitouch_event.append(MoveEvent((960,(1080-y3)*(1-ratio)+y3),2))
# multitouch_event.append(MoveEvent((960,(1080-y4)*(1-ratio)+y4),3))
# multitouch_event.append(UpEvent(0))
# multitouch_event.append(UpEvent(1))
# multitouch_event.append(UpEvent(2))
# multitouch_event.append(UpEvent(3))
# device().minitouch.perform(multitouch_event)
# 990,517   1002,384
# 1729,216  1920,0


# pos = location_pos("云白板")
# poco.adb_client.start_cmd('root')
# poco.adb_client.start_cmd('remount')
# time.sleep(2)
# poco.adb_client.shell('screencap -p /data/screen.png')
# poco.adb_client.start_cmd(r'pull /data/screen.png C:\Users\86186\Desktop')
# poco.adb_client.shell('rm /data/screen.png')

# newpos = find_image(image_path=r'C:\Users\86186\MVP3.0_OS_Test\features\steps\pic\云白板图标0.8.png',target_image=r'C:\Users\86186\Desktop\screen.png')
# # # print(newpos[0])

# # xpos = 960+(pos[0]-960)*ratio
# # ypos = 1080-(1080-pos[1])*ratio
# # print(xpos,ypos)
# print(newpos)
# # # if xpos<2 and ypos<2:
# # #     assert True
# # # else:
# # #     assert False
