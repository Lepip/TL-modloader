import os
import sys
import logging
log = logging.getLogger(__name__)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def open_file(file_path, mode):
    new_path = resource_path(file_path)
    log.info(f"Opening file: {new_path}")
    return open(resource_path(file_path), mode)