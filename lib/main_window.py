import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from lib.tunnel import Tunnel

class MainWindow(Gtk.Window):

    def __init__(self, config):
        Gtk.Window.__init__(self, title="Tunnelman")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        hbox.pack_start(listbox, True, True, 0)

        for profile in config['profiles']:
            tunnel = Tunnel(profile)
            self.all_tunnels = tunnel._all_tunnels
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
            row.add(hbox)

            label = Gtk.Label(profile['name'], xalign=0)
            hbox.pack_start(label, True, True, 0)

            #details_btn = Gtk.Button(None,image=Gtk.Image(stock=Gtk.STOCK_EDIT))
            #hbox.pack_start(details_btn, False, True, 0)

            switch = Gtk.Switch()
            switch.connect("notify::active", self.on_switch_activated, tunnel)
            hbox.pack_start(switch, False, True, 0)

            listbox.add(row)
    
    def main_quit(self, gparam):
        print("quitting")
        for t in self.all_tunnels:
            t.close_tunnel()
        Gtk.main_quit()

    def on_switch_activated(self, switch, gparam, tunnel):
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

    def get_status_all(self):
        for t in self.all_tunnels:
            print("{}: {}".format(t.profile['name'], t.status))

    


        

