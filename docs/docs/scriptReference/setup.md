---
layout: page
title: Script Setup
permalink: /scriptReference/setup/
parent: Script Reference
nav_order: 100
---

# Setup

Before starting with your actual script you need to add 2 things to your script:
- import taskZen
- register your device

First add this line at the beginning of your script to import taskZen:
```
import taskZen
```

Then register your device:
```
taskZen.registerDevice('<your device name>')
```
Information about your device can be found in the [device reference](../../deviceReference/).

---

One possible example is this:
```
import taskZen
taskZen.registerDevice('taskZen-minimal')
```