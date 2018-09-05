#!/usr/bin/python3

import signal
from pathlib import Path
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from app.main_ui import MainUi
from app.config import Config

config = Config()


def main():

    main_window = MainUi()
    #To refresh icon, rm ~/.local/share/applications/tunnelman_py.desktop
    main_window.set_icon_from_file("{}/logo.png".format(config.conf['base_path']))
    main_window.connect("destroy", main_window.main_quit)
    main_window.show_all()

    Gtk.main()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
