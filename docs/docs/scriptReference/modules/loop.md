---
layout: page
title: Loop
permalink: /scriptReference/modules/loop/
parent: Modules
grand_parent: Script Reference
nav_order: 700
---

### Loop

The `loop` module is used to create for loops. It has sub-steps, which it will loop over for the value that is set in the `value` field.

Parameters:
  - value: int
  - subSteps: array

Example usage:
```
  - type: loop
    value: 10
    subSteps:
      - type: tap
        value: KEY_A
```

The `value` field defines how many times the sub-steps will be executed. The `subSteps` field defines the sub-steps that will be executed.
