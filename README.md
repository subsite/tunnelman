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

### Building as Flatpak

```bash
# Install build tools (once)
sudo apt install flatpak flatpak-builder
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.gnome.Platform//47 org.gnome.Sdk//47

# Build and install locally
flatpak-builder --install --user build-dir flatpak/io.github.subsite.TunnelMan.yml

# Run
flatpak run io.github.subsite.TunnelMan
```

### Roadmap

- Password prompt for connections without key-authentication
- Support for remote and dynamic (SOCKS) tunnels
- App indicator (top panel menu)
- Packaging (.deb or AppImage)

### Bugs

Please report issues to the issue tracker.

---

### Notes for developers

**One-time setup** — tell git to use the repo's hook directory:
```bash
git config core.hooksPath .githooks
```

**Releasing a new version:**

1. Edit `VERSION` (e.g. `1.0.0` → `1.1.0`)
2. Add a `<release>` entry in `flatpak/io.github.subsite.TunnelMan.metainfo.xml`
3. Commit: `git commit -am "release 1.1.0"` — the post-commit hook auto-creates the `v1.1.0` tag
4. Push: `git push origin master --tags`

GitHub Actions picks up the tag, builds the `.flatpak` bundle, and publishes a GitHub release automatically.
