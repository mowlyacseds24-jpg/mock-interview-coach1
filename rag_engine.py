
import json
from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

# Load embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Load sample question dataset
data_path = Path(__file__).parent / "questions.json"

with open(data_path, "r", encoding="utf-8") as file:
    questions = json.load(file)

# Convert questions into documents
documents = []

for item in questions:
    documents.append(
        Document(
            page_content=item["question"],
            metadata={
                "company": item["company"],
                "role": item["role"],
                "difficulty": item["difficulty"]
            }
        )
    )

# Connect to persistent ChromaDB
vectorstore = Chroma(
    collection_name="interview_questions",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

# Add documents if database is empty
if vectorstore._collection.count() == 0:
    vectorstore.add_documents(documents)


def retrieve_questions(
    company,
    role,
    difficulty,
    topic=""
):

    search_query = (
        f"{company} {role} {difficulty} "
        f"technical interview {topic}"
    )

    # Retrieve semantically similar questions
    results = vectorstore.similarity_search(
        search_query,
        k=10
    )

    # Match role and difficulty
    matching = [
        doc for doc in results
        if doc.metadata.get("role") == role
        and doc.metadata.get("difficulty") == difficulty
    ]

    # Fallback: match role only
    if not matching:
        matching = [
            doc for doc in results
            if doc.metadata.get("role") == role
        ]

    # Prefer selected company
    company_matches = [
        doc for doc in matching
        if doc.metadata.get("company") == company
    ]

    if company_matches:
        matching = company_matches

    # Return up to three relevant questions
    return [
        doc.page_content
        for doc in matching[:3]
    ]
