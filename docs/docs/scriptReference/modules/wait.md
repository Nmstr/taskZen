---
layout: page
title: Wait
permalink: /scriptReference/modules/wait/
parent: Modules
grand_parent: Script Reference
nav_order: 100
---

### Wait

The `wait` modules waits n amount of milliseconds, pausing the execution for that time.

Parameters:
  - value: int

Example usage:
```
  - type: wait
    value: 250
```

_Note: The module still waits for the execution speed defined in the `speed` section of the header. Thus a value of, for example, 250 and a `speed` value of 100 would result in a total waiting time of 450ms (100+250+100)_