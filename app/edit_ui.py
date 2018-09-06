import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from app.tunnel import Tunnel
from app.config import Config

config = Config()

class EditProfile(Gtk.Dialog):
    
    def __init__(self, parent, profile_index):
        profile = config.conf['profiles'][profile_index]

        if profile_index == 0:
            dialog_title = "Add Profile"
        else:
            dialog_title = "Edit Profile {}".format(profile['name'])


        Gtk.Dialog.__init__(self, profile['name'], parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        print(parent)

        self.set_default_size(150, 100)

        label = Gtk.Label("This is a dialog to display additional information")

        box = self.get_content_area()
        box.add(label)
        self.show_all()
