---
layout: page
title: execute
permalink: /commandReference/execute/
parent: Command Reference
nav_order: 200
---

# execute

The `execute` command is used to execute a script. By default it will take the scripts name as its input. This is an example of how it would look like when executing one of the example scripts:
```
$ taskZen execute exampleKeyboard
Executing exampleKeyboard
```

To see your scripts use the [lists](https://nmstr.github.io/taskZen/commandReference/list/) command.

Recap:
- Executes scripts by name

## -v / --verbose

The `-v` or `--verbose` option can be used to get a verbose output. It will print what the script does to console. It can be appended to any other combination of options to achieve that verbose output. Using it on one of the example scripts looks like this:
```
$ taskZen execute exampleKeyboard -v
Executing exampleKeyboard
{'type': 'tap', 'value': 'KEY_LEFTMETA'}
{'type': 'wait', 'value': 250}
{'type': 'tap', 'value': 'KEY_H', 'modifier': 'SHIFT'}
{'type': 'tap', 'value': 'KEY_E'}
{'type': 'tap', 'value': 'KEY_L'}
{'type': 'tap', 'value': 'KEY_L'}
{'type': 'tap', 'value': 'KEY_O'}
{'type': 'tap', 'value': 'KEY_SPACE'}
{'type': 'tap', 'value': 'KEY_W', 'modifier': 'SHIFT'}
{'type': 'tap', 'value': 'KEY_O'}
{'type': 'tap', 'value': 'KEY_R'}
{'type': 'tap', 'value': 'KEY_L'}
{'type': 'tap', 'value': 'KEY_D'}
{'type': 'tap', 'value': 'KEY_1', 'modifier': 'SHIFT'}
```

Recap:
- Makes the output verbose.

## -f / --file

The `-f` or `--file` option can be used to specify an absolute file path instead of a script name as an input. For example, for the exampleKeyboard script you would use `taskZen execute /path/to/exampleKeyboard.yaml` instead of `taskZen execute exampleKeyboard`.

This is usefull if you for example have conflicting script names and dont know that or dont want to change them.

Recap:
- Executes a script from a file instead of a name

## -y / --yes

The `-y` or `--yes` option can be used to answer yes to all prompts. It can be appended to any other combination of options. An example of such a prompt is the confirmation prompt for when running a script with an exec module.

Recap:
- Answers yes to all prompts

## -k / --kill

The `-k` or `--kill` option can be used to kill the running script. It will take the ID of the execution to kill as an input. You can find the IDs of the running scripts using the [list](https://nmstr.github.io/taskZen/commandReference/list/) command.

Recap:
- Kills a running script using its ID
