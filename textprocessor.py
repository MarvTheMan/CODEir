import os
from string import punctuation
from standard_functions import *
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.stem.snowball import DutchStemmer


class Textprocessor:
    # Handles all the lexical analysis and stemming.
    def __init__(self):
        self.language = "dutch"
        self.unwanted_chars = punctuation + "1234567890"
        self.hard_processing = False      # Can be set to True for heavier stemming, results can be non-linguistic!

    def create_clean_wordcount(self, wordlist):
        # Creates a standard cleaned wordlist.
        wordlist = self.remove_unwanted_characters(wordlist)
        wordlist = self.remove_stopwords(wordlist)
        wordlist = self.stem_words(wordlist)
        wordcount = self.get_wordcount(wordlist)
        return wordcount

    def get_wordcount(self, wordlist):
        # Takes a wordlist and returns the wordcount.
        wordcount = {}
        for word in wordlist:
            if word in wordcount:
                wordcount[word] += 1
            else:
                wordcount[word] = 1
        return wordcount

    def remove_stopwords(self, wordlist):
        # Takes a wordlist and removes all stopwords from that list.
        stopwords = get_list_from_file(os.path.join("config", "stopwords", self.language))
        for word in list(wordlist): # creating a copy of the list so we can modify the original
            if word in stopwords:
                wordlist.remove(word)
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

    def stem_words(self, wordlist):
        # checks which stemmer to use and stems words in wordlist
        if self.language == "english":
            if self.hard_processing != True:
                stemmer = PorterStemmer()
            else:
                stemmer = LancasterStemmer()
        elif self.language == "dutch":
            stemmer = DutchStemmer()
        else:
            print(f"No stemmer for {self.language} installed! Proceeding...")
            return wordlist
        stemmed_words = []
        for word in wordlist:
            stemmed_words.append(stemmer.stem(word))
        return stemmed_words

    def lemmatize_words(self, wordlist):
        # morphological analysis of words (usually preferred over stemming). works for English only.
        if self.language != "english":
            return wordlist
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = []
        for word in wordlist:
            lemmatized_words.append(lemmatizer.lemmatize(word))
        return lemmatized_words
