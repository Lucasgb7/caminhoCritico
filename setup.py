import sys
import os
from cx_Freeze import setup, Executable

includes = []
include_files = [r"C:\Users\lucas\PycharmProjects\CaminhoCritico\task1.txt",
                 r"C:\Users\lucas\PycharmProjects\CaminhoCritico\task2.txt",
                 r"C:\Users\lucas\PycharmProjects\CaminhoCritico\task3.txt"]
base = 'Win32GUI' if sys.platform == 'win32' else None


setup(name='Caminho Crítico', version='1.0', description='Algoritmo de Caminho Critico',
      options={"build_exe": {"includes": includes, "include_files": include_files}},
      executables=[Executable(r'C:\Users\lucas\PycharmProjects\CaminhoCritico\caminhoCritico.py', base=base)])