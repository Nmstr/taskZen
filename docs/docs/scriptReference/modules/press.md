---
layout: page
title: Press
permalink: /scriptReference/modules/press/
parent: Modules
grand_parent: Script Reference
nav_order: 300
---

### Press

The `press` modules presses a key down and keeps it pressed. The key can be released again using the [release](../release/) module. Otherwise it will stay pressed.

Parameters:
  - value: string

Example usage:
```
  - type: press
    value: KEY_A
```

The key specified in the `value` field needs to be valid and supported by your [device](https://nmstr.github.io/taskZen/deviceReference/).


Related:
  - [Release Module](../release/)
  - [Tap Module](../tap/)
