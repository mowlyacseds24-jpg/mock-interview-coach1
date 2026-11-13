
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(
    model="gemma3:1b",
    temperature=0.2
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a professional technical interview evaluator. "
        "Evaluate the candidate's answer based on correctness, "
        "depth and communication. Give a score out of 10. "
        "Explain the score briefly and identify missing points."
    ),
    (
        "human",
        "Company: {company}\n"
        "Role: {role}\n"
        "Question: {question}\n"
        "Candidate Answer: {answer}\n\n"
        "Provide score, strengths and areas to improve."
    )
])

evaluator_chain = prompt | llm | StrOutputParser()


def evaluate_answer(company, role, question, answer):
    return evaluator_chain.invoke({
        "company": company,
        "role": role,
        "question": question,
        "answer": answer
    })
