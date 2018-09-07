import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from app.tunnel import Tunnel
from app import util

config = util.Config()

class EditProfile(Gtk.Dialog):
    
    def __init__(self, parent, profile_index):

        self.parent = parent
        self.profile_index = profile_index
        
        if self.profile_index is None:
            # New profile
            self.profile_model = config.default_profile
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

        self.profile_error = builder.get_object("profile_error")

        self.dialog = builder.get_object("edit_dialog")
        self.dialog.set_transient_for(parent)
        self.dialog.show_all()

        self.fields = {}
        for fld in self.profile_model:
            if builder.get_object(fld):
                self.fields[fld] = builder.get_object(fld)
                self.fields[fld].set_text(str(self.profile_model[fld]))

        



    def save_profile(self, button):
        self.profile_error.set_text("")
        
        if self.fields["name"].get_text().strip() == "":
            self.profile_error.set_text("Profile Name is required.")
            return
        
        for fld in self.fields:
            self.profile_model[fld] = self.fields[fld].get_text()
            print(self.fields[fld].get_text())
        if self.profile_index is None:
            # New profile
            config.conf['profiles'].append(self.profile_model)
            self.profile_index = len(config.conf['profiles'])-1
            response = Gtk.ResponseType.OK
        else:
            # Update profile
            config.conf['profiles'][self.profile_index] = self.profile_model
            response = Gtk.ResponseType.APPLY
        
        config.save_profiles_conf()
        self.dialog.response(response)
        
        return True


    def cancel(self, widget):
        self.dialog.close()
        



