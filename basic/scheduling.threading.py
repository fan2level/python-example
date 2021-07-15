# -*-coding:utf-8-*-

import time
import threading

sdelay = 1
def timetick(delay):
    print('do something')
    threading.Timer(delay, timetick,args=(delay,)).start()

timetick(sdelay)

print('done')
