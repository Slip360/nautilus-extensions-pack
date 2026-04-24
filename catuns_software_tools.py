import gi
from gi.repository import GObject, Nautilus
from copy_path_extension import CopyPathExtension
from pdf_tools_extension import PdfToolsExtension

"""
Class for catun's software tools extension.
"""
class CatunsSoftwareTools(GObject.GObject, Nautilus.MenuProvider):
    """
    Initialize the extension.
    """
    def __init__(self):
        super().__init__()
        self._path_tool = CopyPathExtension()
        self._pdf_tool = PdfToolsExtension()
    
    """
    Get the file items for the context menu.
    """
    def get_file_items(self, files):
        items = []
        pdf_items = self._pdf_tool.get_file_items(files)
        path_items = self._path_tool.get_file_items(files)
        if (pdf_items or path_items):
            items.extend(pdf_items)
            items.extend(path_items)
        return items
