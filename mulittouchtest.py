from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco()
import os
from airtest.core.android.touch_methods.minitouch import *
from airtest.core.android.touch_methods.base_touch import *
import random
from mappings import *
from airtest.core.cv import Template, TargetPos
import numpy as np, numpy.random
import math
from airtest.aircv import aircv



def swipe_move(tuple_from_xy, tuple_to_xy, duration=0.8, steps=5):
    # 单指滑动
    from_x, from_y = tuple_from_xy
    to_x, to_y = tuple_to_xy

    ret = []
    interval = float(duration) / (steps + 1)

    for i in range(1, steps):
        ret.append(MoveEvent((from_x + (to_x - from_x) * i / steps,
                                from_y + (to_y - from_y) * i / steps),0))
        ret.append(SleepEvent(interval))
    ret += [MoveEvent((to_x, to_y),0, pressure=50), SleepEvent(interval)]
    return ret

def mulit_swipe_move(tuple_from_xy, tuple_to_xy,finger=0,duration=0.8, steps=5):
    #多指滑动
    from_x, from_y = tuple_from_xy
    to_x, to_y = tuple_to_xy

    ret = []
    interval = float(duration) / (steps + 1)
    for i in range(1, steps):
        for j in range(0,finger+1):
            ret.append(MoveEvent((from_x + (to_x - from_x) * i / steps + 20*(j-1),
                                    from_y + (to_y - from_y) * i / steps),contact=finger))
        ret.append(SleepEvent(interval))
    for j in range(0,finger):
        ret += [MoveEvent((to_x + 20*(j-1), to_y),contact=finger, pressure=50),SleepEvent(interval)]
    return ret


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

    return multitouch_event

'''原始函数'''
# def mulit_swipe(tuple_from_xy, tuple_to_xy,finger=0, duration=0.8, steps=5):
#     from_x, from_y = tuple_from_xy
#     to_x, to_y = tuple_to_xy
#     swipe_events = []

#     interval = float(duration) / (steps + 1)
#     for i in range(1, steps + 1):
#         move_events = [
#                 SleepEvent(interval),
#                 # MoveEvent((from_x + ((to_x - from_x) * i / steps), from_y + (to_y - from_y) * i / steps),
#                 #             contact=0, pressure=50),
#             ]
#         for j in range(0,finger+1):
#             move_events += [MoveEvent((from_x + ((to_x - from_x) * i / steps)+(10*(j-1)), from_y + (to_y - from_y) * i / steps),
#                             contact=j, pressure=50),]
#         swipe_events.extend(move_events)
#     return swipe_events

'''测试mulit_swipe多指'''
# finger = random.randint(0,4)
# multitouch_event = []
# x = random.randint(10,1890)
# y = 1000
# st = random.randint(50,160)

# multitouch_event = []
# multitouch_event += multi_swipe((x,y), (x,y-st),finger=finger, duration=0.8, steps=5)
# print("1111111111111111111111111111111111111111111111")
# print(multitouch_event)

# device().minitouch.perform(multitouch_event)



'''测试mulit_swipe_move多指'''
# multitouch_event = []
# multitouch_event.append(DownEvent((960,500),0))
# multitouch_event.append(DownEvent((930,500),1))
# multitouch_event.append(DownEvent((900,500),2))
# multitouch_event += mulit_swipe_move((960,500), (960,100),finger=2, duration=0.8, steps=5)
# multitouch_event.append(UpEvent(0))
# multitouch_event.append(UpEvent(1))
# multitouch_event.append(UpEvent(2))
# device().minitouch.perform(multitouch_event)

'''最初多指滑动'''
# multitouch_event = []
# multitouch_event.append(DownEvent((960,500),0))
# multitouch_event.append(DownEvent((930,500),1))
# multitouch_event.append(DownEvent((900,500),2))
# multitouch_event += swipe_move((960,500), (960,100),finger=0, duration=0.8, steps=5)
# multitouch_event += swipe_move((930,500), (960,100),finger=1, duration=0.8, steps=5)
# multitouch_event += swipe_move((900,500), (960,100),finger=2, duration=0.8, steps=5)
# multitouch_event.append(UpEvent(0))
# multitouch_event.append(UpEvent(1))
# multitouch_event.append(UpEvent(2))
# device().minitouch.perform(multitouch_event)

'''循环测试合理距离'''
# while True:
    # multitouch_event = []
    # x = random.randint(1,1920)
    # y = random.randint(1031,1080)
    # multitouch_event.append(DownEvent((x,1080),0))
    # multitouch_event.append(MoveEvent((x,y),0))
    # # multitouch_event += swipe_move((x,1050), (x,y), duration=0.8, steps=5)
    # # multitouch_event.append(SleepEvent(1))
    # multitouch_event.append(UpEvent(0))
    # device().minitouch.perform(multitouch_event)
    # time.sleep(0.5)

'''测试swipe_move多指'''
# touch((1,1))
# time.sleep(2)
# multitouch_event = []
# x = random.randint(1,1920)
# y = random.randint(1020,1080)
# st = random.randint(50,160)
# print("11111111111111111111111111111111111111111")
# print(x,y,st)
# # multitouch_event.append(DownEvent((x,y),0))
# # multitouch_event.append(MoveEvent((x,y-st),0))
# multitouch_event.append(DownEvent((x,1021),0))
# multitouch_event.append(MoveEvent((x,1021-160),0))
# # multitouch_event += swipe_move((x,1050), (x,y), duration=0.8, steps=5)
# # multitouch_event.append(SleepEvent(1))
# multitouch_event.append(UpEvent(0))
# device().minitouch.perform(multitouch_event)
# time.sleep(2)

'''滑动按压，延时，抬起'''
# multitouch_event = []
# x = random.randint(1,1920)
# multitouch_event.append(DownEvent((x, 1000), 0))
# multitouch_event.append(MoveEvent((x,600),0))
# # multitouch_event.append(UpEvent(0))
# device().minitouch.perform(multitouch_event)
# time.sleep(3)
# multitouch_event.append(UpEvent(0))
# device().minitouch.perform(multitouch_event)

'''测试mulit_swipe_noup多指'''
# finger = random.randint(1,5)
# # finger = 1
# x = random.randint(10,1890)
# y = 1080
# # st = random.randint(0,40)
# st = 30
# multitouch_event = []
# multitouch_event += multi_swipe_noup((x,y), (x,y-st),finger=finger, duration=0.8, steps=5)
# # print("1111111111111111111111111111111111111111111111")
# # print(multitouch_event)
# device().minitouch.perform(multitouch_event)
# # time.sleep(5)
# multitouch_event = []
# for i in range(0,5):
#     multitouch_event.append(UpEvent(i))
# print("1111111111111111111111111111111111111111111111")
# print(multitouch_event)
# device().minitouch.perform(multitouch_event)
'''测试回到桌面'''
# while True:
#     # finger = random.randint(1,5)
#     finger = 1
#     multitouch_event = []
#     x = random.randint(10,1890)
#     # y = random.randint(1070,1080)
#     y=1080
#     # st = random.randint(OAppHigh,1080)
#     # st = random.randint(110,y)
#     st=200
#     # duration = round(float(st)/float(1500),2)
#     # duration = round(float(st)/float(3000),2)
#     duration = 0
#     # swipe((x,y),(x,y-st),duration=0)
#     touch((996,381))
#     time.sleep(1)
#     multitouch_event += multi_swipe((x,y), (x,y-st),finger=finger, duration=duration, steps=5)
#     # print("1111111111111111111111111111111111111111111111")
#     # print(multitouch_event)
#     # device().minitouch.perform(multitouch_event)
#     # # print("1111111111111111111111111111111111111111111111")
#     # # print(y-st)
#     # # print(duration)
#     # multitouch_event = []
#     # multitouch_event.append(DownEvent((1000, 1080), 0))
#     # for y in range(40,200,40):
#     #     multitouch_event.append(MoveEvent((1000,1080-y),0))
#     # multitouch_event.append(UpEvent(0))
#     device().minitouch.perform(multitouch_event)
#     i+=1
#     time.sleep(2)
#     print("1111111111111111111111111111111111")
#     print(i)
#     assert location_for("时间")

# 624/0.15   465/0.2    869/0.07     744/0.11    907/0.05      442/0.21     425/0.22

'''点击正在运行应用外围'''
# while True:
#     x=random.randint(1,1920)
#     y=random.randint(1,1080)
#     if 290<x<714 and 190<y<493:
#         continue
#     if 737<x<1161 and 190<y<493:
#         continue
#     if 1183<x<1607 and 190<y<493:
#         continue
#     if 290<x<714 and 514<y<816:
#         continue
#     if 737<x<1161 and 514<y<816:
#         continue
#     if 1183<x<1607 and 514<y<816:
#         continue
#     if 592<x<1324 and 920<y<1061:
#         continue
#     else:
#         print("1111111111111111111111111111111111111111111111")
#         print(x,y)
#         touch((x,y))
#         break

# while True:
#     x=random.randint(1,1920)
#     y=random.randint(1,1080)
#     if 592<x<1324 and 920<y<1061:
#         continue
#     else:
#         print("1111111111111111111111111111111111111111111111")
#         print(x,y)
#         touch((x,y))
#         break
i=0
while True:
    x=random.randint(400,1500)
    y=random.randint(1,500)
    multitouch_event=[]
    multitouch_event += multi_swipe(tuple_from_xy=(x,y),tuple_to_xy=(x,y+500),finger=4,duration=0)
    device().minitouch.perform(multitouch_event)
    touch((1,1))
    i+=1
    print("11111111111111111111111111111111111")
    print(x,y)
    print(i)