from standard_functions import *
from matrix import *
from textprocessor import Textprocessor
import os

documents = os.listdir("documents") #this variable can be set to other folders on the machine to search them.

if __name__ == "__main__":
    if os.path.exists(os.path.join("config", "twmatrix.csv")):
        print("Found an existing term weight matrix!")
        term_weight_matrix = get_twmatrix_from_csv()
    else:
        print("Term weight matrix was not found. Creating one for the provided documents...")
        wordcounts = {}
        tp = Textprocessor()
        for file in documents:
            if not file.endswith(".txt"):
                print(f"{file} is not a textfile! Skipping it!")
                continue
            wordlist = get_list_from_file(os.path.join("documents", file))
            wordcounts[file] = tp.create_clean_wordcount(wordlist)
        freq_matrix = create_freq_matrix(wordcounts)
        term_weight_matrix = create_term_weight_matrix(freq_matrix)
        term_weight_matrix.to_csv(os.path.join("config", "twmatrix.csv"))
        print("Saved term weight matrix for next startup.")
