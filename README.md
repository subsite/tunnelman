# TunnelMan
SSH Tunnel Manager written Python GTK+ 3

### Features

- Manage local tunnels with multiple port forwards, equivalent to `ssh host.com -L 8080:localhost:80 -L 55432:192.168.2.2:5432`
- Uses sshtunnel (SSHTunnelForwarder) library for ssh stuff: https://pypi.org/project/sshtunnel/

### Screenshots
![Main Window](https://subsite.github.io/tunnelman/screenshots/main_window.png)

![Edit Profile](https://subsite.github.io/tunnelman/screenshots/profile_window.png)


### Setup

No automatic install yet, so you have to do it manually. This is tested on Ubuntu 18.04, but should work on other Linux variants that support GTK+ 3.

Also note that it doesn't have a password prompt yet, so you need to have key-auyhentication set up for all hosts.

- Install python3 packages `sudo apt install python3 python3-pip python3-gi`
- Install additional packages `pip3 install sshtunnel`
- Clone this repo and cd into it
- Run `./tunnelman.py` from the command line 
- Install additional missing dependecies if it complains
- If everything works, pin the app icon to the launcher so you can run it from there in the future. 

### Roadmap

Features to implement:

- Password prompt for connections without key-authentication
- Support for remote tunnels and dynamic (SOCKS) tunnels
- App indicator (top panel indicator menu)
- Packaging to .deb or AppImage or something


### Errors

Please report any bugs to the issue tracker. 












