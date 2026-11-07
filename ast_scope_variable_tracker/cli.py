"""CLI for ast-scope-variable-tracker."""
import sys
import argparse
from .tracker import ASTScopeVariableTracker


def main():
    parser = argparse.ArgumentParser(description="AST Scope Variable Tracker")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    args = parser.parse_args()

    if args.demo:
        bad_code = "def process():\n    total = count * 2\n    return total"
        res = ASTScopeVariableTracker.analyze(bad_code)
        print("=== Scope Analysis ===")
        print(f"Clean: {res.to_dict()['is_clean']}")
        print(f"Undefined variables: {res.to_dict()['undefined']}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
