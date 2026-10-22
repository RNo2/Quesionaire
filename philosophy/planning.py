"""Direct answer -> connected reasons -> implication -> complication -> limit.

Topic scores can select support. Neither a score nor an objection is allowed
to replace an answer after the central demand has been resolved.
"""

from dataclasses import dataclass
import re

from .classifier import QuestionType as Q
from .composer import AnswerPlan, select
from .concepts import CHAINS, MODELS_BY_ID, SYNTHESES
from .demand import conflicting_predications


@dataclass(frozen=True)
class PlannedAnswer:
    plan: AnswerPlan
    concept_ids: tuple[str, ...]
    chain_ids: tuple[str, ...]
    principle_ids: tuple[str, ...]
    applied_rule_ids: tuple[str, ...]


def direct_position(text, demand, model):
    operation = demand.operation
    if operation == Q.DEFINITION:
        return model.principle.definition
    if operation == Q.EXISTENCE:
        return model.existence or select(model.interpretation, text.normalized, "existence")
    if operation in (Q.EXPLANATION, Q.CAUSAL, Q.MECHANISM, Q.PERSONAL):
        emotion = re.search(r"\b(?:fear|afraid of|anxious about) (.+)$", demand.subject.label)
        if model.id == "suffering" and emotion:
            return (f"Fear about “{emotion[1]}” can arise from anticipated harm, attachment and uncertainty, "
                "even before the imagined outcome occurs.")
        return model.explanation
    if operation in (Q.NORMATIVE, Q.PRACTICAL):
        return model.conduct
    if operation == Q.EPISTEMIC:
        return f"A justified account of {model.label} must distinguish the concept's meaning from evidence for the stronger claims made about it."
    if operation == Q.HYPOTHETICAL:
        position = select(model.interpretation, text.normalized, "hypothesis")
        return f"Under the assumption described by “{demand.subject.premise or demand.subject.label}”, {position[:1].lower() + position[1:]}"
    return select(model.interpretation, text.normalized, "position")


def construct_plan(text, demand, universal_plan, rules, retrieved):
    if demand.subject.factual:
        return PlannedAnswer(universal_plan, (), (), tuple(p.id for p in retrieved), ())
    matches = demand.concepts
    primary = matches[0].model if matches else None
    # An incidental concept must not displace an unfamiliar central subject:
    # e.g. money's material options are not answered by a definition of choice.
    if matches and not matches[0].is_subject:
        primary = None
    if primary is None:
        # Universal/profile reasoning remains constructive for unfamiliar nouns.
        # Retain relevant distinctions without handing them control of opening.
        relevant = tuple(rule for rule in rules
            if set(rule.principles) & {p.id for p in retrieved})
        distinction = universal_plan.distinction
        if relevant:
            distinction = relevant[0].distinction
        position = universal_plan.position
        # Attribute questions can have an unfamiliar entity as their subject.
        # Resolve the attribution, not a definition of an incidental concept.
        if matches and matches[0].model.id == "consciousness" and demand.operation in (Q.TRUTH, Q.EXISTENCE):
            position = (f"Whether {demand.subject.quoted} has subjective experience is distinct from whether it displays complex behavior; "
                "complexity or the absence of human language alone does not settle consciousness.")
        plan = AnswerPlan(position, universal_plan.reasoning,
            distinction, universal_plan.implication)
        return PlannedAnswer(plan, (), (), tuple(p.id for p in retrieved),
            tuple(rule.id for rule in relevant[:1]))

    chain = CHAINS[primary.chain_id]
    position = direct_position(text, demand, primary)
    reasons = tuple(edge.reasoning for edge in chain.edges[:2])
    implication = chain.consequence
    complication = ""
    qualification = primary.qualification or primary.principle.qualifications[0]
    applied = []
    chain_ids = [chain.id]
    principle_ids = list(primary.principle_ids)

    conflict = conflicting_predications(text, demand)
    active = {match.model.id for match in matches}
    synthesis = next((candidate for candidate in SYNTHESES
        if demand.operation.value in candidate.operations
        and all(set(group) & active for group in candidate.groups)), None)
    if conflict:
        a, b = conflict
        left, right = MODELS_BY_ID[a.concept].label, MODELS_BY_ID[b.concept].label
        position = (f"If {left} and {right} name the same reality in the same respect, "
            f"that reality cannot consistently be both {a.attribute} and not {a.attribute}.")
        reasons = ("The contradiction concerns properties attributed to the same whole. A conscious local being and a whole without one unified experience are not the same subject, so their different properties need not contradict each other.",)
        implication = "Resolve the tension by keeping the referent and level of description consistent, rather than transferring a part's property to the whole or changing definitions mid-argument."
        complication = "Separating the two referents removes the identity premise, but also changes the interpretation being tested."
        applied.append("same_reference_consistency")
    elif demand.operation == Q.COMPARISON and len(matches) >= 2:
        other = matches[1].model
        if primary.reference_group and primary.reference_group == other.reference_group:
            position = (f"In this interpretation, {primary.label} and {other.label} "
                "name the same underlying reality under different descriptions, rather than an external maker and an independent product.")
        else:
            position = primary.principle.definition + " " + other.principle.definition
        principle_ids.extend(other.principle_ids)
    elif synthesis:
        position, implication = synthesis.conclusion, synthesis.implication
        chain_ids = list(synthesis.chain_ids)
        reasons = tuple(CHAINS[id].edges[0].reasoning for id in chain_ids)
        if len(chain_ids) == 1:
            reasons += (CHAINS[chain_ids[0]].edges[1].reasoning,)
        applied.append(synthesis.id)
        for match in matches:
            principle_ids.extend(match.model.principle_ids)
    elif text.has_any(("prove", "proves", "proof", "establish", "establishes")) and primary.chain_id == "epistemic_grounds" and len(matches) > 1:
        target = matches[1].model
        if target.chain_id != "epistemic_grounds":
            position = (f"Evidence about {primary.label} does not automatically establish a philosophical claim about {target.label}; "
                "the connection requires its own argument.")
    elif demand.operation in (Q.TRUTH, Q.CHALLENGE) and text.has_any(("therefore", "must", "means", "implies")):
        gap = next((rule for rule in rules if rule.id == "ignorance_not_evidence"), None)
        if gap:
            position = gap.position
            reasons = (primary.explanation, gap.bridge)
            applied.append(gap.id)

    # Add only a complication relevant to this concept. It cannot rewrite the
    # position or substitute broad uncertainty for a substantive interpretation.
    if not complication:
        relevant = [rule for rule in rules if set(rule.principles) & set(primary.principle_ids)]
        if relevant:
            complication = relevant[0].distinction
            applied.append(relevant[0].id)
    if chain.analogy and demand.operation == Q.DEFINITION:
        # The analogy explains the concept; it is never offered as its proof.
        reasons += (chain.analogy,)
    if demand.operation in (Q.NORMATIVE, Q.PRACTICAL):
        implication = primary.principle.conclusions[0]
    plan = AnswerPlan(position, reasons, complication, implication,
        qualification=qualification)
    return PlannedAnswer(plan, tuple(match.model.id for match in matches),
        tuple(chain_ids), tuple(dict.fromkeys(principle_ids)), tuple(dict.fromkeys(applied)))
