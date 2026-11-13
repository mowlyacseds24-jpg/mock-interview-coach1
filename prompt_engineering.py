
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(
    model="gemma3:1b",
    temperature=0.3
)

# ZERO-SHOT PROMPTING
zero_shot_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a professional technical interviewer. "
        "Generate one clear interview question."
    ),
    (
        "human",
        "Company: {company}\n"
        "Role: {role}\n"
        "Difficulty: {difficulty}"
    )
])

zero_shot_chain = zero_shot_prompt | llm | StrOutputParser()


# FEW-SHOT PROMPTING
few_shot_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a technical interviewer. "
        "Follow the style of the examples."
    ),
    (
        "human",
        """
        Example 1:
        Role: Python Developer
        Question: What is the difference between a list and tuple?

        Example 2:
        Role: Python Developer
        Question: Explain Python dictionaries with an example.

        Now generate a new question.

        Company: {company}
        Role: {role}
        Difficulty: {difficulty}
        """
    )
])

few_shot_chain = few_shot_prompt | llm | StrOutputParser()


# REFLECTION PROMPTING
reflection_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert interview feedback reviewer. "
        "Review the initial evaluation and improve its clarity. "
        "Correct inconsistencies and provide useful feedback. "
        "Do not invent information or reveal private reasoning."
    ),
    (
        "human",
        """
        Interview Question: {question}
        Candidate Answer: {answer}
        Initial Evaluation: {evaluation}

        Provide the improved evaluation.
        """
    )
])

reflection_chain = reflection_prompt | llm | StrOutputParser()


def generate_zero_shot(company, role, difficulty):
    return zero_shot_chain.invoke({
        "company": company,
        "role": role,
        "difficulty": difficulty
    })


def generate_few_shot(company, role, difficulty):
    return few_shot_chain.invoke({
        "company": company,
        "role": role,
        "difficulty": difficulty
    })


def reflect_on_evaluation(question, answer, evaluation):
    return reflection_chain.invoke({
        "question": question,
        "answer": answer,
        "evaluation": evaluation
    })
