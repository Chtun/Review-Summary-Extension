import json
import os

# global variables - adding cwd to the system path to access variables
import sys
sys.path.insert(0, os.getcwd())
import variables


# Launches API script
if __name__ == "__main__":
    os.system('python ' + os.getcwd() + variables.get_api_script_path())

