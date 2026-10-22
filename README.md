# What do you seek

A minimal Streamlit question-and-answer app backed entirely by a local,
deterministic philosophical engine. Type a question and press Enter.
The interface uses Times New Roman (with local serif fallbacks), a bold wine-red
heading and a locally served pixel-art Hermes Trismegistus background. The
background is a decorative generated asset in `static/hermes-pixel.png`; it is
not loaded from an external image service. Static serving is enabled in
`.streamlit/config.toml`.

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
question → intent + subject/kind extraction + weighted topics
         → permanent universal lenses + optional topic principles
         → subject bridge + tension/relationship synthesis
         → tailored answer plan → deterministic prose
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
- `classifier.py`: fifteen question intentions, weighted textual evidence and
  local token-overlap similarity against representative statements. Each graph
  boost is one-hop and capped at 1.5; a boost alone cannot retrieve a principle
  or activate a tension rule.
- `engine.py`: retrieves up to three connected principles with direct support.
  Multi-domain topic principles require support for each domain. This threshold
  no longer controls whether the engine reasons: every non-whitespace string,
  including symbolic input, receives a universal interpretation and a plan.
  Pure `reason(text)` exposes subject/kind, selected lens IDs, topic IDs,
  `topic_matched`, matching rules, truncation status and the answer plan.
  `supported` means an interpretation exists, not that every factual premise
  is verified. `answer_question(text)` returns only the visitor's prose.
- `logic.py`: reusable tension/synthesis rules. These cover agency/determinism,
  fate/passivity, oneness/locality, perception/external fact, intelligence/
  consciousness, purpose/function, ignorance/evidence, witness/personality,
  regret/action, material suffering, science/metaphysics and purpose/action.
  When several rules match, the highest-priority rule supplies the main
  synthesis; the trace includes all matching rule IDs.
- `subjects.py`: linguistic subject extraction and reusable profiles for
  systems, resources, experience, institutions, tools, relationships and other
  kinds. Profile information helps select lenses without becoming fake direct
  evidence for a topic match. Unlisted subjects retain their own wording.
- `universal.py`: ten permanent lenses: causality, structure, participation,
  perception, agency, knowledge, change, purpose, whole/parts and truth. Intent,
  subject kind/profile and available topic evidence select three relevant
  lenses. This path remains active even with zero topic overlap.
- `composer.py`: position → reasoning → distinction → implication. Definitions,
  personal questions, comparisons and challenges use different plans. A stable
  SHA-256 selection varies equivalent topic wording without runtime randomness.
  Subject-based arguments are combined with relevant topic details and tension
  rules, rather than replacing an unfamiliar noun with a stock topic summary.

The engine reasons within a finite, authored English vocabulary and rule base.
It is not unrestricted language understanding, a theorem prover, a general
fact-finder or a replacement for evidence. Negation handling is limited to
local context; answers discuss distinctions without attributing a belief to
someone simply because they mention it. Complex or unsupported wording may be
missed. Unmatched subjects receive a conditional philosophical argument, not
an abstention. External factual requests distinguish verification from
interpretation without inventing a result. Very long inputs are interpreted
from the first 6,000 characters after trimming outer whitespace. No session chat history or
shared response cache is used; questions are interpreted independently.

## Extend the worldview

Edit a principle's banks in `knowledge.py`, add recognition language and theme
relationships in `lexicon.py`, and add an explicit relationship in `logic.py`
when two ideas need a shared argument. Expand universal lenses in `universal.py`
and subject profiles in `subjects.py`. Add paraphrases, counterexamples and
expected distinctions to `tests/test_engine.py` and `tests/test_universal.py`. Do not add exact question-to-
answer mappings. Sentence choices should remain equivalent in claim and scope.

## Validate

```sh
python -m pip check
python -m unittest discover -s tests -v
```

The engine tests also run without installing Streamlit:

```sh
python -m unittest discover -s tests -p test_engine.py -v
python -m unittest discover -s tests -p test_universal.py -v
```

The corpus covers all philosophical domains, question types, paraphrases,
tensions, exclusions, typos, previously unsupported subjects, input bounds, negation,
consistent output across process hash seeds and blocked outbound sockets.
Streamlit AppTest exercises real local answers, empty submissions, reruns,
duplicates and Markdown rendering without raw response HTML. No API mocks or
external test credentials are needed.

## Why the abstention was removed

The former `engine.py` returned a constant message immediately when
`retrieve(scores)` was empty. No answer planner ran for an unfamiliar topic.
Now subject extraction and permanent lens selection always produce an
interpretation; topic retrieval is an optional enrichment layer. Matching
thresholds were retained for topic accuracy rather than lowered to force a
match. The original 17 topic principles remain intact. A bare `what if` is
classified as hypothetical reasoning rather than automatically mistaken for
regret about the past.

The interface is unchanged in function: one input, Enter to submit, one answer,
no dashboard controls. Browser checks cover desktop and mobile, actual Enter
submission for known and unlisted subjects, heading styling, background loading,
and no outbound requests. A normal app startup is required for the local static
background; no extra asset host or secret is needed.
