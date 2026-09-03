from pathlib import Path
import py_compile

for p in Path("primebeats").rglob("*.py"):
    py_compile.compile(str(p), doraise=True)
print("Python compilation: OK")
