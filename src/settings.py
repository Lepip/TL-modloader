from src.utils.reader import ArgsManager, PropManager
from src.utils.consts import Args
import logging
log = logging.getLogger(__name__)

class SettingsEditor:
    @classmethod
    def init(self):
        log.debug("settings.py: init")
        args_path = Args.get("tl_args_path")
        self.args = ArgsManager(args_path)
        prop_path = Args.get("tl_properties_path")
        self.prop = PropManager(prop_path)

    @classmethod
    def set_version(self, version, is_exit=True):
        log.debug(f"settings.py: set_version: {version}")
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