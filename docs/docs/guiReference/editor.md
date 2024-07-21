---
layout: page
title: Editor
permalink: /guiReference/scriptEditor/
parent: Gui Reference
nav_order: 200
---

The Editor is the central part of taskZen, where you can create and edit your scripts. It consists of a text field on the right-hand side, where you write your script. To learn more about the script syntax, click [here](../scriptReference).

On the left-hand side of the editor, there are three elements:

1. **Save** and **Run** buttons: 
    - **Save**: This button saves your script to disk.

    - **Run**: This button executes your script.
        It executes the version of the script that is currently saved on disk. Thus it is crucial to save your script before running to ensure that you execute the latest version of your script.
        By default, it executes `Exec` modules. This can be dangerous, as it may result in arbitrary code execution. Always verify the safety of your scripts before running them.

2. **Information field**: This field is used to display information about the last command that was run. It shows any errors that occurred during the execution, as well as other related information.

