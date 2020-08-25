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
from airtest.core.android.minitouch import *
from airtest.core.android.base_touch import *
ButtonDis=40 #常用应用栏上划1/3距离
ButtonStartDis=10 #响应底部上滑事件距离
OAppHigh=110 #常用应用栏高度,实际160
ButtonUpSpeed=1500 #上划速度


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

def multi_swipe(tuple_from_xy, tuple_to_xy,finger=1, duration=0.8, steps=5):
    #多指按压滑动抬起
    from_x, from_y = tuple_from_xy
    to_x, to_y = tuple_to_xy
    multitouch_event = []
    for i in range(0,finger):
        multitouch_event.append(DownEvent((from_x+10*(i-1),from_y),i))

    interval = float(duration) / (steps + 1)
    for i in range(1, steps + 1):
        move_events = [
                SleepEvent(interval),
                # MoveEvent((from_x + ((to_x - from_x) * i / steps), from_y + (to_y - from_y) * i / steps),
                #             contact=0, pressure=50),
            ]
        for j in range(0,finger):
            move_events += [MoveEvent((from_x + ((to_x - from_x) * i / steps)+(10*(j-1)), from_y + (to_y - from_y) * i / steps),
                            contact=j, pressure=50),]
        multitouch_event.extend(move_events)

    for i in range(0,finger):
        multitouch_event.append(UpEvent(i))

    return multitouch_event

def multi_swipe_noup(tuple_from_xy, tuple_to_xy,finger=1, duration=0.8, steps=5):
    #多指按压滑动不抬起
    from_x, from_y = tuple_from_xy
    to_x, to_y = tuple_to_xy
    multitouch_event = []
    for i in range(0,finger):
        multitouch_event.append(DownEvent((from_x+10*(i-1),from_y),i))

    interval = float(duration) / (steps + 1)
    for i in range(1, steps + 1):
        move_events = [
                SleepEvent(interval),
                # MoveEvent((from_x + ((to_x - from_x) * i / steps), from_y + (to_y - from_y) * i / steps),
                #             contact=0, pressure=50),
            ]
        for j in range(0,finger):
            move_events += [MoveEvent((from_x + ((to_x - from_x) * i / steps)+(10*(j-1)), from_y + (to_y - from_y) * i / steps),
                            contact=j, pressure=50),]
        multitouch_event.extend(move_events)

    # for i in range(0,finger):
    #     multitouch_event.append(UpEvent(i))

    return multitouch_event
'''手指动作'''
def screen_shoot(name):
    poco.adb_client.start_cmd('root')
    poco.adb_client.start_cmd('remount')
    time.sleep(2)
    poco.adb_client.shell('screencap -p /data/screen.png')
    time.sleep(2)
    screenshootpath = 'pull /data/screen.png '+os.path.join(PicPath,str(name))+'.png'
    poco.adb_client.start_cmd(eval('%r'%screenshootpath))
    poco.adb_client.shell('rm /data/screen.png')
    time.sleep(2)

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
    # multitouch_event = []
    # x = random.randint(1,1920)
    # y = random.randint(ButtonDis,1080)
    # st = random.randint(ButtonUPDis,160)
    # # multitouch_event.append(DownEvent((x,1080),0))
    # # multitouch_event.append(MoveEvent((x,1000),0))
    # multitouch_event.append(DownEvent((x,y),0))
    # # multitouch_event.append(MoveEvent((x,y-st),0))
    # multitouch_event += swipe_move((x,y), (x,y-st), duration=0.8, steps=5)
    # multitouch_event.append(UpEvent(0))
    # device().minitouch.perform(multitouch_event)
    # time.sleep(0.5)
    finger = random.randint(1,5)
    # finger = 1
    multitouch_event = []
    x = random.randint(10,1890)
    y = random.randint(1080-ButtonStartDis,1080)
    # y = 1080
    st = random.randint(ButtonDis,OAppHigh)
    multitouch_event = []
    multitouch_event += multi_swipe((x,y), (x,y-st),finger=finger, duration=2, steps=5)
    # print("1111111111111111111111111111111111111111111111")
    # print(multitouch_event)
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)

@Step('底部上划小于应用栏三分之一')
def mycommonapp(context):
    # finger = random.randint(1,5)
    finger = 1
    multitouch_event = []
    x = random.randint(10,1890)
    y = 1080
    st = 30
    # st = random.randint(0,ButtonDis)
    multitouch_event = []
    multitouch_event += multi_swipe_noup((x,y), (x,y-st),finger=finger, duration=0.8, steps=5)
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)


@Step('松开手指')
def upfinger(context):
    multitouch_event=[]
    for i in range(0,5):
        multitouch_event.append(UpEvent(i))
    device().minitouch.perform(multitouch_event)

@Step('底部上划唤出运行应用')
def myusingapp(context):
    # multitouch_event = []
    # x = random.randint(1,1920)
    # # y = random.randint(0,949)
    # multitouch_event.append(DownEvent((x, 1080), 0))
    # multitouch_event.append(MoveEvent((x,850),0))
    # # multitouch_event += swipe_move((x,1050), (x,y), duration=0.8, steps=5)
    # # multitouch_event.append(SleepEvent(1))
    # multitouch_event.append(UpEvent(0))
    # device().minitouch.perform(multitouch_event)
    # time.sleep(0.5)
    finger = random.randint(1,5)
    # finger = 1
    multitouch_event = []
    x = random.randint(10,1890)
    y = random.randint(1080-ButtonStartDis,1080)
    # st = random.randint(OAppHigh,1080)
    st = random.randint(OAppHigh,y)
    multitouch_event = []
    multitouch_event += multi_swipe((x,y), (x,y-st),finger=finger, duration=2, steps=20)
    # print("1111111111111111111111111111111111111111111111")
    # print(multitouch_event)
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)


@Step('底部上划回到桌面')
def myswipehome(context):
    finger = random.randint(1,5)
    # finger = 1
    multitouch_event = []
    x = random.randint(10,1890)
    y = 1080-ButtonStartDis
    # st = random.randint(OAppHigh,1080)
    st = random.randint(OAppHigh,y)
    # duration = round(float(st)/float(1500),2)
    # duration = round(float(st)/float(2000),2)
    duration = 0.2
    multitouch_event = []
    multitouch_event += multi_swipe((x,y), (x,y-st),finger=finger, duration=duration, steps=5)
    # print("1111111111111111111111111111111111111111111111")
    # print(multitouch_event)
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)

@Step('四指下划缩小屏幕至{ratio}')
def mysmallpanel(context,ratio):
    context.ratio = float(ratio)
    multitouch_event = []
    # x = random.randint(30,1890)
    x = random.randint(384,1536)
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
    multitouch_event.append(MoveEvent(((x+random.randint(16,29)),(1080-y2)*(1-context.ratio)+y2),1))
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
    finger = random.randint(1,5)
    multitouch_event = []
    x = random.randint(10,1890)
    y = random.randint(1080-ButtonStartDis,1080)
    st = random.randint(OAppHigh,y)
    multitouch_event = []
    multitouch_event += multi_swipe((x,y), (x,y-st),finger=finger, duration=0.8, steps=20)
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)
    img = location_img("关闭正在运行应用")
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    while True:
        if existsimg(img):
            touch(Template(img, record_pos=None, resolution=(resolution_x, resolution_y)))
            time.sleep(0.5)
        else:
            break
    gotohome()

@Step('截图保存')
def my_screen_shoot(context):
    # context.name='screen'
    # try:
    #     screen_shoot(context.name)
    # except:
    #     print("截图失败")
    #     multitouch_event=[]
    #     for i in range(0,5):
    #         multitouch_event.append(UpEvent(i))
    #     device().minitouch.perform(multitouch_event)
    filename = os.path.join(PicPath,'screen.png')
    snapshot(filename=filename)

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
def img_assert(context,img_path):
    context.img=location_img(img_path)
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    assert_exists(Template(context.img, record_pos=None, resolution=(resolution_x, resolution_y)),context.img+"存在")

@Step('不应该看到"{img_path}"')
def img_no_assert(context,img_path):
    context.img=location_img(img_path)
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    assert_not_exists(Template(context.img, record_pos=None, resolution=(resolution_x, resolution_y)),context.img+"存在")

@Step('截图与"{img_path}"一致')
def img_compile(context,img_path):
    context.img=location_img(img_path)
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    target_image = os.path.join(PicPath,'screen.png')
    pos = find_image(image_path=context.img,target_image=target_image)
    if len(pos) == 0:
        assert False
    else:
        assert True

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

@Step('{pic}成比例缩小至{ratio}')
def smallpanelaccert(context,pic,ratio):
    context.ratio = float(ratio)
    context.pic = pic
    r = int((float(ratio))*100)
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    pos = location_pos(context.pic)
    poco.adb_client.start_cmd('root')
    poco.adb_client.start_cmd('remount')
    time.sleep(2)
    screen_shoot(str(r))
    time.sleep(2)
    image_path = os.path.join(PicPath,context.pic+str(r)+'.png')
    target_image = os.path.join(PicPath,'screen'+str(r)+'.png')
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
        if 290<x<714 and 190<y<493:
            continue
        if 592<x<1324 and 920<y<1061:
            continue
        else:
            touch((x,y))
            break

@Step('点击运行应用之间')
def Outusing_Click(context):
    x=random.randint(714,737)
    y=random.randint(190,493)
    touch((x,y))

@Step('点击运行应用空白区域')
def Outusing_Click(context):
    while True:
        x=random.randint(714,1607)
        y=random.randint(290,816)
        if 290<x<714 and 514<y<816:
            continue
        else:
            touch((x,y))
            break

@Step('点击常用应用栏外围')
def Outnormal_Click(context):
    while True:
        x=random.randint(1,1920)
        y=random.randint(1,1080)
        if 592<x<1324 and 920<y<1061:
            continue
        else:
            touch((x,y))
            break