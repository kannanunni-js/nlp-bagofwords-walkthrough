from nltk.tokenize import word_tokenize
import string

def load_corpus_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]

def preprocess(text):
    return text.translate(str.maketrans('', '', string.punctuation)).lower()

def get_bow_representation(corpus, frequency=True):
    tokens = word_tokenize(" ".join(preprocess(sentence) for sentence in corpus))
    vocabulary = sorted(set(word for word in tokens if word.isalnum()))

    bow_vectors = []

    for sentence in corpus:
        sentence_tokens = word_tokenize(preprocess(sentence))
        vector = [sentence_tokens.count(word) if frequency else int(word in sentence_tokens) for word in vocabulary]
        bow_vectors.append(vector)

    return bow_vectors, vocabulary

def get_vector_for_sentence_scratch(sentence, vocabulary, frequency=True):
    tokens = word_tokenize(preprocess(sentence))
    return [tokens.count(word) if frequency else int(word in tokens) for word in vocabulary]
