import datetime
import logging
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from airtest.core.cv import Template, TargetPos
from airtest.core.android.touch_methods.minitouch import *
from airtest.core.android.touch_methods.base_touch import *
from airtest.core.api import *
from airtest.aircv import aircv
from config.config import *
poco = AndroidUiautomationPoco()

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler(os.path.join(LogPath,'log'))
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def location_for(key):
    location = POCO_DICT.get(key)
    if isinstance(location, dict) and location["type"] == "text":
        return poco(text=location["attrs"])
    elif isinstance(location, dict) and location["type"] == "complex":
        return eval(location["attrs"])
    else:
        return poco(location)

def location_soft(key):
    location = SOFT_DICT.get(key)
    return location
    
def location_img(key):
    # location = IMG_DICT.get(key)
    location = key + '.png'
    location = os.path.join(PicPath,location)
    return location

def location_pos(key):
    position = []
    location = POS_DICT.get(key)
    if int(location[1]):
        position.append(int(location[1:5]))
    else:
        position.append(int(location[2:5]))
    if int(location[6]):
        position.append(int(location[6:10]))
    else:
        position.append(int(location[7:10]))
    return position

def poco_type(type, content):
    attr = {
        "type": type,
        "attrs": content
    }
    return attr

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
    # query = Template(image_path, target_pos=target_pos, resolution=(1920, 1080),rgb = rgb)
    while True:
        if target_image:
            screen = aircv.imread(target_image)
        else:
            imagepath = ScreenshotPath + datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + ".png"
            snapshot(imagepath)
            screen = aircv.imread(imagepath)
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

def multi_swipe(tuple_from_xy, tuple_to_xy,finger=1, duration=0.8, steps=5,sleep=True,move=True,up=True):
    #多指按压滑动抬起
    from_x, from_y = tuple_from_xy
    to_x, to_y = tuple_to_xy
    multitouch_event = []
    for i in range(0,finger):
        multitouch_event.append(DownEvent((from_x+10*(i-1),from_y),i))

    interval = float(duration) / (steps + 1)
    for i in range(1, steps + 1):
        move_events = []
        if sleep == True:
            move_events = [
                    SleepEvent(interval),
                    # MoveEvent((from_x + ((to_x - from_x) * i / steps), from_y + (to_y - from_y) * i / steps),
                    #             contact=0, pressure=50),
                ]
        if move == True:
            for j in range(0,finger):
                move_events += [MoveEvent((from_x + ((to_x - from_x) * i / steps)+(10*(j-1)), from_y + (to_y - from_y) * i / steps),
                                contact=j, pressure=50),]
            multitouch_event.extend(move_events)
    if up == True:
        for i in range(0,finger):
            multitouch_event.append(UpEvent(i))

    return multitouch_event

def screen_shoot(name):
    poco.adb_client.shell('screencap -p /sdcard/screen.png')
    time.sleep(2)
    screenshootpath = 'pull /sdcard/screen.png '+os.path.join(ScreenshotPath,'screen'+str(name))+'.png'
    poco.adb_client.start_cmd(eval('%r'%screenshootpath))
    time.sleep(2)
    poco.adb_client.shell('rm /sdcard/screen.png')

def write_log(log,name="Result"):
    log_name = name
    # print(log_name)
    with open(os.path.join(LogPath,log_name), "a+") as f:
        f.write(log)

POCO_DICT = {
    "账号" : "com.ruijie.launcher20200520:id/et_account",
    "密码" : "com.ruijie.launcher20200520:id/et_password",
    "登录" : "com.ruijie.launcher20200520:id/btn_login_go",
    "下课" : "com.ruijie.launcher20200520:id/btn_class_over",
    "账号登录":"com.ruijie.launcher20200520:id/btn_login_manual",
    "登录头像":"com.ruijie.launcher20200520:id/iv_avatar",
    "快速登录":"com.ruijie.launcher20200520:id/iv_avatar",
    "允许快捷登录":"com.ruijie.launcher20200520:id/cb_save_password",
    "关闭云资料夹":"com.ruijie.whiteboard.cloudfile.screen:id/iv_close",
    "云资料夹":poco_type("text","云资料夹"),
    "返回标题":"com.ruijie.launcher20200520:id/tv_title_bar",
    "登录历史":"com.ruijie.launcher20200520:id/btn_show_account_history",
    # "云资料夹":"com.ruijie.launcher20200520:id/iv_app_icon",
    "移除账号" : "com.ruijie.launcher20200520:id/btn_login_go",
    "时间" : "com.ruijie.launcher20200520:id/tv_time_hour",
    "日期" : "com.ruijie.launcher20200520:id/tv_time_calendar",
    "云白板":poco_type("text","云白板"),
    "重新开始" : "android:id/button2",
    "取消按钮":"com.ruijie.launcher20200520:id/tv_cancel",
    "新建白板":"android.widget.ImageView",
    "画笔":"com.ruijie.whiteboard.lscreen:id/penview",
    "提笔即写":"com.ruijie.whiteboard.lscreen:id/view_pen_start",
    "白板返回":"com.ruijie.whiteboard.lscreen:id/doodle_back_iv",
    "浏览器新建页":"com.android.browser:id/newtab",
    "关闭浏览器页":"com.android.browser:id/close",
    "PPT":"com.ruijie.whiteboard.cloudfile.screen:id/tv_name",
    "批注画笔":"com.ruijie.launcher:id/btn_paint",
    "批注细笔":"com.ruijie.launcher:id/rb_size_small",
    "批注中笔":"com.ruijie.launcher:id/rb_size_middle",
    "批注粗笔":"com.ruijie.launcher:id/rb_size_big",
    "批注橡皮":"com.ruijie.launcher:id/btn_rubber",
    "批注小橡皮":"com.ruijie.launcher:id/rb_size_small",
    "批注中橡皮":"com.ruijie.launcher:id/rb_size_middle",
    "批注大橡皮":"com.ruijie.launcher:id/rb_size_big",
    "批注滑动清除":"com.ruijie.launcher:id/iv_slide",
    "批注保存":"com.ruijie.launcher:id/btn_save",
    "批注关闭":"com.ruijie.launcher:id/btn_close",
}

SOFT_DICT = {
    # "登录软件" : 'adb shell am start -n com.ruijie.login.server/com.ruijie.login.server.ui.login.LoginActivity',
    # "登录软件" : 'com.ruijie.login.server',
    "云资料夹" : 'com.ruijie.whiteboard.cloudfile.screen',
    "云白板" : 'com.ruijie.whiteboard.lscreen',
    "云资料夹ac":"com.ruijie.whiteboard.cloudfile.screen/.home.MainActivity",
    "云白板ac":"com.ruijie.whiteboard.lscreen/com.ruijie.whiteboard.rj_board.BoardListActivity",
    "NB物理实验" : 'nb.com.nobook.nbPhysStudent',
    "NB化学实验" : 'nb.com.nobook.nbChemicalStudent',
    "浏览器" : 'com.android.browser',
    "桌面程序" : 'com.ruijie.launcher20200520',
    "视频播放器" : 'com.mstar.tv.tvplayer.ui',
    "WPS" : 'com.kingsoft.moffice_pro',
    "语音激励": 'com.ruijie.speech.appear',
    "文件": 'com.android.documentsui',
    "外研通": 'com.viaton.wyt',
}

POS_DICT = {
    "云资料夹" : '(1189,0384)',
    "云白板图标" : '(1000,0384)',
    "账号登录图标" : '(0350,0452)',
    "宝可梦图片" : '(0780,0359)',
}