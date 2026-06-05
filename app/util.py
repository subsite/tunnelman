
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

        self.verbose = False

        base_path = os.path.join( os.path.dirname(os.path.realpath(__file__)) , os.path.pardir)
        user_config_dir = "{}/.config/tunnelman".format(os.path.expanduser("~"))
        self.conf['base_path'] = base_path

        self.confs = [
            {'name': "profiles", 'file':  "{}/profiles.json".format(user_config_dir)},
            {'name': "app", 'file':  "{}/app.json".format(user_config_dir) }
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
                Path(c['file']).parent.mkdir(parents=True, exist_ok=True)
                self.conf[c['name']] = self.conf['default_app']
                with open(c['file'], 'w') as outfile:
                    json.dump(self.conf['app'], outfile, indent=4)
            else:
                self.conf[c['name']] = []



    def create_id(self, size=16, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def list_to_dict_by_key(self, list_of_dicts, key):
        return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(list_of_dicts))

    def get_id_profiles(self):
        return self.list_to_dict_by_key(self.conf['profiles'], "id")

    def save_profiles_conf(self):
        if os.path.exists(self.confs[0]['file']):
            copyfile(self.confs[0]['file'], "{}.bak".format(self.confs[0]['file']))

        with open(self.confs[0]['file'], 'w') as outfile:
            json.dump(self.conf['profiles'], outfile, indent=4)
        self.load_conf()

    def glade_file(self, file_ident):
        return "{}/assets/glade/{}.glade".format(self.conf['base_path'], file_ident)

    def log(self, msg):
        if self.verbose:
            print(msg)

    def is_valid_tunnel(self, tunnel):
        return tunnel['port1'] > 0 and tunnel['port2'] > 0 and tunnel['host'].strip() != ""

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
