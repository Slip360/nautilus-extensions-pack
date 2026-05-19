import gi
gi.require_version('Nautilus', '4.1')
from gi.repository import GObject, Nautilus
from copy_path_extension import CopyPathExtension
from pdf_tools_extension import PdfToolsExtension
from file_creator_extension import FileCreatorExtension

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
        self._file_creator_tool = FileCreatorExtension()
    
    """
    Get the file items for the context menu.
    """
    def get_file_items(self, files):
        items = []
        pdf_items = self._pdf_tool.get_file_items(files)
        path_items = self._path_tool.get_file_items(files)
        items.extend(pdf_items)
        items.extend(path_items)
        return items
    
    """
    Get the background items for the context menu.
    """
    def get_background_items(self, *args):
        folder = args[-1]
        items = []
        items.extend(self._file_creator_tool.get_background_items(folder))
        return items
