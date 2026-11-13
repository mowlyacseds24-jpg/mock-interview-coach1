
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from rag_engine import retrieve_questions
from router import decide_route


llm = ChatOllama(
    model="gemma3:1b",
    temperature=0.4
)


# ---------- INTERVIEW QUESTION PROMPT ----------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a professional company interviewer.

        Your task is to generate exactly ONE clear interview question.

        Rules:
        - Match the selected company, role and difficulty.
        - Use retrieved questions as reference material.
        - Do not copy reference questions word for word.
        - Do not repeat any previously asked questions.
        - Ask a realistic technical interview question.
        - Do not provide the answer.
        """
    ),

    (
        "human",
        """Company: {company}
        Role: {role}
        Difficulty: {difficulty}

        Reference questions:
        {context}

        Previously asked questions:
        {previous_questions}

        Generate one new suitable interview question.
        """
    )
])


interviewer_chain = prompt | llm | StrOutputParser()


# ---------- GENERATE INTERVIEW QUESTION ----------
def generate_question(
    company,
    role,
    difficulty,
    previous_questions=None
):

    previous_questions = previous_questions or []

    request = "Generate a company-specific interview question."

    # Decide whether retrieval is required
    route = decide_route(
        company,
        role,
        difficulty,
        request
    )

    # Retrieve reference questions
    if route == "RETRIEVE":

        retrieved = retrieve_questions(
            company,
            role,
            difficulty
        )

        context = "\n".join(retrieved)

    else:
        context = "No database retrieval required."

    # Generate one new question
    return interviewer_chain.invoke({
        "company": company,
        "role": role,
        "difficulty": difficulty,
        "context": context,
        "previous_questions": "\n".join(previous_questions)
    })
