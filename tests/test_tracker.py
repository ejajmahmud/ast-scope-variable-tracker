"""Tests for ast-scope-variable-tracker."""
import unittest
from ast_scope_variable_tracker.tracker import ASTScopeVariableTracker


class TestScopeTracker(unittest.TestCase):
    def test_detects_undefined_variable(self):
        code = "def foo():\n    return missing_var + 10"
        res = ASTScopeVariableTracker.analyze(code)
        self.assertFalse(res.to_dict()["is_clean"])
        self.assertIn("missing_var", res.undefined_vars)

    def test_clean_imports_and_definitions(self):
        code = "import math\nx = 10\ndef foo(y):\n    return x + y + math.pi"
        res = ASTScopeVariableTracker.analyze(code)
        self.assertTrue(res.to_dict()["is_clean"])
        self.assertEqual(len(res.undefined_vars), 0)
