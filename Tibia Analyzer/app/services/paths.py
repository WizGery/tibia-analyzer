import os

def project_root() -> str:
    # carpeta raíz del proyecto (dos niveles arriba de este archivo)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def library_dir() -> str:
    path = os.path.join(project_root(), "data", "json")
    os.makedirs(path, exist_ok=True)
    return path
