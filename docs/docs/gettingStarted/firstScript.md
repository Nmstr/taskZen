---
layout: page
title: Create your first script
permalink: /firstScript/
parent: Getting started
nav_order: 300
---

# Create your first script

## Introduction

Scripts are .yaml files used by taskZen to automate tasks. This page will walk you through on how to create your own script from scratch. If you already know the basics and want to create more advanced scripts you can view the script reference [here](https://nmstr.github.io/taskZen/scriptReference).
To follow this tutorial you will need to have taskZen and a text editor installed.

Scripts are located in "~/.config/taskZen/". Create a .yaml file there and open it.

## Writing the header

The header of the file is the top most part. Here you will define its properties.

The first thing you will need to set is the `name`. For this script the name will be `exampleScript`.

`name: exampleScript`

_Note that allthough you can use spaces, you wont be able to execute the script if you do so._

***

The next thing to set is the `speed`. The speed it the time between instructions in ms. We will be using the value 100.

`speed: 100`

***

Now follows another critical part for the header. The `device` section. Here you need to define what device you want to use in your script. Different devices have different capabilites. Later you can even define your own devices, but for now the built-in `taskZen-minimal` device will do the job.

`device: taskZen-minimal`

***

Now the last part of the header. The `screen` section. Here goes the width and height of your screens. This is used for absolute mouse positioning. For 1 single 1920x1080 display this section would look like this:
```
screen:
  width: 1920
  height: 1080
```
This is what we will be using here.
If you have multiple screens next to each other their resolution will sum up. For example for 2 1920x1080 displays next to each other the width would be 3840

_Note that this is the only optional section in the header. If not set, it will default to 1920x1080._

***
A more detailed explanation of the header can be found [here](https://nmstr.github.io/taskZen/scriptReference/header/).

Our final header should now look like this

```
name: exampleScript
speed: 100
keys:
  - KEY_A
  - KEY_B
  - KEY_LEFTSHIFT
  - BTN_MOUSE
screen:
  width: 1920
  height: 1080
```

## Writing the body

The body is the most important part of your script. And it is simple. It just consists of one single part. `steps`. Now, steps do have a lot of options, but we will keep it simple here.

This is what we want to do with our script:
* Type an "A"
* Wait half a second
* Type a capital "B"
* Move the mouse to an absolute position
* Wait another half a second
* Move the mouse 100 units down from there

Simple enough.

***

Steps is a collection of modules, which consist of a `type` and a `value`. To achieve our first instruction, typing "A", we can use the most simple module available. The `tap`. A tap just presses a key and releases it immedietely afterwards. Its the same behaviour as when you tap a key on your keyboard. A list of all available modules can be found [here](https://nmstr.github.io/taskZen/scriptReference/body/). We can define a tap on the "A" key as follows:
```
steps:
  - type: tap
    value: KEY_A
```
_Note that the `steps` keywords is only defined once for all following modules._

***

Next we wait half a second. This is achieved using the `wait` module. The wait module just takes one value and then waits for that amount of time (in ms). We want to wait half a second, thus we will be using the value 500. This is our wait module:
```
  - type: wait
    value: 500
```

***

Now we can again use the `tap` module to write a capital B. One more feature of tap is that it can add modifiers. To press shift while tapping B, we can use a `SHIFT` modifier. To do this we can do the same thing as before, but need to add the modifier at the end. Just like this:
```
  - type: tap
    value: KEY_B
    modifier: SHIFT
```

***

Now something interesting again. Moving the mouse to an absolute position. For that taskZen provides the `move-absolute` module. It takes 2 arguments. X and y. These are the positions the mouse should be put at. We want to put our mouse to X=500 and Y=500. This is how we do that:
```
  - type: move-absolute
    x: 500
    y: 500
```
_Note that this needs the screen in the header to be setup correctly to properly work._
_Note that mouse movement requires BTN_MOUSE to be set_

***

Now we wait again. Simple enough. We can just copy the module we already have. Nothing special here.

```
  - type: wait
    value: 500
```

***

For our last instruction we want to move the mouse relative to its current position. For this taskZen offers the `move-relative` module. The usage is exactly the same as with the `move-absolute` module. To move 100 units down we can just increase Y by 100 while keeping X the same. To do this, write this:
```
  - type: move-relative
    x: 0
    y: 100
```

***

With that we are done. Our script should now look like this:
```
name: exampleScript
speed: 100
device: taskZen-minimal
screen:
  width: 1920
  height: 1080

steps:
  - type: tap
    value: KEY_A
  - type: wait
    value: 500
  - type: tap
    value: KEY_B
    modifier: SHIFT
  - type: move-absolute
    x: 500
    y: 500
  - type: wait
    value: 500
  - type: move-relative
    x: 0
    y: 100
```

## Executing

Of course we are still missing the fun part. Executing our script. This is the simplest part.

First confirm the script exists. This part is not needed, but might help you out if you did something wrong before. Just type `taskZen ls` into your terminal.
```
$ taskZen ls
        taskZen
Automation utility for Wayland

Available scripts:
        - exampleScript (/home/user/.config/taskZen/exampleScript.yaml)
```
Here we can see that our script is indeed present. Now the execution. Type `taskZen execute exampleScript` into your terminal and enjoy the result of what you have just created!

Now, this is a very basic and arguably pretty useless script. However these are the fundamentals needed to create more sophisticated scripts, ultimately making a lot of stuff easier. To see how to create more advanced scripts you can view the script reference [here](https://nmstr.github.io/taskZen/scriptReference).