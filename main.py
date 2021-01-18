from standard_functions import *
from matrix import *
from textprocessor import Textprocessor
import os

if __name__ == "__main__":
    if os.path.exists(os.path.join("config", "twmatrix.csv")):
        print("Found a term weight matrix! Reading it in...")
    else:
        print("Term weight matrix was not found. Creating one with the provided files...")
        wordcounts = {}
        tp = Textprocessor()
        for file in os.listdir("documents"):
            wordlist = get_list_from_file(os.path.join("documents", file))
            wordcounts[file] = tp.create_clean_wordcount(wordlist)
        freq_matrix = create_freq_matrix(wordcounts)
        term_weight_matrix = create_term_weight_matrix(freq_matrix)
        term_weight_matrix.to_csv(os.path.join("config", "twmatrix.csv"))
        print("Saved term weight matrix for next startup.")
