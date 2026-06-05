
import threading
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf

from app.tunnel import Tunnel, HostKeyError
from app.edit_ui import EditProfile
from app.util import utl, ConfirmDelete


class MainUi(Gtk.Window):

    def __init__(self):

        self.tunnels = {}

        builder = Gtk.Builder()
        builder.add_from_file(utl.glade_file("main_ui"))
        builder.connect_signals({"onDestroy": self.main_quit})

        self.window = builder.get_object("main_ui")
        self.window.set_icon_from_file("{}/assets/img/icon.png".format(utl.conf['base_path']))

        self._load_css()
        self._build_headerbar()

        self.tunnel_listbox = builder.get_object("profiles")
        self.tunnel_listbox.get_style_context().add_class("profile-list")

        self.create_list_items()
        self.window.show_all()

    def _load_css(self):
        css = Gtk.CssProvider()
        css.load_from_path("{}/assets/style.css".format(utl.conf['base_path']))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _build_headerbar(self):
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_title("TunnelMan")

        add_btn = Gtk.Button.new_from_icon_name("list-add-symbolic", Gtk.IconSize.BUTTON)
        add_btn.set_tooltip_text("Add profile")
        add_btn.connect("clicked", self.on_add_profile_btn_clicked)
        add_btn.get_style_context().add_class("suggested-action")
        hb.pack_end(add_btn)

        about_btn = Gtk.Button.new_from_icon_name("help-about-symbolic", Gtk.IconSize.BUTTON)
        about_btn.set_tooltip_text("About TunnelMan")
        about_btn.connect("clicked", self.on_about_clicked)
        about_btn.get_style_context().add_class("flat")
        hb.pack_start(about_btn)

        self.window.set_titlebar(hb)

    def create_list_items(self):

        for item in self.tunnel_listbox:
            self.tunnel_listbox.remove(item)

        current_ids = {p['id'] for p in utl.conf['profiles']}

        for stale_id in list(self.tunnels.keys()):
            if stale_id not in current_ids:
                self.tunnels[stale_id].close_tunnel()
                del self.tunnels[stale_id]

        for profile in utl.conf['profiles']:
            pid = profile['id']
            existing = self.tunnels.get(pid)
            if existing and existing.is_open:
                self.tunnels[pid] = existing
            else:
                self.tunnels[pid] = Tunnel(profile)

            tunnel = self.tunnels[pid]

            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            hbox.get_style_context().add_class("profile-row")
            row.add(hbox)

            # Status dot
            dot = Gtk.Label("●")
            dot.get_style_context().add_class("status-dot")
            self._update_dot(dot, tunnel)
            hbox.pack_start(dot, False, False, 0)

            # Profile name
            name_label = Gtk.Label(xalign=0)
            name_label.set_text(profile['name'])
            name_label.get_style_context().add_class("profile-name")
            hbox.pack_start(name_label, True, True, 0)

            # Edit button
            edit_btn = Gtk.Button.new_from_icon_name("document-edit-symbolic", Gtk.IconSize.BUTTON)
            edit_btn.set_tooltip_text("Edit profile")
            edit_btn.get_style_context().add_class("flat")
            edit_btn.connect("clicked", self.on_edit_profile_btn_clicked, pid)
            hbox.pack_start(edit_btn, False, False, 0)

            # Delete button
            delete_btn = Gtk.Button.new_from_icon_name("edit-delete-symbolic", Gtk.IconSize.BUTTON)
            delete_btn.set_tooltip_text("Delete profile")
            delete_btn.get_style_context().add_class("flat")
            delete_btn.connect("clicked", self.on_delete_profile_btn_clicked, pid)
            hbox.pack_start(delete_btn, False, False, 0)

            # Toggle switch
            switch = Gtk.Switch()
            switch.set_valign(Gtk.Align.CENTER)
            switch.connect("notify::active", self.on_switch_activated, tunnel, dot)
            switch.set_active(tunnel.is_open)
            hbox.pack_start(switch, False, False, 0)

            self.tunnel_listbox.add(row)

        self.tunnel_listbox.show_all()

    def _update_dot(self, dot, tunnel):
        ctx = dot.get_style_context()
        for cls in ('status-open', 'status-closed', 'status-error', 'status-connecting'):
            ctx.remove_class(cls)
        css_class = {
            'Open':          'status-open',
            'Error':         'status-error',
            'Connecting...': 'status-connecting',
        }.get(tunnel.status['message'], 'status-closed')
        ctx.add_class(css_class)
        dot.set_tooltip_text(tunnel.status['message'])

    def main_quit(self, gparam):
        for tunnel in list(self.tunnels.values()):
            if tunnel.is_open:
                tunnel.close_tunnel()
        Gtk.main_quit()

    def on_switch_activated(self, switch, gparam, tunnel, dot):
        if switch.get_active() and tunnel.is_open:
            return
        elif switch.get_active():
            switch.set_sensitive(False)
            tunnel.status['message'] = 'Connecting...'
            self._update_dot(dot, tunnel)

            def do_connect():
                result = tunnel.open_tunnel()
                GLib.idle_add(on_connect_done, result)

            def on_connect_done(result):
                switch.set_sensitive(True)
                if result is True:
                    self._update_dot(dot, tunnel)
                elif isinstance(result, HostKeyError):
                    if self._confirm_host_key(str(result)):
                        switch.set_sensitive(False)
                        tunnel.status['message'] = 'Connecting...'
                        self._update_dot(dot, tunnel)
                        def do_retry():
                            r = tunnel.open_tunnel(trust_new_host=True)
                            GLib.idle_add(on_connect_done, r)
                        threading.Thread(target=do_retry, daemon=True).start()
                    else:
                        self._suppress_switch = True
                        switch.set_active(False)
                        self._suppress_switch = False
                        self._update_dot(dot, tunnel)
                else:
                    self._suppress_switch = True
                    switch.set_active(False)
                    self._suppress_switch = False
                    self._update_dot(dot, tunnel)
                    self._show_error_dialog(str(result))
                return False

            threading.Thread(target=do_connect, daemon=True).start()
        else:
            if getattr(self, '_suppress_switch', False):
                return
            if tunnel.is_open:
                tunnel.close_tunnel()
            self._update_dot(dot, tunnel)

    def _confirm_host_key(self, stderr):
        lines = [l for l in stderr.splitlines()
                 if not l.startswith('Are you sure')
                 and 'Host key verification failed' not in l]
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Unknown host — connect anyway?",
        )
        dialog.format_secondary_text('\n'.join(lines))
        response = dialog.run()
        dialog.destroy()
        return response == Gtk.ResponseType.YES

    def _show_error_dialog(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text="Failed to open tunnel",
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def on_about_clicked(self, widget):
        dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        dialog.set_program_name("TunnelMan")
        dialog.set_version("1.0")
        dialog.set_authors(["Fredrik Welander"])
        dialog.set_website("https://github.com/subsite/tunnelman")
        dialog.set_website_label("github.com/subsite/tunnelman")
        dialog.set_comments("SSH tunnel manager")
        dialog.set_license_type(Gtk.License.GPL_3_0)
        dialog.set_logo_icon_name(None)
        try:
            dialog.set_logo(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    "{}/assets/img/icon.png".format(utl.conf['base_path']), 64, 64, True
                )
            )
        except Exception:
            pass
        dialog.run()
        dialog.destroy()

    def on_add_profile_btn_clicked(self, widget):
        self.on_edit_profile_btn_clicked(widget, None)

    def on_edit_profile_btn_clicked(self, widget, profile_id):
        if profile_id is None:
            profile_index = None
        else:
            ids = [p['id'] for p in utl.conf['profiles']]
            profile_index = ids.index(profile_id) if profile_id in ids else None

        dialog = EditProfile(self.window, profile_index).dialog
        dialog.run()
        dialog.close()
        self.create_list_items()

    def on_delete_profile_btn_clicked(self, widget, profile_id):
        dialog = ConfirmDelete(self.window).dialog
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            ids = [p['id'] for p in utl.conf['profiles']]
            if profile_id in ids:
                profile_index = ids.index(profile_id)
                name = utl.conf['profiles'][profile_index]['name']
                utl.conf['profiles'].pop(profile_index)
                if profile_id in self.tunnels:
                    self.tunnels[profile_id].close_tunnel()
                    del self.tunnels[profile_id]
                utl.save_profiles_conf()
                utl.log(f"[{name}] Profile deleted")
                self.create_list_items()
        dialog.close()
