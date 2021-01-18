import pandas as pd
from math import log

def create_freq_matrix(wordcounts):
    df = pd.DataFrame(wordcounts)
    df.fillna(0, inplace=True)      # replaces all NaN values with 0.
    return df

def create_term_weight_matrix(freq_matrix):
    N = len(freq_matrix.columns)
    idf_list = []
    for word, row in freq_matrix.iterrows():
        df = 0
        for text in freq_matrix.columns:
            if row[text] != 0.0:
                df+=1
        idf = log((N/df), 2)
        idf_list.append(idf)
    term_weight_matrix = freq_matrix.mul(idf_list, axis=0)
    return term_weight_matrix