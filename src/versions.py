import os
from src.utils.consts import Args

def populate_versions():
    versions_path = Args.get("versions_path")
    files = [f for f in os.listdir(versions_path)]
    return files

def update_version(version_var):
    selected_version = version_var.get()
    Args.set("version", selected_version)

def select_version(versions):
    last_version = Args.get("version")
    if last_version in versions:
        return last_version
    if versions:
        return versions[0]
    return None