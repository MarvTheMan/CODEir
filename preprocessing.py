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

def remove_stopwords(wordlist, language):
    if language == 0:
        file = "dutch"
    elif language == 1:
        file = "english"
    stopwords = get_list_from_file(os.path.join("config", "stopwords", file))
    for word in list(wordlist): # creating a copy of the list so we can modify the original
        if word in stopwords:
            wordlist.remove(word)
    return wordlist

def remove_punctuation_and_numbers(wordlist):
    punctuation = string.punctuation
    numbers = "1234567890"
    cleanlist = []
    for word in wordlist:
        newword = ""
        for char in word: 
            if char not in punctuation and char not in numbers:
                newword += char
        if newword != "":       # no empty strings in wordlist
            cleanlist.append(newword.lower())
    return cleanlist

