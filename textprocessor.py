import os

import pandas as pd
from string import punctuation
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.stem.snowball import DutchStemmer
from math import log, sqrt



class Textprocessor:
    # Handles all the lexical analysis and stemming.
    # contains the term weight matrix for chosen texts and settings.

    def __init__(self):
        # Sets the standard settings for the Textprocessor.
        self.documents_folder = os.path.join(os.getcwd(), "documents")
        self.language = "english"
        self.unwanted_chars = punctuation + "1234567890"
        self.enable_stopwords = False
        self.enable_stemmer = False
        self.enable_lemmatizer = True
        self.create_term_weight_matrix()
        
    def create_term_weight_matrix(self):
        # Call this function to create
        # a term weight matrix with the provided settings.
        wordcounts = {}
        for file in os.listdir(self.documents_folder):
            if not file.endswith(".txt"):   # skip file if it is not *.txt.
                continue
            wordlist = self.open_file(os.path.join(self.documents_folder,
                                                   file))
            wordlist = self.clean_words(wordlist)
            wordcounts[file] = self.count_words(wordlist)
        term_weight_matrix = self.calculate_term_weights(wordcounts)
        term_weight_matrix.to_csv(os.path.join("config", "twmatrix.csv"))
        self.term_weight_matrix = term_weight_matrix
       # self.document_vectors = self.calc_doc_vectors(self.term_weight_matrix)

    def open_file(self, path):
        # opens file and puts all words in a wordlist.
        with open(path, "r") as f:
            wordlist = f.read().split()
        return wordlist

    def clean_words(self, wordlist):
        words = self.remove_unwanted_characters(wordlist)
        words = self.remove_stopwords(words)
        words = self.lemmatize_words(words)
        words = self.stem_words(words)
        return words

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
        if self.enable_stopwords is True:
            return wordlist
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

    # def calc_doc_vectors(self, twmatrix):
    #     # Takes an dataframe object with term weights and
    #     # returns a dict with the vector lenghts of each text.
    #     vector_lengths = {}
    #     for column in twmatrix.columns:
    #         vectorcount = 0
    #         for item in twmatrix[column]:
    #             vectorcount += (item ** 2)
    #         vector_lengths[column] = sqrt(vectorcount)
    #     return vector_lengths        

    def reset_default_settings(self):
        # Can be called to reset the program to default settings.
        # Also creates a new term weight matrix (if anything was changed.)
        self.documents_folder = os.path.join(os.getcwd(), "documents")
        self.language = "english"
        self.unwanted_chars = punctuation + "1234567890"
        self.enable_stopwords = False
        self.enable_stemmer = False
        self.enable_lemmatizer = True
        self.create_term_weight_matrix()
        