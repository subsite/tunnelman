import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from app.tunnel import Tunnel
from app.config import Config

config = Config()

class EditProfile(Gtk.Dialog):
    
    def __init__(self, parent, profile_index):
        self.parent = parent
        self.profile_index = profile_index
        if self.profile_index is None:
            # New profile
            self.profile_model = 	{
                "name": "",
                "server": "",
                "username": "",
                "tunnels": [{
                    "port1": 0,
                    "host": "localhost",
                    "port2": 0,						
                    "comment": ""
                }]
            }
        else:
            self.profile_model = config.conf['profiles'][profile_index]

        if profile_index == None:
            dialog_title = "Add Profile"
        else:
            dialog_title = "Edit Profile {}".format(self.profile_model['name'])


        handlers = {
            "onSaveProfile": self.save_profile,
            "onCancel":  self.cancel
        }

        
        builder = Gtk.Builder()
        builder.add_from_file("assets/glade/edit_profile.glade")
        builder.connect_signals(handlers)

        self.dialog = builder.get_object("edit_dialog")
        self.dialog.set_transient_for(parent)
        self.dialog.show_all()

        self.fields = {}
        for fld in self.profile_model:
            if builder.get_object(fld):
                self.fields[fld] = builder.get_object(fld)
                self.fields[fld].set_text(str(self.profile_model[fld]))



    def save_profile(self, button):
        print("save profile")
        for fld in self.fields:
            self.profile_model[fld] = self.fields[fld].get_text()
            print(self.fields[fld].get_text())
        if self.profile_index is None:
            # New profile
            config.conf['profiles'].append(self.profile_model)
            self.profile_index = len(config.conf['profiles'])-1
            print(self.profile_index)
        else:
            # Update profile
            config.conf['profiles'][self.profile_index] = self.profile_model
        
        config.save_profiles_conf()
        self.parent.add_listbox_row(self.profile_index)

        return True
        #print(config.conf['profiles'])

        """Gtk.Dialog.__init__(self, profile['name'], parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        print(parent)

        self.set_default_size(150, 100)

        label = Gtk.Label("This is a dialog to display additional information")

        box = self.get_content_area()
        box.add(label)
        self.show_all()"""
    def cancel(self, *args):
        self.dialog.close()
        print(args)
        