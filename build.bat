pyinstaller -i icon.ico --onefile --clean --distpath dev/ -n lte main.py
del lte.spec
rd /s /q "build"