from pathlib import Path
import platform


def normalize_path(path: str) -> str:
    if platform.system() != "Linux":
        return path

    if len(path) > 2 and path[1] == ":":
        drive = path[0].lower()
        rest = path[2:].replace("\\", "/")
        return f"/mnt/{drive}{rest}"
    return path

