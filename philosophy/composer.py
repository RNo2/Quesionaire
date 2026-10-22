"""Construct a bounded answer plan, then render it; no random quote shuffling."""

from dataclasses import dataclass
from hashlib import sha256

from .classifier import QuestionType


def select(bank, question, component):
    # Python's built-in hash changes between processes; SHA-256 does not.
    number = int.from_bytes(sha256(f"{question}|{component}".encode()).digest()[:8], "big")
    return bank[number % len(bank)]


@dataclass(frozen=True)
class AnswerPlan:
    position: str
    reasoning: tuple[str, ...]
    distinction: str
    implication: str
    closing: str = ""

    def render(self):
        # Suppress exact repetition across components while retaining argument
        # order: position -> grounds -> distinction -> consequence.
        seen = set()

        def fresh(parts):
            result = []
            for part in parts:
                if part and part not in seen:
                    seen.add(part)
                    result.append(part)
            return " ".join(result)

        paragraphs = (
            fresh((self.position,)),
            fresh(self.reasoning),
            fresh((self.distinction,)),
            fresh((self.implication, self.closing)),
        )
        return "\n\n".join(part for part in paragraphs if part)


def compose(text, intent, selected, rules):
    primary = selected[0]
    seed = text.normalized
    rule = rules[0] if rules else None
    opening = select(primary.openings, seed, "opening")
    qualification = select(primary.qualifications, seed, "qualification")
    reasoning = [primary.reasoning[0]]

    if intent == QuestionType.DEFINITION:
        position = primary.definition
    elif intent in (QuestionType.NORMATIVE, QuestionType.PERSONAL):
        position = select(primary.applications, seed, "application")
    elif intent == QuestionType.CAUSAL:
        position = primary.reasoning[0]
        reasoning = [opening]
    elif intent == QuestionType.HYPOTHETICAL:
        position = f"Treat the premise as a possibility rather than an established fact. {opening}"
    else:
        position = opening

    if rule:
        if intent not in (QuestionType.DEFINITION, QuestionType.NORMATIVE, QuestionType.PERSONAL):
            position = rule.position
        reasoning.append(rule.bridge)
        distinction = rule.distinction
        # Preserve epistemic limits of the primary even when a rule supplies
        # the cross-theme synthesis. Never turn possibility into proof.
        if qualification not in distinction:
            distinction = f"{distinction} {qualification}"
        implication = rule.implication
    else:
        reasoning.append(select(primary.reasoning[1:], seed, "reasoning"))
        distinction = qualification
        implication = select(primary.conclusions, seed, "conclusion")
        # Only directly retrieved themes reach this branch. Make the link
        # explicit, rather than append a second unrelated topic's paragraph.
        if len(selected) > 1:
            secondary = selected[1]
            if intent == QuestionType.COMPARISON:
                position = f"{primary.definition} {secondary.definition}"
                transition = select(primary.transitions, seed, "transition")
                distinction = f"{transition} {qualification}"
            else:
                reasoning.append(f"A related distinction is this: {secondary.core_claim}")
    return AnswerPlan(position, tuple(reasoning), distinction, implication)
