---
layout: page
title: Installation
permalink: /installation/
nav_order: 100
---

# Installation

## Run from Source

This section describes how to run taskZen directly from the source code.

Prerequisites: Make sure you have Python, pip, python3-venv, and git installed on your system.

1. Clone the repo

`git clone https://github.com/Nmstr/taskZen.git`

2. Go into the installation directory

`cd taskZen/src/`

3. Install the dependencies inside a virtual enviorment
```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

_If you have problems installing pyevdev take a look at troubleshooting section below._

4. (Optional) Put the program into your path

`sudo ln -s /path/to/current/dir/run.sh /usr/local/bin/taskZen`

5. (Optional) Run the program

`taskZen`

6. (Optional) Clone the example scripts into the scripts directory

`cp -r ../examples/* ~/.config/taskZen/`

## Troubleshooting

### Pyevdev installation

One package required is pyevdev. On some systems it does not install properly out of the box. For example Fedora 40 is one of those.

You will need `linux/input.h` and `linux/input-event-codes.h`, which are part of the Linux Kernel Headers, as well as gcc installed on your system.

Depending on your distro, you will need to use one of these commands:
```
dnf install gcc kernel-headers-$(uname -r)
apt-get install gcc linux-headers-$(uname -r)
emerge sys-devel/gcc sys-kernel/linux-headers
pacman -S gcc linux-headers
```

### /dev/uinput cannot be opened for writing

`/dev/uinput cannot be opened for writing` is a permission issue. Unfortunately running taskZen as root results in unwanted side-effects and thus isnt advised.

An easy solution for this problem is to give yourself the necessary permissions. This can be done using this command:
```
sudo chmod a+rw /dev/uinput
```