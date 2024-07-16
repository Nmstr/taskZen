---
layout: page
title: Move Relative
permalink: /scriptReference/modules/move-relative/
parent: Modules
grand_parent: Script Reference
nav_order: 600
---

### Move Relative

The `move-relative` module moves the mouse to an position relative to the current position. It takes 2 arguments. `x` and `y`, which are the amounts units the mouse should be moved.

Parameters:
  - x: int
  - y: int

Example usage:
```
  - type: move-relative
    x: 75
    y: 150
```

Related:
  - [Move Absolute](../move-absolute/)
