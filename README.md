A wrapper for TL that adds support for modpacks.

You need to specify in .args file where is your launcher and where is your folder with modpacks. Names of modpacks should be the same as the names of versions.

To build use 
```python -m PyInstaller --onefile --clean --windowed --icon=icon.ico main.py --add-data="media/*:media" --add-data="src/cleanup/window_config.ini:src/cleanup"```
