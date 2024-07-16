---
layout: page
title: Tap
permalink: /scriptReference/modules/tap/
parent: Modules
grand_parent: Script Reference
nav_order: 200
---

### Tap

The `tap` modules taps a key once. They key will be pressed and then released immeditely, resulting in a single actuation.

Parameters:
  - value: string
  - modifier: string

Example usage:
```
  - type: tap
    value: KEY_A
    modifier: KEY_LEFTSHIFT
```

The modifier parameter is optional. If it is not set, the key will be pressed and released without any modifier. If it is set, the key will be pressed and released with the modifier. The key specified in the `value` field needs to be valid and supported by your [device](https://nmstr.github.io/taskZen/deviceReference/).


Related:
  - [Press Module](../press/)
  - [Release Module](../release/)
