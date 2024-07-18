import taskZen
import time

taskZen.registerDevice('taskZen-minimal')

taskZen.moveAbsolute(75, 150)
time.sleep(0.5)
for i in range(10):
  time.sleep(0.1)
  taskZen.moveRelative(100, 0)
for i in range(5):
  time.sleep(0.1)
  taskZen.moveRelative(0, 100)
for i in range(10):
  time.sleep(0.1)
  taskZen.moveRelative(-100, 0)
for i in range(5):
  time.sleep(0.1)
  taskZen.moveRelative(0, -100)
