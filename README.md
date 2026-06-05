# TunnelMan
SSH Tunnel Manager written in Python with GTK3

### Features

- Manage SSH tunnels with multiple port forwards per profile, equivalent to:
  `ssh host.com -L 8080:localhost:80 -L 55432:192.168.2.2:5432`
- Key-based authentication only — no password prompts
- Profiles stored in `~/.config/tunnelman/profiles.json`

### Screenshots
![Main Window](https://subsite.github.io/tunnelman/screenshots/main_window.png)

![Edit Profile](https://subsite.github.io/tunnelman/screenshots/profile_window.png)

### Setup

Tested on Ubuntu/Fedora with Python 3.11+.

**Install system dependencies:**
```
sudo apt install python3-gi openssh-client   # Debian/Ubuntu
sudo dnf install python3-gobject openssh     # Fedora/RHEL
```

**Run:**
```
git clone <repo-url>
cd tunnelman
./tunnelman.py
```

No pip packages required. Tunnels are opened by shelling out to the system `ssh` binary, so all key types (Ed25519, ECDSA, RSA), `~/.ssh/config`, and SSH agent forwarding work automatically.

### Roadmap

- Password prompt for connections without key-authentication
- Support for remote and dynamic (SOCKS) tunnels
- App indicator (top panel menu)
- Packaging (.deb or AppImage)

### Bugs

Please report issues to the issue tracker.
