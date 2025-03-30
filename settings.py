from reader import ArgsManager, PropManager
import logging

class Args:
    _args = {}

    @classmethod
    def read(self):
        args = {}
        try:
            with open(".args", 'r') as file:
                for line in file:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        value = value.strip('"')
                        args[key] = value
                for key, value in args.items():
                    try:
                        args[key] = value.format(**args)
                    except KeyError as e:
                        logging.error(f"Missing placeholder in configuration: {e}")
        except FileNotFoundError:
            logging.error(f"The file {self.file_path} does not exist.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        self._args = args
    
    @classmethod
    def get(self, key):
        return self._args.get(key, None)

Args.read()

class SettingsEditor:
    @classmethod
    def init(self):
        args_path = Args.get("tl_args_path")
        self.args = ArgsManager(args_path)
        prop_path = Args.get("tl_properties_path")
        self.prop = PropManager(prop_path)

    @classmethod
    def set_version(self, version, is_exit=True):
        logging.debug(f"settings.py: set_version: {version}")
        self.args.set("version", version)
        if is_exit:
            self.args.set("launch", "")
        else:
            self.args.remove("launch")

    @classmethod
    def modify_settings(self, exit_launcher=True):
        if exit:
            self.prop.set("minecraft.onlaunch", "exit")

    @classmethod
    def restore(self):
        self.args.restore()
        self.prop.restore()

SettingsEditor.init()