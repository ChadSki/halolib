@echo off
set HOME=%~dp0
set PATH=%~dp0bin\MinGW\bin;%~dp0bin\Python32
del *.pyd
python .\setup.py build_ext --inplace
del .\*.c .\c_file_cache\