"""Pure local question -> analysis -> retrieval -> reasoning -> answer pipeline."""

from dataclasses import dataclass
from math import sqrt

from .classifier import QuestionType, ThemeScore, classify_intent, detect_themes
from .composer import AnswerPlan
from .knowledge import PRINCIPLES
from .lexicon import RELATIONSHIPS, VOCABULARY
from .logic import evaluate
from .preprocessing import Text, preprocess
from .subjects import Subject, extract_subject
from .universal import choose_lenses, interpret
from .demand import Demand, identify_demand
from .planning import construct_plan

MAX_QUESTION_LENGTH = 6000


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
    subject: Subject | None = None
    lens_ids: tuple[str, ...] = ()
    topic_matched: bool = False
    truncated: bool = False
    demand: Demand | None = None
    concept_ids: tuple[str, ...] = ()
    chain_ids: tuple[str, ...] = ()
    applied_rule_ids: tuple[str, ...] = ()


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
    # Interpret a bounded prefix rather than replace a long input with refusal.
    cleaned = question.strip()
    truncated = len(cleaned) > MAX_QUESTION_LENGTH
    bounded = cleaned[:MAX_QUESTION_LENGTH]
    text = preprocess(bounded, VOCABULARY)
    intent = classify_intent(text)
    if not cleaned:
        return Result("", text, intent, (), (), (), None, False)
    subject = extract_subject(text, intent)
    demand = identify_demand(text, intent, subject)
    scores = detect_themes(text, PRINCIPLES)
    selected = retrieve(scores)
    lenses = choose_lenses(intent, subject, scores)
    universal_plan = interpret(subject, intent, lenses)
    rules = evaluate(scores, text)
    planned = construct_plan(text, demand, universal_plan, rules, selected)
    plan = planned.plan
    return Result(
        answer=plan.render(), text=text, intent=intent, themes=scores,
        principle_ids=planned.principle_ids,
        rule_ids=tuple(rule.id for rule in rules), plan=plan, supported=True,
        subject=subject, lens_ids=tuple(lens.id for lens in lenses),
        topic_matched=bool(selected), truncated=truncated,
        demand=demand, concept_ids=planned.concept_ids,
        chain_ids=planned.chain_ids, applied_rule_ids=planned.applied_rule_ids,
    )


def answer_question(question):
    """Return only prose for the UI; reason() also exposes an auditable trace."""
    return reason(question).answer
