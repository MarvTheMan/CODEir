import pandas as pd
from math import sqrt
import os
import re


def calc_weight_sum(twmatrix, search_terms):
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
    vectormatrix.fillna(0, inplace=True)  # replaces all NaN values with 0.
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


def calc_cosine_similarity(query, doc_weight_sum, doc_vectors):
    # Calculates the cosine similarity, returns a sorted list with text name
    # and the ranking.
    query_vector = sqrt(len(query))
    ansmatrix = []
    for doc1 in doc_weight_sum.index:
        for doc2 in doc_vectors:
            if doc1 == doc2:
                ans = doc_weight_sum[doc1]/(doc_vectors[doc1]*query_vector)
                if ans != 0:  # No results that have no similarity with query.
                    if len(doc1) > 60:  # Alter name if it's too long for GUI.
                        name = doc1[:27] + " (...) " + doc1[-27:]
                    else:
                        name = doc1
                    ansmatrix.append([doc1, name, ans])
    sorted_output = sorted(ansmatrix, key=lambda score: score[2], reverse=True)
    rank = 1
    # add a rank to the lists to show in GUI
    for item in sorted_output:
        item.append(rank)
        rank += 1
    return sorted_output


def get_text_snippet(textname, directory, query):
    # searches and parses a text snippet containing the keyword(s)
    LENGTH = 550
    HALF_LENGTH = int(LENGTH//2)
    snippet = ""
    sub_snippet_list = []
    with open(os.path.join(directory, textname), "r", encoding="utf8") as f:
        for line in f:
            for word in query:
                regex = re.compile(word, flags=re.IGNORECASE)
                match = regex.search(line)
                if match is not None:
                    start, end = match.start(), match.end()
                    if start <= HALF_LENGTH:
                        start = 0
                        prefix = ""
                    else:
                        start -= HALF_LENGTH
                        prefix = "..."
                    if len(line) - end <= HALF_LENGTH:
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
