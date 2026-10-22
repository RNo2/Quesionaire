"""Small, auditable English normalization, not a downloaded NLP model."""

import re
import unicodedata
from dataclasses import dataclass
from difflib import get_close_matches

STOPWORDS = frozenset(
    "a an the is are was were be being been do does did of to for and or in on "
    "at with as it its this that those these i me my we our you your they their "
    "he she them what which who how why when where can could would should will "
    "have has had am if then than there really all any something everything "
    "thing things about from by into also even so just such".split()
)

# Explicit aliases avoid aggressive stemming that confuses unrelated words.
ALIASES = {
    "choices": "choice", "choosing": "choose", "chose": "choose",
    "chosen": "choose", "decisions": "decision", "deciding": "decide",
    "causes": "cause", "caused": "cause", "causal": "causality",
    "causation": "causality", "deterministic": "determinism",
    "causally": "causality",
    "determined": "predetermined", "predestined": "predestination",
    "destiny": "fate", "fated": "fate", "prewritten": "predestination",
    "thoughts": "thought", "thinking": "thought", "impulses": "impulse",
    "emotions": "emotion", "feelings": "feeling", "experiences": "experience",
    "experiencing": "experience", "suffer": "suffering", "suffers": "suffering",
    "suffered": "suffering", "painful": "pain", "afraid": "fear",
    "scared": "fear", "fears": "fear", "anxious": "anxiety",
    "regrets": "regret", "regretting": "regret", "mistakes": "mistake",
    "memories": "memory", "beliefs": "belief", "believing": "believe",
    "perceive": "perception", "perceived": "perception",
    "perceptions": "perception", "senses": "sense", "interpretations": "interpretation",
    "scientific": "science", "empirically": "empirical", "proven": "proof",
    "prove": "proof", "proves": "proof", "evidences": "evidence",
    "souls": "soul", "spiritual": "metaphysical", "metaphysics": "metaphysical",
    "oneness": "unity", "unified": "unity", "separateness": "separate",
    "separation": "separate", "individuals": "individual",
    "consciously": "conscious", "sentience": "consciousness",
    "sentient": "conscious", "robots": "robot", "machines": "machine",
    "functions": "function", "structures": "structure", "purposes": "purpose",
    "participating": "participation", "acts": "act", "acting": "act",
    "actions": "action", "habits": "habit", "disciplined": "discipline",
    "efforts": "effort", "trying": "try", "tried": "try",
    "truths": "truth", "uncertain": "uncertainty", "unknowns": "unknown",
    "dead": "death", "dying": "death", "died": "death",
    "meaninglessness": "meaningless", "hopeless": "hopelessness",
}


def normalize(text):
    text = unicodedata.normalize("NFKC", text).lower().replace("’", "'")
    for old, new in {
        "can't": "cannot", "cannot": "can not", "won't": "will not",
        "isn't": "is not", "aren't": "are not", "don't": "do not",
        "doesn't": "does not", "couldn't": "could not", "shouldn't": "should not",
        "i'm": "i am", "it's": "it is", "that's": "that is",
        "there's": "there is", "we're": "we are", "i've": "i have",
    }.items():
        text = re.sub(r"\b" + re.escape(old) + r"\b", new, text)
    text = re.sub(r"\bfreewill\b", "free will", text)
    return " ".join(re.findall(r"[^\W_]+", text, flags=re.UNICODE))


@dataclass(frozen=True)
class Text:
    normalized: str
    tokens: tuple[str, ...]
    concepts: frozenset[str]
    negated_concepts: frozenset[str]

    def contains(self, phrase):
        return f" {normalize(phrase)} " in f" {self.normalized} "

    def has_any(self, phrases):
        return any(self.contains(phrase) for phrase in phrases)


def preprocess(question, vocabulary=()):
    normalized = normalize(question)
    tokens = tuple(normalized.split())
    vocabulary = tuple(sorted(set(vocabulary)))
    concepts = []
    negated = set()
    for index, token in enumerate(tokens):
        concept = ALIASES.get(token, token)
        # Correct only near-identical longer words, never short ordinary words.
        if len(concept) >= 6 and vocabulary and concept not in vocabulary and token not in STOPWORDS:
            matches = get_close_matches(concept, vocabulary, n=1, cutoff=0.88)
            if matches and abs(len(matches[0]) - len(concept)) <= 1:
                concept = matches[0]
        concepts.append(concept)
        if set(tokens[max(0, index - 3):index]) & {"not", "never", "no"}:
            negated.add(concept)
    return Text(normalized, tokens, frozenset(concepts) - STOPWORDS, frozenset(negated))
