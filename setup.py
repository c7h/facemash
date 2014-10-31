#!/usr/bin/python
import os, subprocess, sys

subprocess.call(["virtualenv", "venv"])

if sys.platform == 'win32':
  bin = 'Scripts'
else:
  bin = 'bin'

pip_command = [os.path.join("venv", bin, 'pip'), 'install', '-r', 'requirements.txt']
subprocess.call(pip_command)
