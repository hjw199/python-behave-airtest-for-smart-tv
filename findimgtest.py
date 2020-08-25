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

'''截图'''
# filename = os.path.join(PicPath,'screen.png')
# print(filename)
# snapshot(filename=filename)

'''启动停止app'''
start_app('com.netease.nie.yosemite')
# start_app('com.ruijie.launcher20200520')
# stop_app('com.netease.nie.yosemite')
# poco.adb_client.shell('am start -n com.ruijie.launcher20200520/com.ruijie.launcher20200520.launcher.LauncherActivity')

'''adb截图'''
def screen_shoot(name):
    poco.adb_client.start_cmd('root')
    poco.adb_client.start_cmd('remount')
    time.sleep(2)
    poco.adb_client.shell('screencap -p /data/screen.png')
    time.sleep(2)
    screenshootpath = 'pull /data/screen.png '+os.path.join(PicPath,str(name))+'.png'
    poco.adb_client.start_cmd(eval('%r'%screenshootpath))
    poco.adb_client.shell('rm /data/screen.png')

# name = 'test'    
# screen_shoot(name)
# print(os.path.join(PicPath,'screen'+'20'+'.png'))


'''存在图片验证'''
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

'''查找图片存在'''
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


# newpos = find_image(image_path=r'C:\Users\86186\MVP3.0_OS_Test\features\steps\pic\云白板图标0.8.png',target_image=r'C:\Users\86186\Desktop\screen.png')
# # # print(newpos[0])

# newpos = find_image(image_path=r'.\features\steps\pic\小于三分之一常用应用栏.png',target_image=r'.\features\steps\pic\screen.png')
# print("111111111111111111111111111111111111111111111111111111")
# print(newpos)
