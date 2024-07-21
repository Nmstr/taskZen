---
layout: page
title: Press
permalink: /scriptReference/modules/press/
parent: Modules
grand_parent: Script Reference
nav_order: 200
---

### Press

The `pressKey` modules presses a key down and keeps it pressed. The key can be released again using the [release](../release/) module. Otherwise it will stay pressed.

Parameters:
  - value: string

Example usage:
```
taskZen.pressKey('KEY_A')
```

The key specified needs to be valid and supported by your [device](https://nmstr.github.io/taskZen/deviceReference/).

<br>
Related:
  - [Release Module](../release/)
  - [Tap Module](../tap/)
