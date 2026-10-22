"""Interpret intention and retrieve themes from explainable textual evidence."""

from dataclasses import dataclass
from enum import Enum
import re

from .lexicon import RELATIONSHIPS, THEMES, VOCABULARY
from .preprocessing import preprocess


class QuestionType(str, Enum):
    DEFINITION = "definition"
    TRUTH = "truth_claim"
    CAUSAL = "causal"
    NORMATIVE = "normative"
    EXISTENTIAL = "existential"
    HYPOTHETICAL = "hypothetical"
    PERSONAL = "personal_application"
    COMPARISON = "comparison"
    CHALLENGE = "challenge"
    EXPLANATION = "explanation"
    MECHANISM = "mechanism"
    PURPOSE = "purpose"
    CONSEQUENCES = "consequences"
    EPISTEMIC = "epistemology"
    PRACTICAL = "practical_decision"


def classify_intent(text):
    question = text.normalized
    if text.has_any(("how should", "how ought", "how can i approach", "what should i do")):
        return QuestionType.PRACTICAL
    if text.has_any(("how could we know", "how can we know", "how do we know", "how can i know", "what evidence", "how would we know")):
        return QuestionType.EPISTEMIC
    if re.search(r"\bwhat (?:would |will )?(?:happen|happens|follow|follows)\b", question):
        return QuestionType.CONSEQUENCES
    if text.has_any(("difference between", "different from", "versus", "vs", "same as", "relationship between")) or re.search(r"\bhow .+ differ\b", question):
        return QuestionType.COMPARISON
    if text.contains("if") and text.has_any(("meaningless", "nothing matters", "why bother", "contradict", "contradiction", "how can", "is not", "does not", "can not", "point in trying", "why should")):
        return QuestionType.CHALLENGE
    if text.has_any(("should", "ought")):
        return QuestionType.NORMATIVE
    if text.has_any(("meaning of life", "purpose of life", "why do i exist", "why am i here", "point of life")):
        return QuestionType.EXISTENTIAL
    if text.has_any(("what if", "suppose", "imagine", "if")):
        return QuestionType.HYPOTHETICAL
    if set(text.tokens) & {"i", "my", "me"} and text.has_any(("why", "how", "afraid", "regret", "fear")):
        return QuestionType.PERSONAL
    if re.search(r"^what (?:is|are) .+ for$", question) or text.has_any(("purpose of", "what purpose")):
        return QuestionType.PURPOSE
    if text.has_any(("what causes", "where does", "where do")) or re.search(r"^what makes .+ (?:happen|occur|arise)$", question):
        return QuestionType.CAUSAL
    if re.search(r"^how (?:does|do|can|is|are)\b", question):
        return QuestionType.MECHANISM
    if text.has_any(("what is", "what are", "define", "definition")) or re.search(r"^what does .+ mean$", question):
        return QuestionType.DEFINITION
    if text.has_any(("why", "because")):
        return QuestionType.EXPLANATION
    return QuestionType.TRUTH


@dataclass(frozen=True)
class ThemeScore:
    theme: str
    direct: float
    similarity: float
    boost: float
    matched: tuple[str, ...]

    @property
    def score(self):
        return self.direct + self.similarity + self.boost


def detect_themes(text, principles):
    evidence = {}
    for name, spec in THEMES.items():
        matched = []
        direct = 0.0
        if not text.has_any(spec.exclusions):
            for word in spec.primary:
                if word in text.concepts:
                    direct += 4
                    matched.append(word)
            for word in spec.secondary:
                if word in text.concepts:
                    direct += 1
                    matched.append(word)
            for phrase in spec.phrases:
                if text.contains(phrase):
                    direct += 7
                    matched.append(phrase)
        similarity = 0.0
        # Local token overlap with representative statements, not exact Q&A.
        # Stopwords never contribute; overlap alone cannot establish relevance.
        if direct:
            for principle in principles:
                if name not in principle.themes:
                    continue
                for example in principle.examples:
                    sample = preprocess(example, VOCABULARY).concepts
                    overlap = text.concepts & sample
                    if len(overlap) >= 2:
                        similarity = max(similarity, 2 * len(overlap) / len(text.concepts | sample))
        evidence[name] = (direct, similarity, tuple(matched))
    results = []
    for name, (direct, similarity, matched) in evidence.items():
        # A single bounded one-hop boost; no recursive spreading or feedback.
        boost = min(1.5, sum(min(0.75, source_direct * 0.08)
            for source, (source_direct, _, _) in evidence.items()
            if source_direct >= 4 and name in RELATIONSHIPS.get(source, ())))
        results.append(ThemeScore(name, direct, similarity, boost, matched))
    return tuple(sorted(results, key=lambda item: (-item.score, -item.direct, item.theme)))
