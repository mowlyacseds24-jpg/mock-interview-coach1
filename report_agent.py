
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(
    model="gemma3:1b",
    temperature=0.3
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an interview report generator. "
        "Prepare a clear and professional candidate performance report. "
        "Include overall score out of 10, strengths, weaknesses, "
        "communication feedback and an improvement plan. "
        "Use only the information provided. Do not invent scores."
    ),
    (
        "human",
        "Company: {company}\n"
        "Role: {role}\n"
        "Question: {question}\n"
        "Candidate Answer: {answer}\n"
        "Evaluation: {evaluation}\n"
        "Coaching Feedback: {coaching}\n\n"
        "Generate the final interview report."
    )
])

report_chain = prompt | llm | StrOutputParser()


def generate_report(company, role, question, answer, evaluation, coaching):
    return report_chain.invoke({
        "company": company,
        "role": role,
        "question": question,
        "answer": answer,
        "evaluation": evaluation,
        "coaching": coaching
    })
