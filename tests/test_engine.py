"""Regression corpus for local interpretation, rules, composition and limits."""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from philosophy import answer_question, reason
from philosophy.classifier import QuestionType, classify_intent
from philosophy.engine import MAX_QUESTION_LENGTH
from philosophy.knowledge import PRINCIPLES
from philosophy.lexicon import VOCABULARY
from philosophy.preprocessing import preprocess


class EngineTests(unittest.TestCase):
    def test_choice_paraphrases_share_underlying_principle(self):
        for question in (
            "Do I have free will?", "Are my choices predetermined?",
            "Could I have chosen differently?", "If everything has a cause, am I really choosing?",
            "Is there such a thing as choice?", "Do humans possess freewill?",
            "Am I in control of my life?", "What is freedom?",
        ):
            with self.subTest(question=question):
                result = reason(question)
                self.assertIn("conditioned_choice", result.principle_ids)
                self.assertTrue(any(word in result.answer for word in ("caus", "condition")))
                self.assertGreater(len(result.answer.split()), 40)
        fate = reason("Does fate control us?")
        self.assertIn("fate_through_action", fate.principle_ids)
        self.assertGreater(next(t for t in fate.themes if t.theme == "free_will").boost, 0)

    def test_worldview_domain_coverage(self):
        cases = {
            "Does everything have a cause?": "causal_unfolding",
            "Is free will real?": "conditioned_choice",
            "Does fate control us?": "fate_through_action",
            "Should I regret a past mistake?": "counterfactual_learning",
            "Am I my thoughts?": "witness_and_identification",
            "What is consciousness?": "consciousness_and_limits",
            "Is everything one reality?": "one_and_many",
            "Why do I feel separate?": "localized_perspective",
            "Is the universe experiencing itself through us?": "universe_experiencing_itself",
            "What is the meaning of life?": "structure_and_purpose",
            "Does perception shape lived reality?": "perception_and_reality",
            "Why am I afraid of failing?": "suffering_and_conditions",
            "Can we know anything with certainty?": "uncertainty_and_evidence",
            "Is truth better than comfort?": "truth_before_comfort",
            "What is metaphysics?": "science_and_metaphysics",
            "Is artificial intelligence part of nature?": "ai_as_nature",
            "Why does discipline matter?": "action_and_discipline",
        }
        for question, principle in cases.items():
            with self.subTest(question=question):
                result = reason(question)
                self.assertTrue(result.supported)
                self.assertIn(principle, result.principle_ids)
                self.assertLess(len(result.answer.split()), 300)

    def test_question_types_and_composition(self):
        cases = {
            "What is consciousness?": QuestionType.DEFINITION,
            "Is free will real?": QuestionType.TRUTH,
            "Why do humans suffer?": QuestionType.EXPLANATION,
            "Should I regret what I did?": QuestionType.NORMATIVE,
            "What is the purpose of life?": QuestionType.EXISTENTIAL,
            "What if everything is predetermined?": QuestionType.HYPOTHETICAL,
            "Why am I afraid of failing?": QuestionType.PERSONAL,
            "Is fate different from determinism?": QuestionType.COMPARISON,
            "If everything has a cause, isn't choice meaningless?": QuestionType.CHALLENGE,
        }
        for question, expected in cases.items():
            with self.subTest(question=question):
                self.assertEqual(classify_intent(preprocess(question)), expected)
        self.assertTrue(answer_question("What is consciousness?").startswith("Consciousness concerns subjective experience"))
        personal = reason("Why am I afraid of failing?")
        self.assertIn("i afraid of failing", personal.subject.label)
        self.assertIn("anticipated", personal.answer.lower())

    def test_reusable_tensions(self):
        cases = {
            "If fate controls us why bother?": ("fate_not_passivity", "Effort"),
            "If everything is predetermined why should I even try?": ("fate_not_passivity", "consequential"),
            "Does causality eliminate choice?": ("determinism_and_agency", "causal irrelevance"),
            "If the universe is one consciousness why do I feel separate?": ("oneness_and_locality", "localized"),
            "Can belief change objective reality?": ("belief_not_external_fact", "conviction alone"),
            "Is artificial intelligence conscious?": ("intelligence_not_consciousness", "unresolved"),
            "Does intelligence prove consciousness?": ("consciousness_not_intelligence", "further question"),
            "Does function imply purpose?": ("purpose_not_function", "morally ought"),
            "Science cannot explain consciousness, therefore it must be spiritual": ("ignorance_not_evidence", "independent grounds"),
            "Does quantum physics prove free will?": ("science_not_metaphysical_proof", "does not itself prove"),
            "Am I my thoughts or my soul?": ("witness_not_personality", "does not prove"),
            "Could I have chosen differently?": ("regret_and_action", "another past"),
            "Is hunger just perspective?": ("material_suffering", "not a substitute"),
            "Can action give life purpose?": ("purpose_through_action", "participation"),
        }
        for question, (rule, meaning) in cases.items():
            with self.subTest(question=question):
                result = reason(question)
                self.assertIn(rule, result.rule_ids)
                self.assertIn(meaning, result.answer)
                self.assertIsNotNone(result.plan)

    def test_negation_and_uncertainty(self):
        text = preprocess("I don't believe that belief creates objective reality", VOCABULARY)
        self.assertIn("believe", text.negated_concepts)
        result = reason("I don't believe that belief creates objective reality")
        self.assertIn("without making an external proposition true", result.answer)
        self.assertNotIn("you believe", result.answer.lower())
        ai = reason("Is AI not conscious?")
        self.assertIn("unresolved", ai.answer)
        self.assertNotIn("AI is conscious", ai.answer)
        self.assertNotIn("ignorance_not_evidence", reason("I do not know what consciousness is").rule_ids)
        for question in ("Is the universe one consciousness?", "Does consciousness survive after death?"):
            with self.subTest(question=question):
                self.assertTrue(any(word in answer_question(question).lower()
                    for word in ("possibility", "not", "do not know", "unresolved")))

    def test_normalization_aliases_typo_and_word_boundaries(self):
        self.assertEqual(preprocess("  FREE—WILL?!  ").normalized, "free will")
        self.assertIn("consciousness_and_limits", reason("What is conscousness?").principle_ids)
        self.assertIn("conditioned_choice", reason("Are decisions predetermind?").principle_ids)
        for question in ("How much is an airline ticket?", "What is free shipping?", "How does remote control work?", "Write a Python function", "What is a data structure?"):
            with self.subTest(question=question):
                result = reason(question)
                self.assertTrue(result.supported)
                self.assertTrue(result.lens_ids)
                self.assertNotIn("ai_as_nature", result.principle_ids)

    def test_unmatched_questions_and_bounds(self):
        for question in ("Who won the match yesterday?", "xyzzy flobble", "What is the best pizza in Philly?"):
            with self.subTest(question=question):
                result = reason(question)
                self.assertTrue(result.supported)
                self.assertGreater(len(result.answer.split()), 50)
                self.assertIsNotNone(result.plan)
                self.assertTrue(result.lens_ids)
        for question in ("", " \t\n "):
            self.assertEqual(answer_question(question), "")
        oversized = reason("x" * (MAX_QUESTION_LENGTH + 1))
        self.assertTrue(oversized.truncated)
        self.assertGreater(len(oversized.answer.split()), 40)
        with self.assertRaises(TypeError):
            answer_question(None)

    def test_same_question_is_identical_across_processes(self):
        question = "What is the meaning of life?"
        expected = answer_question(question)
        self.assertEqual(expected, answer_question("  WHAT is the meaning of LIFE?!  "))
        command = [sys.executable, "-c", "from philosophy import answer_question; print(answer_question(" + json.dumps(question) + "))"]
        for seed in ("1", "999"):
            output = subprocess.check_output(command, cwd=ROOT,
                env={**os.environ, "PYTHONHASHSEED": seed}, text=True)
            self.assertEqual(output.strip(), expected)

    def test_graph_boosts_and_repeated_words(self):
        result = reason("What is consciousness?")
        self.assertEqual(result.principle_ids, ("consciousness_and_limits",))
        for score in result.themes:
            self.assertLessEqual(score.boost, 1.5)
            self.assertGreaterEqual(score.boost, 0)
        first = {t.theme: t.direct for t in reason("consciousness").themes}
        repeated = {t.theme: t.direct for t in reason("consciousness " * 30).themes}
        self.assertEqual(first, repeated)

    def test_no_network_or_environment_needed(self):
        with patch.dict(os.environ, {}, clear=True), \
             patch("socket.create_connection", side_effect=AssertionError("network forbidden")), \
             patch("socket.socket.connect", side_effect=AssertionError("network forbidden")):
            result = reason("If the universe is one consciousness, why do I feel separate?")
        self.assertIn("oneness_and_locality", result.rule_ids)
        self.assertIn("local", result.answer)

    def test_modular_wording_banks(self):
        answers = {answer_question(q) for q in (
            "Do I have free will?", "Are my choices predetermined?", "Is there such a thing as choice?",
        )}
        self.assertGreater(len(answers), 1)
        for principle in PRINCIPLES:
            for bank in (principle.openings, principle.reasoning, principle.qualifications,
                         principle.conclusions, principle.applications):
                self.assertGreaterEqual(len(bank), 2)


if __name__ == "__main__":
    unittest.main()
