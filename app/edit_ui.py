import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import copy
from app.tunnel import Tunnel
import app.util

#temp
import json

utl = app.util.Utl()

class EditProfile(Gtk.Dialog):
    
    def __init__(self, parent, profile_index):

        self.parent = parent
        self.profile_index = profile_index
        
        if self.profile_index is None:
            # New profile
            self.profile_model = utl.conf['default_profile']
        else:
            self.profile_model = copy.deepcopy(utl.conf['profiles'][profile_index])

            print("INIT EditProfile {}".format(self.profile_index))

        self.original_model = copy.deepcopy(self.profile_model)

        if profile_index == None:
            dialog_title = "Add Profile"
        else:
            dialog_title = "Edit Profile {}".format(self.profile_model['name'])


        handlers = {
            "onSaveProfile": self.save_profile,
            "onCancel":  self.cancel,
            "onDelTunnel": self.on_del_tunnel
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


        # Tunnels list
        self.tunnel_keys = ["port1", "host", "port2", "comment"]
        self.tunnels_store = Gtk.ListStore(int, str, int, str, str)
        self.tunnels_list = Gtk.TreeView(self.tunnels_store)
        self.selected_tunnel = self.tunnels_list.get_selection()
        self.selected_tunnel.connect("changed", self.on_select_tunnel)
        self.del_button = builder.get_object("delete_tunnel")
        self.save_button = builder.get_object("save_profile")
    
        self.profile_model['tunnels'].append(utl.conf['default_tunnel'])


        for t in self.profile_model['tunnels']:
            tlist = [t[key] for key in self.tunnel_keys]
            # Add key for color
            tlist.append("#222222")
            self.tunnels_store.append(tlist)
        
        # Set color of default tunnel
        self.tunnels_store[-1][4] = "gray"

        # Create columns
        
        
        for i, column_title in enumerate(["Port1", "Host", "Port2", "Comment"]):
            renderer = Gtk.CellRendererText()
            renderer.set_property("editable", True)
            
            renderer.connect("editing-started", self.on_edit_tunnel_start, i)
            renderer.connect("editing-canceled", self.on_edit_tunnel_cancel)
            renderer.connect("edited", self.on_edit_tunnel_finish, i)
            column = Gtk.TreeViewColumn(column_title, renderer, text=i, foreground=4)
            if column_title == "Comment":
                column.set_expand(True)
            self.tunnels_list.append_column(column)

        # Add listview to container
        tunnels_container = builder.get_object("tunnels_list")
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
        
        self.profile_model['tunnels'] = [t for t in self.profile_model['tunnels'] if utl.is_valid_tunnel(t)]
        
        utl.save_profiles_conf()
        self.dialog.response(response)
        
        return True

    def on_edit_tunnel_start(self, widget, path, text, i):
        # Deactivate save button until editing finished
        self.save_button.set_sensitive(False)

    def on_edit_tunnel_cancel(self, widget):
        # Deactivate save button until editing finished
        self.save_button.set_sensitive(True)        

    def on_edit_tunnel_finish(self, widget, path, text, i):
        self.save_button.set_sensitive(True)
        if type(self.tunnels_store[path][i]) is str:
            newval = text
        elif type(self.tunnels_store[path][i]) is int:
            newval = int(text)
        
        updated_tunnel = self.profile_model['tunnels'][int(path)]
        updated_tunnel[self.tunnel_keys[i]] = newval

        self.tunnels_store[path][i] = newval

        # Check valid
        if utl.is_valid_tunnel(updated_tunnel):
            self.tunnels_store[path][4] = "green"
        else:
            self.tunnels_store[path][4] = "red"

    def on_select_tunnel(self, selection):
        self.del_button.set_sensitive(True)

    def on_del_tunnel(self, button):
        (model, paths) = self.selected_tunnel.get_selected_rows()
        index = paths[0].get_indices()[0]
        iter = model.get_iter(paths[0])
        del self.profile_model['tunnels'][index]
        model.remove(iter)

    def cancel(self, widget):
        self.profile_model = copy.deepcopy(self.original_model)
        self.dialog.close()
        
        
