import os
import shutil
import logging
log = logging.getLogger(__name__)

class ModManager:
    @classmethod
    def load_mods(self, source_folder, target_folder):
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
                    log.info(f'Loaded mod {filename} to {dst_file}')
                    shutil.copy2(src_file, dst_file)
                else:
                    log.error(f'Source file {src_file} is not a file.')
        else:
            log.error(f'Source folder {source_folder} does not exist.')