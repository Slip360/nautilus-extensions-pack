import os
import subprocess
import gi
from gi.repository import GObject, GLib, Nautilus, Gdk, Gio

"""
Class for copying the path of a file to the clipboard.
"""
class CopyPathExtension(GObject.GObject):
    """
    Initialize the extension.
    """
    def __init__(self):
        super().__init__()
    """
    Copy the path of a file to the clipboard.
    """
    def _copy_path(self, menu, files):
        file_path = files[0].get_location().get_path()
        display = Gdk.Display.get_default()
        clipboard = display.get_clipboard()
        clipboard.set_content(Gdk.ContentProvider.new_for_value(file_path))
        return
    """
    Get the file items for the context menu.
    """
    def get_file_items(self, files):
        if (len(files) != 1):
            return[]
        item = Nautilus.MenuItem(
            name="CopyPath::Root",
            label="Copiar ruta",
            icon="edit-copy-symbolic",
        )
        item.connect("activate", self._copy_path, files)
        return [item]
