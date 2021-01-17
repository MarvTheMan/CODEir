import pandas as pd
import numpy as np
import os
import string
from standard_functions import *

def get_wordcount(wordlist):
    wordcount = {}
        for word in wordlist:
            if word in wordcount:
                wordcount[word] += 1
            else:
                wordcount[word] = 1
    return wordcount

def clear_wordlist(wordlist):
    clearlist = []
    for word in wordlist:
        

wordcounts = {}
for file in os.listdir("documents"):
    wordlist = get_list_from_file(file)
    wordcount = get_wordcount(wordlist)
    wordcounts[file] = wordcount    # TODO: make sure that files do not have the same name
    
