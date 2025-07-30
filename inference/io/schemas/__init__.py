from enum import Enum

class BoWMethod(str, Enum):
    vectorizer = "vectorizer"
    scratch = "scratch"
