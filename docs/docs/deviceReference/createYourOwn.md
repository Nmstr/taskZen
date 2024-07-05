---
layout: page
title: Create your own device
permalink: /deviceReference/createYourOwn/
parent: Device Reference
nav_order: 100
---

# Create your own device

Devices are `.yaml` files located in the `~/.config/taskZen/devices/` directory. They consist of 4 parts. The `name`, `phys`, `version` and `keys`. All are explained below.

## Name

This is the name used for a device. It will be used to access a device in a script. They should be unique, but dont have to, as devices can further be distinguised using their `version`. Here is an example of how this section could look like:
```
name: my-device
```

## Phys

This is the physical name of the device. In most cases this should be the same as the name. Here is an example of how this section could look like:
```
phys: my-device
```

## Version

This is the version of the device. This is used to distinguish between devices with the same name. They have to be an integer. Here is an example of how this section could look like:
```
version: 1
```

## Keys

Keys is the most important part of a device. It defines what keys your device has access to. If you dont define your keys properly here your script wont be able to preform its tasks properly. This section should look like this:
```
keys:
  - KEY_A
  - KEY_B
  - KEY_LEFTSHIFT
  - BTN_MOUSE
```

Refer to the [available keys](https://nmstr.github.io/taskZen/deviceReference/availableKeys) page for a list of all available keys.

Recap:
- 4 parts: `name`, `phys`, `version` and `keys`
- Name: The name of the device
- Phys: The physical name of the device
- Version: The version of the device (integer)
- Keys: The keys that the device has access to
