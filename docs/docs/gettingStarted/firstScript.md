---
layout: page
title: Create your first script
permalink: /firstScript/
parent: Getting started
nav_order: 300
---

# Create your first script

## Introduction

Scripts are python (.py) files used by taskZen to automate tasks. This page will walk you through on how to create your own script from scratch. If you already know the basics and want to create more advanced scripts you can view the script reference [here](../scriptReference).
To follow this tutorial all you need is a text editor of your choice and taskZen.

Scripts are located in "~/.config/taskZen/scripts/". Create a file there with the .py extension and open it. I will name my file `tutorialScript.py`. Alternatively you can click on "Create Script" in the top left of the GUI.

## Writing the script

First we will need to set things up. For that we need to import taskZen and register a device. Put the following at the beginning of your script:
```
import taskZen
```
For those familiar with python, this is nothing new. We are just importing the taskZen module. For those who are not, all that is important for now is that we need to import the module in order to use its functions, like pressing keys or moving the mouse.

The 2nd step we need to do before writing out actual script is registering a device. To do so, type:
```
taskZen.registerDevice('taskZen-minimal')
```
This will register a device with the name `taskZen-minimal`, which is a pre-installed device. A device is used to define the capabilities of a script. For example a device can define the keys that the script will have access to. For our purpose `taskZen-minimal` is enough. Later you can look into other pre-installed devices or create your own.

Now we are ready to write out our script. As a basic example, we will make over script type `test` on our keyboard and move the mouse to the center of the screen.

Lets start with writing `test`. taskZen provides a simple module called `tapKey`. It will be our friend here. Using `tapKey` we are able to press any key once. It can be accessed, as any other module, using the `taskZen` keyword, followed by a dot and then the module name. Then, inside parentheses, we need to specify the key that we want to press. In our example, we need to start with the letter `t`. Lets do that now:
```
taskZen.tapKey('KEY_T')
```
Using the same scheme we can write out the entire word.
```
taskZen.tapKey('KEY_T')
taskZen.tapKey('KEY_E')
taskZen.tapKey('KEY_S')
taskZen.tapKey('KEY_T')
```
You can find out which keys are available [here](../deviceReference/availableKeys).

Now we are already almost done! Last thing to add is to move the mouse to the center of the screen. For that we will be using the `moveAbsolute` module. We can use it the same way we used `tapKey`. The only difference is that we need to specify the `x` and `y` values inside the parentheses. Here is how we can do that:
```
taskZen.moveAbsolute(960, 540)
```
The values `960` and `540` are the coordinates of the center of the screen. Even if you have a different screen size than 1920x1080, it will still be mapped to the middle of the screen.

Our entire script should now look like this:
```
import taskZen
taskZen.registerDevice('taskZen-minimal')

taskZen.tapKey('KEY_T')
taskZen.tapKey('KEY_E')
taskZen.tapKey('KEY_S')
taskZen.tapKey('KEY_T')
taskZen.moveAbsolute(960, 540)
```

We need to quickly save and then we are ready to execute our script.

## Executing

I named the script tutorialScript.py. This is important as it influences the exact way to run the script. We can either execute it using the CLI or GUI. For the CLI we can use the `execute` command. Simply type: `taskZen execute <your script name>` (or in my case `taskZen execute tutorialScript`) into the terminal and the script will be executed. If you are using the GUI you'll need to first click on your script in the list that is on the left side of the Home page and then click the "Run" button. Note that you will not actually see it writing `test`, if you are not in a textbox. To see it you need to quickly click on a textbox.

Now, this is a very basic and arguably pretty useless script. However these are the fundamentals needed to create more sophisticated scripts, ultimately making a lot of stuff easier. To see how to create more advanced scripts you can view the script reference [here](../scriptReference).
