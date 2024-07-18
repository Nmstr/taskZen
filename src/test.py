import taskZen
import time

taskZen.registerDevice('taskZen-minimal')

# Calling a function directly from taskZen
taskZen.pressKey('KEY_A')
time.sleep(0.5)
taskZen.releaseKey('KEY_A')
time.sleep(0.5)
taskZen.tapKey('KEY_TAB')
time.sleep(0.5)
taskZen.tapKey('KEY_B', 'SHIFT')
time.sleep(0.5)
taskZen.moveAbsolute(1000, 100)

for i in range(5):
    time.sleep(0.1)
    taskZen.moveRelative(100, 100)
    time.sleep(0.1)
    taskZen.moveRelative(-100, -100)

for i in range(5):
    time.sleep(0.1)
    taskZen.moveRelative(100, 100)

taskZen.moveAbsolute(1001, 100)
