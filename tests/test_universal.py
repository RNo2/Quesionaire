"""Regressions for subject-specific interpretation without a matching topic."""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from philosophy import answer_question, reason
from philosophy.classifier import QuestionType
from philosophy.universal import LENSES


class UniversalTests(unittest.TestCase):
    CASES = (
        ("Why do cities have traffic?", "traffic", "causality", "coordination", "shared"),
        ("Does money make people free?", "money", "agency", "resources", "unconditioned"),
        ("What makes art meaningful?", "art", "perception", "aesthetic_relation", "observer"),
        ("Is technology progress?", "technology", "agency", "capability", "well-being"),
        ("Why do people compete?", "compete", "causality", "competition", "incentives"),
        ("What makes a law legitimate?", "law", "truth", "institutions", "justification"),
        ("Is beauty objective?", "beauty", "perception", "aesthetic_relation", "features"),
        ("Why do traditions persist?", "traditions", "change", "continuity", "repetition"),
        ("Should people prioritize efficiency over happiness?", "efficiency", "purpose", "values", "end"),
        ("What makes a society just?", "society", "agency", "institutions", "burdens"),
        ("Why do humans assign names to things?", "names", "participation", "communication", "coordinate"),
        ("What does silence mean?", "silence", "perception", "communication", "context"),
        ("Is a machine merely a tool?", "machine", "structure", "capability", "user"),
        ("Can a mistake be valuable?", "mistake", "change", "learning", "repair"),
        ("What is the relationship between order and chaos?", "chaos", "change", "patterns", "constraints"),
    )

    def test_requested_regression_corpus_has_relevant_arguments(self):
        answers = set()
        for question, anchor, lens, profile, concept in self.CASES:
            with self.subTest(question=question):
                result = reason(question)
                self.assertTrue(result.supported)
                self.assertEqual(result.subject.profile.id, profile)
                self.assertIn(anchor, result.subject.label)
                self.assertIn(anchor, result.answer.lower())
                self.assertIn(lens, result.lens_ids)
                self.assertIn(concept, result.answer.lower())
                self.assertGreaterEqual(len(result.answer.split()), 65)
                self.assertLessEqual(len(result.answer.split()), 240)
                self.assertNotIn("cannot resolve", result.answer)
                self.assertNotIn("I do not know how to resolve", result.answer)
                self.assertNotIn("more precise", result.answer)
                self.assertEqual(result.answer, answer_question(question))
                answers.add(result.answer)
        self.assertEqual(len(answers), len(self.CASES))

    def test_completely_new_subjects_have_real_plans_not_score_fallbacks(self):
        cases = (
            ("Why do flurps rotate?", "flurps", "causality"),
            ("What is an unfamiliar wobblewidget?", "wobblewidget", "structure"),
            ("Should I acquire a zephyrbox?", "zephyrbox", "agency"),
            ("Is a glimble real?", "glimble", "knowledge"),
            ("How does a whirligizmo work?", "whirligizmo", "structure"),
            ("What if frobnitz vanished?", "frobnitz", "change"),
            ("Why do beavers build dams?", "beavers", "causality"),
        )
        for question, anchor, lens in cases:
            with self.subTest(question=question):
                result = reason(question)
                self.assertFalse(result.topic_matched)
                self.assertEqual(result.principle_ids, ())
                self.assertIn(anchor, result.answer)
                self.assertIn(lens, result.lens_ids)
                self.assertIsNotNone(result.plan)
                self.assertGreater(len(result.plan.reasoning), 0)
                self.assertGreater(len(result.plan.implication), 20)
                self.assertGreater(len(result.answer.split()), 75)

    def test_extended_intents_are_subject_independent(self):
        cases = {
            "What is a glorb?": QuestionType.DEFINITION,
            "Why does a glorb recur?": QuestionType.EXPLANATION,
            "How does a glorb work?": QuestionType.MECHANISM,
            "Is a glorb justified?": QuestionType.TRUTH,
            "Should I accept a glorb?": QuestionType.NORMATIVE,
            "How do a glorb and a vrell differ?": QuestionType.COMPARISON,
            "What if a glorb vanished?": QuestionType.HYPOTHETICAL,
            "Why do I fear a glorb?": QuestionType.PERSONAL,
            "What is a glorb for?": QuestionType.PURPOSE,
            "What causes a glorb?": QuestionType.CAUSAL,
            "What happens if a glorb changes?": QuestionType.CONSEQUENCES,
            "How could we know whether a glorb is true?": QuestionType.EPISTEMIC,
            "If a glorb is real does that contradict a vrell?": QuestionType.CHALLENGE,
            "How should I approach a glorb?": QuestionType.PRACTICAL,
        }
        for question, intent in cases.items():
            with self.subTest(question=question):
                result = reason(question)
                self.assertEqual(result.intent, intent)
                self.assertIn("glorb", result.answer)
                self.assertTrue(result.lens_ids)
        comparison = reason("How do a glorb and a vrell differ?")
        self.assertIn("vrell", comparison.answer)
        self.assertEqual(comparison.subject.pair, ("a glorb", "a vrell"))

    def test_explanation_paraphrases_share_worldview_lenses(self):
        questions = (
            "Why do people compete?", "What makes competition happen?",
            "Where does the urge to compete come from?", "Why is everything a competition?",
        )
        for question in questions:
            result = reason(question)
            self.assertIn("causality", result.lens_ids)
            self.assertEqual(result.subject.profile.id, "competition")
            self.assertIn("incentives", result.answer)

    def test_external_facts_are_interpreted_without_inventing_results(self):
        for question in ("Who won the match yesterday?", "How many people live in glorbville?", "What is the current price of a zephyrbox?"):
            with self.subTest(question=question):
                result = reason(question)
                self.assertTrue(result.subject.factual)
                self.assertIn("knowledge", result.lens_ids)
                self.assertIn("verification", result.answer)
                self.assertIn("not", result.answer)
                self.assertFalse(any(character.isdigit() for character in result.answer))
                self.assertGreater(len(result.answer.split()), 70)

    def test_malformed_and_long_strings_still_have_interpretations(self):
        for question in ("???", "🜍", "\x00", "a" * 100000, "Why do flurps rotate? " * 1000):
            with self.subTest(size=len(question)):
                result = reason(question)
                self.assertTrue(result.answer)
                self.assertTrue(result.supported)
                self.assertEqual(len(result.lens_ids), 3)
                self.assertLess(len(result.answer), 5000)
        self.assertTrue(reason("a" * 100000).truncated)
        self.assertEqual(answer_question(" " * 10000 + "What is a glorb?"), answer_question("What is a glorb?"))
        for question in ("", " ", "\t\n"):
            self.assertEqual(answer_question(question), "")

    def test_universal_layer_always_available_offline(self):
        self.assertEqual(len(LENSES), 10)
        questions = [case[0] for case in self.CASES] + ["What is a completely unlisted zorkwheel?", "Do we have free will?"]
        with patch.dict(os.environ, {}, clear=True), \
             patch("socket.create_connection", side_effect=AssertionError("network forbidden")), \
             patch("socket.socket.connect", side_effect=AssertionError("network forbidden")):
            for question in questions:
                result = reason(question)
                self.assertTrue(result.lens_ids)
                self.assertTrue(result.answer)

    def test_tensions_and_unknown_subjects_keep_their_subject(self):
        cases = (
            ("If everything is causally determined why should I try to change my life?", "fate_not_passivity"),
            ("If we are all expressions of one reality why do I feel separate?", "oneness_and_locality"),
            ("Does brain structure determine consciousness?", "consciousness_and_structure"),
            ("Why am I afraid of what will happen in the future?", "suffering_and_anticipation"),
            ("How does an individual participate in a larger system?", "individual_and_system"),
        )
        for question, rule in cases:
            with self.subTest(question=question):
                self.assertIn(rule, reason(question).rule_ids)
        cabbage = reason("What is the metaphysical role of cabbage?")
        self.assertIn("cabbage", cabbage.answer)
        self.assertNotIn("Quantum", cabbage.answer)
        hunger = reason("Is hunger just perspective?")
        self.assertNotEqual(hunger.subject.profile.id if hunger.subject.profile else None, "institutions")
        self.assertIn("not a substitute", hunger.answer)
        for question, excluded in (("What is a law of physics?", "institutions"), ("How does a dead battery work?", "mortality"), ("What does HTTP status code mean?", "competition")):
            with self.subTest(question=question):
                result = reason(question)
                self.assertNotEqual(result.subject.profile.id if result.subject.profile else None, excluded)


if __name__ == "__main__":
    unittest.main()
