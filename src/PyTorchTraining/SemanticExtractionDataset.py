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
from torch.utils.data import Dataset, Dataloader
from torchtext import 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if __name__ == "__main__":
    
    
    
    print("Beginning Training.")


class FaceLandmarksDataset(Dataset):
    # Semantic Information Extraction custom dataset.

    def __init__(self, review_data_path, extracted_words_data_path, transform=None):
        # Args:
        #     review_data_path (string): Path to the csv file with array of set of tuples for reviews;
        #       Each tuple contains string value, word vector representation, Part-Of-Speech tag, and syntactic dependency;
        #       EX: ('word', meaning_val (np array), POS_Val (int), Dependency_Val (int)).
        #     extracted_words_data_path (string): Path to csv file with array of set of tuples for extracted words.
        #     transform (callable, optional): Optional transform to be applied on a sample.


        self.review_data = pd.read_csv(review_data_path)
        self.extracted_words_data = extracted_words_data_path
        self.transform = transform

    def __len__(self):
        return len(self.landmarks_frame)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = os.path.join(self.root_dir,
                                self.landmarks_frame.iloc[idx, 0])
        image = io.imread(img_name)
        landmarks = self.landmarks_frame.iloc[idx, 1:]
        landmarks = np.array([landmarks])
        landmarks = landmarks.astype('float').reshape(-1, 2)
        sample = {'image': image, 'landmarks': landmarks}

        if self.transform:
            sample = self.transform(sample)

        return sample
