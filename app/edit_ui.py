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


        # Tunnels list
        self.tunnel_keys = ["port1", "host", "port2", "comment"]
        self.tunnels_store = Gtk.ListStore(int, str, int, str, str)
        self.tunnels_list = Gtk.TreeView(self.tunnels_store)


        self.profile_model['tunnels'].append(utl.conf['default_tunnel'])
        for t in self.profile_model['tunnels']:
            tlist = [t[key] for key in self.tunnel_keys]
            tlist.append("green")
            self.treeiter = self.tunnels_store.append(tlist)

        print(self.tunnels_store)

        # Create columns
        
        
        for i, column_title in enumerate(["Port1", "Host", "Port2", "Comment"]):
            renderer = Gtk.CellRendererText()
            renderer.set_property("editable", True)
            
        
            renderer.connect("edited", self.on_edit_tunnel, i)
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            if column_title == "Comment":
                column.set_expand(True)
            self.tunnels_list.append_column(column)

        # Add listview to container
        tunnels_container = builder.get_object("tunnels_list")
        tunnels_container.add(self.tunnels_list)

        print(self.tunnels_list)
        
        self.dialog.show_all()


        print(json.dumps(self.profile_model['tunnels']))


    def save_profile(self, button):
        self.profile_error.set_text("")
        
        if self.fields["name"].get_text().strip() == "":
            self.profile_error.set_text("Profile Name is required.")
            return

        print([t for t in self.profile_model['tunnels'] if utl.is_valid_tunnel(t)])
        

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

    def on_edit_tunnel(self, widget, path, text, i):

        widget.set_property("foreground", "red")
        print("{}: {} => {} type: {}".format(path, self.tunnels_store[path][i], text, type(self.tunnels_store[path][i])))
        
        if type(self.tunnels_store[path][i]) is str:
            newval = text
        elif type(self.tunnels_store[path][i]) is int:
            newval = int(text)
        
        updated_tunnel = self.profile_model['tunnels'][int(path)]
        updated_tunnel[self.tunnel_keys[i]] = newval

        self.tunnels_store[path][i] = newval

        # Check valid
        if utl.is_valid_tunnel(updated_tunnel):
            print("valid")
            
            #print(json.dumps(self.profile_model['tunnels'][int(path)]))
        else:
            print("invalid tunnel")
        
        
    
    def cancel(self, widget):
        self.dialog.close()
        
