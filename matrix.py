import numpy as np
import pandas as pd

def create_freq_matrix(wordcounts):
    df = pd.DataFrame(wordcounts)
    df.fillna(0, inplace=True)      # replaces all NaN values with 0.

def create_term_weight_matrix(freq_matrix):
    means = freq_matrix.mean(axis = 1)