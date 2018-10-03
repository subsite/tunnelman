
import sys, os
from pathlib import Path
from shutil import copyfile
import json
import string, random

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Utl():

    conf = {}
    _args = {}

    # read command line arguments
    for arg in sys.argv[1:]:
        try:
            _args[arg.split("=")[0]] = arg.split("=")[1]
        except:
            print("Bad argument {}".format(arg))

    def __init__(self):

        base_path = os.path.join( os.path.dirname(os.path.realpath(__file__)) , os.path.pardir)
        
        self.conf['base_path'] = base_path

        # Assign run time config_dir from argument confdir=/path/to/conf for testing purposes
        if 'confdir' in self._args:
            self.config_dir = self._args['confdir']
        else:
            self.config_dir = "{}/.config/tunnelman".format(os.path.expanduser("~"))
        
        # create conf path if not exists
        Path(self.config_dir).mkdir(parents=True, exist_ok=True)

        self.confs = [
            {'name': "profiles", 'file':  "{}/profiles.json".format(self.config_dir)},
            {'name': "app", 'file':  "{}/app.json".format(self.config_dir) }
        ]        
        self.load_conf()

    
    def load_conf(self):

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

        self.conf['default_app'] = {
            "default_ssh_port": 22,
            "localhost": "127.0.0.1",
            "send_keepalive_seconds": 60
        }

        for c in self.confs:
            if os.path.exists(c['file']):
                with open(c['file'], "r", encoding="utf-8") as handle:
                    data = handle.read()
                    self.conf[c['name']] = json.loads(data)
            elif c['name'] == "app":
                # First run, write default app conf if not exists
                self.conf[c['name']] = self.conf['default_app']
                with open(c['file'], 'w') as outfile:
                    json.dump(self.conf['app'], outfile, indent=4)
            else:
                # First run, empty profiles conf
                self.conf[c['name']] = []
                


 
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
        if os.path.exists(self.confs[0]['file']):
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
    


