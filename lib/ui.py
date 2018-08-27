import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow(Gtk.Window):

    def __init__(self, config):
        Gtk.Window.__init__(self, title="Hello World")

        self.button = Gtk.Button(label="Open Tunnel")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

        self.button = Gtk.Button(label="Close Tunnel")
        self.button.connect("clicked", self.on_button_close_clicked)
        self.add(self.button)



    def on_button_clicked(self, widget):
        print("Hello World")


    def on_button_close_clicked(self, widget):
        print("HelloClose")