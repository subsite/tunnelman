
import os
from pathlib import Path
import json

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Config():

    conf = {}
    default_profile = 	{
        "name": "",
        "server": "",
        "username": "",
        "ssh_port": 22,
        "send_keepalive_seconds": 60,
        "tunnels": [{
            "port1": 0,
            "host": "localhost",
            "port2": 0,						
            "comment": ""
        }]
    }

    def __init__(self):

        base_path = os.path.join( os.path.dirname(os.path.realpath(__file__)) , os.path.pardir)
        user_config_dir = "{}/.config/tunnelman".format(os.path.expanduser("~"))
        
        self.confs = [
            {'name': "profiles", 'file':  "{}/profiles.json".format(user_config_dir)},
            {'name': "app", 'file':  "{}/app.json".format(user_config_dir) }
        ]

        for c in self.confs:
            with open(c['file'], "r", encoding="utf-8") as handle:
                data = handle.read()
                self.conf[c['name']] = json.loads(data)

        self.conf['base_path'] = base_path

    def save_profiles_conf(self):
        with open(self.confs[0]['file'], 'w') as outfile:
            json.dump(self.conf['profiles'], outfile, indent=4)
        print("Profile saved")

class ConfirmDelete(Gtk.Dialog):

    def __init__(self, parent):

        builder = Gtk.Builder()
        builder.add_from_file("assets/glade/confirm_delete.glade")
        builder.connect_signals({ 
            "onConfirm": [ self.respond, Gtk.ResponseType.OK],
            "onCancel": [ self.respond, Gtk.ResponseType.CANCEL]
        })

        self.dialog = builder.get_object("confirm_delete")
        self.dialog.set_transient_for(parent)
        self.dialog.show_all()

    def respond(self, widget, response):
        self.dialog.response(response)
    
