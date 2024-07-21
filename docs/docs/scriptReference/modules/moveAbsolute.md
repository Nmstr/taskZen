---
layout: page
title: Move Absolute
permalink: /scriptReference/modules/move-absolute/
parent: Modules
grand_parent: Script Reference
nav_order: 400
---

### Move Absolute

The `moveAbsolute` module moves the mouse to an absolute position. The position is mapped to a 1920x1080 screen. If your screen is not 1920x1080, it will still be mapped correctly.

Parameters:
  - x: int
  - y: int

Example usage:
```
taskZen.moveAbsolute(960, 540)
```

The `x` and `y` values need to be between 0 and the width and height of the screen. You will have to set the screen in the header properly for this to work correctly.

<br>
Related:
  - [Move Relative](../move-relative/)
