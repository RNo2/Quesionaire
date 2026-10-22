# what is it you seek

A minimal Streamlit question-and-answer app whose visible interface contains
only:

> what is it you seek

plus the input field and the answer after submission.

## Run locally

1. Install dependencies:

   python -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt

   On Windows, activate with `.venv\Scripts\Activate.ps1` instead.

2. Set your API key:

   Windows PowerShell:
   $env:OPENAI_API_KEY="your-key"

   macOS/Linux:
   export OPENAI_API_KEY="your-key"

3. Run:

   streamlit run app.py

## Streamlit Community Cloud

Create an app using repository `RNo2/Quesionaire`, branch `main`, and main file
`app.py`. In Advanced settings choose Python 3.12. If already deployed, pushing
to `main` updates the app automatically; reboot from Manage app if needed.

Add this to the app's Secrets (never commit a real key):

```toml
OPENAI_API_KEY = "your-key"
OPENAI_MODEL = "gpt-5.5"
```

`OPENAI_MODEL` is optional. The app defaults to `gpt-5.5`.

The user submits by pressing Enter. The submit control exists only to support
the Streamlit form and is hidden from the interface.

For local secrets, use `.streamlit/secrets.toml` (ignored by Git). Each setting
falls back to the matching environment variable when absent from Secrets.
The selected model must be available to your API account and support the
Responses API. The app sends the full `WORLDVIEW` as instructions, does not
request response storage, and renders replies as Markdown without raw HTML.
It has no shared response cache; session state keeps only the current answer
and last successful question.

## Validation

```sh
python -m pip check
python -m unittest discover -s tests -v
```

Tests run the Streamlit app with mocked API calls, covering blank submissions,
configuration fallbacks, full worldview delivery, Markdown, duplicate handling,
and safe, retryable failures. They do not validate live model/account access.
