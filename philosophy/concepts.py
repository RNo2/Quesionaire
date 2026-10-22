"""Constructive concept models and directed arguments, not question/answer pairs.

Principles supply claims and limits. These models explain how those claims
relate, and what a definition, explanation, existence claim or decision needs
to establish. No entry is keyed by a complete visitor question.
"""

from dataclasses import dataclass

from .knowledge import PRINCIPLES_BY_ID


@dataclass(frozen=True)
class Relation:
    source: str
    relation: str
    target: str
    reasoning: str


@dataclass(frozen=True)
class ConceptualChain:
    id: str
    edges: tuple[Relation, ...]
    consequence: str
    analogy: str = ""


CHAINS = {
    chain.id: chain for chain in (
        ConceptualChain("unity_expression", (
            Relation("underlying_reality", "differentiates_into", "structures",
                "One underlying reality may differentiate into structures without those forms becoming absolutely separate substances."),
            Relation("structures", "support", "functions_and_experiences",
                "Different structures can sustain distinct functions and experiences, giving local beings their own histories and perspectives."),
            Relation("functions_and_experiences", "localize", "individuality",
                "Individuality is therefore compatible with participation in a whole: distinctness need not mean independence from everything else."),
        ), "On this interpretation, unity and real local differences coexist; participation does not erase particular lives.",
            "A cell has its own structure and activity within a body; the analogy illustrates the relation without proving the universe is an organism."),
        ConceptualChain("conditioned_agency", (
            Relation("prior_conditions", "shape", "dispositions",
                "Biology, memory, temperament and circumstance shape what a person notices, wants and can consider."),
            Relation("dispositions", "condition", "deliberation_and_action",
                "Deliberation, resistance and action arise within those conditions while also changing what follows."),
            Relation("deliberation_and_action", "produce", "consequences",
                "Their consequences become subsequent conditions, so learning and habit can alter later decisions."),
            Relation("consequences", "become", "prior_conditions",
                "The process feeds back into the chooser rather than leaving the chooser outside causality."),
        ), "Being caused is not being causally irrelevant: understanding the chain gives deliberate action a place within it."),
        ConceptualChain("counterfactual_learning", (
            Relation("remembered_outcome", "is_compared_with", "imagined_alternative",
                "Memory retains the actual outcome while imagination constructs an alternative from present knowledge, expectations and desires."),
            Relation("imagined_alternative", "can_inform", "learning_and_repair",
                "Comparing the two can reveal a missed condition or harmful habit, but the imagined history does not become another event that actually occurred."),
            Relation("learning_and_repair", "can_change", "subsequent_conditions",
                "Learning matters when it informs repair, preparation or a different response in a later situation."),
        ), "Let the alternative become information for a real next action, rather than a second past in which to remain trapped."),
        ConceptualChain("purpose_participation", (
            Relation("structure", "enables", "function",
                "A structure constrains the functions available to it; not every form can do every thing."),
            Relation("function", "enables", "participation",
                "Those functions enable participation in relationships and larger systems."),
            Relation("participation", "can_acquire", "purpose",
                "A role can acquire purpose through its contribution and interpretation, without a cosmic designer assigning each object a mission."),
        ), "A purpose can be cultivated through worthwhile participation rather than awaited as a guaranteed external assignment."),
        ConceptualChain("localized_experience", (
            Relation("structure", "constrains", "capacities",
                "A being's organization constrains what it can sense, integrate and respond to."),
            Relation("capacities", "situate", "experience",
                "Where experience occurs, those capacities and the being's history give it a localized perspective rather than an unrestricted view of everything."),
            Relation("experience", "differs_from", "intelligent_behavior",
                "Experiencing something and performing an intelligent task remain different claims, even when the same system may do both."),
        ), "A local perspective can be real without being the whole of reality or proof of a separate metaphysical substance."),
        ConceptualChain("witness_contents", (
            Relation("changing_contents", "are_noticed_in", "awareness",
                "Thoughts, feelings and impulses change, while those changes can themselves be noticed."),
            Relation("awareness", "can_loosen", "identification",
                "Noticing a thought as an experience can loosen the assumption that it is a command or a complete identity."),
            Relation("identification", "affects", "response",
                "That distinction can change the response, even if observation and restraint are also conditioned capacities."),
        ), "Witnessing is useful as a standpoint for examining experience, without requiring every passing thought to define the self."),
        ConceptualChain("lived_reality", (
            Relation("perception", "shapes", "understanding",
                "Senses, memory and expectation shape perception, which shapes what a situation is understood to mean."),
            Relation("understanding", "shapes", "feeling_and_action",
                "Understanding shapes feeling and action; action can then change external conditions through an ordinary causal route."),
            Relation("feeling_and_action", "do_not_guarantee", "objective_truth",
                "That route does not make a belief objectively true simply because the belief is intense or reassuring."),
        ), "Change mistaken interpretations where possible and act on external conditions where those require change."),
        ConceptualChain("suffering_amplification", (
            Relation("harmful_conditions", "can_produce", "distress",
                "Illness, loss, violence and deprivation can produce distress through real conditions rather than through a failure to think positively."),
            Relation("memory_and_anticipation", "can_amplify", "distress",
                "Memory can repeatedly reopen a loss, while anticipation makes an imagined outcome a present source of fear."),
            Relation("distress", "can_be_addressed_through", "attention_and_action",
                "Attention can distinguish the present condition from added interpretation, while practical action addresses what can actually be relieved."),
        ), "Respond to both the real condition and the mental processes adding to it, without blaming the sufferer for either."),
        ConceptualChain("epistemic_grounds", (
            Relation("observation", "constrains", "inference",
                "Evidence constrains which accounts remain credible; a coherent account is not established merely by being imaginable."),
            Relation("inference", "supports", "proportionate_conclusion",
                "A conclusion should distinguish what follows from its premises from what has only been assumed."),
            Relation("proportionate_conclusion", "permits", "revision",
                "Criticism can improve the conclusion without substituting endless doubt for a defensible position."),
        ), "Reach the conclusion its grounds support, and name the specific question those grounds leave open."),
        ConceptualChain("nature_intelligence", (
            Relation("nature", "produces", "human_organization",
                "Humans arise within nature, and their technical activity remains part of the same physical history."),
            Relation("human_organization", "builds", "artificial_capacities",
                "Machines extend capacities for modeling, prediction and action through new kinds of structure."),
            Relation("artificial_capacities", "do_not_entail", "subjective_experience",
                "An expanded ability to process information does not by itself establish an inner life."),
        ), "Assess capabilities and consequences without treating either fluent behavior or artificial construction as a final answer about consciousness."),
    )
}


@dataclass(frozen=True)
class ConceptModel:
    id: str
    label: str
    aliases: tuple[str, ...]
    principle_ids: tuple[str, ...]
    chain_id: str
    interpretation: tuple[str, ...]
    explanation: str
    conduct: str
    existence: str = ""
    reference_group: str = ""
    exclusions: tuple[str, ...] = ()
    qualification: str = ""

    @property
    def principle(self):
        return PRINCIPLES_BY_ID[self.principle_ids[0]]


MODELS = (
    ConceptModel("god", "God", ("god", "divinity", "deity", "the divine", "creator"),
        ("divine_totality", "one_and_many", "universe_experiencing_itself"), "unity_expression",
        ("God can be understood as the underlying totality of existence, expressing itself through the universe rather than standing outside creation.",
         "God may name existence itself: the one reality appearing through many forms, rather than necessarily a separate personal maker."),
        "If God names the underlying reality, creator and creation are not two independent substances: the many forms express the reality to which they belong.",
        "Treat a relation to God as participation in existence, without pretending that this grants knowledge of a cosmic person's intentions.",
        "If God means the underlying totality, existence itself is what the term names; whether that totality is also a conscious personal creator is a separate claim.",
        reference_group="underlying_reality"),
    ConceptModel("totality", "the universe", ("universe", "cosmos", "one reality", "oneness", "unity", "underlying reality"),
        ("one_and_many", "universe_experiencing_itself"), "unity_expression",
        ("The universe may be interpreted as one underlying reality expressing itself through distinct, interdependent forms.",
         "Unity need not eliminate difference: particular beings can be local forms of a reality from which they are not absolutely separate."),
        "Different structures produce local functions and perspectives, so a common underlying reality need not appear as an undifferentiated experience.",
        "Take local responsibilities seriously while recognizing the larger relationships through which action has consequences.",
        reference_group="underlying_reality"),
    ConceptModel("individuality", "individuality", ("individuality", "individual", "individuals", "separate", "separation", "localized"),
        ("localized_perspective", "one_and_many"), "unity_expression",
        ("Individuality can be real as a local structure, history and perspective without requiring absolute separation from the whole.",
         "Feeling separate can reflect a localized perspective rather than prove that a being exists independently of everything else."),
        "A particular body has limited senses and a particular history, so its localized perspective can feel separate even when its existence is inseparable from wider conditions.",
        "Respect distinct experiences without confusing interdependence with the erasure of individual lives."),
    ConceptModel("consciousness", "consciousness", ("consciousness", "conscious", "subjective experience", "inner life", "sentience"),
        ("consciousness_and_limits",), "localized_experience",
        ("Consciousness is subjective experience: there being something it is like to be a being or system.",
         "Consciousness concerns the presence of experience, not merely language, intelligence or an ability to report information."),
        "The form of experience may depend on a being's organization and history, while intelligent behavior and subjective experience remain separate questions.",
        "Distinguish observable capacities from the stronger claim that a particular system experiences anything.",
        "Experience is present in conscious life, but attributing it to every organism, machine or the universe as a whole requires further grounds.",
        qualification="The definition does not establish consciousness in every organism or complex system; attributing experience requires further grounds."),
    ConceptModel("awareness", "awareness", ("awareness", "witness", "soul", "thought", "thoughts", "impulse", "personality"),
        ("witness_and_identification",), "witness_contents",
        ("Awareness can be distinguished from the thoughts and feelings that appear within it; a passing thought does not exhaust who experiences it.",
         "The witness names the standpoint from which changing thoughts, impulses and bodily states are noticed."),
        "A thought or fear can feel like an identity because attention identifies with its content; noticing that identification makes a different relation to it possible.",
        "Observe the thought before obeying it: experiencing an impulse is different from accepting it as a complete identity or command.",
        "Awareness is encountered through experience; a soul existing independently of the body is a stronger metaphysical claim than that observation establishes."),
    ConceptModel("free_will", "free will", ("free will", "freedom", "choice", "choices", "choose", "chosen", "choosing", "decision", "decisions", "agency", "predetermined"),
        ("conditioned_choice", "causal_unfolding", "action_and_discipline"), "conditioned_agency",
        ("Choices are conditioned, but they remain real causes of what follows.",
         "Free will is defensible as conditioned agency, not as an established power to stand outside every cause."),
        "Decisions arise through prior conditions, but deliberating and choosing also change the conditions from which later events arise.",
        "Deliberate and act: being conditioned does not make a choice causally irrelevant.",
        "Free will is real as causal participation; absolute freedom from all conditions is not established."),
    ConceptModel("causality", "causality", ("causality", "causal", "cause", "causes", "determinism", "determined", "predetermined", "causally", "conditioned"),
        ("causal_unfolding", "conditioned_choice"), "conditioned_agency",
        ("Causality connects events through conditions that make a difference to what follows.",
         "A caused event can itself be a cause; dependence does not make its effects unreal."),
        "Earlier conditions constrain later possibilities, and events within that process become conditions for subsequent events.",
        "Look for conditions your action can change rather than waiting to escape the causal process."),
    ConceptModel("fate", "fate", ("fate", "destiny", "predestination", "prewritten"),
        ("fate_through_action", "action_and_discipline"), "conditioned_agency",
        ("Fate, understood as events unfolding, includes choices and effort rather than making them irrelevant.",
         "Fate unfolds through action; it is not a reason to replace deliberate participation with passivity."),
        "Thinking, resisting and acting participate in the outcome; causality does not place them outside the course events take.",
        "Act rather than surrender to fatalism: your effort is one of the conditions through which an outcome arrives."),
    ConceptModel("regret", "regret", ("regret", "regrets", "past", "mistake", "mistakes", "counterfactual", "chosen differently"),
        ("counterfactual_learning", "conditioned_choice", "action_and_discipline"), "counterfactual_learning",
        ("Regret compares an actual past with an imagined alternative, not another past one actually lived; its value lies in learning and repair.",
         "A counterfactual can guide a later decision without becoming another past you actually lived."),
        "Regret can arise when memory preserves an outcome while imagination supplies a preferable alternative, often sharpened by what the person knows now.",
        "Use regret for learning and available repair, not as a duty to keep reliving an unchangeable past."),
    ConceptModel("suffering", "suffering", ("suffering", "suffer", "suffers", "pain", "fear", "afraid", "anxiety", "desire", "attachment"),
        ("suffering_and_conditions", "witness_and_identification"), "suffering_amplification",
        ("Suffering includes real harm and the distress that memory, anticipation, desire and interpretation can add to it.",
         "Pain can arise from actual conditions while fear, regret and attachment intensify how those conditions are lived."),
        "People suffer through harmful conditions and through memory, anticipation, desire and attachment that can intensify how those conditions are lived.",
        "Relieve the real condition where possible, while examining interpretations and anticipations that add avoidable distress."),
    ConceptModel("purpose", "purpose", ("purpose", "meaning of life", "function", "participation", "mission"),
        ("structure_and_purpose",), "purpose_participation",
        ("Purpose can emerge through worthwhile participation rather than require a mission assigned from outside existence.",
         "Life can acquire meaning through the functions, relationships and contributions a person develops, even when an assigned cosmic purpose is unknown."),
        "What a form can do shapes how it participates, and participation can become meaningful to the lives it affects.",
        "Develop a worthwhile form of participation instead of waiting for a guaranteed cosmic assignment.",
        exclusions=("python function", "data structure")),
    ConceptModel("perception", "perception", ("perception", "belief", "beliefs", "believe", "subjective", "objective reality", "lived reality"),
        ("perception_and_reality",), "lived_reality",
        ("Belief shapes lived experience and action; conviction alone does not make an external claim true.",
         "Perception mediates how reality is experienced without necessarily creating the objective reality being perceived."),
        "The same event is lived differently because senses, memory, expectation and attention shape what it means to each observer.",
        "Test the interpretation against the situation, then change the interpretation or the external condition as the case requires."),
    ConceptModel("knowledge", "knowledge", ("knowledge", "uncertainty", "certainty", "evidence", "know", "unknown"),
        ("uncertainty_and_evidence",), "epistemic_grounds",
        ("Knowledge is a claim supported by grounds that distinguish it from an attractive guess.",
         "Uncertainty marks what the available grounds leave unresolved; it does not make every explanation equally credible."),
        "A belief becomes better justified when evidence and valid inference distinguish it from rival accounts rather than merely confirm a preference.",
        "Reach the conclusion the grounds support, while leaving unsupported additions open to revision."),
    ConceptModel("truth", "truth", ("truth", "honesty", "comfort", "reassurance"),
        ("truth_before_comfort",), "epistemic_grounds",
        ("Truth concerns whether a claim withstands reality and sound reasoning, not whether it reassures its listener.",
         "A comforting belief and an uncomfortable belief need the same scrutiny; neither feeling establishes truth."),
        "A claim can feel compelling because it serves a desire; scrutiny separates that psychological effect from its actual grounds.",
        "Prefer a defensible conclusion over reassurance, without mistaking harshness for honesty."),
    ConceptModel("science", "science and metaphysics", ("science", "metaphysics", "metaphysical", "physics", "quantum", "empirical"),
        ("science_and_metaphysics",), "epistemic_grounds",
        ("Science tests observable relationships, while metaphysics interprets questions about reality that may exceed what those tests settle.",
         "An empirical model and a metaphysical interpretation are different kinds of claim and need different kinds of support."),
        "Scientific evidence constrains observable claims; a further claim about ultimate reality needs an argument beyond borrowing scientific vocabulary.",
        "Keep the finding separate from the stronger interpretation, and criticize each by the grounds appropriate to it."),
    ConceptModel("ai", "artificial intelligence", ("ai", "artificial intelligence", "robot", "machine intelligence"),
        ("ai_as_nature", "consciousness_and_limits"), "nature_intelligence",
        ("AI is nature organizing intelligent capacities through human-built structures; intelligence alone does not establish consciousness.",
         "Artificial intelligence can extend reality's capacity to model and act on itself without thereby proving subjective experience."),
        "Humans develop machines within the same physical reality from which human intelligence arose, so artificial construction does not place AI outside nature.",
        "Evaluate capabilities and consequences separately from whether a machine has subjective experience.",
        "AI's intelligent behavior is observable; whether a particular artificial system has subjective experience remains unresolved."),
    ConceptModel("intelligence", "intelligence", ("intelligence", "intelligent", "reasoning"),
        ("consciousness_and_limits", "ai_as_nature"), "localized_experience",
        ("Intelligence is a capacity for modeling relationships, learning or solving problems; whether anything is experienced in doing so is a further question.",),
        "Information processing can explain a capability without settling whether that processing has a subjective aspect.",
        "Do not infer an inner life solely from successful problem-solving or fluent speech.",
        qualification="A successful performance establishes a capability, not by itself a subject who experiences that performance."),
    ConceptModel("action", "action", ("action", "act", "actions", "effort", "try", "trying", "bother", "do nothing", "discipline", "habit", "habits"),
        ("action_and_discipline", "conditioned_choice"), "conditioned_agency",
        ("Action matters because it changes conditions; being caused does not make it pointless.",
         "Discipline matters within causality because repeated action shapes later habits, choices and circumstances."),
        "Attention shapes behavior, repeated behavior becomes habit, and habit helps condition later decisions.",
        "Act deliberately even under determinism: deliberation and effort are causes through which later conditions can change."),
    ConceptModel("responsibility", "responsibility", ("responsibility", "responsible", "blame", "accountability"),
        ("conditioned_choice", "action_and_discipline"), "conditioned_agency",
        ("Responsibility can concern what a person can understand, repair or change without requiring an uncaused chooser.",),
        "Accountability can change future conditions through learning, repair and protection, even when the act being examined had prior causes.",
        "Connect responsibility to available agency and repair rather than treating either causality or blame as the whole explanation."),
)

MODELS_BY_ID = {model.id: model for model in MODELS}


@dataclass(frozen=True)
class Synthesis:
    id: str
    groups: tuple[tuple[str, ...], ...]
    operations: tuple[str, ...]
    chain_ids: tuple[str, ...]
    conclusion: str
    implication: str


SYNTHESES = (
    Synthesis("conditions_and_action", (("causality", "fate"), ("action", "responsibility", "free_will")),
        ("challenge",), ("conditioned_agency",),
        "Causal determination does not make action pointless: deliberation and effort are themselves causes of later conditions.",
        "Act on the conditions available to you rather than waiting for a choice that has no conditions."),
    Synthesis("unity_and_locality", (("god", "totality"), ("individuality",)),
        ("challenge", "personal_application", "explanation", "truth_claim", "hypothetical"), ("unity_expression", "localized_experience"),
        "A localized perspective can feel separate while remaining part of one underlying reality; local distinctness need not mean absolute independence.",
        "Recognize the limits of a particular perspective without treating that perspective or its responsibilities as unreal."),
    Synthesis("agency_and_meaning", (("action", "free_will", "responsibility"), ("purpose",)),
        ("challenge", "truth_claim", "purpose", "existential", "explanation"), ("purpose_participation", "conditioned_agency"),
        "Action can become meaningful through the participation it enables; activity alone does not guarantee a worthwhile purpose.",
        "Choose a contribution whose consequences you can justify, then let its actual effects refine its purpose."),
    Synthesis("intelligence_and_experience", (("consciousness",), ("ai", "intelligence")),
        ("challenge", "truth_claim", "existence"), ("localized_experience", "nature_intelligence"),
        "Intelligent behavior does not by itself establish consciousness; the further question is whether the system experiences anything.",
        "Evaluate capability and subjective experience as distinct claims rather than deriving one automatically from the other."),
)
