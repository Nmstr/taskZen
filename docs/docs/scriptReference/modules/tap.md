---
layout: page
title: Tap
permalink: /scriptReference/modules/tap/
parent: Modules
grand_parent: Script Reference
nav_order: 100
---

### Tap

The `tapKey` module taps a key once. They key will be pressed and then released immeditely, resulting in a single actuation.

Parameters:
  - value: string
  - modifier: string

Example usage:
```
taskZen.tapKey('KEY_A', 'KEY_LEFTSHIFT')
```

The `tapKey` module takes two arguments: `key` and `modifier`. `key` is the key that will be pressed and `modifier` is the modifier that will be used. If no modifier is specified, it will only press the `key`. Common modifiers are `KEY_LEFTSHIFT` and `KEY_LEFTCTRL`.

The keys need to be valid and supported by your [device](../../../deviceReference/).

<br>
Related:
  - [Press Module](../press/)
  - [Release Module](../release/)
