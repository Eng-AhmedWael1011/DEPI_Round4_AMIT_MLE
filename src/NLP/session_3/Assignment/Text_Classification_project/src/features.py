import numpy as np
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer

def create_vectorizer():

    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1,2)
    )

    return vectorizer


class Word2VecVectorizer:

    def __init__(
        self, vector_size=100,window=5,min_count=2):
        self.vector_size = vector_size
        self.window = window
        self.min_count = min_count
        self.model = None

    def fit(self, documents):

        tokenized_documents = [ doc.split() for doc in documents ]

        self.model = Word2Vec(
            sentences=tokenized_documents,
            vector_size=self.vector_size,
            window=self.window,
            min_count=self.min_count,
            workers=4
        )

    def document_vector(self, document):
        words = document.split()
        word_vectors = []

        for word in words:
            try:
                if word in self.model.wv:
                    word_vectors.append(
                        self.model.wv[word]
                    )
            except:
                print('error')
                return
        if len(word_vectors) == 0:
            return np.zeros(self.vector_size)
        
        return np.mean(
            word_vectors,
            axis=0
        )
    
    def transform(self, documents):

        return np.array([
            self.document_vector(doc)
            for doc in documents
        ])
    
    def fit_transform(self, documnets):
        self.fit(documents=documnets)
        return self.transform(documents=documnets)