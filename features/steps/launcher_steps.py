import time
import datetime
import re
import random
import requests
import json
import hashlib
import platform
import subprocess
import numpy as np, numpy.random
from poco.utils.track import *
from poco.proxy import UIObjectProxy
from vediotest.vediotest import *
from mappings import *
ButtonDis=40 #常用应用栏上划1/3距离
ButtonStartDis=10 #响应底部上滑事件距离
OAppHigh=110 #常用应用栏高度,实际160
ButtonUpSpeed=1500 #上划速度
resolution_x = poco.get_screen_size()[0]
resolution_y = poco.get_screen_size()[1]
NFC = poco.adb_client.shell('getprop persist.ruijie.serialno')


'''手指简单动作'''
@Step('在{input}输入{content}')
def input_(context,input,content):
    context.input=location_for(input)
    context.input.set_text(content)

@Step('点击按钮{button}')
def click_button(context,button):
    context.button=location_for(button)
    context.button.click()

@Step('点击坐标')
def pos_click(context):
    for point in context.table:
        touch((float(point["x"]),float(point["y"])))
        # touch((100,200))

@Step('右键点击{button}')
def right_click(context,button):
    context.button=location_for(button)
    context.button.long_click()

@Step('勾选{button}')
def checkbox(context,button):
    context.button=location_for(button)
    if context.button.attr("checked"):
        return
    else:
        context.button.click()

@Step('点击图片{img_path}')
def touch_img(context,img_path):
    context.img=location_img(img_path)
    # resolution_x = poco.get_screen_size()[0]
    # resolution_y = poco.get_screen_size()[1]
    touch(Template(context.img, record_pos=None, resolution=(resolution_x, resolution_y)))
    # touch(Template(context.img, record_pos=(0,0), resolution=(1920, 1080)))

'''手指组合动作'''

@Step('进行{finger}指滑动')
def multiswipes(context,finger):
    points = []
    # resolution_x = poco.get_screen_size()[0]
    # resolution_y = poco.get_screen_size()[1]
    for i in range(int(finger)):
        for point in context.table:
            points.append(MotionTrack().start([float(point["x1"])/resolution_x+0.01*(i-int(finger)/2), float(point["y1"])/resolution_y]).move([float(point["x2"])/resolution_x+0.01*(i-int(finger)/2), float(point["y2"])/resolution_y]).hold(1))
    poco.apply_motion_tracks(points)

@step('向左滑动切到下一页')
def swipe_left(context):
    swipe(v1=(1400,525),v2=(1100,525),steps=20)

@step('划动头像到最左边')
def swipe_head_left(context):
    swipe(v1=(431,440),v2=(728,440),steps=20)
    swipe(v1=(431,440),v2=(728,440),steps=20)
    swipe(v1=(431,440),v2=(728,440),steps=20)
    swipe(v1=(431,440),v2=(728,440),steps=20)
    swipe(v1=(431,440),v2=(728,440),steps=20)

@step('划动头像到最右边')
def swipe_head_right(context):
    swipe(v1=(728,440),v2=(431,440),steps=20)
    swipe(v1=(728,440),v2=(431,440),steps=20)
    swipe(v1=(728,440),v2=(431,440),steps=20)
    swipe(v1=(728,440),v2=(431,440),steps=20)
    swipe(v1=(728,440),v2=(431,440),steps=20)

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

'''底部上划相关'''

@Step('底部上划唤出常用应用')
def normal_toolbar(context):
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
    logger.info('底部上划唤出常用应用finger:{},x:{},y:{},distance:{}'.format(finger,x,y,st))
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)

@Step('底部上划小于应用栏三分之一')
def buttom_up_less_than(context):
    # finger = random.randint(1,5)
    finger = 1
    multitouch_event = []
    x = random.randint(10,1890)
    y = 1080
    st = 30
    # st = random.randint(0,ButtonDis)
    multitouch_event = []
    # multitouch_event += multi_swipe((x,y), (x,y-st),finger=finger, duration=0.8, steps=5,up=False)
    multitouch_event += multi_swipe((x,y), (x,y-st),finger=finger, duration=0.8, steps=5)
    logger.info('底部上划小于应用栏三分之一finger:{},x:{},y:{},distance:{}'.format(finger,x,y,st))
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)

@Step('松开手指')
def up_finger(context):
    multitouch_event=[]
    for i in range(0,5):
        multitouch_event.append(UpEvent(i))
    device().minitouch.perform(multitouch_event)

@Step('底部上划唤出运行应用')
def running_app(context):
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
    multitouch_event += multi_swipe((x,y), (x,y-st),finger=finger, duration=1, steps=20)
    # print("1111111111111111111111111111111111111111111111")
    # print(multitouch_event)
    logger.info('底部上划唤出运行应用finger:{},x:{},y:{},distance:{}'.format(finger,x,y,st))
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)

@Step('底部上划回到桌面')
def swipe_home(context):
    # finger = random.randint(1,5)
    finger = 1
    multitouch_event = []
    x = random.randint(10,1890)
    y = 1080
    # st = random.randint(OAppHigh,y)
    st = 200
    # duration = round(float(st)/float(1500),2)
    duration = 0
    multitouch_event = []
    multitouch_event += multi_swipe((x,y), (x,y-st),finger=finger,duration=duration,steps=5,sleep=False)
    # print("1111111111111111111111111111111111111111111111")
    # print(multitouch_event)
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)
    x = random.randint(10,1890)
    multitouch_event = []
    multitouch_event += multi_swipe((x,y), (x,y-st),finger=finger,duration=duration,steps=5,sleep=False)
    # print("1111111111111111111111111111111111111111111111")
    # print(multitouch_event)
    logger.info('底部上划回到桌面finger:{},x:{},y:{},distance:{}'.format(finger,x,y,st))
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)

@Step('四指下划缩小屏幕至{ratio}')
def small_panel(context,ratio):
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
    multitouch_event.append(SleepEvent(1.1))
    multitouch_event.append(MoveEvent((x,(1080-y1)*(1-context.ratio)+y1),0))
    multitouch_event.append(MoveEvent(((x+random.randint(16,29)),(1080-y2)*(1-context.ratio)+y2),1))
    multitouch_event.append(MoveEvent(((x-random.randint(1,29)),(1080-y3)*(1-context.ratio)+y3),2))
    multitouch_event.append(MoveEvent(((x+random.randint(1,15)),(1080-y4)*(1-context.ratio)+y4),3))
    multitouch_event.append(UpEvent(0))
    multitouch_event.append(UpEvent(1))
    multitouch_event.append(UpEvent(2))
    multitouch_event.append(UpEvent(3))
    logger.info('四指下划缩小屏幕x:{},y:{}'.format(x,y))
    device().minitouch.perform(multitouch_event)

@Step('点击运行应用外围')
def outside_running_app_click(context):
    while True:
        x=random.randint(1,1920)
        y=random.randint(1,1080)
        if 290<x<714 and 190<y<493:
            continue
        if 592<x<1324 and 920<y<1061:
            continue
        else:
            logger.info('点击运行应用外围x:{},y:{}'.format(x,y))
            touch((x,y))
            break

@Step('点击运行应用之间')
def between_running_app_click(context):
    x=random.randint(714,737)
    y=random.randint(190,493)
    logger.info('点击运行应用之间x:{},y:{}'.format(x,y))
    touch((x,y))

@Step('点击运行应用空白区域')
def overside_running_app_click(context):
    x=random.randint(725,1618)
    y=random.randint(505,828)
    logger.info('点击运行应用空白区域x:{},y:{}'.format(x,y))
    touch((x,y))

@Step('点击常用应用栏外围')
def outside_normal_toolbar_click(context):
    while True:
        x=random.randint(1,1920)
        y=random.randint(1,1080)
        if 592<x<1324 and 920<y<1061:
            continue
        else:
            logger.info('点击常用应用栏外围x:{},y:{}'.format(x,y))
            touch((x,y))
            break

'''触控相关'''

@Step('写小正字')
def draw_small_zheng(context):
    startx=resolution_x/2
    starty=resolution_y/2
    large=20
    swipe(v1=(startx,starty),v2=(startx+large,starty))
    swipe(v1=(startx+large/2,starty),v2=(startx+large/2,starty+large))
    swipe(v1=(startx+large/2,starty+large/2),v2=(startx+large,starty+large/2))
    swipe(v1=(startx+large/4,starty+large/2),v2=(startx+large/4,starty+large))
    swipe(v1=(startx,starty+large),v2=(startx+large,starty+large))

@Step('一指点击一指划线')
def touchdown_and_swipe(context):
    distance = 6
    x1=random.randint(distance,resolution_x-distance)
    y1=random.randint(distance,resolution_y-distance)
    multitouch_event = []
    multitouch_event.append(DownEvent((x1,y1),0))
    multitouch_event.append(DownEvent((x1-distance,y1-distance),1))
    multitouch_event.append(SleepEvent(0.5))
    multitouch_event.append(MoveEvent((x1+distance,y1-distance),1))
    multitouch_event.append(SleepEvent(0.5))
    multitouch_event.append(MoveEvent((x1+distance,y1+distance),1))
    multitouch_event.append(SleepEvent(0.5))
    multitouch_event.append(MoveEvent((x1-distance,y1+distance),1))
    multitouch_event.append(SleepEvent(0.5))
    multitouch_event.append(MoveEvent((x1-distance,y1-distance),1))
    multitouch_event.append(UpEvent(0))
    multitouch_event.append(UpEvent(1))
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)

@Step('全屏划线')
def full_swipe(context):
    for x in range(1,resolution_x,20):
        swipe(v1=(x,0),v2=(x,resolution_y))
    for y in range(1,resolution_y,20):
        swipe(v1=(0,y),v2=(resolution_x,y))

@Step('向后翻{page}页')
def turn_after_page(context,page):
    context.page = int(page)
    for i in range(0,context.page):
        x=random.randint(100,resolution_x)
        y=random.randint(100,resolution_y-100)
        while True:
            st=random.randint(-50,50)
            if (st != 0) :break
        swipe(v1=(x,y),v2=(x-100,y-st),duration=0)
        time.sleep(1)

'''登录相关'''

@Step('未登录账号')
def no_login(context):
    gotohome()
    wait = location_for("时间")
    wait.wait_for_appearance()
    # poco("com.ruijie.launcher20200520:id/tv_time_hour").wait_for_appearance()
    if location_for("下课"):
        location_for("下课").click()
    if location_for("账号"):
        location_for("返回标题").click()

@Step('已登录账号')
def already_login(context):
    gotohome()
    wait = location_for("时间")
    wait.wait_for_appearance()
    if location_for("账号登录"):
        location_for("账号登录").click()
        location_for("账号").set_text(18659132313)
        location_for("密码").set_text(123456)
        location_for("登录").click()
    if location_for("账号"):
        location_for("账号").set_text(18659132313)
        location_for("密码").set_text(123456)
        location_for("登录").click()
    time.sleep(0.5)
    assert location_for("下课")

@Step('登录账号{phone}')
def log_in(context,phone):
    context.phone = int(phone)
    gotohome()
    wait = location_for("时间")
    wait.wait_for_appearance()
    if location_for("下课"):
        location_for("下课").click()
        wait = location_for("账号登录")
        wait.wait_for_appearance()
        location_for("账号登录").click()
        location_for("账号").set_text(context.phone)
        location_for("密码").set_text(123456)
        location_for("登录").click()
    if location_for("账号登录"):
        location_for("账号登录").click()
        location_for("账号").set_text(context.phone)
        location_for("密码").set_text(123456)
        location_for("登录").click()
    if location_for("账号"):
        location_for("账号").set_text(context.phone)
        location_for("密码").set_text(123456)
        location_for("登录").click()
    assert location_for("下课")

@Step('删除登录头像')
def del_login(context):
    while True:
        if location_for("登录头像"):
            context.button=location_for("登录头像")
            context.button.long_click()
            context.img=location_img('从快速登录移除图片')
            touch(Template(context.img, record_pos=None, resolution=(resolution_x, resolution_y)))
            time.sleep(0.5)
        else:
            break

@Step('登录{account}个账号')
def login_20(context,account):
    zh = [18659132313,18659131313,18659232323,18659131323,18659132323,18659231313,18659231323,18659232313,18659123456,18659345678,18659456789,18659111111,18659222222,18659333333,18659444444,18659555555,18659666666,18659777777,18659888888,18659999999]
    for i in range(int(account)) :
        if location_for("下课"):
            location_for("下课").click()
            wait = location_for("账号登录")
            wait.wait_for_appearance()
        location_for("账号登录").click()
        location_for("账号").set_text(zh[i])
        location_for("密码").set_text(123456)
        context.button=location_for("允许快捷登录")
        if context.button.attr("checked"):
            pass
        else:
            context.button.click()
        location_for("登录").click()

@Step('NFC登录账号{phone}')
def nfc_login(context,phone):
    context.phone = int(phone)
    # url = "http://47.114.138.212/service-user/authUser/getTokenAndRefreshToken"
    url = Server_IP +"/service-user/authUser/getTokenAndRefreshToken"
    headers = {"Content-Type": "application/json"}
    password = "123456"
    password = hashlib.md5(password.encode()).hexdigest()
    myjson = {"phone": context.phone,"password": password,"appType": "app_web"}
    response = requests.post(url=url,json=myjson, headers=headers)
    out = json.loads(response.text)
    # print(out)
    headers['X-Authorization'] = out["content"]["token"]
    # print(headers)
    # url1 = "http://47.114.138.212/service-user/user/screenLoginByPhoneSn"
    url1 = Server_IP+"/service-user/user/screenLoginByPhoneSn"
    myjson1 = {
    "sn": NFC
    }
    resp = requests.post(url=url1, json=myjson1,verify=False, headers=headers)
    loads = json.loads(resp.text)

'''系统相关'''

@Given('我已连接大屏')
def connect_android(context):
    connect_device('android:///' + Android_Serial_No)

@Step('打开软件{soft}')
def open_soft(context,soft):
    context.soft=location_soft(soft)
    start_app(context.soft)
    time.sleep(3.0)

@Step('回到桌面')
def goto_home(context):
    gotohome()
    if location_for('批注关闭'):
        location_for('批注关闭').click()
    wait = location_for("时间")
    wait.wait_for_appearance()

@Step('回到首页')
def goto_home_page(context):
    gotohome()
    wait = location_for("时间")
    wait.wait_for_appearance()
    while not location_for("云白板"):
        swipe(v1=(1100,525),v2=(1400,525),steps=20)

@Step('未运行应用')
def no_running_app(context):
    # for i in SOFT_DICT:
    #     context.soft=location_soft(i)
    #     stop_app(context.soft)
    gotohome()
    finger = random.randint(1,5)
    multitouch_event = []
    x = random.randint(10,1890)
    y = 1080
    st = random.randint(OAppHigh,y)
    multitouch_event = []
    multitouch_event += multi_swipe((x,y), (x,y-st),finger=finger, duration=0.8, steps=20)
    device().minitouch.perform(multitouch_event)
    time.sleep(0.5)
    img = location_img("关闭正在运行应用")
    # resolution_x = poco.get_screen_size()[0]
    # resolution_y = poco.get_screen_size()[1]
    while True:
        if existsimg(img):
            touch(Template(img, record_pos=None, resolution=(resolution_x, resolution_y)))
            time.sleep(0.5)
        else:
            break
    gotohome()

@Step('截图保存{name}')
def my_screen_shoot(context,name):
    # context.name='screen'
    # try:
    #     screen_shoot(context.name)
    # except:
    #     print("截图失败")
    #     multitouch_event=[]
    #     for i in range(0,5):
    #         multitouch_event.append(UpEvent(i))
    #     device().minitouch.perform(multitouch_event)
    context.name=name
    filename = os.path.join(ScreenshotPath,context.name+'.png')
    snapshot(filename=filename)

@Step('等待{t}秒')
def my_sleep(context,t):
    time.sleep(float(t))

@Step('安装{app}')
def my_install(context,app):
    filepath = os.path.join(AppPath,app)
    cmd = 'install -r '+filepath
    poco.adb_client.cmd(cmd)
    # install(filepath=filepath)

@Step('授予{app}权限')
def give_permission(context,app):
    context.app = location_soft(app)
    cmd = 'pm grant '+context.app+' android.permission.READ_EXTERNAL_STORAGE'
    poco.adb_client.shell(cmd)


'''断言'''

@Step('不存在{id}')
def my_not_exists(context,id):
    assert not location_for(id)

@Step('存在{id}')
def my_exists(context,id):
    assert location_for(id)

@Step('应该看到图片{img_path}')
def img_assert(context,img_path):
    context.img=location_img(img_path)
    # resolution_x = poco.get_screen_size()[0]
    # resolution_y = poco.get_screen_size()[1]
    assert_exists(Template(context.img, record_pos=None, resolution=(resolution_x, resolution_y)),context.img+"存在")

@Step('不应该看到图片{img_path}')
def img_no_assert(context,img_path):
    context.img=location_img(img_path)
    # resolution_x = poco.get_screen_size()[0]
    # resolution_y = poco.get_screen_size()[1]
    assert_not_exists(Template(context.img, record_pos=None, resolution=(resolution_x, resolution_y)),context.img+"存在")

@Step('截图与{img_path}一致')
def img_compile(context,img_path):
    context.img=location_img(img_path)
    # resolution_x = poco.get_screen_size()[0]
    # resolution_y = poco.get_screen_size()[1]
    target_image = os.path.join(ScreenshotPath,'screen.png')
    pos = find_image(image_path=context.img,target_image=target_image)
    if len(pos) == 0:
        assert False
    else:
        assert True

@Step('日期时间准确')
def time_assert(context):
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
def small_panel_accert(context,pic,ratio):
    context.ratio = float(ratio)
    context.pic = pic
    r = int((float(ratio))*100)
    # resolution_x = poco.get_screen_size()[0]
    # resolution_y = poco.get_screen_size()[1]
    # pos = location_pos(context.pic)
    screen_shoot(str(r))
    time.sleep(2)
    target_image = os.path.join(ScreenshotPath,'screen'+str(r)+'.png')
    image_path = os.path.join(PicPath,context.pic+str(r)+'.png')
    # with open("text.log",'a+') as f:
    #     f.write("before find_image")
    newpos = find_image(image_path=image_path,target_image=target_image)
    # with open("text.log",'a+') as f:
    #     f.write("after find_image")
    # newpos = find_image(image_path=r'C:\Users\86186\MVP3.0_OS_Test\features\steps\pic\云白板图标0.8.png',target_image=r'C:\Users\86186\Desktop\screen.png')
    # xpos = resolution_x/2+(pos[0]-resolution_x/2)*context.ratio
    # ypos = resolution_y-(resolution_y-pos[1])*context.ratio
    # xpos = abs(xpos-newpos[0])
    # ypos = abs(ypos-newpos[1])
    # if xpos<5 and ypos<5:
    #     assert True
    # else:
    #     assert False
    # assert True
    assert newpos

@Step('重启大屏，关机时间不超过{second1}秒，开机时间不超过{second2}秒')
def reboot_time(context,second1,second2):
    def action():
        context.showdowntime = int(second1)
        context.starttime = int(second2)
        # poco.adb_client.shell('reboot')
        beforetime = time.time()
        timeout_time = 0
        # device().adb.disconnect()
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', Android_Ip]
        for i in range(120):
            if subprocess.call(command) == 0:
                time.sleep(1)
                continue
            else:
                break
        middletime = time.time()
        showdown_times = middletime-beforetime
        for i in range(120):
            if not subprocess.call(command) == 0:
                time.sleep(1)
                continue
            else:
                break
        for i in range(60):
            time.sleep(1)
            out = poco.adb_client.shell('ps')
            if 'com.ruijie.launcher20200520' in out:
                break
        aftertime = time.time()
        start_time = aftertime - middletime
        if showdown_times<context.showdowntime and start_time<context.starttime:
            assert True
        else:
            assert False
    thread = threading.Thread(target = action)
    thread.start()
    thread.join()

@Step('批注移动到对应位置')
def assert_comments_move(context):
    posi = location_for('批注画笔').get_position()
    # write_log(log=str(context.pos))
    if abs(posi[0]*resolution_x-context.pos[0])<10 and abs(posi[1]*resolution_y-context.pos[1])<10 :
        assert True
    else:
        assert False

@Step('{app}已安装')
def already_install(context,app):
    context.app = location_soft(app)
    cmd = 'pm list package'
    package_list = poco.adb_client.shell(cmd)
    if context.app in package_list:
        assert True
    else:
        assert False

'''云白板'''
@Step('回到云白板主页')
def cloud_home(context):
    if location_for("白板返回"):
        location_for("白板返回").click()

@Step('关闭提笔即写模式')
def close_quick_write(context):
    if location_for("提笔即写"):
        location_for("提笔即写").click()
    img=location_img("提笔即写")
    resolution_x = poco.get_screen_size()[0]
    resolution_y = poco.get_screen_size()[1]
    if Template(img, record_pos=None, resolution=(resolution_x, resolution_y)):
        touch(Template(img, record_pos=None, resolution=(resolution_x, resolution_y)))
    # touch((181,947))

@Step('新建白板')
def cloud_home(context):
    if location_for("白板返回"):
        location_for("白板返回").click()
    time.sleep(0.5)
    location_for("新建白板").click()

"音视频检测"

@Step('进行视频检测')
def vedio_test(context):
    vediotest(ip=Camera_Ip,savDir=SavDir,recordTime=int(RecordTime))

@Step('播放视频{vedio}')
def play_vedio(context,vedio):
    context.vedio = "\'am start -n "+ MediaSoft +' -d \"'+TestVedioPath + vedio + '\"'+"\'"
    poco.adb_client.shell(eval(context.vedio))
    # poco.adb_client.shell('am start -n com.android.gallery3d/.app.MovieActivity -d "/mnt/usb/FC281A222819DD08/烤鸭.mp4"')
    time.sleep(1.0)
    if location_for("重新开始"):
        location_for("重新开始").click()

@Step('进行音频检测')
def voice_test(context):
    voicetest(ip=Camera_Ip,savDir=SavDir,recordTime=int(RecordTime))

@Step('播放音频{voice}')
def play_voice(context,voice):
    context.voice = "\'am start -n "+ MediaSoft +' -d \"'+TestVedioPath + vedio + '\"'+"\'"
    poco.adb_client.shell(eval(context.voice))
    # poco.adb_client.shell(am start -n com.android.gallery3d/.app.MovieActivity -d "/mnt/sdcard/test.mp4")

'''性能测试'''

@Step('对{app}进行mokey测试')
def monkey_test(context,app):
    context.soft=location_soft(app)
    log='\n'+'\n'+'MONKEY'+'\n'+'\n'
    write_log(log=log)
    cmd = "monkey -p "+context.soft+" --throttle 100 -s 5000 100"
    result = True
    FAIL_INFO = ["CRASH", "ANR", "Exception"]
    try:
        output = poco.adb_client.shell(cmd.split(" "))
        for info in FAIL_INFO:
            if info in output:
                result = False
    except Exception as e:
        result = False
        output = str(e)
    # log = "  cmd: " + cmd + "\r\r" + output
    # write_log(log)
    if not result:
        log = context.soft + "monkey test FAIL" + '\n' + output+'\n'
        logger = context.soft+output+'\n'
        write_log(log=logger)
        assert False
    else:
        log = context.soft + "monkey test PASS"+'\n'
        assert True
    write_log(log)

@Step('对{app}进行启动时间测试')
def monkey_test(context,app):
    context.soft=location_soft(app)
    log='\n'+'\n'+'STARTTIME'+'\n'+'\n'
    write_log(log=log)
    cmd = 'su root am start -W '+context.soft
    output=poco.adb_client.shell(cmd.split(" "))
    TIME_RE=re.compile(r"TotalTime: (\d+)")
    time=TIME_RE.findall(output)
    if len(time):
        if int(time[0])>3000:#启动时间
            log=context.soft+':START TIMEOUT '+str(time)+'\n'
            logger = context.soft+output+'\n'
            write_log(log=logger)
            assert False
        else:
            log=context.soft+':PASS'+str(time)+'\n'
            assert True
    else:
        log=context.soft+':NOT FOUND APP'+'\n'
        logger = context.soft+output+'\n'
        write_log(log=logger)
        assert False
    write_log(log=log)

@Step('对{app}进行UI性能测试')
def monkey_test(context,app):
    context.soft=location_soft(app)
    log='\n'+'\n'+'UI'+'\n'+'\n'
    write_log(log=log)
    cmd = "dumpsys gfxinfo "+context.soft
    output=poco.adb_client.shell(cmd)
    FPS_RE=re.compile(r"Janky frames: (\d+) \((\S+)\)")
    fps=FPS_RE.findall(output)
    if fps:
        if fps[0]=="0":
            log=context.soft+'FPS TEST PASS '+str(fps)+'\n'
            assert True
        else:
            log=context.soft+'FPS TEST FAIL '+str(fps)+'\n'
            assert False
    else:
        log=context.soft+':COMPILE FAIL'+'\n'
        logger = context.soft+output+'\n'
        write_log(log=logger)
        assert False
    write_log(log=log)

@Step('重启大屏')
def my_reboot(conetxt):
    output=poco.adb_client.shell('reboot')

@Step('连续ping丢包率为{ratio}')
def lose_package(context,ratio):
    context.ratio = int(ratio)
    cmd = 'ping '+Android_Ip+' -n 100'
    out = os.system(cmd)
    if int(out) <= context.ratio :
        assert True
    else:
        assert False

'''批注'''
@Step('画正方形')
def draw_square(context):
    swipe(v1=(365,744),v2=(465,744))
    swipe(v1=(465,744),v2=(465,844))
    swipe(v1=(465,844),v2=(365,844))
    swipe(v1=(365,844),v2=(365,744))

@Step('移动批注到任意位置')
def comments_move(context):
    posi = location_for('批注画笔').get_position()
    x = random.randint(40,1600)
    y = random.randint(40,1040)
    context.pos = [x,y]
    multitouch_event = []
    multitouch_event.append(DownEvent((posi[0]*resolution_x,posi[1]*resolution_y),0))
    multitouch_event.append(SleepEvent(1))
    multitouch_event.append(MoveEvent((x,y),0))
    multitouch_event.append(UpEvent(0))
    device().minitouch.perform(multitouch_event)

@Step('滑动擦除')
def swipe_rubber(context):
    pos = location_for('批注滑动清除').get_position()
    swipe(v1=(pos[0]*resolution_x,pos[1]*resolution_y),v2=(pos[0]*resolution_x+150,pos[1]*resolution_y))

'''云资料夹后台下载'''
@Step('删除{user}文件')
def delete_user_files(context,user):
    cmd = ''
    poco.adb_client.shell(cmd.split(""))