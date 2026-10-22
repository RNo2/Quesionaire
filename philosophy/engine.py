"""Pure local question -> analysis -> retrieval -> reasoning -> answer pipeline."""

from dataclasses import dataclass
from math import sqrt

from .classifier import QuestionType, ThemeScore, classify_intent, detect_themes
from .composer import AnswerPlan, compose
from .knowledge import PRINCIPLES, PRINCIPLES_BY_ID
from .lexicon import RELATIONSHIPS, VOCABULARY
from .logic import evaluate
from .preprocessing import Text, preprocess

MAX_QUESTION_LENGTH = 6000
FALLBACK = (
    "I do not know how to resolve that question from these principles alone. "
    "A confident answer would exceed the grounds available.\n\n"
    "Make the underlying claim more precise: what is being asserted, and what "
    "would count for or against it? Questions about choice, awareness, purpose, "
    "suffering or the limits of knowledge provide a clearer starting point."
)


@dataclass(frozen=True)
class Result:
    answer: str
    text: Text
    intent: QuestionType
    themes: tuple[ThemeScore, ...]
    principle_ids: tuple[str, ...]
    rule_ids: tuple[str, ...]
    plan: AnswerPlan | None
    supported: bool


def retrieve(scores):
    by_theme = {score.theme: score for score in scores}
    ranked = []
    for principle in PRINCIPLES:
        if len(principle.themes) > 1 and any(by_theme[theme].direct < 3 for theme in principle.themes):
            continue
        direct = sum(by_theme[theme].direct for theme in principle.themes)
        if direct < 3:
            continue
        score = sum(by_theme[theme].score for theme in principle.themes) / sqrt(len(principle.themes))
        ranked.append((score, principle))
    ranked.sort(key=lambda pair: (-pair[0], pair[1].id))
    if not ranked:
        return ()
    lead_score, lead = ranked[0]
    selected = [lead]
    for score, principle in ranked[1:]:
        if score < max(3, lead_score * 0.35):
            continue
        # Synthesis needs a declared relationship, not arbitrary co-occurrence.
        related = any(b in RELATIONSHIPS.get(a, ()) or a == b
            for a in lead.themes for b in principle.themes)
        if related:
            selected.append(principle)
        if len(selected) == 3:
            break
    return tuple(selected)


def reason(question):
    if not isinstance(question, str):
        raise TypeError("question must be text")
    # Bound processing before tokenization or fuzzy matching of an unbounded input.
    if len(question) > MAX_QUESTION_LENGTH:
        text = preprocess("")
        return Result("Please ask one focused question in 6,000 characters or fewer.",
            text, QuestionType.TRUTH, (), (), (), None, False)
    text = preprocess(question, VOCABULARY)
    intent = classify_intent(text)
    if not text.normalized:
        return Result("", text, intent, (), (), (), None, False)
    scores = detect_themes(text, PRINCIPLES)
    selected = retrieve(scores)
    if not selected:
        return Result(FALLBACK, text, intent, scores, (), (), None, False)
    rules = evaluate(scores, text)
    if rules:
        # A rule is an explicit argument linking these principles. Make its
        # foundations visible to callers inspecting the reasoning trace.
        rule_principles = tuple(PRINCIPLES_BY_ID[id] for id in rules[0].principles)
        primary = selected[0]
        if primary not in rule_principles:
            # A narrowly applicable tension may outrank a noisy broad theme.
            primary = rule_principles[0]
        selected = (primary,) + tuple(p for p in rule_principles if p.id != primary.id)
    plan = compose(text, intent, selected, rules)
    return Result(plan.render(), text, intent, scores,
        tuple(p.id for p in selected), tuple(rule.id for rule in rules), plan, True)


def answer_question(question):
    """Return only prose for the UI; reason() also exposes an auditable trace."""
    return reason(question).answer
