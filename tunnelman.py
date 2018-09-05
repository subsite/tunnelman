#!/usr/bin/python3

import os, sys
import signal
from pathlib import Path
import json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from lib.main_window import MainWindow

#ssh = '/usr/bin/ssh -fnN -o "ServerAliveInterval 60" -o "ServerAliveCountMax 3"'

signal.signal(signal.SIGINT, signal.SIG_DFL)

base_path = os.path.dirname(os.path.realpath(__file__))

# Read config
user_config_dir = os.path.expanduser("~") + "/.config/tunnelman"
profiles_conf = user_config_dir + "/profiles.json"

with open(profiles_conf, "r", encoding="utf-8") as handle:
    data = handle.read()
    profiles = json.loads(data)

config = { 'profiles': profiles }    
# /Read config


main_window = MainWindow(config)
#To refresh icon, rm ~/.local/share/applications/tunnelman_py.desktop
main_window.set_icon_from_file("{}/logo.png".format(base_path))
main_window.connect("destroy", main_window.main_quit)
main_window.show_all()
Gtk.main()

