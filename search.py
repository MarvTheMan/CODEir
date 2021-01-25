import pandas as pd
from textprocessor import Textprocessor
from math import sqrt
import csv
import os


def calculate_vector_lengths(twmatrix):
    # Takes an dataframe object with term weights and
    # returns a dict with the vector lenghts of each text.
    vector_lengths = {}
    for column in twmatrix.columns:
        vectorcount = 0
        for item in twmatrix[column]:
            vectorcount += (item ** 2)
        vector_lengths[column] = sqrt(vectorcount)
    return vector_lengths

# def update_matrix_with_query(twmatrix, query=["three", "mies"]):
#     for index, item in freq_matrix.iterrows():
#         for word in query:
#             if word == index:

if __name__ == "__main__":
    data = pd.read_csv(os.path.join("config", "recepten.csv"))
    print(data.head())
    #tp = Textprocessor()
   # tp.create_term_weight_matrix()
   # calculate_vector_lengths(tp.term_weight_matrix)
    #update_matrix_with_query(tp.term_weight_matrix)
