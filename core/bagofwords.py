from nltk.tokenize import word_tokenize

def get_bow_representation(corpus, frequency=True):
    tokens = word_tokenize(" ".join(corpus).lower())
    vocabulary = sorted(set(word for word in tokens if word.isalnum()))

    bow_vectors = []

    for sentence in corpus:
        sentence_tokens = word_tokenize(sentence.lower())
        vector = []
        for word in vocabulary:
            if frequency:
                count = sentence_tokens.count(word)
            else:
                count = 1 if word in sentence_tokens else 0
            vector.append(count)
        bow_vectors.append(vector)

    return bow_vectors, vocabulary

def get_vector_for_sentence(sentence, vocabulary, frequency=True):
    tokens = word_tokenize(sentence.lower())
    vector = []
    for word in vocabulary:
        if frequency:
            count = tokens.count(word)
        else:
            count = 1 if word in tokens else 0
        vector.append(count)
    return vector