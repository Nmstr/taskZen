---
layout: page
title: list / ls
permalink: /commandReference/list/
parent: Command Reference
nav_order: 100
---

# list / ls

The `list` or `ls` command is used to list all scripts available. By default it will list both the name and full absolute file path of each script.

The output will look similar to this:
```
$ taskZen ls
        taskZen
Automation utility for Wayland

Available scripts:
        - exampleExec (/home/user/.config/taskZen/scripts/exampleExec.yaml)
        - exampleKeyboard (/home/user/.config/taskZen/scripts/exampleKeyboard.yaml)
        - exampleMouse (/home/user/.config/taskZen/scripts/exampleMouse.yaml)
```

Recap:
- List all available scripts
- Shows names and absolute paths

## -r / --running

The `-r` or `--running` option can be used to only show scripts that are currently running. It will display both the name of the script and the id of the execution.

The output will look similar to this:
```
$ taskZen ls -r
        taskZen
Automation utility for Wayland

Running scripts:
4: exampleKeyboard
6: exampleMouse
```

Recap:
- Lists all running scripts
- Shows names and IDs.
