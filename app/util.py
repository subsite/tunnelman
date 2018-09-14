
import os
from pathlib import Path
from shutil import copyfile
import json
import string, random

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Utl():

    conf = {}

    def __init__(self):

        base_path = os.path.join( os.path.dirname(os.path.realpath(__file__)) , os.path.pardir)
        user_config_dir = "{}/.config/tunnelman".format(os.path.expanduser("~"))
        self.conf['base_path'] = base_path
        
        self.confs = [
            {'name': "profiles", 'file':  "{}/profiles.json".format(user_config_dir)},
            {'name': "app", 'file':  "{}/app.json".format(user_config_dir) }
        ]        
        self.load_conf()

    
    def load_conf(self):


        for c in self.confs:
            with open(c['file'], "r", encoding="utf-8") as handle:
                data = handle.read()
                self.conf[c['name']] = json.loads(data)

        self.conf['default_profile'] = {
            "id": self.create_id(),
            "name": "",
            "server": "",
            "username": "",
            "ssh_port": 22,
            "send_keepalive_seconds": 60,
            "tunnels": []
        }

        self.conf['default_tunnel'] = {
            "port1": 0,
            "host": "",
            "port2": 0,						
            "comment": "New tunnel"
        }
 
    def create_id(self, size=16, chars=string.ascii_lowercase + string.digits):
        """Create random string to use as tunnel id"""
        return ''.join(random.choice(chars) for _ in range(size))

    def list_to_dict_by_key(self, list_of_dicts, key):
        """Create a dict of dicts by key from list of dicts"""
        return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(list_of_dicts))

    def get_id_profiles(self):
        """Return profiles as dict by id"""
        return self.list_to_dict_by_key(self.conf['profiles'], "id")

    def save_profiles_conf(self):
        """Save profiles conf from memory to file"""
        # copy current conf to .bak
        copyfile(self.confs[0]['file'], "{}.bak".format(self.confs[0]['file']))
        # Write new conf file
        with open(self.confs[0]['file'], 'w') as outfile:
            json.dump(self.conf['profiles'], outfile, indent=4)
        # Overwrite memory with new conf
        self.load_conf()            
        print("Profile saved")

    def glade_file(self, file_ident):
        """Return parsed glade file with absolute path"""
        return "{}/assets/glade/{}.glade".format(self.conf['base_path'], file_ident)

    def is_valid_tunnel(self, tunnel):
        if tunnel['port1'] > 0 and tunnel['port2'] > 0 and tunnel['host'].strip() != "":
            return True
        else:
            return False

utl = Utl()

class ConfirmDelete(Gtk.Dialog):

    def __init__(self, parent):


        builder = Gtk.Builder()
        builder.add_from_file(utl.glade_file("confirm_delete"))
        builder.connect_signals({ 
            "onConfirm": [ self.respond, Gtk.ResponseType.OK],
            "onCancel": [ self.respond, Gtk.ResponseType.CANCEL]
        })

        self.dialog = builder.get_object("confirm_delete")
        self.dialog.set_transient_for(parent)
        self.dialog.show_all()

    def respond(self, widget, response):
        self.dialog.response(response)
    


