import sys
from pathlib import Path
import os

# Take a sysroot directory and turn all the absolute symlinks and turn them into
# relative ones such that the sysroot is usable within another system.

if len(sys.argv) != 2:
    print(f"Usage is {sys.argv[0]} <sysroot-directory>")
    sys.exit(-1)

topdir = Path(sys.argv[1]).absolute()

def handlelink(filep, subdir):
    link = filep.readlink()
    if str(link)[0] != "/":
        return
    if link.startswith(topdir):
        return
    relpath = os.path.relpath((topdir / link).resolve(), subdir)
    #os.unlink(filep)
    #os.symlink(relpath, filep)
    print(filep, relpath, filep)

for f in topdir.glob("**/*"):
    if f.is_file() and f.is_symlink():
        handlelink(f, f.parent)
