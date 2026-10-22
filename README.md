# what is it you seek

A minimal Streamlit question-and-answer app backed entirely by a local,
deterministic philosophical engine. Type a question and press Enter.
The existing interface and styling are unchanged.

No API keys, paid inference, language models, embeddings, downloaded neural
models or external services are used to answer a question. Once dependencies
are installed, answering requires no outbound network access. Streamlit still
uses its normal browser/server connection to display the app.

## Run locally

Use Python 3.12 (tested).

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py --browser.gatherUsageStats false
```

On Windows, activate with `.venv\Scripts\Activate.ps1` instead.
No secrets file or environment variables are required. Existing secrets files
remain ignored and are not read by the app.

## Streamlit Community Cloud

- Repository: `RNo2/Quesionaire`
- Branch: `main`
- Main file: `app.py`
- Python: **3.12**
- Secrets: **none**

An existing deployment normally rebuilds when `main` changes. If necessary,
select **Manage app → Reboot**. Old inference keys/model settings may be removed
from Streamlit Secrets; they are no longer used. Only Streamlit is a direct
runtime dependency. No usage-based inference costs are incurred; normal free
hosting resource and availability limits still apply.

## How answers are constructed

```text
question → normalization/aliases → weighted themes + question intent
         → principle retrieval → tension/relationship rules
         → answer plan → deterministic prose
```

- `philosophy/knowledge.py`: 17 structured principles converted from the original
  worldview: causal unfolding, conditioned choice, fate through action,
  counterfactual learning, witness/awareness, consciousness, one-and-many,
  localized perspective, universe experiencing itself, structure/function/
  participation/purpose, perception, suffering, uncertainty, truth, science/
  metaphysics, AI as nature, and discipline. Each has definitions, claims,
  reasoning, qualifications, implications and equivalent sentence banks.
- `worldview.py`: compatibility entry point exposing the structured knowledge.
  The original prose is retained in Git history, not used as a system prompt.
- `preprocessing.py`: Unicode/case/whitespace normalization, contraction
  expansion, tokenization, explicit inflection/synonym aliases, bounded typo
  correction, phrase boundaries and limited negation context.
- `lexicon.py`: weighted keywords, phrases, exclusions and a theme graph.
- `classifier.py`: nine question intentions, weighted textual evidence and
  local token-overlap similarity against representative statements. Each graph
  boost is one-hop and capped at 1.5; a boost alone cannot retrieve a principle
  or activate a tension rule.
- `engine.py`: retrieves up to three connected principles with direct support.
  Multi-domain principles require support for each domain. Pure `reason(text)`
  exposes the interpretation, scores, retrieved IDs, matching rules and plan.
  `answer_question(text)` returns only the visitor's prose.
- `logic.py`: reusable tension/synthesis rules. These cover agency/determinism,
  fate/passivity, oneness/locality, perception/external fact, intelligence/
  consciousness, purpose/function, ignorance/evidence, witness/personality,
  regret/action, material suffering, science/metaphysics and purpose/action.
  When several rules match, the highest-priority rule supplies the main
  synthesis; the trace includes all matching rule IDs.
- `composer.py`: position → reasoning → distinction → implication. Definitions,
  personal questions, comparisons and challenges use different plans. A stable
  SHA-256 selection varies equivalent wording without runtime randomness.

The engine reasons within a finite, authored English vocabulary and rule base.
It is not unrestricted language understanding, a theorem prover, a general
fact-finder or a replacement for evidence. Negation handling is limited to
local context; answers discuss distinctions without attributing a belief to
someone simply because they mention it. Complex or unsupported wording may be
missed. Unmatched questions receive an honest limitation rather than invented
certainty. Input is bounded at 6,000 characters. No session chat history or
shared response cache is used; questions are interpreted independently.

## Extend the worldview

Edit a principle's banks in `knowledge.py`, add recognition language and theme
relationships in `lexicon.py`, and add an explicit relationship in `logic.py`
when two ideas need a shared argument. Add paraphrases, counterexamples and
expected distinctions to `tests/test_engine.py`. Do not add exact question-to-
answer mappings. Sentence choices should remain equivalent in claim and scope.

## Validate

```sh
python -m pip check
python -m unittest discover -s tests -v
```

The engine tests also run without installing Streamlit:

```sh
python -m unittest discover -s tests -p test_engine.py -v
```

The corpus covers all philosophical domains, question types, paraphrases,
tensions, exclusions, typos, unsupported questions, input bounds, negation,
consistent output across process hash seeds and blocked outbound sockets.
Streamlit AppTest exercises real local answers, empty submissions, reruns,
duplicates and Markdown rendering without raw response HTML. No API mocks or
external test credentials are needed.
