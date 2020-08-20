from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import os
from airtest.core.android.minitouch import *
from airtest.core.android.base_touch import *
import random
from mappings import *
from airtest.core.cv import Template, TargetPos
import numpy as np, numpy.random
import math
from airtest.aircv import aircv
import platform
import subprocess
from airtest.core.android import adb as airtest_adb, Android
connect_device("android:///%s" % Android_Serial_No)
poco = AndroidUiautomationPoco()
def gotohome():
    # poco.adb_client.shell('input keyevent 3')
    poco.adb_client.shell('am start -n com.ruijie.launcher20200520/com.ruijie.launcher20200520.launcher.LauncherActivity')
    # home()
    touch((1,1))
    time.sleep(0.5)

def wait_restart_start(host, timeout):
    """
        等待安卓系统关机
    :param host: android系统ip
    :param timeout: 等待时长
    :return: 是否成功关机
    """
    restart_start = False
    for i in range(timeout):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', host]
        if subprocess.call(command) == 0:
            # LOGGING.info(host + " preparing to restart, current [%s]s, please wait." % str(i + 1))
            time.sleep(1)
            continue
        else:
            restart_start = True
            # LOGGING.info(host + " restarting")
            return restart_start
    if not restart_start:
        # LOGGING.error(host + " restart timeout")
        from common.exception import OSException
        raise OSException("cannot shutdown host")

def wait_restart_success(host, timeout):
    """
        等待安卓系统重启
    :param host: android系统的ip
    :param timeout: 最大等待时间(min)
    :return: bool 是否重启成功
    """
    restart_ok = False
    for i in range(timeout):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', host]
        if not subprocess.call(command) == 0:
            # LOGGING.info(host + " restarting, current [%s] min, please wait." % str(i + 1))
            # time.sleep(60)
            time.sleep(30)
            continue
        else:
            restart_ok = True
            # LOGGING.info(host + " restart ok")
            # time.sleep(60)
            return restart_ok
    if not restart_ok:
        # LOGGING.error(host + " restart timeout")
        from common.exception import OSException
        raise OSException("cannot conncect host")

host = Android_Ip
start_app('com.netease.nie.yosemite')
sleep(5)
poco.adb_client.start_cmd("reboot")

from airtest.core.error import AdbError, DeviceConnectionError
wait_restart_start(host, 100)
wait_restart_success(host, 10)
adb = device().adb if device() else airtest_adb.ADB(serialno=Android_Serial_No)
try:
    adb.disconnect()
    # sleep(40)
    sleep(20)
except (AdbError, DeviceConnectionError):
    print("进入了except")
finally:
    # sleep(20)
    sleep(5)
    connect_device("android:///%s" % Android_Serial_No)
    # LOGGING.info(device().list_app(third_only=True))
    device().minicap.install_or_upgrade()
    device().minitouch.install_and_setup()
    device().rotation_watcher.start()
    device().yosemite_ime.start()
    device()._register_rotation_watcher()
    # LOGGING.info(device().list_app(third_only=True))
sleep(10)
poco = AndroidUiautomationPoco()
app = location_for("云白板")
app.click()