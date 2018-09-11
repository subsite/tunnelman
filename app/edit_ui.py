import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from app.tunnel import Tunnel
import app.util

utl = app.util.Utl()

class EditProfile(Gtk.Dialog):
    
    def __init__(self, parent, profile_index):

        self.parent = parent
        self.profile_index = profile_index
        
        if self.profile_index is None:
            # New profile
            self.profile_model = utl.conf['default_profile']
        else:
            self.profile_model = utl.conf['profiles'][profile_index]

        if profile_index == None:
            dialog_title = "Add Profile"
        else:
            dialog_title = "Edit Profile {}".format(self.profile_model['name'])


        handlers = {
            "onSaveProfile": self.save_profile,
            "onCancel":  self.cancel
        }

        
        builder = Gtk.Builder()
        builder.add_from_file(utl.glade_file("edit_profile"))
        builder.connect_signals(handlers)

        self.profile_error = builder.get_object("profile_error")

        self.dialog = builder.get_object("edit_dialog")
        self.dialog.set_transient_for(parent)
        

        self.fields = {}
        for fld in self.profile_model:
            if builder.get_object(fld):
                self.fields[fld] = builder.get_object(fld)
                self.fields[fld].set_text(str(self.profile_model[fld]))


        tunnels_store = Gtk.ListStore(int, str, int, str)
        tunnels_container = builder.get_object("tunnels_list")
        self.tunnels_list = Gtk.TreeView(tunnels_store)

        renderer = Gtk.CellRendererText()
        for i, column_title in enumerate(["Port1", "Host", "Port2", "Comment"]):
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.tunnels_list.append_column(column)

        
        for i, column_title in enumerate(["STOCK_EDIT", "Delete"]):
            renderer = Gtk.CellRendererPixbuf()
            column = Gtk.TreeViewColumn(column_title, renderer, gicon=Gtk.STOCK_EDIT)
            self.tunnels_list.append_column(column)

        for t in self.profile_model['tunnels']:
            treeiter = tunnels_store.append([t['port1'], t['host'], t['port2'], t['comment']])


                
        
        tunnels_container.add(self.tunnels_list)
        
        self.dialog.show_all()


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
            utl.conf['profiles'].append(self.profile_model)
            self.profile_index = len(utl.conf['profiles'])-1
            response = Gtk.ResponseType.OK
        else:
            # Update profile
            utl.conf['profiles'][self.profile_index] = self.profile_model
            response = Gtk.ResponseType.APPLY
        
        utl.save_profiles_conf()
        self.dialog.response(response)
        
        return True


    def cancel(self, widget):
        self.dialog.close()
        



