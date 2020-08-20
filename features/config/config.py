#!/usr/bin/env python
# encoding: utf-8
"""
@author: hjw
@file: CONST.py
@time: 2020/5/7 17:35
@desc: 解析ini配置文件
"""

import configparser
import os
from configparser import ConfigParser

conf = configparser.ConfigParser()
ini_path = os.path.join(os.path.dirname(__file__), "config.ini")
conf.read(ini_path, encoding="utf-8")

global Android_Ip
global Android_Serial_No
global System_Version
global Touch_Frame_Version

global Camera_Ip
global SavDir
global RecordTime

global ArmPort

global PicPath
global TestVedioPath

global MediaSoft

Android_Ip = conf.get("Android", "ip").strip()
Android_Serial_No = conf.get("Android", "serial_no").strip()
# System_Version = conf.get("Android", "system_version").strip()
# Touch_Frame_Version = conf.get("Android", "touch_frame_version").strip()

RecordTime = conf.get("Camera", "RecordTime").strip()
Camera_Ip = conf.get("Camera", "CameraIp").strip()
SavDir = conf.get("Camera", "SavDir").strip()

ArmPort = conf.get("Arm", "ArmPort").strip()
ArmUse = conf.get("Arm", "ArmUse").strip()

PicPath = conf.get("path", "PicPath").strip()
TestVedioPath = conf.get("path", "TestVedioPath").strip()

MediaSoft = conf.get("soft", "MediaSoft").strip()
