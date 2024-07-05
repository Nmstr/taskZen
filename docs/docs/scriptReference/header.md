---
layout: page
title: Header
permalink: /scriptReference/header/
parent: Script Reference
nav_order: 100
---

# Header

The header is the top most part of any script. It defines the scripts properties.

### Name

The name of the script.

Example:
`name: exampleScript`

- This is required.
- This may contain spaces but will not be executable, if it does so.

### Speed

The execution speed of the script. It determines the delay between the execution of modules. The value is in ms.

Example:
`speed 100`

- This is required.
- This may only be an int.

### Device

The device that the script will be using.

Example:
```
device: taskZen-minimal
```

- This is required.
- The [device](https://nmstr.github.io/taskZen/deviceReference) must exist and be valid.

### Device Version

This is be the version of the device yourr script will be using.

Example:
```
device-version: 1
```

- This is optional.
- The version has to exist.
- The version must be an integer.

### Screen

This is the resolution of your screens.

Example:
```
screen:
  width: 1920
  height: 1080
```

- This is optional. It will default to 1920x1080.
- This is required for proper positioning when using move-absolute.
- On multi monitor setups the monitors should be treated as one big monitor. So 2 1920x1080 displays next to each other will result in one 3840x1080 display.

### Variables

Here you need to define any variables you have in your script.

Example:
```
variables:
  distance: 1
  startPositionX: 50
  startPositionY: 300
  iterations: 3
```

- Variable names may not contain spaces
