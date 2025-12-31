import math

class BM25:
    def __init__(self, documents, k1=1.5, b=0.75):
        self.documents = documents
        self.k1 = k1
        self.b = b
        self.N = len(documents)

        self.doc_lengths = []
        self.avgdl = 0
        self.term_freqs = []
        self.doc_freqs = {}

        self._build_index()

    def _build_index(self):
        total_length = 0

        for doc in self.documents:
            tokens = doc.lower().split()
            total_length += len(tokens)
            self.doc_lengths.append(len(tokens))

            tf = {}
            for token in tokens:
                tf[token] = tf.get(token, 0) + 1
            self.term_freqs.append(tf)

            for token in tf.keys():
                self.doc_freqs[token] = self.doc_freqs.get(token, 0) + 1

        self.avgdl = total_length / self.N

    def _idf(self, term):
        df = self.doc_freqs.get(term, 0)
        if df == 0:
            return 0
        return math.log(self.N / df)

    def score(self, query, index):
        score = 0
        doc_tf = self.term_freqs[index]
        doc_len = self.doc_lengths[index]

        for term in query.lower().split():
            if term not in doc_tf:
                continue

            tf = doc_tf[term]
            idf = self._idf(term)

            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)

            score += idf * (numerator / denominator)

        return score

    def rank(self, query):
        scores = []

        for i in range(self.N):
            s = self.score(query, i)
            scores.append((self.documents[i], s))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores
