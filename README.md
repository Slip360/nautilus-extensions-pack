# Nautilus Extensions Pack

Por **Catun's Software**.

Un paquete de extensiones útiles para el gestor de archivos Nautilus (GNOME Files) integradas directamente en el menú contextual.

## Características

### 1. Copiar ruta
* **Copiar ruta**: Permite copiar la ruta absoluta de un archivo o directorio seleccionado directamente al portapapeles.

### 2. Herramientas PDF
* **Comprimir PDF(s)**: Reduce el tamaño de los PDFs seleccionados utilizando Ghostscript. Crea un nuevo archivo con el sufijo `_comprimido`.
* **Combinar PDF(s)**: Selecciona dos o más archivos PDF y únelos en un solo archivo llamado `_combinado.pdf`.
* **Combinar y comprimir PDF(s)**: Une múltiples archivos PDF y reduce su tamaño en un solo paso, creando un archivo `_combinado_y_comprimido.pdf`.

## Requisitos Previos

Para que estas extensiones funcionen correctamente, necesitas tener instalados los siguientes paquetes en tu sistema:
- `python3-nautilus` (o equivalente, proporciona el soporte de Python para Nautilus)
- `ghostscript` (herramienta encargada de procesar, comprimir y combinar los PDFs)

### Instalación de dependencias

**En distribuciones basadas en Debian/Ubuntu:**
```bash
sudo apt update
sudo apt install python3-nautilus ghostscript
```

**En distribuciones basadas en Arch Linux:**
```bash
sudo pacman -S python-nautilus ghostscript
```

**En distribuciones basadas en Fedora:**
```bash
sudo dnf install nautilus-python ghostscript
```

## Instalación

Puedes instalar o actualizar todas las extensiones fácilmente usando el script de configuración incluido:

1. Abre una terminal en el directorio de este repositorio.
2. Da permisos de ejecución al script `setup.sh`:
```bash
chmod +x setup.sh
```
3. Ejecuta el script:
```bash
./setup.sh
```
El script se encargará de crear el directorio necesario, copiar los archivos de las extensiones (`catuns_software_tools.py`, `copy_path_extension.py`, `pdf_tools_extension.py`) a `~/.local/share/nautilus-python/extensions/` y reiniciará Nautilus automáticamente para aplicar los cambios.

## Uso

### Usar "Copiar ruta"
1. Abre Nautilus.
2. Haz clic derecho sobre un único archivo.
3. Selecciona la opción **Copiar ruta** en el menú contextual.

### Usar "Opciones para PDF"
1. Abre Nautilus y navega hasta donde tengas tus archivos `.pdf`.
2. Selecciona uno o más archivos PDF.
3. Haz clic derecho sobre los archivos seleccionados.
4. En el menú contextual, busca el submenú **Opciones para PDF** (con un icono de propiedades de documento).
5. Elige la acción deseada (Comprimir, Combinar, o Combinar y comprimir).
