import logging
from src.utils.open_file import resource_path

log = logging.getLogger(__name__)

NAME="LMC Launcher"
VERSION="0.0.2"

ARGS_PATH = ".args"

class Args:
    _args = {}
    _write_args = {}

    @classmethod
    def read(self):
        log.info("Reading arguments")
        args = {}
        write_args = {}
        try:
            with open(ARGS_PATH, 'r') as file:
                for line in file:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        value = value.strip('"')
                        args[key] = value
                        write_args[key] = line
                for key, value in args.items():
                    try:
                        args[key] = value.format(**args)
                    except KeyError as e:
                        log.error(f"Missing placeholder in configuration: {e}")
        except FileNotFoundError:
            log.error(f"The file .args does not exist.")
        except Exception as e:
            log.error(f"An error occurred: {e}")
        self._args = args
        self._write_args = write_args
    
    @classmethod
    def get(self, key, default=None):
        return self._args.get(key, default)
    
    @classmethod
    def set(self, key, value):
        self._args[key] = value
        self._write_args[key] = f"{key}={value}\n"

    @classmethod
    def save(self):
        with open(ARGS_PATH, 'w') as file:
            for key, value in self._write_args.items():
                file.write(value)
Args.read()