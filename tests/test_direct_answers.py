"""Central-demand and constructive-reasoning regressions."""
import unittest
from philosophy import reason
from philosophy.classifier import QuestionType as Q
from philosophy.concepts import CHAINS


class DirectAnswerTests(unittest.TestCase):
    def test_god_definitions_answer_before_qualification(self):
        for question in ('Who is God?', 'What is God?', 'Define God', 'Who is the deity?'):
            with self.subTest(question=question):
                result = reason(question)
                self.assertEqual(result.demand.operation, Q.DEFINITION)
                self.assertIn('totality', result.plan.position)
                self.assertIn('divine_totality', result.principle_ids)
                self.assertTrue(result.answer.startswith(result.plan.position))
                self.assertTrue(result.answer.endswith(result.plan.qualification))
                self.assertIn('unity_expression', result.chain_ids)

    def test_existence_is_distinct_from_definition(self):
        definition = reason('Who is God?')
        existence = reason('Does God exist?')
        self.assertEqual(existence.demand.operation, Q.EXISTENCE)
        self.assertNotEqual(definition.plan.position, existence.plan.position)
        self.assertIn('personal', existence.answer)

    def test_same_reference_conflict_is_scoped(self):
        conflict = reason('If God is conscious and the universe is unconscious, can God be the universe?')
        self.assertIn('same_reference_consistency', conflict.applied_rule_ids)
        self.assertIn('same reality', conflict.plan.position)
        ordinary = reason('If humans are conscious and the universe is unconscious, is that a contradiction?')
        self.assertNotIn('same_reference_consistency', ordinary.applied_rule_ids)

    def test_demand_specific_openings(self):
        for question, fragment in (
            ('Why do people suffer?', 'harmful'),
            ('Why do I regret my decisions?', 'memory'),
            ('Should I regret a mistake?', 'repair'),
            ('If everything is predetermined why should I even try?', 'action pointless'),
            ('If the universe is one consciousness why do I feel separate?', 'local'),
        ):
            with self.subTest(question=question):
                self.assertIn(fragment, reason(question).plan.position.lower())

    def test_incidental_topic_cannot_erase_subject(self):
        for question in ('What causes a glorb?', 'How can I know a glorb?',
                         'Why am I afraid of a glorb?', 'What is the metaphysical role of cabbage?'):
            with self.subTest(question=question):
                noun = 'cabbage' if 'cabbage' in question else 'glorb'
                self.assertIn(noun, reason(question).plan.position.lower())

    def test_required_connected_chains(self):
        for key in ('unity_expression', 'conditioned_agency', 'purpose_participation'):
            edges = CHAINS[key].edges
            for left, right in zip(edges, edges[1:]):
                self.assertEqual(left.target, right.source)
        self.assertEqual(CHAINS['conditioned_agency'].edges[-1].target,
                         CHAINS['conditioned_agency'].edges[0].source)


if __name__ == '__main__':
    unittest.main()
