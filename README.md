
# Company-Smart Mock Interview Coach

## Project Overview
An AI-powered mock interview application that helps candidates
prepare for technical interviews based on their selected company,
job role and difficulty level.

## Features
- AI-generated interview questions
- Five-question interview sessions
- Automated answer evaluation
- AI-powered coaching feedback
- Reflection-based evaluation improvement
- Interview performance report
- Downloadable interview report
- Semantic question retrieval using ChromaDB

## Technologies Used
- Python
- Streamlit
- Ollama
- Gemma 3:1b
- LangChain
- ChromaDB
- Nomic Embeddings

## Project Structure
- app.py - Streamlit frontend
- interviewer.py - Question generation
- evaluator.py - Answer evaluation
- coach.py - Coaching feedback
- report_agent.py - Final report generation
- router.py - Intent routing
- rag_engine.py - Retrieval system
- prompt_engineering.py - Prompting techniques
- questions.json - Sample interview question dataset

## How to Run

1. Install Python.
2. Install Ollama and download the required models.
3. Install dependencies:

   pip install -r requirements.txt

4. Run the application:

   streamlit run app.py

## Dataset
The project uses an illustrative sample question dataset.
The sample questions are not verified historical company
interview questions.

## Project Objective
To demonstrate the use of Large Language Models, prompt
engineering, retrieval-augmented generation and interactive
AI applications for interview preparation.
