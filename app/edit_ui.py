
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import copy

from app.util import utl


class EditProfile(Gtk.Dialog):

    def __init__(self, parent, profile_index, read_only=False):

        self.parent = parent
        self.profile_index = profile_index
        self.read_only = read_only

        if self.profile_index is None:
            self.profile_model = copy.deepcopy(utl.conf['default_profile'])
        else:
            self.profile_model = copy.deepcopy(utl.conf['profiles'][profile_index])

        self.original_model = copy.deepcopy(self.profile_model)

        if profile_index is None:
            dialog_title = "Add Profile"
        elif read_only:
            dialog_title = "View Profile {}".format(self.profile_model['name'])
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
                if read_only:
                    self.fields[fld].set_sensitive(False)

        # Tunnels list
        self.tunnel_keys = ["port1", "host", "port2", "comment"]
        self.tunnels_store = Gtk.ListStore(int, str, int, str, str)
        self.tunnels_list = Gtk.TreeView(self.tunnels_store)
        self.selected_tunnel = self.tunnels_list.get_selection()
        self.selected_tunnel.connect("changed", self.on_select_tunnel)
        self.del_button = builder.get_object("delete_tunnel")
        self.save_button = builder.get_object("save_profile")
        self.save_button.get_style_context().add_class("suggested-action")
        self.del_button.get_style_context().add_class("destructive-action")
        if read_only:
            self.save_button.set_sensitive(False)
            self.del_button.set_sensitive(False)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(False)
        hb.set_title(dialog_title)
        self.dialog.set_titlebar(hb)

        for t in self.profile_model['tunnels']:
            tlist = [t[key] for key in self.tunnel_keys]
            tlist.append("#222222")
            self.tunnels_store.append(tlist)

        for i, column_title in enumerate(["Local", "Host", "Remote", "Comment"]):
            renderer = Gtk.CellRendererText()
            renderer.set_property("editable", not read_only)
            if not read_only:
                renderer.connect("editing-started", self.on_edit_tunnel_start, i)
                renderer.connect("editing-canceled", self.on_edit_tunnel_cancel)
                renderer.connect("edited", self.on_edit_tunnel_finish, i)
            column = Gtk.TreeViewColumn(column_title, renderer, text=i, foreground=4)
            if column_title == "Comment":
                column.set_expand(True)
            self.tunnels_list.append_column(column)

        self.tunnels_list.get_style_context().add_class("tunnel-list")

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_height(100)
        scroll.get_style_context().add_class("tunnel-list-scroll")
        scroll.add(self.tunnels_list)
        scroll.show_all()

        add_btn = Gtk.Button(label="+ New Tunnel")
        add_btn.get_style_context().add_class("tunnel-add-row")
        add_btn.connect("clicked", self.add_tunnel)
        add_btn.set_sensitive(not read_only)
        add_btn.show()

        tunnels_container = builder.get_object("tunnels_container")
        tunnels_container.pack_start(scroll, True, True, 0)
        tunnels_container.pack_start(add_btn, False, True, 0)

        self.dialog.show_all()

    def save_profile(self, button):
        self.profile_error.set_text("")

        if self.fields["name"].get_text().strip() == "":
            self.profile_error.set_text("Profile Name is required.")
            return

        for fld in self.fields:
            self.profile_model[fld] = self.fields[fld].get_text()

        self.profile_model['tunnels'] = [t for t in self.profile_model['tunnels'] if utl.is_valid_tunnel(t)]

        if self.profile_index is None:
            utl.conf['profiles'].append(self.profile_model)
            response = Gtk.ResponseType.OK
        else:
            utl.conf['profiles'][self.profile_index] = self.profile_model
            response = Gtk.ResponseType.APPLY

        utl.save_profiles_conf()
        utl.log(f"[{self.profile_model['name']}] Profile {'added' if self.profile_index is None else 'saved'}")
        self.dialog.response(response)

    def on_edit_tunnel_start(self, widget, path, text, i):
        self.save_button.set_sensitive(False)

    def on_edit_tunnel_cancel(self, widget):
        self.save_button.set_sensitive(True)

    def on_edit_tunnel_finish(self, widget, path, text, i):
        self.save_button.set_sensitive(True)
        col_type = type(self.tunnels_store[path][i])
        if col_type is int:
            try:
                newval = int(text)
            except ValueError:
                self.profile_error.set_text("Port must be a number.")
                return
        else:
            newval = text
            self.profile_error.set_text("")

        updated_tunnel = self.profile_model['tunnels'][int(path)]
        updated_tunnel[self.tunnel_keys[i]] = newval
        self.tunnels_store[path][i] = newval

        if utl.is_valid_tunnel(updated_tunnel):
            self.tunnels_store[path][4] = "green"
        else:
            self.tunnels_store[path][4] = "red"

    def on_select_tunnel(self, selection):
        (model, paths) = selection.get_selected_rows()
        self.del_button.set_sensitive(bool(paths) and not self.read_only)

    def on_del_tunnel(self, button):
        (model, paths) = self.selected_tunnel.get_selected_rows()
        if not paths:
            return
        index = paths[0].get_indices()[0]
        iter = model.get_iter(paths[0])
        del self.profile_model['tunnels'][index]
        model.remove(iter)

    def add_tunnel(self, button):
        new_tunnel = copy.deepcopy(utl.conf['default_tunnel'])
        self.profile_model['tunnels'].append(new_tunnel)
        tlist = [new_tunnel[key] for key in self.tunnel_keys]
        tlist.append("gray")
        self.tunnels_store.append(tlist)

    def cancel(self, widget):
        self.profile_model = copy.deepcopy(self.original_model)
        self.dialog.close()
