import json
import os

# system
import sys, subprocess
# adding cwd to the system path to access variables
sys.path.insert(0, os.getcwd())
import variables


# Launches API script
if __name__ == "__main__":
    subprocess.call([sys.executable, os.getcwd() + variables.get_api_script_path()])

