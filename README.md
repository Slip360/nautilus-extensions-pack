# Nautilus PDF Tools Extension

Por **Catun's Software**.

Una extensión sencilla para el gestor de archivos Nautilus (GNOME Files) que permite comprimir y combinar archivos PDF directamente desde el menú contextual.

## Características
* **Comprimir PDF(s)**: Reduce el tamaño de los PDFs seleccionados utilizando Ghostscript. Crea un nuevo archivo con el sufijo `_comprimido`.
* **Combinar PDF(s)**: Selecciona dos o más archivos PDF y únelos en un solo archivo llamado `pdf_combinado.pdf`.

## Requisitos Previos

Para que esta extensión funcione correctamente, necesitas tener instalados los siguientes paquetes en tu sistema:
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

## Instalación de la Extensión

1. Abre una terminal.
2. Asegúrate de que el directorio para las extensiones de Python de Nautilus exista para tu usuario:
```bash
mkdir -p ~/.local/share/nautilus-python/extensions
```
3. Copia el archivo `pdf-tools-extension.py` al directorio de extensiones:
```bash
cp pdf-tools-extension.py ~/.local/share/nautilus-python/extensions/
```
4. Reinicia Nautilus para que cargue la nueva extensión:
```bash
nautilus -q
```

## Uso

1. Abre Nautilus y navega hasta donde tengas tus archivos `.pdf`.
2. Selecciona uno o más archivos PDF.
3. Haz clic derecho sobre los archivos seleccionados.
4. En el menú contextual, busca el submenú **Opciones para PDF** (con un icono de propiedades de documento).
5. Elige la acción deseada (Comprimir o Combinar).
