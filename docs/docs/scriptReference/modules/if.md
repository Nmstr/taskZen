---
layout: page
title: If
permalink: /scriptReference/modules/if/
parent: Modules
grand_parent: Script Reference
nav_order: 800
---

### If

The `if` module is used to create if statements. It has sub-steps, which it will execute if the condition is true and sub-steps, which it will execute if the condition is false. These sub-steps are called branches. It takes an operation and either one or two values to determine which branch to execute. Valid operations are `bool` (checks if bool is true or false), `==`, `!=`, `>`, `<`, `>=` and `<=`.

Parameters:
  - operation: string
  - value1: string
  - value2: string
  - trueSteps: array
  - falseSteps: array

Example 1 (trueSteps | operation: bool):
```
- type: if
  operation: bool
  value1: True
  trueSteps:
  - type: tap
    value: KEY_1
```
Example 2 (falseSteps | operation: ==):
```
- type: if
  operation: "=="
  value1: $variableName
  value2: 25
  falseSteps:
  - type: tap
    value: KEY_1
```
Example 3 (Both | operation: <):
```
- type: if
  operation: "<"
  value1: $variableName
  value2: 100
  trueSteps:
  - type: tap
    value: KEY_1
  falseSteps:
  - type: tap
    value: KEY_2
```