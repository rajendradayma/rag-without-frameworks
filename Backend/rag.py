from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class InMemoryRAG:
    def __init__(self):
        self.chunks = []
        self.chunk_embeddings = []
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def add_chunks(self, chunks):
        for c in chunks:
            self.chunks.append(c)
            emb = self.model.encode([c])[0]
            self.chunk_embeddings.append(emb)

    def retrieve(self, query, top_k=3):
        if not self.chunks:
            return []
        query_emb = self.model.encode([query])[0]
        similarities = cosine_similarity(
            [query_emb], self.chunk_embeddings
        )[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [self.chunks[i] for i in top_indices]
