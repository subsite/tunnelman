#!/usr/bin/python3

import signal
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from app.main_ui import MainUi

def main():

    MainUi()
    Gtk.main()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
