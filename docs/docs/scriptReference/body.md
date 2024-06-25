---
layout: page
title: Body
permalink: /scriptReference/body/
parent: Script Reference
nav_order: 200
---

# Body

The body is the main part of the script. It contains one `steps` element. This steps element is filled with modules.

Example:
```
steps:
  - type: tap
    value: KEY_A
```

## Modules

### Wait

This waits n amount of ms. N is specified in the value field.

Example:
```
  - type: wait
    value: 250
```

- The value may only be an int.
- This still waits for the execution speed defined in the `speed` section of the header. Thus a value of 250 and a `speed` value of 100 would result in a total waiting time of 450ms (100+250+100)

### Tap

This taps any key once. Modifiers may be applied.

Example:
```
  - type: tap
    value: KEY_A
```
Example 2:
```
  - type: tap
    value: KEY_A
    modifier: SHIFT
```

- This only taps the key once.
- This only handles one key.
- Available modifiers:
  - SHIFT

### press

This presses a key down.

Example:
```
  - type: press
    value: KEY_A
```

- The key will remain pressed until released.

### release

This releases a pressed key.

Example:
```
  - type: release
    value: KEY_A
```

- This does nothing on keys not pressed down.

### move-absolute

This moves the mouse to an absolute position on the screen. It takes x and y as an input.

Example:
```
  - type: move-absolute
    x: 500
    y: 500
```

- The position is absolute.
- The mouse movement is instantaneous.
- For accurate positioning the screen section in the header needs to be configured correctly.
- BTN_MOUSE is required to be in the header under `keys` for this to work.

### move-relative

This moves the mouse to position on the screen relative to the current position of the mouse. It takes x and y as an input.

Example:
```
  - type: move-relative
    x: 100
    y: 50
```

- The position is relative to the mouse cursor.
- The mouse movement is instantaneous.
- BTN_MOUSE is required to be in the header under `keys` for this to work.

### exec

This is used to execute terminal commands. It can be run both blocking and non-blocking.

Example:
```
  - type: exec
    value: notify-send "Example"
```
Example 2:
```
  - type: exec
    value: /path/to/some/application
    blocking: True
```

- This can both be blocking or non-blocking
- It will default to non-blocking
- This can execute ANY command (some might need user action; like e.g. sudo)

**Caution: Scripts using this might be malicious and should always be treated with a high level of distrust! Only run these scripts when you know what you are doing and have verified that the script is safe!**

### loop

This is used to create loops. Loops can loop over any amount of any module for any amount of iterations.

Example 1 (1 subStep):
```
  - type: loop
    value: 5
    subSteps:
      - type: tap
        value: KEY_A
```

Example 2 (multiple Substeps):
```
  - type: loop
    value: 10
    subSteps:
      - type: move-relative
        x: 100
        y: 0
      - type: wait
        value: 100
```

Example 3 (nested loops):
```
  - type: loop
    value: 3
    subSteps:
      - type: tap
        value: KEY_A
      - type: loop
        value: 3
        subSteps:
          - type: tap
            value: KEY_B
```

- Loops may contain multiple subSteps.
- Loops can be nested.
- The value "value" indicates how many times the loop is repeated.
- The value "value" may only be an int.

### modify-variable

This is used to modify variables. It supports setting, adding, subtracting, multiplying and dividing them.

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

- Add, subtract, multiply and divide may only deal with numbers.
- Variables need to first be defined in the header.

### if

This is used to check if the given input is true or false and if it is so execute one of 2 branches.

Valid operations are: `bool` (checks if bool is true or false), `==`, `!=`, `>`, `<`, `>=` and `<=`.

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

- If statements may contain multiple trueSteps or falseSteps.
- If statements may contain both trueSteps and falseSteps.
- If statements can also only contain trueSteps or falseSteps.
- If statements can be nested.
- The value2 field is not required for the bool operation.
- The `==`, `!=`, `>`, `<`, `>=` and `<=` operations all work pretty much the same.

## Other

This section describes other behaviors of scripts that do not fit in any other category.

### Usage of Variables

Variables can be used anywhere, where a value is used. Just replace the value with `$variableName`. For example, if you have a variable called sleepTime you can use it like this:
```
- type: wait
  value: $sleepTime
```

If `sleepTime` is set to 100, then this would sleep for 100ms.
