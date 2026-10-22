"""Extract the central demand independently of topic retrieval and criticism."""

import re
from dataclasses import dataclass

from .classifier import QuestionType, classify_intent
from .concepts import MODELS, ConceptModel
from .preprocessing import STOPWORDS, Text, normalize, preprocess
from .subjects import Subject, extract_subject


@dataclass(frozen=True)
class ConceptMatch:
    model: ConceptModel
    score: float
    is_subject: bool


@dataclass(frozen=True)
class Demand:
    operation: QuestionType
    subject: Subject
    central: str
    premise: str
    concepts: tuple[ConceptMatch, ...]


def identify_demand(text: Text, intent, subject):
    central = text.normalized
    premise = ""
    if central.startswith("if "):
        question = re.search(r"\b(?:why|how|am i|are we|can i|do i|should i|does that|does this)\b", central)
        if question:
            premise, central = central[:question.start()].strip(), central[question.start():]
            if intent == QuestionType.HYPOTHETICAL:
                intent = classify_intent(preprocess(central))
    elif " if " in central:
        central, premise = central.split(" if ", 1)
    # Grammatical scaffolding is not the subject's conceptual head.
    central_subject = extract_subject(preprocess(central), intent) if central != text.normalized else subject
    head_tokens = central_subject.label.split()
    leaders = STOPWORDS | {"people", "humans", "human", "really", "actually", "still", "there", "feel", "feels", "not", "never"}
    while head_tokens and head_tokens[0] in leaders:
        head_tokens.pop(0)
    head = " ".join(head_tokens)
    subject_head = head
    about = re.search(r"\b(?:role|meaning|purpose|nature|status|function|structure|concept|definition) of (.+)$", central_subject.label)
    if about:
        head = subject_head = about[1]
    candidates = []
    for model in MODELS:
        if text.has_any(model.exclusions):
            continue
        whole_matches = [alias for alias in model.aliases if text.contains(alias)]
        if not whole_matches:
            continue
        score = sum(7 if " " in alias else 3 for alias in whole_matches)
        is_subject = False
        for alias in whole_matches:
            normalized = normalize(alias)
            if f" {normalized} " in f" {central} ":
                score += 4
            if head == normalized or head.startswith(normalized + " "):
                score += 16
                is_subject = True
            if subject_head == normalized or subject_head.startswith(normalized + " "):
                score += 10
                is_subject = True
        candidates.append(ConceptMatch(model, score, is_subject))
    candidates.sort(key=lambda match: (-match.score, match.model.id))
    return Demand(intent, central_subject, central, premise, tuple(candidates))


@dataclass(frozen=True)
class Predication:
    concept: str
    group: str
    attribute: str
    positive: bool


ATTRIBUTES = {
    "conscious": ("conscious", True), "unconscious": ("conscious", False),
    "changing": ("changing", True), "unchanging": ("changing", False),
    "dependent": ("dependent", True), "independent": ("dependent", False),
    "caused": ("caused", True), "uncaused": ("caused", False),
}


def conflicting_predications(text, demand):
    """Bind attributes to entities, not to a bag of positive/negative words.

    A conflict needs the SAME reference, attribute and respect. A conscious
    part and an unconscious whole are not automatically the same referent.
    Reference groups are explicitly conditional on the worldview's model.
    """
    bindings = []
    for match in demand.concepts:
        model = match.model
        if not model.reference_group:
            continue
        for alias in model.aliases:
            pattern = (r"\b" + re.escape(normalize(alias))
                + r"\s+(?:(?:can|could|be|is|are|a|the|wholly|entirely|completely)\s+)*"
                + r"(?P<negative>not\s+|never\s+)?(?P<attribute>" + "|".join(ATTRIBUTES) + r")\b")
            for found in re.finditer(pattern, text.normalized):
                attribute, positive = ATTRIBUTES[found["attribute"]]
                if found["negative"]:
                    positive = not positive
                binding = Predication(model.id, model.reference_group, attribute, positive)
                if binding not in bindings:
                    bindings.append(binding)
    for index, a in enumerate(bindings):
        for b in bindings[index + 1:]:
            if a.group == b.group and a.attribute == b.attribute and a.positive != b.positive:
                return a, b
    return None
