"""Permanent worldview lenses and intent-sensitive philosophical interpretation.

This layer is always available. Topic retrieval can enrich an argument, never
decide whether there is an argument. Templates express conditional reasoning,
not unverified factual knowledge about an unfamiliar noun.
"""

from dataclasses import dataclass

from .classifier import QuestionType
from .composer import AnswerPlan


@dataclass(frozen=True)
class Lens:
    id: str
    claim: str
    reasoning: str
    qualification: str
    implication: str
    themes: tuple[str, ...]


LENSES = {
    lens.id: lens for lens in (
        Lens("causality",
            "An occurrence is explained by the conditions that produce or sustain it, not by giving it another name.",
            "An enabling condition, a trigger and a sustaining feedback can play different roles. Changing one condition can change what follows without requiring an uncaused intervention.",
            "A plausible causal story is not yet evidence that those were the actual causes in this case.",
            "Prefer an account that identifies what would change the outcome over a label that merely repeats it.",
            ("causality", "fate")),
        Lens("structure",
            "Organization constrains what a thing can do; a name alone does not disclose that organization.",
            "Distinguishing a subject's parts, constraints and capacities connects what it is to what it enables, without assuming that every function was designed in advance.",
            "Describing a capacity does not establish a cosmic intention or exhaust the subject's significance.",
            "Understand the arrangement and its effects before assigning it a final essence or mission.",
            ("purpose", "ai", "consciousness")),
        Lens("participation",
            "Significance can emerge through participation rather than belong to a thing in isolation.",
            "A role depends on relations: change the surrounding practices, participants or constraints and the same local capacity can acquire different consequences and meaning.",
            "A useful role in one arrangement is not automatically a justified role in every arrangement.",
            "Evaluate both the local contribution and the wider relationships it sustains.",
            ("oneness", "individuality", "purpose")),
        Lens("perception",
            "An experience and the interpretation placed upon it are distinguishable, even when they feel inseparable.",
            "Memory, expectation and attention shape lived reality. Those effects can alter behavior without making an interpretation true merely because it feels compelling.",
            "Variation in experience neither erases external constraints nor proves that every interpretation is equally sound.",
            "Keep the situation, its felt significance and the evidence for an interpretation distinct.",
            ("perception", "awareness", "suffering")),
        Lens("agency",
            "Conditioned action remains consequential: deliberation is part of what shapes the next state.",
            "A decision links available means to an end under constraints. Consequences include effects on other people and on the habits that make later choices easier or harder.",
            "Influencing an outcome is not controlling every condition, and explaining a choice does not justify its effects.",
            "Choose a defensible end, act on the conditions available, and revise the action in light of its consequences.",
            ("free_will", "action", "fate")),
        Lens("knowledge",
            "A claim should be no stronger than its grounds, even when a stronger claim would be comforting.",
            "Observation, inference and assumption do different work. A missing explanation leaves room for inquiry without becoming positive evidence for a preferred story.",
            "A philosophical interpretation is not a verified report of an external event.",
            "Let evidence constrain belief while using uncertainty to guide inquiry rather than manufacture certainty.",
            ("knowledge", "science", "truth")),
        Lens("change",
            "What persists may be a pattern continually reproduced under changing conditions, not an untouched substance.",
            "A later state inherits constraints from an earlier one while new interactions can alter the pattern. Repetition connects continuity with the possibility of revision.",
            "Survival of a pattern does not establish that it is necessary, good or beyond criticism.",
            "Distinguish what is being preserved from the conditions that keep reproducing it.",
            ("counterfactuals", "action")),
        Lens("purpose",
            "What something does and what makes it worth doing are different questions.",
            "Structure enables function, function enables participation, and purpose can emerge through that participation. An assigned cosmic mission is a stronger and separate claim.",
            "A description of an existing function does not by itself establish a moral duty to preserve it.",
            "Judge participation by its consequences and defensible ends rather than mistaking an existing role for a guaranteed purpose.",
            ("purpose",)),
        Lens("whole_parts",
            "A whole can have patterns that are not visible when its parts are considered separately.",
            "Each participant acts under local conditions, but shared constraints connect those acts. An aggregate result can differ from what any participant intended.",
            "Interdependence does not prove a single cosmic mind or make local differences unreal.",
            "Connect the local action to the wider arrangement instead of treating either level as the entire explanation.",
            ("individuality", "oneness")),
        Lens("truth",
            "A conclusion needs a valid connection to its premises, not merely an appealing association.",
            "An example does not prove a universal claim, and rejecting one explanation does not establish its rival. A framework must remain open to the criticism it applies to others.",
            "Conviction and discomfort are neither evidence nor refutation by themselves.",
            "Retain the part of the claim its reasons support, and revise the part that depends on an unsupported leap.",
            ("truth", "knowledge")),
    )
}

INTENT_LENSES = {
    QuestionType.DEFINITION: ("structure", "participation", "knowledge"),
    QuestionType.EXPLANATION: ("causality", "whole_parts", "change"),
    QuestionType.CAUSAL: ("causality", "change", "knowledge"),
    QuestionType.MECHANISM: ("structure", "causality", "participation"),
    QuestionType.TRUTH: ("truth", "knowledge", "perception"),
    QuestionType.NORMATIVE: ("agency", "purpose", "participation"),
    QuestionType.PRACTICAL: ("agency", "causality", "truth"),
    QuestionType.COMPARISON: ("structure", "participation", "truth"),
    QuestionType.HYPOTHETICAL: ("causality", "knowledge", "change"),
    QuestionType.CONSEQUENCES: ("change", "causality", "agency"),
    QuestionType.PERSONAL: ("perception", "agency", "causality"),
    QuestionType.PURPOSE: ("purpose", "structure", "participation"),
    QuestionType.EXISTENTIAL: ("purpose", "participation", "agency"),
    QuestionType.EPISTEMIC: ("knowledge", "truth", "perception"),
    QuestionType.CHALLENGE: ("truth", "causality", "agency"),
}

KIND_LENSES = {
    "object": ("structure", "purpose"),
    "process": ("causality", "change"),
    "event": ("change", "causality"),
    "experience": ("perception", "knowledge"),
    "decision": ("agency", "purpose"),
    "relationship": ("participation", "perception"),
    "claim": ("knowledge", "truth"),
    "system": ("whole_parts", "participation"),
    "institution": ("agency", "truth"),
    "natural phenomenon": ("causality", "knowledge"),
    "concept": ("structure", "knowledge"),
    "resource": ("agency", "participation"),
}


def choose_lenses(intent, subject, scores):
    weights = {id: 0 for id in LENSES}
    for weight, id in zip((6, 4, 2), INTENT_LENSES[intent]):
        weights[id] += weight
    for weight, id in zip((2, 1), KIND_LENSES[subject.kind]):
        weights[id] += weight
    if subject.profile:
        for weight, id in zip((5, 4, 3), subject.profile.lenses):
            weights[id] += weight
    for score in scores:
        if score.direct >= 3:
            for lens in LENSES.values():
                if score.theme in lens.themes:
                    weights[lens.id] += min(8, 4 + score.direct / 2)
    if subject.factual:
        weights["knowledge"] += 20
    return tuple(LENSES[id] for id in sorted(weights, key=lambda id: (-weights[id], id))[:3])


def _lower_first(sentence):
    return sentence[:1].lower() + sentence[1:]


def interpret(subject, intent, lenses):
    """Produce a substantive path even for a completely unrecognized noun."""
    focus = subject.quoted
    primary, secondary = lenses[:2]
    profile = subject.profile
    if subject.factual:
        return AnswerPlan(
            f"A claim about {focus} concerns an external event, identity or measurement. Its truth depends on what happened, not on which answer would be satisfying.",
            ("A record or reliable observation can support the particular fact. Philosophically, the event and its meaning are distinct: an outcome describes what occurred, while judging its importance adds a relation to goals, rules or expectations.",),
            "No particular name, result or number follows from the question's wording alone; interpreting a fact must not be passed off as observing it.",
            "Keep verification separate from evaluation. Let the established event inform your response rather than letting preference decide what the event supposedly was.",
        )
    if profile:
        position = f"For {focus}, {_lower_first(profile.interpretation)}"
        reasoning = (profile.mechanism,)
        distinction, implication = profile.distinction, profile.implication
    else:
        position = f"Concerning {focus}, {_lower_first(primary.claim)}"
        reasoning = (primary.reasoning, secondary.reasoning)
        distinction, implication = primary.qualification, primary.implication

    if intent == QuestionType.DEFINITION:
        if not profile:
            position = f"A philosophical definition of {focus} should distinguish its organization, its capacities and the relations in which the term has a use. A label alone does not establish an essence."
    elif intent == QuestionType.COMPARISON:
        if subject.pair and not profile:
            a, b = subject.pair
            position = f"The decisive comparison between “{a}” and “{b}” concerns their roles, constraints and effects, rather than their names alone. A shared effect need not mean an identical structure or purpose."
    elif intent in (QuestionType.NORMATIVE, QuestionType.PRACTICAL):
        position = f"A defensible approach to {focus} must connect the choice to its ends, constraints and consequences. " + (profile.interpretation if profile else "Being conditioned does not remove responsibility for the effects an available action can change.")
    elif intent == QuestionType.PERSONAL and not profile:
        position = f"The experience described by {focus} can be real without making its interpretation a fact or an impulse a command. Noticing the experience creates room to examine how it shapes action."
    elif intent in (QuestionType.HYPOTHETICAL, QuestionType.CONSEQUENCES):
        position = f"Take “{subject.premise or subject.label}” as an assumption for the argument. " + (profile.interpretation if profile else "A changed condition can alter what follows; it does not follow that every relationship or consequence changes in the same way.")
    elif intent == QuestionType.EPISTEMIC:
        position = f"Knowing whether {focus} requires separating what is observed, what is inferred and what is assumed. An account becomes stronger when evidence distinguishes it from rival explanations."
    elif intent == QuestionType.CHALLENGE and not profile:
        position = f"The apparent conflict in {focus} should be tested at the link between premise and conclusion. A dependence between events does not by itself make either event unreal or inconsequential."
    elif intent in (QuestionType.EXPLANATION, QuestionType.CAUSAL) and not profile:
        position = f"The occurrence described by {focus} should be examined as a process conditioned by earlier events, present constraints and interactions. Naming the pattern is not yet explaining it."
    elif intent == QuestionType.MECHANISM and not profile:
        position = f"To understand how {focus} works, connect its organization to the effects it enables. A mechanism explains the steps and constraints linking one state to the next, rather than merely naming an outcome."
    elif intent in (QuestionType.PURPOSE, QuestionType.EXISTENTIAL) and not profile:
        position = f"The purpose of {focus} can be investigated through participation: what it enables and which relationships it sustains. That meaning need not imply a mission assigned by a cosmic designer."
    if subject.predicate in ("real", "true", "justified") and not profile:
        position = f"Calling {focus} {subject.predicate} requires a distinction between an experience, an interpretation and a claim about what exists independently of that experience. The force of a feeling does not settle all three."
    return AnswerPlan(position, reasoning, distinction, implication)
