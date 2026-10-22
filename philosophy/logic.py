"""Reusable relationships, not exact-question answers.

Rules discuss distinctions without assuming the visitor endorses a mentioned
claim. Negated and hypothetical claims must not become attributed beliefs.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    id: str
    groups: tuple[tuple[str, ...], ...]
    cues: tuple[str, ...]
    position: str
    bridge: str
    distinction: str
    implication: str
    principles: tuple[str, ...]
    priority: int
    context: tuple[str, ...] = ()

    def applies(self, themes, text):
        return (all(set(group) & themes for group in self.groups)
            and (not self.cues or text.has_any(self.cues))
            and (not self.context or text.has_any(self.context)))


RULES = (
    Rule(
        id="material_suffering", groups=(("suffering",),),
        cues=("hunger", "poverty", "illness", "violence", "war", "abuse", "starvation"),
        position="Material suffering is not merely an interpretation that a person can think away.",
        bridge="Attention can change how a condition is lived, while illness, hunger and violence still require changes in material conditions.",
        distinction="An altered perspective is not a substitute for treatment, food or protection.",
        implication="Address the harmful condition first; examine added psychological distress without blaming the person for the harm.",
        principles=("suffering_and_conditions", "perception_and_reality"), priority=110,
    ),
    Rule(
        id="fate_not_passivity", groups=(("fate", "causality", "free_will"),),
        cues=("why bother", "point in trying", "try", "trying", "stop trying", "nothing matters", "meaningless", "give up", "doing nothing", "passivity"),
        position="The conclusion does not follow: being caused does not make a choice meaningless.",
        bridge="A heartbeat has causes and remains consequential; so does a decision. Effort and refusal are both conditions that affect what happens next.",
        distinction="Causal unfolding includes action; passive fatalism wrongly treats action as irrelevant to the unfolding.",
        implication="Ask which action changes a relevant condition, rather than whether action can exist outside all conditions.",
        principles=("conditioned_choice", "fate_through_action", "action_and_discipline"), priority=100,
    ),
    Rule(
        id="belief_not_external_fact", groups=(("perception",),),
        cues=("create", "creates", "change reality", "objective", "manifest", "becomes true", "makes it true", "believe", "belief"),
        position="Belief can change lived experience and behavior without making an external proposition true by conviction alone.",
        bridge="Interpretation can alter feeling; feeling can alter action; action can sometimes alter external conditions. That causal route is different from belief directly rewriting reality.",
        distinction="A perception's effect on the perceiver is not proof that its content is objectively correct.",
        implication="Test the belief against the world and distinguish a changed interpretation from a changed external condition.",
        principles=("perception_and_reality", "uncertainty_and_evidence"), priority=95,
    ),
    Rule(
        id="ignorance_not_evidence", groups=(("knowledge", "science"),),
        cues=("can not explain", "cannot explain", "unexplained", "do not know", "no explanation", "unknown", "no evidence"),
        position="A missing explanation does not establish a preferred spiritual or material explanation.",
        bridge="Showing that one account is incomplete leaves a gap; it does not supply the independent grounds needed for another account.",
        distinction="Unknown means unresolved, not impossible and not proven. A lack of disproof is not positive evidence.",
        implication="Ask what would distinguish the proposed explanation from its alternatives; if nothing settles it, say 'I do not know'.",
        principles=("uncertainty_and_evidence", "science_and_metaphysics"), priority=94,
        context=("therefore", "must", "prove", "proof", "evidence", "mean", "means", "imply", "spiritual", "supernatural", "god", "soul"),
    ),
    Rule(
        id="oneness_and_locality", groups=(("oneness",), ("individuality",)),
        cues=(),
        position="A local perspective can be experientially real even if ultimate separation remains open to question.",
        bridge="A structure with particular senses and a particular history has a localized point of view. Like a wave in an ocean, local form need not imply a separate underlying substance.",
        distinction="This makes individuality and metaphysical oneness conceptually compatible; it does not prove the universe is one conscious subject.",
        implication="Keep the local experience real while treating a universal consciousness as a possibility requiring further grounds.",
        principles=("one_and_many", "localized_perspective", "universe_experiencing_itself"), priority=90,
    ),
    Rule(
        id="intelligence_not_consciousness", groups=(("ai",), ("consciousness",)),
        cues=(),
        position="Intelligent behavior does not by itself establish subjective experience.",
        bridge="A machine can model relationships, produce language and participate in human systems while the question of whether it experiences anything remains unresolved.",
        distinction="Observable capability and consciousness are distinct claims; neither fluent speech nor complexity alone closes the gap.",
        implication="Evaluate what the system does and what evidence could bear on experience without assuming AI consciousness.",
        principles=("ai_as_nature", "consciousness_and_limits"), priority=88,
    ),
    Rule(
        id="consciousness_not_intelligence", groups=(("consciousness",),),
        cues=("intelligence", "intelligent", "language", "reasoning", "smart"),
        position="Intelligence and subjective experience are distinct: one does not establish the other by definition.",
        bridge="Solving a problem describes a capability; experiencing anything while doing so is a further question. Human language is not the only conceivable form of experience.",
        distinction="Differences in intelligent behavior do not by themselves measure or prove the presence or absence of consciousness.",
        implication="Ask separately about observable capacities and the grounds for attributing subjective experience.",
        principles=("consciousness_and_limits",), priority=87,
    ),
    Rule(
        id="determinism_and_agency", groups=(("free_will",), ("causality", "fate", "action")),
        cues=(),
        position="A conditioned choice can still be a real cause; agency need not mean being an uncaused cause.",
        bridge="The conditions shaping a person also shape deliberation, and that deliberation can change the action that follows.",
        distinction="Causal dependence is different from causal irrelevance. An uncaused event would not automatically be mastery rather than randomness.",
        implication="Cultivate reflection and discipline as causes within the process, rather than requiring freedom from every cause.",
        principles=("conditioned_choice", "causal_unfolding", "action_and_discipline"), priority=80,
    ),
    Rule(
        id="regret_and_action", groups=(("counterfactuals",), ("free_will", "action")),
        cues=(),
        position="An imagined alternative can guide a future choice without becoming another past you actually lived.",
        bridge="The past supplies information about conditions; reflection on a missed alternative becomes one of the conditions of the next decision.",
        distinction="Learning from regret is different from proving an unconditioned capacity to have chosen otherwise in an identical total situation.",
        implication="Turn the counterfactual into repair or a changed habit rather than repeatedly inhabiting a history that did not occur.",
        principles=("counterfactual_learning", "conditioned_choice", "action_and_discipline"), priority=82,
    ),
    Rule(
        id="witness_not_personality", groups=(("awareness",),),
        cues=("thought", "thoughts", "personality", "emotion", "emotions", "fear", "who am i", "soul"),
        position="A changing thought or personality can be observed without exhausting the standpoint from which it is observed.",
        bridge="Calling fear an experience rather than a complete identity can create room to examine its claims before acting.",
        distinction="That experiential distinction does not prove an independently existing soul or a witness outside causality.",
        implication="Notice the experience, question its demand, and choose a response without pretending observation makes you unconditioned.",
        principles=("witness_and_identification", "conditioned_choice"), priority=72,
    ),
    Rule(
        id="purpose_not_function", groups=(("purpose",),),
        cues=("function", "structure", "designer", "design", "mission", "assigned", "participation"),
        position="Function, participation and purpose are related, but they are not interchangeable.",
        bridge="Structure enables certain functions, those functions enable participation, and that participation may acquire meaning without an external designer assigning it.",
        distinction="Describing what a thing does does not by itself establish what it morally ought to do or what a cosmic mind intended.",
        implication="Investigate a role's consequences and worth instead of treating an existing function as a guaranteed mission.",
        principles=("structure_and_purpose",), priority=75,
    ),
    Rule(
        id="science_not_metaphysical_proof", groups=(("science",),),
        cues=("metaphysics", "metaphysical", "spiritual", "quantum", "god", "soul", "prove", "proof", "proven"),
        position="An empirical result and a metaphysical interpretation of that result are different claims.",
        bridge="A scientific model constrains observable relationships; a stronger claim about ultimate reality needs its own argument and must not borrow certainty from the model.",
        distinction="Quantum uncertainty does not itself prove free will, a soul or a cosmic consciousness.",
        implication="Identify what was observed, what was inferred and what remains a possibility rather than a finding.",
        principles=("science_and_metaphysics", "uncertainty_and_evidence"), priority=74,
    ),
    Rule(
        id="purpose_through_action", groups=(("purpose",), ("action",)),
        cues=(),
        position="Meaning can develop through participation even without a guaranteed cosmic mission.",
        bridge="Your capacities enable actions; repeated actions shape relationships and contributions through which a purpose can become concrete.",
        distinction="A meaningful contribution need not prove that the universe assigned it, and effort does not guarantee every desired outcome.",
        implication="Choose a worthwhile form of participation and let its actual consequences inform the next step.",
        principles=("structure_and_purpose", "action_and_discipline"), priority=70,
    ),
)


def evaluate(scores, text):
    # Related themes may be retrieved, but a rule needs direct textual support
    # for every required group, not a chain of relationship boosts.
    supported = {item.theme for item in scores if item.direct >= 3}
    return tuple(sorted((rule for rule in RULES if rule.applies(supported, text)),
        key=lambda rule: (-rule.priority, rule.id)))
