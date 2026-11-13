
def decide_route(company, role, difficulty, request):

    request = request.lower().strip()

    # Requests that need information from the question bank
    retrieval_keywords = [
        "interview question",
        "company-specific",
        "company specific",
        "mock interview",
        "technical round",
        "question bank",
        "previous questions",
        "similar interview questions",
        "retrieve questions"
    ]

    # General requests that can go directly to the LLM
    direct_keywords = [
        "explain",
        "define",
        "what is",
        "what are",
        "write code",
        "give an example",
        "general explanation"
    ]

    if any(word in request for word in retrieval_keywords):
        return "RETRIEVE"

    if any(word in request for word in direct_keywords):
        return "DIRECT"

    return "DIRECT"
