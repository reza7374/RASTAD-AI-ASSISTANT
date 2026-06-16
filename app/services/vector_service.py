# app/services/vector_service.py

import os
from typing import List

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorService:
    """
    VectorService handles:
    - loading knowledge base files
    - creating embeddings
    - building FAISS index
    - semantic search
    """

    def __init__(self, knowledge_path: str = "knowledge_base"):
        self.knowledge_path = knowledge_path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.documents: List[str] = []
        self.index = None

        self._load_documents()
        self._build_index()

    def _load_documents(self):
        """
        Load all text files from knowledge_base directory
        """
        docs = []

        for file in os.listdir(self.knowledge_path):
            if file.endswith(".txt"):
                path = os.path.join(self.knowledge_path, file)

                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()

                    docs.append(text)

        self.documents = docs

    def _build_index(self):
        """
        Create embeddings and build FAISS index
        """

        if not self.documents:
            return

        embeddings = self.model.encode(self.documents)

        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def search(self, query: str, top_k: int = 3) -> List[str]:
        """
        Perform semantic search in the knowledge base
        """

        if self.index is None:
            return []

        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])

        return results


# Singleton instance
vector_service = VectorService()
