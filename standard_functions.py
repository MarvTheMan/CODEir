import os
import pandas as pd

def get_list_from_file(path):
    with open(path, "r") as f:
        wordlist = f.read().split()
    return wordlist
    
def get_twmatrix_from_csv():
    matrix = pd.read_csv(os.path.join("config", "twmatrix.csv"))
    return matrix
