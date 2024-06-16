# taskZen

taskZen is a free and open source automation software for Wayland!
```

  █████                      █████      ███████████                    
 ░░███                      ░░███      ░█░░░░░░███                     
 ███████    ██████    █████  ░███ █████░     ███░    ██████  ████████  
░░░███░    ░░░░░███  ███░░   ░███░░███      ███     ███░░███░░███░░███ 
  ░███      ███████ ░░█████  ░██████░      ███     ░███████  ░███ ░███ 
  ░███ ███ ███░░███  ░░░░███ ░███░░███   ████     █░███░░░   ░███ ░███ 
  ░░█████ ░░████████ ██████  ████ █████ ███████████░░██████  ████ █████
   ░░░░░   ░░░░░░░░ ░░░░░░  ░░░░ ░░░░░ ░░░░░░░░░░░  ░░░░░░  ░░░░ ░░░░░ 

```
## Features
- Create scripts to automate the boring stuff
- Include mouse movements, button presses, commands and much more in your scripts
- Quickly list all your available scripts
- Full Wayland compatability out of the box

# Installation Instructions

## Run from Source

This section describes how to run taskZen directly from the source code.

Prerequisites: Make sure you have Python, pip, and git installed on your system.

1. Clone the repo

`git clone https://github.com/Nmstr/taskZen.git`

2. Go into the installation directory

`cd taskZen/src/`

3. Install the dependencies

`pip install -r requirements.txt`

4. (Optional) Put the program into your path

`sudo ln -s /path/to/current/dir/run.sh /usr/local/bin/taskZen`

5. (Optional) Run the program

`taskZen`

6. (Optional) Clone the example scripts into the scripts directory

`cp -r ../examples/* ~/.config/taskZen/`

# Authors

Namester (Nmstr)

## License

This project is licensed under the GNU General Public License v3.0 (GPLv3)

See LICENSE.md for more information
