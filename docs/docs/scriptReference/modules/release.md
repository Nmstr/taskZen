---
layout: page
title: Release
permalink: /scriptReference/modules/release/
parent: Modules
grand_parent: Script Reference
nav_order: 300
---

### Release

The `releaseKey` modules releases a key which is pressed down. This will not have any effect on unpressed keys.

Parameters:
  - value: string

Example usage:
```
taskZen.releaseKey('KEY_A')
```

The key specified in the `value` field needs to be valid and supported by your [device](https://nmstr.github.io/taskZen/deviceReference/).

<br>
Related:
  - [Press Module](../press/)
  - [Tap Module](../tap/)
