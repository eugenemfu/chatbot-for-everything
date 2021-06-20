from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from pymystem3 import Mystem
from string import punctuation

from typing import List


def lemmatize(msg: str) -> List[str]:
    msg = msg.lower()
    tokens = word_tokenize(msg)
    # words without punctuation
    filtered_tokens = [w for w in tokens if not w.lower() in punctuation]
    # lemmatizer = WordNetLemmatizer()
    lemmatizer = Mystem()
    # words in infinitive form
    lemmas = [str(lemmatizer.lemmatize(w)[0]) for w in filtered_tokens]
    return lemmas


def lemmatize_list(words: List) -> List:
    # lemmatizer = WordNetLemmatizer()
    lemmatizer = Mystem()
    return [str(lemmatizer.lemmatize(w.lower())[0]) for w in words]
