import shutil
import os

dev = os.path.abspath('src\\logbook')
venv = os.path.abspath('venv\\Lib\\site-packages\\logbook')
if os.path.exists(venv) is True:
  shutil.rmtree(venv)
shutil.copytree(dev, venv)
print('Release implemented.')
