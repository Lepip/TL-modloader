import logging

NAME="LMC Launcher"
VERSION="0.0.2"

class Args:
    _args = {}

    @classmethod
    def read(self):
        logging.info("Reading arguments")
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