from standard_functions import *
from preprocessing import *
from matrix import *
from textprocessor import Textprocessor
import os

if __name__ == "__main__":
    wordcounts = {}
    tp = Textprocessor()
    for file in os.listdir("documents"):
        wordlist = get_list_from_file(os.path.join("documents", file))
        wordcounts[file] = tp.create_clean_wordcount(wordlist)
    create_freq_matrix(wordcounts)