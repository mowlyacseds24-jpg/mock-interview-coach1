
import streamlit as st
import re

from interviewer import generate_question
from evaluator import evaluate_answer
from coach import generate_coaching
from report_agent import generate_report
from prompt_engineering import reflect_on_evaluation


TOTAL_QUESTIONS = 5


st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)


# ---------- DESIGN ----------
st.markdown("""
<style>
.stApp {
    background-color: #101827;
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #182438;
}
h1, h2, h3 {
    color: #e8efff;
}
.stButton button {
    background-color: #5865f2;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 22px;
}
[data-testid="stMetric"] {
    background: #202f46;
    padding: 18px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ---------- SCORE EXTRACTION ----------
def extract_score(evaluation):
    """
    Extract a score such as 8/10 or 8 out of 10.
    Returns None if a score cannot be identified.
    """
    match = re.search(
        r'(?i)score\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(?:/10|out of 10)?',
        evaluation
    )

    if not match:
        match = re.search(
            r'(\d+(?:\.\d+)?)\s*(?:/10|out of 10)',
            evaluation,
            re.IGNORECASE
        )

    if match:
        score = float(match.group(1))
        if 0 <= score <= 10:
            return score

    return None


# ---------- SESSION INITIALIZATION ----------
defaults = {
    "questions": [],
    "answers": [],
    "evaluations": [],
    "coachings": [],
    "current_index": 0,
    "interview_started": False,
    "report": None,
    "interview_id": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("🎯 Interview Coach")
    st.caption("AI-powered interview preparation")
    st.divider()

    company = st.selectbox(
        "Select Company",
        ["Google", "Microsoft", "Amazon", "Infosys", "TCS"]
    )

    role = st.selectbox(
        "Select Job Role",
        ["Python Developer", "Software Developer", "Data Analyst"]
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Beginner", "Intermediate", "Advanced"]
    )

    st.divider()
    st.caption("Powered by Ollama + LangChain + ChromaDB")


# ---------- CALCULATE DASHBOARD VALUES ----------
attempted = len(st.session_state.answers)

scores = [
    extract_score(evaluation)
    for evaluation in st.session_state.evaluations
]

valid_scores = [
    score for score in scores if score is not None
]

average_score = (
    sum(valid_scores) / len(valid_scores)
    if valid_scores else None
)

remaining = TOTAL_QUESTIONS - attempted


# ---------- DASHBOARD ----------
st.title("🎯 Company-Smart Mock Interview Coach")

st.write(
    "Practice interviews and improve your technical skills with AI."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Questions Attempted",
        f"{attempted}/{TOTAL_QUESTIONS}"
    )

with col2:
    st.metric(
        "Average Score",
        f"{average_score:.1f}/10"
        if average_score is not None else "N/A"
    )

with col3:
    st.metric(
        "Remaining Questions",
        remaining
    )

with col4:
    st.metric(
        "Interview Status",
        "Completed" if attempted == TOTAL_QUESTIONS
        else "In Progress" if st.session_state.interview_started
        else "Not Started"
    )

if st.session_state.interview_started:
    st.progress(attempted / TOTAL_QUESTIONS)

st.divider()


# ---------- START INTERVIEW ----------
if not st.session_state.interview_started:

    st.header("🚀 Start Your Interview")

    if st.button("Start Interview", type="primary"):

        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.evaluations = []
        st.session_state.coachings = []
        st.session_state.current_index = 0
        st.session_state.report = None

        # Give each interview a unique ID
        st.session_state.interview_id += 1

        st.session_state.company = company
        st.session_state.role = role
        st.session_state.difficulty = difficulty

        with st.spinner("Preparing your interview..."):
            try:
                first_question = generate_question(
                    company,
                    role,
                    difficulty,
                    []
                )

                st.session_state.questions.append(first_question)
                st.session_state.interview_started = True

                st.rerun()

            except Exception as e:
                st.error(f"Interview error: {e}")


# ---------- GENERATE NEXT QUESTION ----------
if (
    st.session_state.interview_started
    and st.session_state.current_index < TOTAL_QUESTIONS
    and len(st.session_state.questions)
    == st.session_state.current_index
    and st.session_state.current_index > 0
):

    with st.spinner("Generating next interview question..."):
        try:
            next_question = generate_question(
                st.session_state.company,
                st.session_state.role,
                st.session_state.difficulty,
                st.session_state.questions
            )

            st.session_state.questions.append(next_question)

        except Exception as e:
            st.error(f"Question generation error: {e}")


# ---------- INTERVIEW SESSION ----------
if (
    st.session_state.interview_started
    and st.session_state.current_index < TOTAL_QUESTIONS
    and len(st.session_state.questions)
    > st.session_state.current_index
):

    index = st.session_state.current_index

    st.header("🤖 Interview Session")

    st.write(
        f"Question {index + 1} of {TOTAL_QUESTIONS}"
    )

    st.info(st.session_state.questions[index])

    answer = st.text_area(
        "✍️ Enter your answer",
        height=150,
        key=f"answer_{st.session_state.interview_id}_{index}"
    )

    if st.button("Submit Answer", type="primary"):

        if not answer.strip():
            st.warning("Please enter your answer.")

        else:
            with st.spinner(
                "Evaluating your answer and preparing feedback..."
            ):
                try:

                    # STEP 1: Evaluate answer
                    evaluation = evaluate_answer(
                        st.session_state.company,
                        st.session_state.role,
                        st.session_state.questions[index],
                        answer
                    )

                    # STEP 2: Improve evaluation using reflection
                    improved_evaluation = reflect_on_evaluation(
                        st.session_state.questions[index],
                        answer,
                        evaluation
                    )

                    # STEP 3: Generate coaching feedback
                    coaching = generate_coaching(
                        st.session_state.company,
                        st.session_state.role,
                        st.session_state.questions[index],
                        answer,
                        improved_evaluation
                    )

                    # STEP 4: Save interview history
                    if len(st.session_state.answers) == index:

                        st.session_state.answers.append(answer)
                        st.session_state.evaluations.append(
                            improved_evaluation
                        )
                        st.session_state.coachings.append(coaching)

                    # STEP 5: Move to next question
                    st.session_state.current_index += 1

                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {e}")


# ---------- INTERVIEW HISTORY ----------
if st.session_state.answers:

    st.divider()
    st.header("📚 Interview History")

    for i in range(len(st.session_state.answers)):

        score = extract_score(
            st.session_state.evaluations[i]
        )

        score_text = (
            f" | Score: {score}/10"
            if score is not None else ""
        )

        with st.expander(
            f"Question {i + 1}{score_text}"
        ):

            st.write("**Question:**")
            st.write(st.session_state.questions[i])

            st.write("**Your Answer:**")
            st.write(st.session_state.answers[i])

            st.write("**Refined Evaluation:**")
            st.write(st.session_state.evaluations[i])

            st.write("**Coaching Feedback:**")
            st.write(st.session_state.coachings[i])


# ---------- COMPLETED INTERVIEW ----------
if (
    st.session_state.interview_started
    and st.session_state.current_index == TOTAL_QUESTIONS
):

    st.divider()

    st.success(
        "🎉 You completed all five interview questions!"
    )

    st.header("📊 Interview Performance Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Questions Completed",
            f"{attempted}/{TOTAL_QUESTIONS}"
        )

    with col2:
        st.metric(
            "Final Average Score",
            f"{average_score:.1f}/10"
            if average_score is not None else "Score unavailable"
        )

    if average_score is not None:

        if average_score >= 8:
            st.success("Excellent performance! Keep practising.")

        elif average_score >= 6:
            st.info("Good effort! Continue improving your answers.")

        else:
            st.warning(
                "Keep practising. Review the coaching feedback "
                "to improve your answers."
            )

    st.subheader("Question-wise Scores")

    for i, score in enumerate(scores):

        st.write(
            f"Question {i + 1}: "
            f"{score}/10" if score is not None
            else f"Question {i + 1}: Score unavailable"
        )

    # ---------- FINAL REPORT ----------
    if st.button("Generate Final Interview Report"):

        with st.spinner("Generating your final report..."):

            try:
                report = generate_report(
                    st.session_state.company,
                    st.session_state.role,
                    "\n".join(st.session_state.questions),
                    "\n".join(st.session_state.answers),
                    "\n".join(st.session_state.evaluations),
                    "\n".join(st.session_state.coachings)
                )

                st.session_state.report = report

            except Exception as e:
                st.error(f"Report error: {e}")

    if st.session_state.report:

        st.subheader("📄 Final Interview Report")

        st.markdown(st.session_state.report)

        st.download_button(
            "⬇️ Download Report",
            data=st.session_state.report,
            file_name="interview_report.txt",
            mime="text/plain"
        )

    # ---------- RESTART ----------
    if st.button("Start Another Interview"):

        st.session_state.interview_started = False

        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.evaluations = []
        st.session_state.coachings = []

        st.session_state.current_index = 0
        st.session_state.report = None

        st.rerun()


# ---------- FOOTER ----------
st.divider()

st.caption(
    "AI Mock Interview Coach | Academic Project"
)
