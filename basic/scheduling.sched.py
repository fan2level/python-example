# -*-coding:utf-8-*-
import sched, time

sdelay = 1
s = sched.scheduler(time.time, time.sleep)

def timetick(delay):
    print('do something')
    s.enter(delay, 1, timetick, argument=(delay,))
timetick(sdelay)

s.run()
print('done')
