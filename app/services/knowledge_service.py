# app/services/knowledge_service.py

from typing import List

from app.services.vector_service import vector_service


class KnowledgeService:
    """
    Service responsible for retrieving relevant knowledge
    from the knowledge base using vector search.
    """

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """
        Retrieve relevant knowledge chunks for a user query
        """

        results = vector_service.search(query=query, top_k=top_k)

        return results

    def build_context(self, query: str, top_k: int = 3) -> str:
        """
        Build context string for LLM from retrieved knowledge
        """

        knowledge_chunks = self.retrieve(query=query, top_k=top_k)

        if not knowledge_chunks:
            return ""

        context = "\n\n".join(knowledge_chunks)

        return context


# Singleton instance
knowledge_service = KnowledgeService()
