---
layout: page
title: Variables
permalink: /scriptReference/variables/
parent: Script Reference
nav_order: 300
---

# Body

Variables need to be defined in the header of a script. See [header](../header/#variables) for more information. They can then be used inside the Body of the script to replace most other inputs. Where you'd normally write a value, you can replace it with the variable name prefixed by `$`.

Example:
```
- type: wait
  value: $sleepTime
```

Example2:
```
- type: key
  value: $key
  modifier: $modifier
```
