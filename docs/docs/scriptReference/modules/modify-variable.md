---
layout: page
title: Modify Variable
permalink: /scriptReference/modules/modify-variable/
parent: Modules
grand_parent: Script Reference
nav_order: 900
---

### Modify Variable

The modify variable module allows you to modify a variable in a script. It supports multiple different actions like `set`, `add`, `subtract`, `multiply` and `divide`. It writes the result to the variable.

Parameters:
  - variable: string
  - operation: string
  - value: string

Example 1 (set):
```
- type: modify-variable
  variable: distance
  operation: set
  value: 50
```
Example 2 (add):
```
- type: modify-variable
  variable: distance
  operation: add
  value: 10
```
Example 3 (subtract):
```
- type: modify-variable
  variable: distance
  operation: subtract
  value: 50
```
Example 4 (multiply):
```
- type: modify-variable
  variable: distance
  operation: multiply
  value: 5
```
Example 5 (divide):
```
- type: modify-variable
  variable: distance
  operation: divide
  value: 2
```

The variable needs to be a valid variable name in the script. See [variables](../../variables/) for more information.
