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



def swipe_move(tuple_from_xy, tuple_to_xy, duration=0.8, steps=5):
    from_x, from_y = tuple_from_xy
    to_x, to_y = tuple_to_xy

    ret = []
    interval = float(duration) / (steps + 1)

    for i in range(1, steps):
        ret.append(MoveEvent((from_x + (to_x - from_x) * i / steps,
                                from_y + (to_y - from_y) * i / steps)))
        ret.append(SleepEvent(interval))
    ret += [MoveEvent((to_x, to_y), pressure=50), SleepEvent(interval)]
    return ret

multitouch_event = []
# x = random.randint(1,1920)
x = 960
multitouch_event.append(DownEvent((960, 500), 0))
multitouch_event += swipe_move((960, 900), (960, 100), duration=10, steps=20)
# multitouch_event.append(SleepEvent(1))
multitouch_event.append(UpEvent(0))
device().minitouch.perform(multitouch_event)
# 950
# swipe_events += swipe_move(tuple_from_xy, tuple_to_xy, duration=duration, steps=steps)