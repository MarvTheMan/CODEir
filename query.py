

class Query:

    def __init__(self, search_terms, twmatrix):
        self.search_terms = search_terms
        self.results = self.rank_output()
    
    def calculate_document_vectors(self, twmatrix):
    # Takes an dataframe object with term weights and
    # returns a dict with the vector lenghts of each text.
    vector_lengths = {}
    for column in twmatrix.columns:
        vectorcount = 0
        for item in twmatrix[column]:
            vectorcount += (item ** 2)
        vector_lengths[column] = sqrt(vectorcount)
    return vector_lengths


    def rank_output(self):
        pass