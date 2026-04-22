import os
import subprocess
import threading
import gi
from gi.repository import GObject, Nautilus

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
    Run a command in a separate thread.
    """
    def run_command(self, cmd):
        def target():
            try:
                subprocess.run(cmd, check=True)
            except Exception:
                print("Error al ejecutar el comando")
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
    
    """
    Compress PDF files using Ghostscript.
    """
    def compress_pdf(self, menu, files):
        for file in files:
            filepath = file.get_location().get_path()
            output_path = filepath.replace(".pdf", "_comprimido.pdf")
            cmd = [
                "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
                "-dPDFSETTINGS=/ebook", "-dNOPAUSE", "-dQUIET", "-dBATCH",
                f"-sOutputFile={output_path}", filepath
            ]
            self.run_command(cmd)
    
    """
    Merge PDF files using Ghostscript.
    """
    def merge_pdfs(self, menu, files):
        paths = [f.get_location().get_path() for f in files]
        output = os.path.join(os.path.dirname(paths[0]), "pdf_combinado.pdf")
        cmd = [
            "gs", "-sDEVICE=pdfwrite", "-dNOPAUSE", "-dQB", "-dBATCH",
            f"-sOutputFile={output}"
        ] + paths
        self.run_command(cmd)
    
    """
    Get the file items for the context menu.
    """
    def get_file_items(self, files):
        pdf_files = [f for f in files if f.get_name().lower().endswith(".pdf") and not f.is_directory()]
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
        return [top_menu_item]
