DEST="$HOME/.local/share/nautilus-python/extensions"

mkdir -p "$DEST" && \
rm -rf "$DEST/__pycache__" && \
cp catuns_software_tools.py copy_path_extension.py pdf_tools_extension.py "$DEST" && \
nautilus -q && \
nohup nautilus > /dev/null 2>&1 &
