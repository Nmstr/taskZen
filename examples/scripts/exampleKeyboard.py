import taskZen
import time

taskZen.registerDevice('taskZen-minimal')

print("Starting exampleKeyboard ")

taskZen.tapKey('KEY_LEFTMETA')
time.sleep(0.25)
taskZen.tapKey('KEY_H', 'SHIFT')
time.sleep(0.1)
taskZen.tapKey('KEY_E')
time.sleep(0.1)
taskZen.tapKey('KEY_L')
time.sleep(0.1)
taskZen.tapKey('KEY_L')
time.sleep(0.1)
taskZen.tapKey('KEY_O')
time.sleep(0.1)

print("Hello")

taskZen.tapKey('KEY_SPACE')
time.sleep(0.1)
taskZen.tapKey('KEY_W', 'SHIFT')
time.sleep(0.1)
taskZen.tapKey('KEY_O')
time.sleep(0.1)
taskZen.tapKey('KEY_R')
time.sleep(0.1)
taskZen.tapKey('KEY_L')
time.sleep(0.1)
taskZen.tapKey('KEY_D')
time.sleep(0.1)
taskZen.tapKey('KEY_1', 'SHIFT')

print("World")