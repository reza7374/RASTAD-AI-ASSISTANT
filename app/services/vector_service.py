import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.services.chunk_service import chunk_service


class VectorService:

    def __init__(self):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.texts = []
        self.metadata = []

        self.index = None

        self.load_knowledge()

    def load_knowledge(self):

        base_path = "knowledge_base"

        for file_name in os.listdir(base_path):

            if not file_name.endswith(".txt"):
                continue

            file_path = os.path.join(base_path, file_name)

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = chunk_service.chunk_text(text)

            for i, chunk in enumerate(chunks):

                self.texts.append(chunk)

                self.metadata.append(
                    {
                        "source": file_name,
                        "chunk_id": i,
                    }
                )

        embeddings = self.model.encode(self.texts)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(np.array(embeddings))

    def search(self, query: str, top_k: int = 3):

        query_embedding = self.model.encode([query])

        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for idx in indices[0]:

            results.append(
                {
                    "text": self.texts[idx],
                    "metadata": self.metadata[idx],
                }
            )

        return results


vector_service = VectorService()
