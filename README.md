# TunnelMan
SSH Tunnel Manager written Python GTK+ 3

### Setup

No automatic install yet, so you have to do it manually. This is tested on Ubuntu 18.04, but should work on other Linux variants that support GTK+ 3.

- Install python3 packages `sudo apt install python3 python3-pip python3-gi`
- Install additional packages `pip3 install sshtunnel`
- Clone this repo and cd into it
- Create config dir `mkdir ~/.config/tunnelman`
- Copy example files `cp example_conf/* ~/.config/tunnelman/`
- Edit tunnels in `~/.config/tunnelman/profiles.json`
- Run `./tunnelman.py` from the command line 
- Install additional missing dependecies if it complains
- If everything works, pin the app icon to the launcher so you can run it from there in the future. 

### Errors

Please report any bugs to the issue tracker. 



