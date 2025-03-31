import os
from src.utils.consts import Args


def populate_versions():
    versions_path = Args.get("versions_path")
    files = [f for f in os.listdir(versions_path)]
    return files