import os
import string
from standard_functions import *

class Textprocessor:
    #handles all the lexical analysis and stemming
    def __init__(self):
        self.language = "dutch"
        self.unwanted_chars = string.punctuation + "1234567890"

    def create_clean_wordcount(self, wordlist):
        wordlist = self.remove_unwanted_characters(wordlist)
        wordlist = self.remove_stopwords(wordlist)
        wordcount = self.get_wordcount(wordlist)
        return wordcount

    def get_wordcount(self, wordlist):
        wordcount = {}
        for word in wordlist:
            if word in wordcount:
                wordcount[word] += 1
            else:
                wordcount[word] = 1
        return wordcount

    def remove_stopwords(self, wordlist):
        stopwords = get_list_from_file(os.path.join("config", "stopwords", self.language))
        for word in list(wordlist): # creating a copy of the list so we can modify the original
            if word in stopwords:
                wordlist.remove(word)
        return wordlist

    def remove_unwanted_characters(self, wordlist):
        cleanlist = []
        for word in wordlist:
            newword = ""
            for char in word: 
                if char not in self.unwanted_chars:
                    newword += char
            if newword != "":       # no empty strings in wordlist
                cleanlist.append(newword.lower())
        return cleanlist


