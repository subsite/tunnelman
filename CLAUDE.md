# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
./tunnelman.py
```

Requires system packages only (no pip): `python3-gi` (PyGObject/GTK3 bindings) and `openssh-client` (the `ssh` binary).

## Config files

User config is stored at `~/.config/tunnelman/`:
- `profiles.json` — list of SSH tunnel profiles (auto-created on first save; a `.bak` is written on each save)
- `app.json` — global app settings (written from defaults on first run); see `example_conf/app.json`

There is no config migration logic — schema changes must be handled manually.

## Architecture

The app is a GTK3 desktop app built with Glade UI files. UI definitions live in `assets/glade/*.glade`; Python connects to them via `Gtk.Builder`.

**Data flow:**
- `app/util.py` — singleton `Utl` instance (`utl`) holds all runtime config in `utl.conf` (a plain dict). Every module instantiates its own `Utl()`, but they all share the same class-level `conf` dict. Profiles are saved via `utl.save_profiles_conf()`, which also reloads conf from disk.
- `app/tunnel.py` — `Tunnel` manages a `subprocess.Popen` running `ssh -N`. Each profile gets one `Tunnel` instance. Tunnels are started/stopped via `open_tunnel()`/`close_tunnel()`.
- `app/main_ui.py` — `MainUi` is the main window. It owns the `tunnels` dict keyed by profile id and rebuilds the profile list (`create_list_items()`) after any edit/add/delete.
- `app/edit_ui.py` — `EditProfile` is the add/edit dialog. The tunnels sub-list is an editable `Gtk.TreeView` backed by a `Gtk.ListStore`. A "default tunnel" (port1=0, port2=0) is always appended as the new-entry row and is stripped out (via `is_valid_tunnel`) before saving.

**Profile data model:**
```json
{
  "id": "<random 16-char string>",
  "name": "",
  "server": "host.example.com",
  "username": "user",
  "ssh_port": 22,
  "send_keepalive_seconds": 60,
  "tunnels": [
    { "port1": 8080, "host": "localhost", "port2": 80, "comment": "" }
  ]
}
```

Each tunnel entry maps to `-L port1:host:port2` in ssh terms. `port1` is the local bind port; `host:port2` is the remote destination as seen from the SSH server.

## Key constraints

- Key-based SSH auth only — no password prompts implemented.
- `Utl.conf` is a class-level dict; `utl` is a module-level singleton imported by all other modules — do not instantiate `Utl()` elsewhere.
- `open_tunnel()` sleeps 2 seconds then checks `poll()` to distinguish fast failures from successful connections. It runs in a background thread (see `main_ui.py`).
