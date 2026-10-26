import os, subprocess, sys
from pathlib import Path
def launch_game(executable):
    """Launch exactly the executable selected by the user."""
    path=Path(executable).expanduser().resolve()
    if not path.exists() or not path.is_file(): raise FileNotFoundError(f"Selected game executable does not exist:\n{path}")
    if os.name!="nt" and not os.access(path,os.X_OK): raise PermissionError(f"File is not executable. Check permissions:\n{path}")
    if sys.platform=="darwin" and path.suffix.lower()==".app": return subprocess.Popen(["open",str(path)],cwd=str(path.parent))
    return subprocess.Popen([str(path)],cwd=str(path.parent))
