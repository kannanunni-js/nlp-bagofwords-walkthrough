from sklearn.feature_extraction.text import CountVectorizer

def load_corpus_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]

def get_bow_representation(corpus, binary=False):
    vectorizer = CountVectorizer(lowercase=True, binary=binary)  # binary=True:: This calculates the binary presnce version
    bow_matrix = vectorizer.fit_transform(corpus)
    return bow_matrix.toarray(), vectorizer.get_feature_names_out()

def get_vector_for_sentence(sentence, vectorizer):
    return vectorizer.transform([sentence]).toarray()[0]