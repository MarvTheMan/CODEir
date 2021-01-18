import os

def get_list_from_file(path):
    with open(path, "r") as f:
        wordlist = f.read().split()
    return wordlist

