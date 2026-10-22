# what is it you seek

A minimal Streamlit question-and-answer app whose visible interface contains
only:

> what is it you seek

plus the input field and the answer after submission.

## Run locally

1. Install dependencies:

   pip install -r requirements.txt

2. Set your API key:

   Windows PowerShell:
   $env:OPENAI_API_KEY="your-key"

   macOS/Linux:
   export OPENAI_API_KEY="your-key"

3. Run:

   streamlit run app.py

## Streamlit Community Cloud

Add this to the app's Secrets:

OPENAI_API_KEY = "your-key"
OPENAI_MODEL = "gpt-5.5"

`OPENAI_MODEL` is optional. The app defaults to `gpt-5.5`.

The user submits by pressing Enter. The submit control exists only to support
the Streamlit form and is hidden from the interface.
