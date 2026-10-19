"""Create a ZIP containing tracked project files only (no secrets/dependencies)."""
from pathlib import Path
import subprocess,zipfile
root=Path(__file__).resolve().parents[1]
files=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0')
destination=root.parent/'cars-dealership-capstone.zip'
with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as archive:
    for name in filter(None,files):
        path=root/name
        if path.is_file(): archive.write(path,'cars-dealership/'+name)
print(destination)
