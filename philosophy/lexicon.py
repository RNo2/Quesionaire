"""Weighted evidence and one-hop relationships; boosts never replace evidence."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    primary: tuple[str, ...]
    secondary: tuple[str, ...] = ()
    phrases: tuple[str, ...] = ()
    exclusions: tuple[str, ...] = ()


THEMES = {
    "causality": Theme(("causality", "cause", "determinism", "conditioned"),
        ("biology", "circumstance", "condition", "randomness", "quantum"),
        ("cause and effect", "everything has a cause", "prior conditions")),
    "free_will": Theme(("choice", "choose", "decision", "decide", "agency", "predetermined", "freedom"),
        ("control", "determinism"),
        ("free will", "could i have", "could have chosen", "chosen differently", "really choosing", "control of my life", "control my life", "am i free"),
        ("free shipping", "remote control", "birth control")),
    "fate": Theme(("fate", "predestination", "destined"), ("karma", "future", "predetermined"),
        ("written in advance", "pre written", "already written")),
    "counterfactuals": Theme(("regret", "mistake", "counterfactual"), ("past", "memory", "differently"),
        ("could i have", "different decision", "change the past", "chosen differently")),
    "awareness": Theme(("awareness", "witness", "soul", "thought", "impulse"),
        ("identity", "emotion", "personality", "observe", "mind", "ego"),
        ("who am i", "am i my thoughts", "higher consciousness", "after death")),
    "consciousness": Theme(("consciousness", "conscious", "experience"),
        ("mind", "living", "tree", "bird", "cell", "death"),
        ("subjective experience", "inner life", "after death", "what it is like", "plants feel", "trees feel", "animals feel", "have feelings")),
    "oneness": Theme(("unity", "universe", "ocean", "divine", "god"),
        ("wave", "whole", "creation", "creator"),
        ("one reality", "everything is one", "we are one", "one consciousness", "all connected")),
    "individuality": Theme(("individuality", "individual", "separate", "localized"),
        ("perspective", "self", "identity", "form"),
        ("feel separate", "different people", "many forms")),
    "purpose": Theme(("purpose", "meaning", "function", "structure", "participation"),
        ("mission", "designer", "design", "role", "contribution"),
        ("meaning of life", "point of life", "why am i here", "why do i exist"),
        ("meaning of this word", "python function", "data structure")),
    "perception": Theme(("perception", "belief", "believe", "interpretation", "subjective"),
        ("attention", "sense", "feeling", "perspective", "reality"),
        ("lived reality", "objective reality", "subjective reality", "create reality", "manifest reality")),
    "suffering": Theme(("suffering", "pain", "fear", "anxiety", "attachment", "desire", "hunger", "poverty", "illness", "violence", "war", "abuse", "starvation"),
        ("regret", "loss", "failure"),
        ("afraid of failing", "why am i afraid", "why do we suffer")),
    "knowledge": Theme(("knowledge", "uncertainty", "unknown", "certainty", "evidence"),
        ("know", "proof", "explanation", "explain", "doubt", "unexplained"),
        ("do not know", "can not explain", "not know", "no evidence")),
    "truth": Theme(("truth", "honesty", "reassurance", "comfort"), ("false", "contradiction", "flatter"),
        ("tell me i am right", "truth hurts", "feel better")),
    "science": Theme(("science", "physics", "empirical", "metaphysical"),
        ("quantum", "evidence", "proof", "spirit", "test", "god"),
        ("scientifically proven", "science can not explain", "beyond science")),
    "ai": Theme(("ai", "robot", "algorithm"), ("machine", "intelligence", "computer", "technology"),
        ("artificial intelligence", "language model", "machine intelligence")),
    "action": Theme(("action", "act", "discipline", "habit", "effort", "passivity"),
        ("try", "attention", "character", "learn", "change", "consequences"),
        ("why bother", "point in trying", "why should i try", "should i even try", "stop trying", "nothing matters", "doing nothing", "do nothing", "give up")),
}

RELATIONSHIPS = {
    "free_will": ("causality", "action", "fate", "awareness"),
    "causality": ("free_will", "action", "fate"),
    "fate": ("causality", "free_will", "action"),
    "counterfactuals": ("free_will", "action", "suffering"),
    "awareness": ("consciousness", "free_will", "individuality"),
    "consciousness": ("awareness", "oneness", "ai", "science"),
    "oneness": ("individuality", "consciousness", "science"),
    "individuality": ("oneness", "perception", "awareness"),
    "purpose": ("action", "oneness", "knowledge"),
    "perception": ("knowledge", "suffering", "individuality"),
    "suffering": ("awareness", "counterfactuals", "action"),
    "knowledge": ("science", "truth"),
    "truth": ("knowledge",),
    "science": ("knowledge", "consciousness"),
    "ai": ("consciousness", "causality", "purpose"),
    "action": ("causality", "free_will", "purpose"),
}

VOCABULARY = frozenset(word for theme in THEMES.values()
    for word in theme.primary + theme.secondary)
