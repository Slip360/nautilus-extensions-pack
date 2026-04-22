import os
import subprocess
import threading
import gi
from gi.repository import GObject, Nautilus, Notify, GLib
from datetime import datetime

"""
Initialize the notifications.
"""
Notify.init("org.gnome.Nautilus")

"""
Class for compressing PDF files using Ghostscript.
"""
class PdfToolsExtension(GObject.GObject, Nautilus.MenuProvider):
    """
    Initialize the extension.
    """
    def __init__(self):
        super().__init__()

    """
    Show a notification.
    """
    def _show_notification(self, title, message):
        def _do_show():
            notification = Notify.Notification.new(title, message, "system-run-symbolic")
            notification.set_category("transfer")
            notification.set_urgency(Notify.Urgency.NORMAL)
            notification.set_hint("transient", GLib.Variant('b', True))
            notification.show()
            return False
        GObject.idle_add(_do_show)
    
    """
    Get a timestamp.
    """
    def _get_timestamp(self):
        return int(datetime.now().timestamp())
    
    """
    Compress PDF files using Ghostscript.
    """
    def compress_pdf(self, menu, files):
        ts = self._get_timestamp()
        for file in files:
            filepath = file.get_location().get_path()
            output_path = os.path.join(os.path.dirname(filepath), f"{ts}_comprimido.pdf")
            cmd = [
                "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
                "-dPDFSETTINGS=/ebook", "-dNOPAUSE", "-dQUIET", "-dBATCH",
                f"-sOutputFile={output_path}", filepath
            ]
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
    
    """
    Merge PDF files using Ghostscript.
    """
    def merge_pdfs(self, menu, files):
        paths = [f.get_location().get_path() for f in files]
        ts = self._get_timestamp()
        output_path = os.path.join(os.path.dirname(paths[0]), f"{ts}_combinado.pdf")
        cmd = [
            "gs", "-sDEVICE=pdfwrite", "-dNOPAUSE", "-dQB", "-dBATCH",
            f"-sOutputFile={output_path}"
        ] + paths
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
    
    """
    Merge and compress PDF files using Ghostscript.
    """
    def merge_and_compress_pdfs(self, menu, files):
        paths = [f.get_location().get_path() for f in files]
        ts = self._get_timestamp()
        output_path = os.path.join(os.path.dirname(paths[0]), f"{ts}_combinado_y_comprimido.pdf")
        cmd = [
            "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/ebook",
            "-dNOPAUSE", "-dQUIET", "-dBATCH",
            f"-sOutputFile={output_path}"
        ] + paths
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
    
    """
    Get the file items for the context menu.
    """
    def get_file_items(self, files):
        pdf_files = [f for f in files if f.get_mime_type() == "application/pdf" and not f.is_directory()]
        if not pdf_files:
            return []
        top_menu_item = Nautilus.MenuItem(
            name="PdfTools::Root",
            label="Opciones para PDF",
            tip="Herramientas de Catun's Software",
            icon="document-properties-symbolic"
        )
        submenu = Nautilus.Menu()
        top_menu_item.set_submenu(submenu)
        item_compress = Nautilus.MenuItem(
            name="PdfTools::Compress",
            label=f"Comprimir {len(pdf_files)} PDF(s)",
            tip="Reduce el tamaño de los PDF"
        )
        item_compress.connect("activate", self.compress_pdf, pdf_files)
        submenu.append_item(item_compress)
        if len(pdf_files) > 1:
            item_merge = Nautilus.MenuItem(
                name="PdfTools::Merge",
                label=f"Combinar {len(pdf_files)} PDF(s)",
                tip="Une todos los PDF en uno solo"
            )
            item_merge.connect("activate", self.merge_pdfs, pdf_files)
            submenu.append_item(item_merge)
            item_merge_and_compress = Nautilus.MenuItem(
                name="PdfTools::MergeAndCompress",
                label=f"Combinar y comprimir {len(pdf_files)} PDF(s)",
                tip="Une todos los PDF en uno solo y reduce el tamaño"
            )
            item_merge_and_compress.connect("activate", self.merge_and_compress_pdfs, pdf_files)
            submenu.append_item(item_merge_and_compress)
        return [top_menu_item]
