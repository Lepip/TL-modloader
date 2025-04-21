import os
import shutil
import logging
from src.utils.open_file import resource_path
from src.utils import Args

log = logging.getLogger(__name__)

class ModManager:
    @classmethod
    def load_mods_from_folder(self, source_folder, target_folder, mod_list=None):
        source_folder = resource_path(source_folder)
        target_folder = resource_path(target_folder)
        if os.path.exists(target_folder):
            for filename in os.listdir(target_folder):
                file_path = os.path.join(target_folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    log.error(f'Failed to delete {file_path}. Reason: {e}')
        else:
            os.makedirs(target_folder)

        if os.path.exists(source_folder):
            for filename in os.listdir(source_folder):
                src_file = os.path.join(source_folder, filename)
                dst_file = os.path.join(target_folder, filename)
                if os.path.isfile(src_file):
                    if mod_list is not None and filename not in mod_list:
                        log.info(f'Skipping mod {filename} as it is not in the mod list')
                        continue
                    log.info(f'Loaded mod {filename} to {dst_file}')
                    shutil.copy2(src_file, dst_file)
                else:
                    log.error(f'Source file {src_file} is not a file.')
        else:
            log.error(f'Source folder {source_folder} does not exist.')

    @classmethod
    def load_mods(self, version_var, mod_list=None):
        modpack_folder = Args.get("modpacks_path") + "\\" + version_var
        mods_folder = Args.get("mods_path")
        log.info(f"Loading mods from: {modpack_folder} to {mods_folder}")
        ModManager.load_mods_from_folder(modpack_folder, mods_folder, mod_list)

    @classmethod
    def list_mods_from_folder(self, folder):
        folder = resource_path(folder)
        mods = []
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                if filename.endswith('.jar'):
                    mods.append(filename)
            return mods
        else:
            log.error(f'Folder {folder} does not exist.')
            return []
        
    @classmethod
    def list_mods(self, version_var):
        modpack_folder = Args.get("modpacks_path") + "\\" + version_var
        return ModManager.list_mods_from_folder(modpack_folder)