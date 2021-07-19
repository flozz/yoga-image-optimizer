# File from: https://gist.github.com/flozz/2560bcced07abde5713d3eeae839bf60

"""
This module contains helpers to deal with GTK 3 themes in Python / PyGObject.


Dependencies
------------

* Python 3
* PyGObject
* GLib, Gio and GTK with introspection files


Run the examples
----------------

::

    python3 gtk_themes_helpers.py


Author
------

* Fabien LOISON (https://github.com/flozz)


License
-------

::

    .           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                        Version 2, December 2004

     Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

     Everyone is permitted to copy and distribute verbatim or modified
     copies of this license document, and changing it is allowed as long
     as the name is changed.

                DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
       TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

      0. You just DO WHAT THE FUCK YOU WANT TO.


See also
--------

The following code was inspired by GTK Inspector and Inkscape sources:

* https://gitlab.gnome.org/GNOME/gtk/-/blob/352898ae/gtk/inspector/visual.c#L536
* https://gitlab.com/inkscape/inkscape/-/blob/53780867/src/ui/themes.cpp#L69
"""


from pathlib import Path

from gi.repository import Gtk, Gio, GLib


def get_gtk_theme_name():
    """Get the name of the currently used GTK theme.

    :rtype: str
    """
    settings = Gtk.Settings.get_default()
    return settings.get_property("gtk-theme-name")


def set_gtk_theme_name(gtk_theme_name):
    """Set the GTK theme to use.

    :param str gtk_theme_name: The name of the theme to use (e.g.
                               ``"Adwaita"``).
    """
    settings = Gtk.Settings.get_default()
    settings.set_property("gtk-theme-name", gtk_theme_name)


def get_gtk_application_prefer_dark_theme():
    """Returns ``True`` if GTK is currently using the dark variant of the
    theme.

    :rtype: bool
    """
    settings = Gtk.Settings.get_default()
    return settings.get_property("gtk-application-prefer-dark-theme")


def set_gtk_application_prefer_dark_theme(use_dark_theme):
    """Defines whether the dark variant of the GTK theme should be used or
    not.

    :param bool use_dark_theme: If ``True`` the dark variant of the theme will
                                be used (if available).
    """
    settings = Gtk.Settings.get_default()
    settings.set_property("gtk-application-prefer-dark-theme", use_dark_theme)


def list_gtk_themes():
    """Lists all available GTK theme.

    :rtype: [str]
    """
    builtin_themes = [
        theme[:-1]
        for theme in Gio.resources_enumerate_children(
            "/org/gtk/libgtk/theme", Gio.ResourceFlags.NONE
        )
    ]

    theme_search_dirs = [
        Path(data_dir) / "themes" for data_dir in GLib.get_system_data_dirs()
    ]
    theme_search_dirs.append(Path(GLib.get_user_data_dir()) / "themes")
    theme_search_dirs.append(Path(GLib.get_home_dir()) / ".themes")
    fs_themes = []
    for theme_search_dir in theme_search_dirs:
        if not theme_search_dir.exists():
            continue

        for theme_dir in theme_search_dir.iterdir():
            if (
                not (theme_dir / "gtk-3.0" / "gtk.css").exists()
                and not (theme_dir / "gtk-3.0" / "gtk-dark.css").exists()
                and not (theme_dir / "gtk-3.20" / "gtk.css").exists()
                and not (theme_dir / "gtk-3.20" / "gtk-dark.css").exists()
            ):
                continue
            fs_themes.append(theme_dir.as_posix().split("/")[-1])

    return sorted(set(builtin_themes + fs_themes))


if __name__ == "__main__":
    print("Available themes: %s" % ", ".join(list_gtk_themes()))
    print("Current theme: %s" % get_gtk_theme_name())
    print("Use dark variant: %s" % get_gtk_application_prefer_dark_theme())
