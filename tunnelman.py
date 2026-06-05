#!/usr/bin/python3

import signal
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from app.util import utl
from app.main_ui import MainUi

def main():
    if '-v' in sys.argv:
        utl.verbose = True
        print("Verbose mode on")

    MainUi()
    Gtk.main()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
