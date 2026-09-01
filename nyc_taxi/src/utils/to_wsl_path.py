def to_wsl_path(path):
    if path.startswith("D:/"):
        return path.replace(
            "D:/",
            "/mnt/d/"
        )
    return path