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

To see your scripts use the [lists](../list/) command.

## -f / --file

The `-f` or `--file` option can be used to specify an absolute file path instead of a script name as an input. For example, for the exampleKeyboard script you would use `taskZen execute /path/to/exampleKeyboard.yaml` instead of `taskZen execute exampleKeyboard`.
