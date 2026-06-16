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

    def _load_documents(self) -> None:
        """
        Load all text files from knowledge base directory.
        """
        docs = []

        if not os.path.exists(self.knowledge_path):
            self.documents = []
            return

        for file_name in os.listdir(self.knowledge_path):
            if file_name.endswith(".txt"):
                file_path = os.path.join(self.knowledge_path, file_name)

                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read().strip()

                    if text:
                        docs.append(text)

        self.documents = docs

    def _build_index(self) -> None:
        """
        Create embeddings and build FAISS index.
        """
        if not self.documents:
            self.index = None
            return

        embeddings = self.model.encode(self.documents)
        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def search(self, query: str, top_k: int = 3) -> List[str]:
        """
        Perform semantic search in the knowledge base.
        """
        if self.index is None or not query.strip():
            return []

        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        top_k = min(top_k, len(self.documents))

        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.documents):
                results.append(self.documents[idx])

        return results


vector_service = VectorService()
