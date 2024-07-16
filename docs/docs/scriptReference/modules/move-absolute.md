---
layout: page
title: Move Absolute
permalink: /scriptReference/modules/move-absolute/
parent: Modules
grand_parent: Script Reference
nav_order: 500
---

### Move Absolute

The `move-absolute` module moves the mouse to an absolute position. The position is mapped to your screen using the [screen](../../header/#screen) section from the header.

Parameters:
  - x: int
  - y: int

Example usage:
```
  - type: move-absolute
    x: 75
    y: 150
```

The `x` and `y` values need to be between 0 and the width and height of the screen. You will have to set the screen in the header properly for this to work correctly.

Related:
  - [Move Relative](../move-relative/)
