import pandas as pd
from math import sqrt
import os
import re

def calc_sum_of_weights(twmatrix, search_terms):
    # Creates a dataframe with the sum of weights for all terms
    # and documents.
    vectormatrix = pd.DataFrame(index=twmatrix.index)
    results_exist = False
    for term in search_terms: 
        for word in twmatrix.index:
            if term == word:
                vectormatrix.at[word, "query"] = 1
                results_exist = True
    if results_exist is False:
        return None
    vectormatrix.fillna(0, inplace=True) # replaces all NaN values with 0.
    dot_product_matrix = twmatrix.multiply(vectormatrix["query"], axis=0)
    # uses Pandas .sum() method to quicky get the sum per column.
    weightsum = dot_product_matrix.sum() 
    return weightsum

def calc_doc_vectors(twmatrix):
    # Calculates the document vectors, returns a dict with 
    # name of the document as key.
    vector_lengths = {}
    for column in twmatrix.columns:
        vectorcount = 0
        for item in twmatrix[column]:
            vectorcount += (item ** 2)
        vector_lengths[column] = sqrt(vectorcount)
    return vector_lengths

def calc_cosine_similarity(query, document_weight_sum, document_vectors):
    # Calculates the cosine similarity, returns a sorted list with text name
    # and the ranking.
    query_vector = sqrt(len(query))
    ansmatrix = []
    for doc1 in document_weight_sum.index:
        for doc2 in document_vectors:
            if doc1 == doc2:
                ans = document_weight_sum[doc1]/(document_vectors[doc1]*query_vector)
                if ans != 0 and len(ansmatrix) <= 4 : # not adding results that have zero similarity with query and also only adding the first five results
                    if len(doc1) > 60: # alter name if the lenght is too long for our GUI
                        name = doc1[:27] + " (...) " + doc1[-27:]
                    else:
                        name = doc1
                    ansmatrix.append([doc1, name, ans])
    sorted_output = sorted(ansmatrix, key=lambda score : score[1], reverse=True)
    return sorted_output

def get_text_snippet(textname, directory, query):
    # searches and parses a text snippet containing the keyword(s) TODO: tidy up so that not only last snippet is shown.
    LENGTH = 550
    HALF_LENGTH = int(LENGTH//2)
    snippet = ""
    sub_snippet_list = []
    with open(os.path.join(directory, textname), "r", encoding="utf8") as f:    
        for line in f:
            for word in query:
                regex = re.compile(word, flags=re.IGNORECASE) # added flag to match upper and lowercase.
                match = regex.search(line)
                if match != None:
                    start, end = match.start(), match.end()
                    if start <= HALF_LENGTH:
                        start = 0
                        prefix = ""
                    else:
                        start -= HALF_LENGTH
                        prefix = "..."
                    if len(line) -end <= HALF_LENGTH:
                        end = len(line)
                        suffix = ""
                    else:
                        end += HALF_LENGTH
                        suffix = "..."
                    sub_snippet = f"{prefix}{line[start:end]}{suffix}"
                    if len(snippet + sub_snippet) < LENGTH:
                        if sub_snippet not in sub_snippet_list:
                            snippet += sub_snippet
                            sub_snippet_list.append(sub_snippet)
    return snippet