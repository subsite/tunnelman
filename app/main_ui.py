import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
# gi.require_version('AppIndicator3', '0.1')
# from gi.repository import AppIndicator3 as appindicator
from app.tunnel import Tunnel
from app.config import Config
from app.edit_ui import EditProfile

config = Config()

class MainUi(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="TunnelMan")
        self.set_border_width(10)

        self.tunnels = []
        
        
        self.tunnel_listbox = None

        self.hbox = Gtk.Box(spacing=6)
        self.add(self.hbox)
        self.tunnel_listbox=Gtk.ListBox()
        self.tunnel_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.hbox.pack_start(self.tunnel_listbox, True, True, 0)

        print(len(config.conf['profiles']))
        #config = Config()
        #for profile in config.conf['profiles']:
            

        hbox = self.hbox
        
        for t, profile in enumerate(config.conf['profiles']):
            self.add_listbox_row(t)
        # Row for add button
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        add_profile_btn = Gtk.Button(None,image=Gtk.Image(stock=Gtk.STOCK_ADD))
        add_profile_btn.connect("clicked", self.on_edit_profile_btn_clicked, None)
        hbox.pack_start(add_profile_btn, False, True, 0)
        self.tunnel_listbox.add(row)
    
        self.tunnel_listbox.show_all()            

    def add_listbox_row(self, t):
        
        profile = config.conf['profiles'][t]
        self.tunnels.append(Tunnel(profile))
        print("tunnel {}".format(t))
        tunnel = self.tunnels[t]
        self.all_tunnels = tunnel._all_tunnels
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)

        label = Gtk.Label(profile['name'], xalign=0)
        hbox.pack_start(label, True, True, 0)

        label_status = Gtk.Label(tunnel.status['message'])
        hbox.pack_start(label_status, False, True, 0)

        edit_profile_btn = Gtk.Button(None,image=Gtk.Image(stock=Gtk.STOCK_EDIT))
        edit_profile_btn.connect("clicked", self.on_edit_profile_btn_clicked, t)
        hbox.pack_start(edit_profile_btn, False, True, 0)

        switch = Gtk.Switch()
        switch.connect("notify::active", self.on_switch_activated, tunnel, label_status)
        hbox.pack_start(switch, False, True, 0)

        self.tunnel_listbox.add(row)
        self.tunnel_listbox.show_all()


    def main_quit(self, gparam):
        print("quitting")
        for t in self.all_tunnels:
            t.close_tunnel()
        Gtk.main_quit()

    def on_switch_activated(self, switch, gparam, tunnel, label_status):
        
        if switch.get_active():
            print("Opening tunnel {}".format(tunnel.profile['name']))
            tunnel.open_tunnel()
            print(self.get_status_all())

        else:
            print("Closing tunnel {}".format(tunnel.profile['name']))
            try:
                tunnel.close_tunnel()
                print(self.get_status_all())
            except:
                print("close failed")
        label_status.set_text(tunnel.status['message'])

    def on_edit_profile_btn_clicked(self, widget, profile_index):
        dialog = EditProfile(self, profile_index)
        print("foo")
        #dialog.destroy()

    def get_status_all(self):
        for t in self.all_tunnels:
            print("{}: {}".format(t.profile['name'], t.status))

    


        

