---
layout: page
title: Release
permalink: /scriptReference/modules/release/
parent: Modules
grand_parent: Script Reference
nav_order: 400
---

### Release

The `release` modules releases a key which is pressed down. This will not have any effect on unpressed keys.

Parameters:
  - value: string

Example usage:
```
  - type: release
    value: KEY_A
```

The key specified in the `value` field needs to be valid and supported by your [device](https://nmstr.github.io/taskZen/deviceReference/).


Related:
  - [Press Module](../press/)
  - [Tap Module](../tap/)
