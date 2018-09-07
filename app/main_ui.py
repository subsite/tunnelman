import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
# gi.require_version('AppIndicator3', '0.1')
# from gi.repository import AppIndicator3 as appindicator
from app.tunnel import Tunnel
from app.edit_ui import EditProfile
from app import util

config = util.Config()

class MainUi(Gtk.Window):

    
    def __init__(self):

        self.tunnels = []

        #Gtk.Window.__init__(self, title="TunnelMan")
        handlers = {
            "onDestroy": self.main_quit,
            "onAddProfile": self.on_add_profile_btn_clicked
        }

        builder = Gtk.Builder()
        builder.add_from_file("assets/glade/main_ui.glade")
        builder.connect_signals(handlers)

        self.window = builder.get_object("main_ui")
        self.tunnel_listbox = builder.get_object("profiles")


        self.create_list_items()
        self.window.show_all()


    def create_list_items(self):

        for item in self.tunnel_listbox:
            self.tunnel_listbox.remove(item)

        for t, profile in enumerate(config.conf['profiles']):
            #self.add_listbox_row(t)

            #print("Add row {}".format(t))
            
            profile = config.conf['profiles'][t]

            #print("Len: {}".format(len(self.tunnels)))

            try:
                self.tunnels[t]
                # Tunnel already exists
            except:
                self.tunnels.append(Tunnel(profile))

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

            delete_profile_btn = Gtk.Button(None,image=Gtk.Image(stock=Gtk.STOCK_DELETE))
            delete_profile_btn.connect("clicked", self.on_delete_profile_btn_clicked, t)
            hbox.pack_start(delete_profile_btn, False, True, 0)

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


    def on_add_profile_btn_clicked(self, widget):        
        self.on_edit_profile_btn_clicked(widget, None)

    def on_edit_profile_btn_clicked(self, widget, profile_index):
        dialog = EditProfile(self.window, profile_index).dialog
        dialog.run()            
        dialog.close()
        self.create_list_items()
        

    def on_delete_profile_btn_clicked(self, widget, profile_index):
        dialog = util.ConfirmDelete(self.window).dialog
        response = dialog.run()  
        if response == Gtk.ResponseType.OK:
            config.conf['profiles'].pop(profile_index)
            self.tunnels.pop(profile_index)
            config.save_profiles_conf()
            self.create_list_items()          
        dialog.close()

    def get_status_all(self):
        for t in self.all_tunnels:
            print("{}: {}".format(t.profile['name'], t.status))

    


        

