import os
import logging
import streamlit as st
from openai import OpenAI
from streamlit.errors import StreamlitSecretNotFoundError
from worldview import WORLDVIEW

logger = logging.getLogger(__name__)

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

        .st-key-answer {
            margin-top: 3.4rem;
            font-size: 1.08rem;
            line-height: 1.85;
            letter-spacing: 0.003em;
            color: #d8d5cf;
        }

        .st-key-answer p {
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

DEFAULT_MODEL = "gpt-5.5"
UNAVAILABLE = "The answer could not be reached. Try again shortly."


def get_setting(name, default=None):
    """Prefer Streamlit Secrets, with an environment fallback per setting."""
    try:
        value = st.secrets.get(name)
    except StreamlitSecretNotFoundError:
        value = None
    return value or os.getenv(name) or default


def answer_question(question):
    """Keep credentials, transport details and provider errors off the page."""
    try:
        api_key = get_setting("OPENAI_API_KEY")
        if not api_key:
            logger.error("Answer unavailable: OPENAI_API_KEY is not configured.")
            return None
        with OpenAI(api_key=api_key, timeout=45.0, max_retries=0) as client:
            response = client.responses.create(
                model=get_setting("OPENAI_MODEL", DEFAULT_MODEL),
                instructions=WORLDVIEW,
                input=question,
                max_output_tokens=1600,
                store=False,
            )
        if response.status != "completed":
            logger.warning(
                "Answer unavailable: response status=%s; incomplete reason=%s",
                response.status,
                getattr(getattr(response, "incomplete_details", None), "reason", None),
            )
            return None
        answer = response.output_text.strip()
        if not answer:
            logger.warning("Answer unavailable: response completed without text.")
        return answer or None
    except Exception as error:
        # Log only diagnostic categories, never exception messages, request
        # bodies, headers, questions or credentials.
        logger.error(
            "Answer unavailable: error_type=%s http_status=%s",
            type(error).__name__,
            getattr(error, "status_code", None),
        )
        # SDK initialization, configuration and request failures share a quiet
        # visitor message. Never render exceptions or credential values.
        return None

st.markdown('<div class="seek">what is it you seek</div>', unsafe_allow_html=True)

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
if submitted and question and question != st.session_state.last_question:
    answer = answer_question(question)
    st.session_state.answer = answer or UNAVAILABLE
    # Successful duplicate submissions reuse the existing response. Failed
    # requests remain retryable, and ordinary reruns never call the API.
    st.session_state.last_question = question if answer else None

if st.session_state.answer:
    with st.container(key="answer"):
        st.markdown(st.session_state.answer, unsafe_allow_html=False)
