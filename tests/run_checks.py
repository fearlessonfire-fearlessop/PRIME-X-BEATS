from pathlib import Path
import ast
ROOT=Path(__file__).parents[1]
for p in ROOT.rglob("*.py"): ast.parse(p.read_text(encoding="utf-8"))
print("AST CHECK: PASS")
import pytest
raise SystemExit(pytest.main(["-q", str(Path(__file__).with_name("test_regression.py"))]))
