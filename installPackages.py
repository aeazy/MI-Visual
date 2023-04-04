import subprocess
import sys


def install_packages():
    # install numpy
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'numpy'])

    # install pandas
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas'])

    # install plotly.express 
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'plotly.express'])

    # install statsmodels
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'statsmodels'])

    # install dash & extensions
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'dash'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'dash_extensions'])
    