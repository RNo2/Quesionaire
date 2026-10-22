from pathlib import Path

import streamlit as st

from philosophy import answer_question
from philosophy.engine import MAX_QUESTION_LENGTH
from philosophy.preprocessing import normalize
from ui.presence import render_presence

st.set_page_config(
    page_title="",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Trusted local stylesheet: visitor text is never interpolated into HTML/CSS.
st.markdown(
    "<style>" + Path(__file__).with_name("ui").joinpath("theme.css").read_text() + "</style>",
    unsafe_allow_html=True,
)

render_presence()
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
