import os
import streamlit as st
from openai import OpenAI
from worldview import WORLDVIEW

st.set_page_config(
    page_title="",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        #MainMenu, header, footer {
            visibility: hidden;
        }

        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {
            display: none !important;
        }

        .stApp {
            background: #0b0b0b;
            color: #ece9e2;
        }

        .block-container {
            max-width: 760px;
            padding-top: 23vh;
            padding-bottom: 12vh;
        }

        .seek {
            text-align: center;
            font-size: clamp(1.7rem, 4vw, 2.8rem);
            font-weight: 400;
            letter-spacing: -0.035em;
            color: #ece9e2;
            margin-bottom: 2.2rem;
        }

        div[data-testid="stForm"] {
            border: 0 !important;
            padding: 0 !important;
        }

        .stTextInput input {
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

        .stTextInput input:focus {
            border-bottom: 1px solid rgba(236, 233, 226, 0.8) !important;
            box-shadow: none !important;
        }

        .stTextInput input::placeholder {
            color: transparent !important;
        }

        .stFormSubmitButton {
            display: none !important;
        }

        .answer {
            margin-top: 3.4rem;
            font-size: 1.08rem;
            line-height: 1.85;
            letter-spacing: 0.003em;
            color: #d8d5cf;
        }

        .answer p {
            margin-bottom: 1.15rem;
        }

        @media (max-width: 640px) {
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

def get_api_key():
    try:
        return st.secrets.get("OPENAI_API_KEY")
    except Exception:
        return None

def get_model():
    try:
        return st.secrets.get("OPENAI_MODEL", "gpt-5.5")
    except Exception:
        return os.getenv("OPENAI_MODEL", "gpt-5.5")

api_key = get_api_key() or os.getenv("OPENAI_API_KEY")

st.markdown('<div class="seek">what is it you seek</div>', unsafe_allow_html=True)

with st.form("ask", clear_on_submit=True, border=False):
    question = st.text_input(
        "question",
        label_visibility="collapsed",
        placeholder="",
        autocomplete="off",
    )
    submitted = st.form_submit_button("submit")

if "answer" not in st.session_state:
    st.session_state.answer = ""

if submitted and question.strip():
    if not api_key:
        st.session_state.answer = (
            "This instance has not been given an OpenAI API key."
        )
    else:
        client = OpenAI(api_key=api_key)
        try:
            response = client.responses.create(
                model=get_model(),
                instructions=WORLDVIEW,
                input=question.strip(),
                max_output_tokens=900,
            )
            st.session_state.answer = response.output_text.strip()
        except Exception:
            st.session_state.answer = (
                "The answer could not be reached. Try again."
            )

if st.session_state.answer:
    st.markdown(
        f'<div class="answer">{st.session_state.answer}</div>',
        unsafe_allow_html=True,
    )
