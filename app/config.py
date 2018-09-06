
import os
from pathlib import Path
import json

class Config():

    conf = {}

    def __init__(self):

        base_path = os.path.join( os.path.dirname(os.path.realpath(__file__)) , os.path.pardir)
        user_config_dir = "{}/.config/tunnelman".format(os.path.expanduser("~"))
        confs = [
            {'name': "profiles", 'file':  "{}/profiles.json".format(user_config_dir)},
            {'name': "app", 'file':  "{}/app.json".format(user_config_dir) }
        ]

        for c in confs:
            with open(c['file'], "r", encoding="utf-8") as handle:
                data = handle.read()
                self.conf[c['name']] = json.loads(data)

        self.conf['base_path'] = base_path

    def save_profile(self, profile):
        print("Profile saved")
