import unittest
import types
from wpfuzz import discovery


class Discovery(unittest.TestCase):

    def test_get_next_php_file(self):
        res = discovery.get_next_php_file("/tmp/thisdoesnotexist")
        self.assertIsInstance(res, types.GeneratorType)

        with self.assertRaises(StopIteration):
            f = next(res)

    def test_get_ajax_action_from_line(self):
        test = {
            "wp_ajax_test_action1": None,
            '"wp_ajax_test_action1"': "test_action1",
            "wp_ajax_nopriv_action1": None,
            '"wp_ajax_nopriv_action1"': "action1",
        }
        for line, action in test.items():
            self.assertEqual(
                action,
                discovery.get_ajax_action_from_line(line),
                "Expected action extracted from {}".format(line)
            )
