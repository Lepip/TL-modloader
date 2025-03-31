import logging

class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path
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
            logging.error(f"The file {self.file_path} does not exist.")
            return {}
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return {}
        return properties
    
    def write(self, properties=None):
        if properties is None:
            properties = self.properties
        try:
            with open(self.file_path, 'w') as file:
                for key, value in properties.items():
                    file.write(f'{key}={value}\n')
        except Exception as e:
            logging.error(f"An error occurred: {e}")
    
    def set(self, key, value, is_write=True):
        self.properties[key] = value
        if is_write:
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
            logging.error(f"The file {self.file_path} does not exist.")
            return {}
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return {}
        return properties

    def write(self, properties=None):
        if properties is None:
            properties = self.properties
        try:
            logging.debug(f"Writing to {self.file_path}")
            with open(self.file_path, 'w') as file:
                for key, value in properties.items():
                    file.write(f'--{key}\n')
                    file.write(f'{value}\n' if value else '\n')
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def set(self, key, value, is_write=True):
        logging.debug(f"Setting {key} to {value}")
        self.properties[key] = value
        logging.debug(f"Properties after setting: {self.properties}")
        if is_write:
            self.write()
    
    def remove(self, key, is_write=True):
        if key in self.properties:
            del self.properties[key]
            if is_write:
                self.write()
