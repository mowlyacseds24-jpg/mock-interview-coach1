
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(
    model="gemma3:1b",
    temperature=0.4
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a friendly and professional interview coach. "
        "Analyse the candidate's answer and evaluation. "
        "Give practical suggestions to improve. "
        "Explain what was missing and provide a short example "
        "of a stronger answer. Keep the language simple."
    ),
    (
        "human",
        "Company: {company}\n"
        "Role: {role}\n"
        "Question: {question}\n"
        "Candidate Answer: {answer}\n"
        "Evaluation: {evaluation}\n\n"
        "Provide personalised coaching feedback."
    )
])

coach_chain = prompt | llm | StrOutputParser()


def generate_coaching(company, role, question, answer, evaluation):
    return coach_chain.invoke({
        "company": company,
        "role": role,
        "question": question,
        "answer": answer,
        "evaluation": evaluation
    })
