
import os
from pathlib import Path
import json

class Config():

    conf = {}

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
        with open(self.confs[0]['file']+"tmp.json", 'w') as outfile:
            json.dump(self.conf['profiles'], outfile, indent=4)
        print("Profile saved")
