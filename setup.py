import json
import os

# system
import sys, subprocess
# adding cwd to the system path to access variables
sys.path.insert(0, os.getcwd())
import variables

# Launches API script
if __name__ == "__main__":  


    if sys.version_info[0] < 3 or (sys.version_info[1] < 7 or sys.version_info[1] > 9):
        raise Exception("Python 3.7-3.9 is required.")
    else:
        print("Python version " + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + " is valid.")
    
    subprocess.run(['pip', 'install', '-r', os.getcwd() + variables.get_requirements_path()])
    
    try:
        import spacy
        spacy.load("en_core_web_sm")
        print("SpaCy Model 'en_core_web_sm' is installed and loaded")

    except Exception:
        print("SpaCy Model 'en_core_web_sm' is not installed")
        subprocess.call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])