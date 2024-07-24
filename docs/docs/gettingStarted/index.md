---
layout: default
title: Getting started
permalink: /gettingStarted/
has_children: true
nav_order: 200
---

# Getting Started

## List your scripts

To list all available scripts you can use the "list" or "ls" command.

To run type: `taskZen ls` or `taskZen list` into your terminal.

In the ouput you will see all the scripts accessible to you. It will look like this:
```
$ taskZen ls
        taskZen
Automation utility for Wayland

Available scripts:
        - exampleExec (/home/user/.config/taskZen/scripts/exampleExec.py)
        - exampleKeyboard (/home/user/.config/taskZen/scripts/exampleKeyboard.py)
        - exampleMouse (/home/user/.config/taskZen/scripts/exampleMouse.py)
```

## Execute a script

To execute a script you can use the execute command. It requires the scripts name as the input.

To run "exampleKeyboard" type `taskZen execute exampleKeyboard` into your terminal.

You can also use the -f flag to select the script by path instead of by name.

To run "exampleKeybard" by path type `taskZen execute -f /home/user/.config/taskZen/scripts/exampleKeyboard.py` into your terminal.

## Creating your first script

For a guide on how to create your first script vistis [this](../firstScript) page.
