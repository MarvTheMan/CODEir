import os
from string import punctuation
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.stem.snowball import DutchStemmer
import pandas as pd
from math import log


class Textprocessor:
    # Handles all the lexical analysis and stemming.

    def __init__(self):
        # Sets the standard settings for the Textprocessor.
        self.documents_folder = os.path.join(os.getcwd(), "documents")
        self.language = "english"
        self.unwanted_chars = punctuation + "1234567890"
        self.enable_stemmer = False
        self.enable_lemmatizer = True

    def create_term_weight_matrix(self):
        # Call this function to create
        # a term weight matrix with the provided settings.
        wordcounts = {}
        for file in os.listdir(self.documents_folder):
            if not file.endswith(".txt"):   # skip file if it is not *.txt.
                continue
            wordlist = self.open_file(os.path.join(self.documents_folder,
                                                   file))
            wordlist = self.remove_unwanted_characters(wordlist)
            wordlist = self.remove_stopwords(wordlist)
            wordlist = self.lemmatize_words(wordlist)
            wordlist = self.stem_words(wordlist)
            wordcounts[file] = self.count_words(wordlist)
        term_weight_matrix = self.calculate_term_weights(wordcounts)
        term_weight_matrix.to_csv(os.path.join("config", "twmatrix.csv"))
        self.term_weight_matrix = term_weight_matrix
        print(self.term_weight_matrix.head())

    def open_file(self, path):
        # opens file and puts all words in a wordlist.
        with open(path, "r") as f:
            wordlist = f.read().split()
        return wordlist

    def remove_unwanted_characters(self, wordlist):
        # Takes a wordlist and removes all unwanted chars from the words.
        cleanlist = []
        for word in wordlist:
            newword = ""
            for char in word:
                if char not in self.unwanted_chars:
                    newword += char
            if newword != "":       # no empty strings in wordlist
                cleanlist.append(newword.lower())
        return cleanlist

    def remove_stopwords(self, wordlist):
        # Takes a wordlist and removes all stopwords from that list.
        stopwords = self.open_file(os.path.join("config",
                                                "stopwords",
                                                self.language))
        for word in list(wordlist):
            if word in stopwords:
                wordlist.remove(word)
        return wordlist

    def lemmatize_words(self, wordlist):
        # Morphological analysis of words.
        # Works for English only, checks if enabled.
        if self.language != "english" or self.enable_lemmatizer is not True:
            return wordlist
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = []
        for word in wordlist:
            lemmatized_words.append(lemmatizer.lemmatize(word))
        return lemmatized_words

    def stem_words(self, wordlist):
        # checks if stemming is enabled and stems words in wordlist.
        if self.enable_stemmer is not True:
            return wordlist
        if self.language == "english":
            stemmer = PorterStemmer()
        elif self.language == "dutch":
            stemmer = DutchStemmer()
        stemmed_words = []
        for word in wordlist:
            stemmed_words.append(stemmer.stem(word))
        return stemmed_words

    def count_words(self, wordlist):
        # Takes a wordlist and returns the wordcount.
        wordcount = {}
        for word in wordlist:
            if word in wordcount:
                wordcount[word] += 1
            else:
                wordcount[word] = 1
        return wordcount

    def calculate_term_weights(self, wordcounts):
        # takes a wordcounts dict and returns a term weight matrix.
        freq_matrix = pd.DataFrame(wordcounts)
        freq_matrix.fillna(0, inplace=True)  # replaces all NaN values with 0.
        N = len(freq_matrix.columns)
        idf_list = []
        for index, item in freq_matrix.iterrows():
            df = 0
            for text in freq_matrix.columns:
                if item[text] != 0.0:
                    df += 1
            idf = log((N/df), 2)
            idf_list.append(idf)
        term_weight_matrix = freq_matrix.mul(idf_list, axis=0)
        return term_weight_matrix

    def reset_default_settings(self):
        self.documents_folder = os.path.join(os.getcwd(), "documents")
        self.language = "english"
        self.unwanted_chars = punctuation + "1234567890"
        self.enable_stemmer = False
        self.enable_lemmatizer = True
        self.create_term_weight_matrix()
        