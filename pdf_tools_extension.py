import os
import subprocess
import gi
gi.require_version('Nautilus', '4.1')
from gi.repository import GObject, Nautilus, GLib
from datetime import datetime

"""
Class for compressing PDF files using Ghostscript.
"""
class PdfToolsExtension(GObject.GObject):
    """
    Initialize the extension.
    """
    def __init__(self):
        super().__init__()
    
    """
    Get a timestamp.
    """
    def _get_timestamp(self):
        return int(datetime.now().timestamp())
    
    """
    Compress PDF files using Ghostscript.
    """
    def _compress_pdf(self, menu, files):
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
    def _merge_pdfs(self, menu, files):
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
    def _merge_and_compress_pdfs(self, menu, files):
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
        item_compress.connect("activate", self._compress_pdf, pdf_files)
        submenu.append_item(item_compress)
        if len(pdf_files) > 1:
            item_merge = Nautilus.MenuItem(
                name="PdfTools::Merge",
                label=f"Combinar {len(pdf_files)} PDF(s)",
                tip="Une todos los PDF en uno solo"
            )
            item_merge.connect("activate", self._merge_pdfs, pdf_files)
            submenu.append_item(item_merge)
            item_merge_and_compress = Nautilus.MenuItem(
                name="PdfTools::MergeAndCompress",
                label=f"Combinar y comprimir {len(pdf_files)} PDF(s)",
                tip="Une todos los PDF en uno solo y reduce el tamaño"
            )
            item_merge_and_compress.connect("activate", self._merge_and_compress_pdfs, pdf_files)
            submenu.append_item(item_merge_and_compress)
        return [top_menu_item]
