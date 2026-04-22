import os
import subprocess
import threading
import gi
from gi.repository import GObject, Nautilus, Notify, GLib

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
    Run a command in a separate thread.
    """
    def run_command(self, cmd, task_name, output_file):
        def target():
            self._show_notification(
                "Proceso iniciado",
                f"Ejecutando: {task_name}..."
            )
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                # self._refresh_nautilus(output_file)
                self._show_notification(
                    "Proceso completado",
                    f"Se ha creado: {os.path.basename(output_file)}"
                )
            except Exception:
                self._show_notification(
                    "Error en la operación",
                    f"Error al ejecutar: {task_name}"
                )
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
            self.run_command(cmd, "Compresión de PDF", output_path)
    
    """
    Merge PDF files using Ghostscript.
    """
    def merge_pdfs(self, menu, files):
        paths = [f.get_location().get_path() for f in files]
        output_path = os.path.join(os.path.dirname(paths[0]), "pdf_combinado.pdf")
        cmd = [
            "gs", "-sDEVICE=pdfwrite", "-dNOPAUSE", "-dQB", "-dBATCH",
            f"-sOutputFile={output_path}"
        ] + paths
        self.run_command(cmd, "Combinación de PDF", output_path)
    
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
