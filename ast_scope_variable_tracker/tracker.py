"""Core AST Scope Variable Tracker implementation."""
import ast
import builtins
from typing import Set, List, Dict, Any


class ScopeAnalysisResult:
    def __init__(self, defined_vars: Set[str], used_vars: Set[str], undefined_vars: Set[str]):
        self.defined_vars = defined_vars
        self.used_vars = used_vars
        self.undefined_vars = undefined_vars

    def to_dict(self) -> Dict[str, Any]:
        return {
            "defined": sorted(list(self.defined_vars)),
            "used": sorted(list(self.used_vars)),
            "undefined": sorted(list(self.undefined_vars)),
            "is_clean": len(self.undefined_vars) == 0
        }


class VariableVisitor(ast.NodeVisitor):
    def __init__(self):
        self.defined: Set[str] = set()
        self.used: Set[str] = set()
        self._builtin_names = set(dir(builtins))

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            name = alias.asname or alias.name
            self.defined.add(name.split(".")[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for alias in node.names:
            name = alias.asname or alias.name
            self.defined.add(name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.defined.add(node.name)
        for arg in node.args.args:
            self.defined.add(arg.arg)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Store):
            self.defined.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            if node.id not in self._builtin_names:
                self.used.add(node.id)
        self.generic_visit(node)


class ASTScopeVariableTracker:
    @staticmethod
    def analyze(source_code: str) -> ScopeAnalysisResult:
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return ScopeAnalysisResult(set(), set(), {f"SyntaxError: {e}"})

        visitor = VariableVisitor()
        visitor.visit(tree)

        undefined = visitor.used - visitor.defined
        return ScopeAnalysisResult(visitor.defined, visitor.used, undefined)
