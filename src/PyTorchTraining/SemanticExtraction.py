#Import OS and System Modules
import os,sys

# import json to read review contents json file
import json

# import text tokenization model
import spacy

# global variables - adding cwd to the system path to access variables
sys.path.insert(0, os.getcwd())
import variables

# Import PyTorch Framework
import torch
from torch.utils.data import Dataset
from torchtext
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    
    
    print("Beginning Training.")

