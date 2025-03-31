import logging
from src.utils.open_file import resource_path
log = logging.getLogger(__name__)

class FileManager:
    def __init__(self, file_path):
        self.file_path = resource_path(file_path)
        with open(file_path, 'r') as file:
            self.original = file.readlines()
    
    def restore(self):
        with open(self.file_path, 'w') as file:
            file.writelines(self.original)

class PropManager(FileManager):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.properties = self.read()
    
    def read(self):
        properties = {}
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    if line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        properties[key] = value
        except FileNotFoundError:
            log.error(f"The file {self.file_path} does not exist.")
            return {}
        except Exception as e:
            log.error(f"An error occurred: {e}")
            return {}
        return properties
    
    def write(self, properties=None):
        if properties is None:
            properties = self.properties
        try:
            log.info(f"PropManager: write: {self.file_path}")
            with open(self.file_path, 'w') as file:
                for key, value in properties.items():
                    file.write(f'{key}={value}\n')
                    log.info(f"PropManager: write: {key}={value}")
        except Exception as e:
            log.error(f"An error occurred: {e}")
    
    def set(self, key, value, is_write=True):
        log.info(f"PropManager: set: {key}={value}")
        self.properties[key] = value
        if is_write:
            log.info(f"PropManager: set: write")
            self.write(self.properties)

class ArgsManager(FileManager):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.properties = self.read()

    def read(self):
        properties = {}
        try:
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
                key = None
                for line in lines:
                    line = line.strip()
                    if line.startswith('--'):
                        if key is not None:
                            properties[key] = ''
                        key = line[2:]
                    elif key:
                        properties[key] = line
                        key = None
                if key is not None:
                    properties[key] = ''
        except FileNotFoundError:
            log.error(f"The file {self.file_path} does not exist.")
            return {}
        except Exception as e:
            log.error(f"An error occurred: {e}")
            return {}
        return properties

    def write(self, properties=None):
        if properties is None:
            properties = self.properties
        try:
            log.info(f"Writing to {self.file_path}")
            with open(self.file_path, 'w') as file:
                for key, value in properties.items():
                    file.write(f'--{key}\n')
                    file.write(f'{value}\n' if value else '\n')
        except Exception as e:
            log.error(f"An error occurred: {e}")

    def set(self, key, value, is_write=True):
        log.info(f"Setting {key} to {value}")
        self.properties[key] = value
        log.info(f"Properties after setting: {self.properties}")
        if is_write:
            self.write()
    
    def remove(self, key, is_write=True):
        if key in self.properties:
            del self.properties[key]
            if is_write:
                self.write()
