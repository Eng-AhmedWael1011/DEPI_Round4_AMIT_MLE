# NLP Libraries
from nltk.corpus import stopwords
import spacy

# cleaning texts libraries
import re
import emoji


nlp = spacy.load('en_core_web_sm')
stop_words = set(stopwords.words('english'))

negation_words = {'not' , 'no' , 'never'}
stop_words = stop_words - negation_words


def clean_text(text):
    # lower casing
    text = text.lower()

    # remove HTML
    text = re.sub(r'<.*?>' , '' , text)

    # remove urls
    text = re.sub(r'http\S+|www\s+' , '' , text)

    # convert emojis
    text = emoji.demojize(text)

    # remove puntuation * special chars
    text = re.sub(r'[^a-zA-Z\s]' , '' , text)

    # tokenization with spacy
    doc = nlp(text)

    tokens = []

    for token in doc:

        if (
            token.text not in stop_words and 
            not token.is_punct and
            not token.like_num and
            len(token.text) > 2
        ):
            tokens.append(token.lemma_)

    return " ".join(tokens)

