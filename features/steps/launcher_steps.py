from config.config import *
from airtest.core.api import *
from airtest.core.cv import Template, TargetPos
from airtest.aircv import aircv
import time
import datetime
import random
import numpy as np, numpy.random
from mappings import *
from poco.utils.track import *
from poco.proxy import UIObjectProxy
from vediotest.vediotest import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco()


def gotohome():
    # poco.adb_client.shell('input keyevent 3')
    poco.adb_client.shell('am start -n com.ruijie.launcher20200520/com.ruijie.launcher20200520.launcher.LauncherActivity')
    # home()
    touch((1,1))
    time.sleep(0.5)

def existsimg(image_path):
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    query = Template(image_path, target_pos=TargetPos.MID, resolution=(resolution_x, resolution_y),rgb = True)
    try:
        pos = loop_find(query,timeout = 5)
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

'''手指动作'''

@Step('在{input}输入{content}')
def input_(context,input,content):
    context.input=location_for(input)
    context.input.set_text(content)


@Step('点击 {button}')
def myclick(context,button):
    context.button=location_for(button)
    context.button.click()

@Step('点击坐标')
def posclick(context):
    for point in context.table:
        touch((float(point["x"]),float(point["y"])))
        # touch((100,200))

@Step('右键点击 {button}')
def myrightclick(context,button):
    context.button=location_for(button)
    context.button.long_click()

@Step('勾选 {button}')
def myclick(context,button):
    context.button=location_for(button)
    if context.button.attr("checked"):
        return
    else:
        context.button.click()

@Step('点击"{img_path}"')
def mytouch(context,img_path):
    context.img=location_img(img_path)
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    touch(Template(context.img, record_pos=None, resolution=(resolution_x, resolution_y)))
    # touch(Template(context.img, record_pos=(0,0), resolution=(1920, 1080)))

@Step('进行{finger}指滑动')
def multiswipes(context,finger):
    points = []
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    for i in range(int(finger)):
        for point in context.table:
            points.append(MotionTrack().start([float(point["x1"])/resolution_x+0.01*(i-int(finger)/2), float(point["y1"])/resolution_y]).move([float(point["x2"])/resolution_x+0.01*(i-int(finger)/2), float(point["y2"])/resolution_y]).hold(1))
    poco.apply_motion_tracks(points)

@Step('手势多指点击')
def multitouchs(context):
    multitouch_event = []
    for i,point in enumerate(context.table):
        multitouch_event.append(DownEvent((int(float(point["x"])), int(float(point["y"]))), i))
    multitouch_event.append(SleepEvent(1))
    for i,point in enumerate(context.table):
        multitouch_event.append(UpEvent(i))
    device().minitouch.perform(multitouch_event)

@Step('手势多指滑动')
def multiswipes(context):
    points = []
    for point in context.table:
        points.append(MotionTrack().start([float(point["x1"]), float(point["y1"])]).move([float(point["x2"]), float(point["y2"])]).hold(1))
    poco.apply_motion_tracks(points)

@Step('底部上划唤出常用应用')
def mycommonapp(context):
    '''上划距离未确定'''
    # multitouch_event = []
    # multitouch_event.append(DownEvent((960, 1080), 0))
    # multitouch_event.append(MoveEvent((960,1000),0))
    # # multitouch_event.append(SleepEvent(1))
    # multitouch_event.append(UpEvent(0))
    # device().minitouch.perform(multitouch_event)
    multitouch_event = []
    x = random.randint(1,1920)
    multitouch_event.append(DownEvent((x, 1080), 0))
    multitouch_event.append(MoveEvent((x,1000),0))
    # multitouch_event.append(SleepEvent(1))
    multitouch_event.append(UpEvent(0))
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)

@Step('底部上划唤出运行应用')
def myusingapp(context):
    multitouch_event = []
    x = random.randint(1,1920)
    multitouch_event.append(DownEvent((x, 1080), 0))
    multitouch_event.append(MoveEvent((x,850),0))
    # multitouch_event.append(SleepEvent(1))
    multitouch_event.append(UpEvent(0))
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)


@Step('底部上划回到桌面')
def myswipehome(context):
    multitouch_event = []
    x = random.randint(1,1920)
    multitouch_event.append(DownEvent((x, 1080), 0))
    multitouch_event.append(MoveEvent((x,600),0))
    # multitouch_event.append(SleepEvent(1))
    multitouch_event.append(UpEvent(0))
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)



# @Step('四指下划缩小屏幕')
# def mysmallpanel(context):
#     multitouch_event = []
#     multitouch_event.append(DownEvent((960, 100), 0))
#     multitouch_event.append(DownEvent((930, 100), 1))
#     multitouch_event.append(DownEvent((900, 100), 2))
#     multitouch_event.append(DownEvent((990, 100), 3))
#     multitouch_event.append(MoveEvent((960,800),0))
#     multitouch_event.append(MoveEvent((930,800),1))
#     multitouch_event.append(MoveEvent((900,800),2))
#     multitouch_event.append(MoveEvent((990,800),3))
#     multitouch_event.append(UpEvent(0))
#     multitouch_event.append(UpEvent(1))
#     multitouch_event.append(UpEvent(2))
#     multitouch_event.append(UpEvent(3))
#     device().minitouch.perform(multitouch_event)
#     time.sleep(0.5)

@Step('四指下划缩小屏幕至{ratio}')
def mysmallpanel(context,ratio):
    context.ratio = float(ratio)
    multitouch_event = []
    x = random.randint(30,1890)
    t = random.randint(1,29)
    y = random.randint(1,1080)
    y1 = y*random.uniform(0.95,1.05)
    y2 = y*random.uniform(0.95,1.05)
    y3 = y*random.uniform(0.95,1.05)
    y4 = y*random.uniform(0.95,1.05)
    multitouch_event.append(DownEvent((x, y1), 0))
    multitouch_event.append(DownEvent(((x+random.randint(16,29)), y2), 1))
    multitouch_event.append(DownEvent(((x-random.randint(1,29)), y3), 2))
    multitouch_event.append(DownEvent(((x+random.randint(1,15)), y4), 3))
    multitouch_event.append(MoveEvent((x,(1080-y1)*(1-context.ratio)+y1),0))
    multitouch_event.append(MoveEvent(((x-random.randint(1,29)),(1080-y2)*(1-context.ratio)+y2),1))
    multitouch_event.append(MoveEvent(((x-random.randint(1,29)),(1080-y3)*(1-context.ratio)+y3),2))
    multitouch_event.append(MoveEvent(((x+random.randint(1,15)),(1080-y4)*(1-context.ratio)+y4),3))
    multitouch_event.append(UpEvent(0))
    multitouch_event.append(UpEvent(1))
    multitouch_event.append(UpEvent(2))
    multitouch_event.append(UpEvent(3))
    device().minitouch.perform(multitouch_event)

'''登录相关'''

@Step('未登录账号')
def nologin(context):
    gotohome()
    wait = location_for("时间")
    wait.wait_for_appearance()
    # poco("com.ruijie.launcher20200520:id/tv_time_hour").wait_for_appearance()
    if location_for("下课"):
        location_for("下课").click()
    if location_for("账号"):
        location_for("返回标题").click()

@Step('已登录账号')
def allogin(context):
    gotohome()
    wait = location_for("时间")
    wait.wait_for_appearance()
    if location_for("账号登录"):
        location_for("账号登录").click()
        location_for("账号").set_text(18659131313)
        location_for("密码").set_text(123456)
        location_for("登录").click()
    if location_for("账号"):
        location_for("账号").set_text(18659131313)
        location_for("密码").set_text(123456)
        location_for("登录").click()
    assert location_for("下课")

@Step('登录账号')
def alogin(context):
    gotohome()
    wait = location_for("时间")
    wait.wait_for_appearance()
    if location_for("下课"):
        location_for("下课").click()
        wait = location_for("账号登录")
        wait.wait_for_appearance()
        location_for("账号登录").click()
        location_for("账号").set_text(18659131313)
        location_for("密码").set_text(123456)
        location_for("登录").click()
    if location_for("账号登录"):
        location_for("账号登录").click()
        location_for("账号").set_text(18659131313)
        location_for("密码").set_text(123456)
        location_for("登录").click()
    if location_for("账号"):
        location_for("账号").set_text(18659131313)
        location_for("密码").set_text(123456)
        location_for("登录").click()
    assert location_for("下课")

@Step('删除登录头像')
def dellogin(context):
    while True:
        if location_for("登录头像"):
            context.button=location_for("登录头像")
            context.button.long_click()
            context.img=location_img('从快速登录移除图片')
            resolution_x = poco.get_screen_size()[0]
            resolution_y = poco.get_screen_size()[1]
            touch(Template(context.img, record_pos=None, resolution=(resolution_x, resolution_y)))
        else:
            break

'''系统相关'''

@Given('我已连接大屏')
def connect_android(context):
    connect_device('android:///' + Android_Serial_No)

@Step('打开"{soft}"')
def opensoft(context,soft):
    context.soft=location_soft(soft)
    start_app(context.soft)
    time.sleep(3.0)

@Step('回到桌面')
def mygotohome(context):
    gotohome()
    wait = location_for("时间")
    wait.wait_for_appearance()

@Step('未运行应用')
def nousingapp(context):
    # for i in SOFT_DICT:
    #     context.soft=location_soft(i)
    #     stop_app(context.soft)
    gotohome()
    multitouch_event = []
    multitouch_event.append(DownEvent((random.randint(1,1920), 1080), 0))
    multitouch_event.append(MoveEvent((random.randint(1,1920),900),0))
    multitouch_event.append(UpEvent(0))
    device().minitouch.perform(multitouch_event)
    img = location_img("关闭正在运行应用")
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    while True:
        if existsimg(img):
            touch(Template(img, record_pos=None, resolution=(resolution_x, resolution_y)))
        else:
            break
    gotohome()



@Step('等待{t}秒')
def mywait(context,t):
    time.sleep(float(t))


    
'''断言'''

@Step('不存在 {id}')
def my_not_exists(context,id):
    assert not location_for(id)

@Step('存在 {id}')
def my_exists(context,id):
    assert location_for(id)

@Step('应该看到"{img_path}"')
def myassert(context,img_path):
    context.img=location_img(img_path)
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    assert_exists(Template(context.img, record_pos=None, resolution=(resolution_x, resolution_y)),context.img+"存在")

@Step('不应该看到"{img_path}"')
def myassert(context,img_path):
    context.img=location_img(img_path)
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    assert_not_exists(Template(context.img, record_pos=None, resolution=(resolution_x, resolution_y)),context.img+"存在")

@Step('日期时间准确')
def mytime(context):
    def get_week_day():
        week_day_dict = {
            0 : '星期一',
            1 : '星期二',
            2 : '星期三',
            3 : '星期四',
            4 : '星期五',
            5 : '星期六',
            6 : '星期天',
        }
        day = datetime.datetime.now().weekday()
        return week_day_dict[day]

    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    nowmin = nowtime[11:16]
    nowmon = nowtime[5:7]
    nowday = nowtime[8:10]
    nowweek=get_week_day()
    tvtime=poco("com.ruijie.launcher20200520:id/tv_time_hour").get_text()
    tvdate=poco("com.ruijie.launcher20200520:id/tv_time_calendar").get_text()
    tvmon = tvdate[0:2]
    tvday = tvdate[3:5]
    tvweek = tvdate[7:10]
    if nowday==tvday and nowmon == tvmon and nowmin == tvtime and nowweek == tvweek:
        assert True
    else:
        assert False

@Step('桌面成比例缩小至{ratio}')
def smallpanelaccert(context,ratio):
    context.ratio = float(ratio)
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    pos = location_pos("云白板")
    poco.adb_client.start_cmd('root')
    poco.adb_client.start_cmd('remount')
    time.sleep(2)
    poco.adb_client.shell('screencap -p /data/screen.png')
    screenshootpath = 'pull /data/screen.png '+PicPath+'screen.png'
    poco.adb_client.start_cmd(eval('%r'%screenshootpath))
    poco.adb_client.shell('rm /data/screen.png')
    image_path = PicPath+'云白板图标'+ratio+'.png'
    target_image = PicPath+'screen.png'
    newpos = find_image(image_path=image_path,target_image=target_image)
    # newpos = find_image(image_path=r'C:\Users\86186\MVP3.0_OS_Test\features\steps\pic\云白板图标0.8.png',target_image=r'C:\Users\86186\Desktop\screen.png')
    xpos = resolution_x/2+(pos[0]-resolution_x/2)*context.ratio
    ypos = resolution_y-(resolution_y-pos[1])*context.ratio
    xpos = abs(xpos-newpos[0])
    ypos = abs(ypos-newpos[1])
    if xpos<5 and ypos<5:
        assert True
    else:
        assert False

'''云白板'''
@Step('回到云白板主页')
def cloudhome(context):
    if location_for("白板返回"):
        location_for("白板返回").click()


"音视频检测"

@Step('进行视频检测')
def myvediotest(context):
    vediotest(ip=Camera_Ip,savDir=SavDir,recordTime=int(RecordTime))

@Step('播放视频{vedio}')
def myvedio(context,vedio):
    context.vedio = "\'am start -n "+ MediaSoft +' -d \"'+TestVedioPath + vedio + '\"'+"\'"
    poco.adb_client.shell(eval(context.vedio))
    # poco.adb_client.shell('am start -n com.android.gallery3d/.app.MovieActivity -d "/mnt/usb/FC281A222819DD08/烤鸭.mp4"')
    time.sleep(1.0)
    if location_for("重新开始"):
        location_for("重新开始").click()

@Step('进行音频检测')
def myvoicetest(context):
    voicetest(ip=Camera_Ip,savDir=SavDir,recordTime=int(RecordTime))

@Step('播放音频{voice}')
def myvoice(context,voice):
    context.voice = "\'am start -n "+ MediaSoft +' -d \"'+TestVedioPath + vedio + '\"'+"\'"
    poco.adb_client.shell(eval(context.voice))
    # poco.adb_client.shell(am start -n com.android.gallery3d/.app.MovieActivity -d "/mnt/sdcard/test.mp4")

'''底部上划'''

@Step('点击运行应用外围')
def Outusing_Click(context):
    while True:
        x=random.randint(1,1920)
        y=random.randint(1,1080)
        if 566<x<1354 and 947<y<1080:
            continue
        if 282<x<1617 and 218<y<856:
            continue
        else:
            touch((x,y))
            break

@Step('点击常用应用栏外围')
def Outnormal_Click(context):
    while True:
        x=random.randint(1,1920)
        y=random.randint(1,1080)
        if 566<x<1354 and 947<y<1080:
            continue
        if 282<x<1617 and 218<y<856:
            continue
        else:
            touch((x,y))
            break


@Step('click_specific_position')
def posclick(context):
    for point in context.table:
        touch((float(point["x"]),float(point["y"])))
        # touch((100,200))
