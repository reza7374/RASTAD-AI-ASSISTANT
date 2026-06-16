from app.services.vector_service import vector_service


class KnowledgeService:

    def retrieve(self, query: str, top_k: int = 3):

        return vector_service.search(query=query, top_k=top_k)

    def build_context(self, query: str, top_k: int = 3):

        results = self.retrieve(query=query, top_k=top_k)

        context_parts = []

        for r in results:
            context_parts.append(r["text"])

        return "\n\n".join(context_parts)


knowledge_service = KnowledgeService()
