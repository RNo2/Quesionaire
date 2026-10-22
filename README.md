# What do you seek

A minimal Streamlit philosophy app: one empty input, Enter to ask, Markdown
answers from a deterministic local worldview engine. No LLM, API key, inference
service, downloaded model or outbound connection is used to answer questions.

## Interface

Hermes is an authored, articulated pixel-stone monument, drawn into a coarse
Canvas framebuffer and enlarged with nearest-neighbor sampling. Faceted stone,
chisel marks and muted bronze details replace the generated photographic image.
On a nonempty Enter submission, the shoulder and elbow slowly raise an open
hand over 3.2 seconds, hold briefly, then lower over 3.5 seconds. Answers appear
immediately; the animation never blocks reading or submission. Repeated questions
replay the gesture, while empty submissions do nothing.

Pointer movement subtly shifts the head. Tap/click the upper figure to awaken
it without asking a question. Touch scrolling and form controls are preserved.
Reduced-motion users receive a still raised pose instead of animation. Drawing
stops when idle; component teardown releases listeners and animation frames.
No graphics library, generated image, API, or external asset host is used for
the figure. Desktop and mobile share the same jointed geometry.

Dusty wine headings and bone answer text use locally embedded EB Garamond,
licensed under the SIL Open Font License (`static/fonts/OFL.txt`). `app.py` owns
the form/state flow; `ui/theme.css` owns composition; `ui/presence.py` and
`ui/presence.js` supply the local Streamlit v2 component. `ui/styles.py` embeds
the font to avoid cloud static routing dependencies. Restart after JS changes.

## Run and deploy

Use Python 3.12:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows use `.venv\Scripts\Activate.ps1` to activate the environment.

For Streamlit Community Cloud select repository `RNo2/Quesionaire`, branch
`main`, main file `app.py`, Python **3.12**. No secrets or environment variables
are required. Existing deployments normally rebuild after a push; use
**Manage app → Reboot** if needed. Old OpenAI secrets can be removed.
Streamlit is the only direct runtime dependency. Secrets files remain ignored.

## Reasoning architecture

```text
normalized question → operation + central subject + conditional premise
                    → concept models / optional topic retrieval
                    → connected conceptual relations + constructive synthesis
                    → direct answer → reasons → implication → complication → limit
```

The old engine missed “Who is” as a definition, had no substantive God concept,
and allowed a topic or critical rule to replace the central answer. The new
planner resolves the demand first. Definitions, existence, explanations,
mechanisms, purpose, practical/normative questions, comparisons, challenges and
hypotheticals have distinct roles. Criticism supplies a relevant complication;
it cannot silently overwrite the opening. Explicit inference challenges and
same-reference contradictions receive direct logical evaluations.

- `philosophy/knowledge.py`: all 17 original structured worldview principles,
  plus a God/totality principle. God can mean the underlying reality manifesting
  as differentiated forms, distinct from an external personal creator. This
  is offered as a metaphysical interpretation, not scientific proof.
- `concepts.py`: 19 reusable concept models, ten directed conceptual chains and
  four constructive joins. Relations include reality → structures → functions/
  experiences → individuality; conditions → dispositions → actions → consequences
  → conditions; and structure → function → participation → purpose. These are
  authored relations, not full-question lookup entries.
- `demand.py`: operation and central-subject analysis independent of topic scores;
  matches concepts while retaining unknown subjects. Scoped attribute binding
  distinguishes a contradiction about the same whole from different properties
  of a part and whole.
- `planning.py`: produces the ordered answer plan, concept/chain/principle trace
  and applied-rule trace. Known concepts receive constructive arguments before
  qualifications. Identity and existence are separate demands.
- `preprocessing.py`, `classifier.py`, `lexicon.py`: normalization, aliases,
  bounded typo correction, local negation, intent detection, weighted topic
  evidence and capped relationship boosts. Boosts alone cannot force retrieval.
- `logic.py`: reusable distinctions concerning agency, unity, perception,
  evidence, consciousness, purpose, suffering and action.
- `subjects.py`, `universal.py`: reusable subject profiles and ten permanent
  philosophical lenses. An unfamiliar subject keeps its wording and receives
  an interpretive argument instead of an abstention or unrelated topic summary.
  External factual questions distinguish interpretation from verification.
- `composer.py`: ordered plan rendering, exact duplicate suppression and stable
  SHA-256 selection among equivalent authored phrasings.
- `engine.py`: pure `reason(text)` exposes operation, subject, concepts, chains,
  principles, matched/applied rules, lenses and plan. `answer_question(text)`
  returns visitor prose. `supported` means an interpretation exists, not that
  its factual premises were verified.
- `worldview.py`: convenient exports for inspecting/editing principles, models,
  chains and lenses. The original prose is preserved in Git history.

## Extend and validate

Edit concept claims in `knowledge.py`, connect them in `concepts.py`, and expand
recognition in `lexicon.py` or subject profiles as needed. Add paraphrases and
counterexamples to the regression corpus rather than exact question/answer
mappings.

```sh
python -m pip check
python -m unittest discover -s tests -v
```

Thirty tests cover worldview domains, direct-answer order, God paraphrases,
existence versus definition, scoped contradictions, connected chains, subject
retention, unknown inputs, negation, deterministic output across processes,
blocked network sockets, input bounds, and Streamlit blank/duplicate/rerun/
Markdown behavior. Desktop and mobile browser checks cover Enter submission,
local font loading, overflow and startup without JavaScript errors.

## Limits

This is a finite authored English rule system, not unrestricted language
understanding, empirical verification or a theorem prover. Complex syntax,
irony, remote negation and unfamiliar paraphrases can be misread. Universal
fallbacks provide philosophical interpretation, not new factual knowledge.
Answers are independent; there is no conversation memory. Inputs are bounded
to the first 6,000 trimmed characters. Empty/whitespace input does nothing.
