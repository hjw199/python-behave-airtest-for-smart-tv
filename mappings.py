from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from features.config.config import *
poco = AndroidUiautomationPoco()

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
    location = IMG_DICT.get(key)
    location = PicPath + location
    return location

def poco_type(type, content):
    attr = {
        "type": type,
        "attrs": content
    }
    return attr


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
}

SOFT_DICT = {
    # "登录软件" : 'adb shell am start -n com.ruijie.login.server/com.ruijie.login.server.ui.login.LoginActivity',
    "登录软件" : 'com.ruijie.login.server',
    "云资料夹" : 'com.ruijie.whiteboard.cloudfile.screen',
    "云白板" : 'com.ruijie.whiteboard.lscreen',
}

IMG_DICT = {
    "已登录图片":'已登录图片.png',
    "未登录图片":'未登录图片.png',
    "账号登录图片":'账号登录图片.png',
    # "下课图片":'C:\\Ruijie\\OS_test\\features\\steps\\pic\\下课图片.png',
    "下课图片":'下课图片.png',
    "快速登录图片":'快速登录图片.png',
    "从快速登录移除图片":'从快速登录移除图片.png',
    "需要登录账号":'需要登录账号.png',
    "账号密码错误提示":'账号密码错误提示.png',
    "云白板图标":'云白板图标.png',
    "白板登录头像":'白板登录头像.png',
    "宝可梦图片":'宝可梦图片.png',
    "ppt图片":'ppt图片.png',
    #"移除账号":'C:\\Ruijie\\OS_test\\features\\steps\\pic\\移除账号.png',
    "移除账号":'移除账号.png',
    "常用应用栏":'常用应用栏.png',
    "常用应用云白板图标":'常用应用云白板图标.png',
    "常用应用云资料夹图标":'常用应用云资料夹图标.png',
    "正在运行应用":'正在运行应用.png',
    "正在运行云白板图标":'正在运行云白板图标.png',
    "正在运行云资料夹图标":'正在运行云资料夹图标.png',
    "关闭正在运行应用":'关闭正在运行应用.png',
}