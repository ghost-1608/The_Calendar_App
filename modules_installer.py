"""A semi-automatic installer to install the required modules needed to run calendar-main.py"""

try:
    import subprocess
    import sys
except ModuleNotFoundError:
    print('[Fatal Error!]: integral modules missing from the python installation!\n')
    input('Press enter to exit... ')
    exit(1)

try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'modules.txt'])
except subprocess.CalledProcessError:
    print('Error!\nThere was a problem trying to install the required modules.')
    print('Make sure that modules_installer.py was run with administrator privileges.')
    print('If the problem persists, please install the modules given in modules.txt manually.\n')

input('Press enter to exit... ')
sys.exit()
