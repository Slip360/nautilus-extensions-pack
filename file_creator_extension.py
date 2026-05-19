import os
import subprocess
import gi
gi.require_version('Nautilus', '4.1')
from gi.repository import GObject, Nautilus

"""
Class for creating smart files in the context menu.
"""
class FileCreatorExtension(GObject.GObject):
    """
    Initialize the extension.
    """
    def __init__(self):
        super().__init__()

    """
    Create a smart file in the given directory.
    """
    def _create_smart_file(self, menu, directory):
        # try:
        #     folder_path = directory.get_location().get_path()
        #     cmd = [
        #         'zenity', '--entry', 
        #         '--title=Nuevo Archivo Inteligente', 
        #         '--text=Introduce nombre y extensión (ej: notas.docx, script.py):',
        #         '--entry-text=documento.docx'
        #     ]
        #     filename = subprocess.check_output(cmd).decode("utf-8").strip()
        #     if (filename):
        #         full_path = os.path.join(folder_path, filename)
        #         if (os.path.exists(full_path)):
        #             subprocess.run(['zenity', '--error', '--text=El archivo ya existe.'])
        #             return
        #     with open(full_path, "w") as f:
        #         f.write("")
        # except subprocess.CalledProcessError:
        #     pass
        try:
            folder_path = directory.get_location().get_path()

            # 1. Menú de selección de tipo de archivo
            # Formato: Descripción | Extensión
            choices = [
                "Documento de Word", ".docx",
                "Hoja de Cálculo", ".xlsx",
                "Presentación", ".pptx",
                "Script de Python", ".py",
                "Archivo de Texto", ".txt",
                "Documento Markdown", ".md"
            ]

            cmd_list = [
                'zenity', '--list',
                '--title=Seleccionar tipo de archivo',
                '--column=Tipo', '--column=Extensión',
                '--hide-column=2', '--print-column=2'
            ] + choices

            extension = subprocess.check_output(cmd_list).decode("utf-8").strip()

            if not extension:
                return

            # 2. Pedir el nombre del archivo
            cmd_name = [
                'zenity', '--entry',
                '--title=Nombre del archivo',
                f'--text=Introduce el nombre (se añadirá {extension}):',
                '--entry-text=nuevo_archivo'
            ]
            
            name = subprocess.check_output(cmd_name).decode("utf-8").strip()

            if name:
                # Aseguramos que no duplique la extensión si el usuario la escribe
                if not name.endswith(extension):
                    filename = name + extension
                else:
                    filename = name
                
                full_path = os.path.join(folder_path, filename)

                if os.path.exists(full_path):
                    subprocess.run(['zenity', '--error', '--text=¡Error! El archivo ya existe.'])
                    return

                # 3. Diccionario de "Bytes Mágicos" para evitar el problema de touch (0 bytes)
                # PK\x03\x04 es la cabecera estándar de archivos ZIP (que usan .docx, .xlsx, .pptx)
                MINIMAL_BYTES = {
                    ".docx": b'PK\x03\x04\x14\x00\x00\x00\x08\x00',
                    ".xlsx": b'PK\x03\x04\x14\x00\x00\x00\x08\x00',
                    ".pptx": b'PK\x03\x04\x14\x00\x00\x00\x08\x00',
                }

                # Escribimos en modo binario "wb"
                with open(full_path, "wb") as f:
                    f.write(MINIMAL_BYTES.get(extension, b""))

        except subprocess.CalledProcessError:
            pass # El usuario canceló o cerró la ventana
    
    """
    Get the background items for the context menu.
    """
    def get_background_items(self, folder):
        item = Nautilus.MenuItem(
            name="FileCreator::Root",
            label="Crear archivo",
            icon="edit-copy-symbolic",
        )
        item.connect("activate", self._create_smart_file, folder)
        return [item]
