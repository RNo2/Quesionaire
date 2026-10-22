"""Subject extraction and reusable domain bridges, independent of topic scores.

Profiles describe properties shared by many subjects, not answers to stored
questions. Unlisted nouns retain their wording and receive a grammatical kind.
No profile claims to establish the actual causes of an unfamiliar event.
"""

import re
from dataclasses import dataclass

from .classifier import QuestionType


@dataclass(frozen=True)
class Profile:
    id: str
    terms: tuple[str, ...]
    kind: str
    interpretation: str
    mechanism: str
    distinction: str
    implication: str
    lenses: tuple[str, ...]
    themes: tuple[str, ...] = ()


PROFILES = (
    Profile("coordination", ("traffic", "cities", "city", "transport", "roads", "crowds", "queue", "coordination", "congestion", "infrastructure"), "system",
        "A collective pattern can emerge from individually intelligible actions without anyone intending the aggregate result.",
        "When many agents share finite space, infrastructure or capacity, individually useful choices can obstruct one another. Constraints and coordination connect the parts to the outcome.",
        "A system's outcome cannot always be explained by blaming one participant; changing a constraint differs from demanding better intentions.",
        "Look for an intervention in shared constraints or coordination, while accounting for the people who bear its costs.",
        ("causality", "whole_parts", "participation"), ("causality",)),
    Profile("resources", ("money", "wealth", "income", "finance", "capital", "resources", "rich", "poor", "wealthy"), "resource",
        "Material capacity can widen practical options without making the chooser unconditioned.",
        "A resource changes which actions are feasible; desires, habits, relationships and social conditions still shape what is chosen. Expanded options and freedom from identification are different changes. Satisfying a desire is not the same capacity as examining whether that desire should command action.",
        "Possession alone establishes neither psychological freedom nor equal access to the opportunities a resource enables.",
        "Judge the resource by which constraints it actually removes, for whom, and which dependencies it may leave intact.",
        ("agency", "participation", "perception"), ("free_will", "action")),
    Profile("aesthetic_relation", ("art", "painting", "music", "poetry", "beauty", "beautiful", "aesthetic", "sculpture", "novel", "dance"), "experience",
        "Meaning can arise in a relationship between an organized form and an observer rather than reside wholly in either one.",
        "Form, rhythm, contrast or expression offer constraints; memory, attention and cultural history shape the response. Different experiences do not erase the features that make those responses possible.",
        "Neither 'everyone must feel the same' nor 'every interpretation is equally supported' follows from variation in experience.",
        "Attend both to the work's actual features and to the relation through which they become significant.",
        ("structure", "perception", "participation"), ("perception", "purpose")),
    Profile("institutions", ("law", "laws", "society", "justice", "legitimate", "legitimacy", "government", "institution", "authority", "policy", "democracy"), "institution",
        "An institution's power to organize behavior is different from its justification for doing so.",
        "Rules distribute permissions, obligations and consequences across people. A serious justification must examine whose agency is protected, whose burdens are imposed, and whether the reasons withstand criticism.",
        "Existing, being enforceable or serving a function does not by itself make an arrangement legitimate or just.",
        "Evaluate the arrangement by defensible reasons and its effects on actual lives, including those with the least power to contest it.",
        ("agency", "purpose", "truth"), ("action", "truth")),
    Profile("capability", ("technology", "progress", "machine", "tool", "tools", "device", "invention", "innovation", "automation", "computer"), "object",
        "An increase in capability is not automatically an improvement in the ends that capability serves.",
        "Structure enables a function; its use changes participation in larger systems. Calling something a tool describes a relation to a user without exhausting its effects or the habits and dependencies it can create.",
        "Progress requires a stated standard of improvement: greater power or speed is not by itself greater well-being.",
        "Examine what the capability enables, who directs it, and which consequences justify calling the change an improvement.",
        ("structure", "agency", "purpose"), ("purpose", "action")),
    Profile("competition", ("competition", "compete", "competitive", "rivalry", "contest", "ranking", "rank", "status", "rivals"), "relationship",
        "Competition is a relationship organized around comparison or incompatible aims, not an essence every human activity must possess.",
        "Scarce rewards, status comparisons or rules that reward relative performance can make rivalry a sensible local response. Repetition can then turn those incentives into habits even where cooperation is possible.",
        "Explaining a competitive impulse does not make competition inevitable everywhere or establish that it serves a worthwhile end.",
        "Distinguish the goal from the ranking, and change incentives or habits where comparison has displaced the activity's value.",
        ("causality", "participation", "agency"), ("causality", "action")),
    Profile("continuity", ("tradition", "traditions", "custom", "customs", "ritual", "rituals", "persist", "persisting", "inherit", "heritage"), "process",
        "Continuity can be produced by repeated participation rather than by an unchanging essence.",
        "Repetition, shared expectations and inherited practices can make a pattern easier to reproduce than to replace. Each enactment preserves parts of the past while occurring under changed conditions. Habits can preserve a practice after its original reasons have weakened.",
        "Persistence shows that a pattern has been sustained, not that it is justified, timeless or immune to revision.",
        "Retain what withstands examination, and change a practice when its consequences no longer justify its continuation.",
        ("change", "causality", "truth"), ("action",)),
    Profile("communication", ("names", "name", "naming", "silence", "silent", "words", "word", "language", "speech", "symbol", "symbols", "communication"), "relationship",
        "Meaning depends on a relation between a sign, its context and the people interpreting it.",
        "Naming can stabilize distinctions and coordinate attention without creating the things named. Silence can mark a pause or acquire significance through an expectation of speech; its meaning is not contained in absence alone.",
        "A shared label does not prove a shared essence, and an interpretation of an absent signal is not proof of another person's intention.",
        "Distinguish the sign, the thing or situation it concerns, and the interpretation the context actually supports.",
        ("perception", "participation", "structure"), ("perception",)),
    Profile("values", ("efficiency", "happiness", "prioritize", "priority", "priorities", "wellbeing", "welfare"), "decision",
        "A means cannot settle the value of the end it serves.",
        "Efficiency concerns the relation between means and an intended result; happiness concerns a quality of lived experience. Optimizing a process can undermine its purpose when the measure replaces the life it was meant to improve.",
        "Neither speed nor momentary satisfaction is a sufficient standard for every decision; constraints, enduring consequences and effects on others matter.",
        "Choose a defensible end first, then treat efficiency as a conditional aid rather than an overriding command.",
        ("purpose", "agency", "perception"), ("purpose", "action")),
    Profile("mortality", ("death", "mortality", "dying", "die", "dead"), "experience",
        "Anticipated loss can become present suffering before the event itself occurs.",
        "Self-preservation, attachment to people and projects, and uncertainty about the end of experience are possible conditions of fear. Awareness can observe that anticipation without treating every imagined outcome as a present fact.",
        "The wish for continuity does not establish survival after death, and uncertainty about death is not proof of either a comforting or a frightening metaphysical story.",
        "Let awareness of finitude inform present action and care without confusing a feared image with knowledge of what lies beyond experience.",
        ("perception", "change", "knowledge"), ("suffering", "knowledge")),
    Profile("learning", ("mistake", "mistakes", "error", "errors", "failure", "failed", "learning", "learn"), "event",
        "A mistake can become valuable through what it changes, without becoming right in retrospect.",
        "An unwanted result can expose a false assumption or ineffective habit. Reflection becomes consequential when it changes later action, repairs harm or prevents repetition.",
        "Learning from an error does not mean the harm was necessary or that all mistakes should be welcomed.",
        "Extract the lesson, make available repair, and embody the learning in a changed condition or habit.",
        ("change", "agency", "truth"), ("counterfactuals", "action")),
    Profile("patterns", ("order", "chaos", "pattern", "patterns", "disorder", "stability", "unstable", "emergence"), "system",
        "Order and chaos concern how patterns and constraints relate, rather than two independent substances fighting for control.",
        "A pattern can persist under some conditions and break down when those conditions change. What appears irregular at one scale may coexist with constraints at another; unpredictability is not the same claim as absence of causes.",
        "This is a conceptual distinction, not proof that every apparently chaotic process has been explained or can be predicted.",
        "Specify the scale, the pattern and the conditions before turning either order or chaos into an ultimate explanation.",
        ("change", "whole_parts", "causality"), ("causality",)),
)

# A word's technical sense should not silently become a human motive or rule.
PROFILE_EXCLUSIONS = {
    "institutions": frozenset(("physics", "gravity", "thermodynamics", "physical", "scientific")),
    "mortality": frozenset(("battery", "circuit", "engine", "electrical")),
    "competition": frozenset(("http", "server", "code", "request", "response")),
}


@dataclass(frozen=True)
class Subject:
    label: str
    kind: str
    profile: Profile | None
    pair: tuple[str, str] | None
    predicate: str
    factual: bool
    premise: str

    @property
    def quoted(self):
        return f"“{self.label}”"


def _short(text, limit=150):
    text = text.strip()
    if len(text) <= limit:
        return text
    shortened = text[:limit].rsplit(" ", 1)[0]
    return shortened + "…"


def extract_subject(text, intent):
    question = text.normalized
    tokens = set(question.split())
    ranked = [
        (sum(word in tokens for word in p.terms)
         if not tokens & PROFILE_EXCLUSIONS.get(p.id, frozenset()) else 0, p)
        for p in PROFILES
    ]
    ranked.sort(key=lambda item: (-item[0], item[1].id))
    profile = ranked[0][1] if ranked[0][0] else None
    factual = bool(re.search(
        r"^(?:who (?:won|invented|discovered)|when (?:did|was|were)|where is|how (?:many|much)|what (?:year|date)|what is the (?:capital|current|price|score|weather))\b",
        question))
    pair = None
    match = re.search(r"(?:between )(.+?) and (.+)$", question)
    if not match:
        match = re.search(r"^how (?:do|does) (.+?) and (.+?) differ$", question)
    if not match:
        match = re.search(r"^is (.+?) (?:different from|the same as|versus|vs) (.+)$", question)
    if match:
        pair = (_short(match[1], 65), _short(match[2], 65))
    premise = ""
    if intent in (QuestionType.HYPOTHETICAL, QuestionType.CONSEQUENCES, QuestionType.CHALLENGE):
        premise = re.sub(r"^(?:what (?:would )?happens? |what |suppose |imagine )?(?:if )?", "", question)
    label = question
    # Strip an operation, preserving the actual unknown nouns and predicates.
    patterns = (
        r"^what (?:is|are) the relationship between (.+)$",
        r"^what makes (.+?)(?: happen| occur| meaningful| legitimate| valuable| just)$",
        r"^what (?:is|are) (.+?) for$",
        r"^what causes (.+)$",
        r"^what does (.+) mean$",
        r"^where (?:does|do) (.+?) come from$",
        r"^how (?:could|can|do) (?:we|i) know (?:whether |if )?(.+)$",
        r"^(?:why|how) (?:do|does|did|is|are|can|should|would) (.+?)(?: work)?$",
        r"^(?:what|who) (?:is|are) (.+)$",
        r"^(?:am|is|are|does|do|can|could|should|would) (.+)$",
        r"^(?:what if|suppose|imagine) (.+)$",
    )
    for pattern in patterns:
        match = re.match(pattern, question)
        if match:
            label = match[1]
            break
    if pair:
        label = f"{pair[0]} and {pair[1]}"
    predicate_match = re.search(r"\b(meaningful|legitimate|valuable|objective|justified|real|true|progress|merely a tool|just|free)$", question)
    predicate = predicate_match[1] if predicate_match else ""
    made = re.match(r"(.+?) (?:make|makes) .+? (?:free|happy|meaningful)$", label)
    if made:
        label = made[1]
    match = re.match(r"(.+?) (?:is |are )?(meaningful|legitimate|valuable|objective|justified|real|true|progress|merely a tool|just|free)$", label)
    if match:
        label, predicate = match[1], match[2]
    label = re.sub(r"\s+(?:be|is|are)$", "", label)
    if profile and profile.id == "coordination":
        location = re.match(r"(.+?) (?:have|has) (.+)$", label)
        if location:
            label = f"{location[2]} in {location[1]}"
    if not label:
        label = "the expression itself"
    kind = profile.kind if profile else "concept"
    if not profile:
        if intent in (QuestionType.CAUSAL, QuestionType.EXPLANATION, QuestionType.MECHANISM, QuestionType.CONSEQUENCES):
            kind = "process"
        elif intent in (QuestionType.NORMATIVE, QuestionType.PRACTICAL):
            kind = "decision"
        elif intent == QuestionType.PERSONAL:
            kind = "experience"
        elif intent in (QuestionType.TRUTH, QuestionType.HYPOTHETICAL, QuestionType.CHALLENGE, QuestionType.EPISTEMIC):
            kind = "claim"
        if tokens & {"rain", "weather", "volcano", "tides", "earthquake", "storm"}:
            kind = "natural phenomenon"
    return Subject(_short(label), kind, profile, pair, predicate, factual, _short(premise))
