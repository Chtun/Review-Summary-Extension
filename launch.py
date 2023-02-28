import json
import os

# global variables - adding cwd to the system path to access variables
import sys
sys.path.insert(0, os.getcwd())
import variables


# Launches API script
if __name__ == "__main__":
    try:
       import en_core_web_ms
    except ModuleNotFoundError:
        print("module 'en_core_web_sm' is not installed")
        os.system('python -m spacy download en_core_web_sm')   
    

    os.system('python ' + os.getcwd() + variables.get_api_script_path())

