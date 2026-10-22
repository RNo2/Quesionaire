import streamlit as st

from philosophy import answer_question
from philosophy.engine import MAX_QUESTION_LENGTH
from philosophy.preprocessing import normalize

st.set_page_config(
    page_title="",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        #MainMenu, header, footer, [data-testid="stSidebar"],
        [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }

        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        [data-testid="InputInstructions"] {
            display: none !important;
        }

        .stApp {
            background-color: #0b0b0b;
            background-image:
                linear-gradient(90deg, rgba(6, 5, 7, 0.60), rgba(6, 5, 7, 0.30)),
                url("/app/static/hermes-pixel.png");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: #ece9e2;
        }

        .stApp, .stApp p, .stApp input, .stApp label, .stApp button,
        .stApp h1, .stApp h2, .stApp h3, .stApp li, .stApp blockquote {
            font-family: "Times New Roman", Times, serif !important;
        }

        .block-container {
            max-width: 760px;
            padding-top: 23vh;
            padding-bottom: 12vh;
        }

        .stApp h1.seek {
            text-align: center;
            font-size: clamp(1.7rem, 4vw, 2.8rem);
            font-weight: 700;
            letter-spacing: -0.025em;
            color: #a94a61;
            margin-bottom: 2.2rem;
            padding: 0;
            text-shadow: 0 1px 12px rgba(0, 0, 0, 0.45);
        }

        div[data-testid="stForm"] {
            border: 0 !important;
            padding: 0 !important;
        }

        [data-testid="stTextInput"] [data-baseweb="input"],
        [data-testid="stTextInputRootElement"] {
            background: transparent !important;
            border: 0 !important;
            border-radius: 0 !important;
            box-shadow: none !important;
        }

        [data-testid="stTextInputRootElement"] {
            border-bottom: 1px solid rgba(236, 233, 226, 0.48) !important;
        }

        [data-testid="stTextInputRootElement"]:focus-within {
            border-bottom-color: rgba(236, 233, 226, 0.85) !important;
        }

        .stTextInput input, [data-testid="stTextInput"] input {
            background: transparent !important;
            color: #ece9e2 !important;
            border: 0 !important;
            border-bottom: 1px solid rgba(236, 233, 226, 0.38) !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            text-align: center;
            font-size: 1.12rem !important;
            padding: 0.7rem 0.2rem !important;
        }

        .stTextInput input:focus, [data-testid="stTextInput"] input:focus {
            border-bottom: 1px solid rgba(236, 233, 226, 0.8) !important;
            box-shadow: none !important;
        }

        .stTextInput input::placeholder, [data-testid="stTextInput"] input::placeholder {
            color: transparent !important;
        }

        .stFormSubmitButton {
            display: none !important;
        }

        .st-key-answer {
            margin-top: 3.4rem;
            font-size: 1.08rem;
            line-height: 1.85;
            letter-spacing: 0.003em;
            color: #d8d5cf;
            text-shadow: 0 1px 3px #000;
        }

        .st-key-answer p {
            margin-bottom: 1.15rem;
        }

        @media (max-width: 640px) {
            .stApp {
                background-position: 85% center;
                background-image:
                    linear-gradient(rgba(6, 5, 7, 0.54), rgba(6, 5, 7, 0.68)),
                    url("/app/static/hermes-pixel.png");
            }
            .block-container {
                padding-top: 18vh;
                padding-left: 1.25rem;
                padding-right: 1.25rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="seek">What do you seek</h1>', unsafe_allow_html=True)

with st.form("ask", clear_on_submit=True, enter_to_submit=True, border=False):
    question = st.text_input(
        "question",
        label_visibility="collapsed",
        placeholder="",
        autocomplete="off",
        key="question",
    )
    submitted = st.form_submit_button("submit")

if "answer" not in st.session_state:
    st.session_state.answer = ""
if "last_question" not in st.session_state:
    st.session_state.last_question = None

question = question.strip()
bounded_question = question[:MAX_QUESTION_LENGTH]
normalized_question = normalize(bounded_question) or bounded_question
if submitted and question and normalized_question != st.session_state.last_question:
    st.session_state.answer = answer_question(question)
    st.session_state.last_question = normalized_question

if st.session_state.answer:
    with st.container(key="answer"):
        st.markdown(st.session_state.answer, unsafe_allow_html=False)
