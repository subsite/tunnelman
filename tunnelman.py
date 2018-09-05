#!/usr/bin/python3

import os, sys

import json

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from lib.main_window import MainWindow

#ssh = '/usr/bin/ssh -fnN -o "ServerAliveInterval 60" -o "ServerAliveCountMax 3"'


# Read config
user_config_dir = os.path.expanduser("~") + "/.config/tunnelman"
profiles_conf = user_config_dir + "/profiles.json"



with open(profiles_conf, "r", encoding="utf-8") as handle:
    data = handle.read()
    profiles = json.loads(data)

config = { 'profiles': profiles }    
# /Read config


# Check arguments
"""if len(sys.argv) < 2:
    print("USAGE: tunnels.py [{}]".format('|'.join([p for p in profiles])))
    sys.exit(1)

prof = sys.argv[1]

if prof not in profiles:
    print("No such profile")
    sys.exit(1)    

profile = profiles[prof]
# Add default ssh port to profile
profile['ssh_port'] = 22
if "description" not in profile:
    profile['description'] = prof

localhost = "127.0.0.1"


print(profile)

local_bind_addresses = []
remote_bind_addresses = []
for t in profile['tunnels']:
    localport = int(t['route'].split(":")[0])
    remote_addr = t['route'].split(":")[1]
    remote_port = int(t['route'].split(":")[2])    
    local_bind_addresses.append((localhost,localport))
    remote_bind_addresses.append((remote_addr,remote_port))


print(local_bind_addresses)
print(remote_bind_addresses)
"""

main_window = MainWindow(config)
main_window.connect("destroy", main_window.main_quit)
main_window.show_all()
Gtk.main()







