import json
import os
from src.utils.consts import Args
import logging

log = logging.getLogger(__name__)

def populate_versions():
    versions_path = Args.get("versions_path")
    files = [f for f in os.listdir(versions_path)]
    return files

def update_version(version_var):
    selected_version = version_var.get()
    Args.set("version", selected_version)

def get_version_number(version):
    versions_path = Args.get("versions_path")
    version_path = os.path.join(versions_path, version)
    version_json_path = os.path.join(version_path, f"{version}.json")
    log.info(f"Getting version of {version} from {version_json_path}")
    if not os.path.exists(version_json_path):
        return "Unknown"
    with open(version_json_path, 'r') as f:
        version_json = json.load(f)
        if "jar" in version_json:
            log.info(f"Loaded version {version_json['jar']}")
            return version_json["jar"]
        if "id" in version_json:
            log.info(f"Loaded version {version_json['id']}")
            return version_json["id"]
        return None

def select_version(versions):
    last_version = Args.get("version")
    if last_version in versions:
        return last_version
    if versions:
        return versions[0]
    return None