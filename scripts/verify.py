#!/usr/bin/env python3
"""Source gate + compiled Lean axiom gate; no third-party Python packages."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
out = root / "verification"
out.mkdir(exist_ok=True)
files = sorted([root / "RCDA.lean", root / "Audit.lean", *root.glob("RCDA/*.lean")])
for path in files:
    text = path.read_text()
    # Reject proof admission/evaluation escape hatches even in comments.
    if re.search(r"\b(sorry|admit|native_decide|sorryAx|unsafe|implemented_by)\b", text):
        sys.exit(f"Forbidden source token in {path.relative_to(root)}")
    if re.search(r"^\s*(?:private\s+)?(?:axiom|opaque)\s", text, re.M):
        sys.exit(f"Forbidden axiom/opaque declaration in {path.relative_to(root)}")
    for line in text.splitlines():
        if line.startswith("import "):
            for module in line.split()[1:]:
                if module not in {"Init", "Lean", "RCDA"} and not module.startswith("RCDA."):
                    sys.exit(f"Unapproved import {module}")
manifest = json.loads((root / "lake-manifest.json").read_text())
if manifest["packages"]:
    sys.exit("Unexpected external package dependencies")

def run(args, name):
    result = subprocess.run(args, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out / name).write_text(result.stdout)
    if result.returncode:
        print(result.stdout)
        sys.exit(result.returncode)
    return result.stdout

version = run(["lake", "env", "lean", "--version"], "toolchain.log").strip()
run(["lake", "build"], "build.log")
audit = run(["lake", "env", "lean", "-DwarningAsError=true", "Audit.lean"], "axioms.log")
summary = next((line for line in audit.splitlines() if line.startswith("AUDIT PASS:")), None)
if not summary:
    sys.exit("Missing Lean audit completion receipt")
foundations = next(line for line in audit.splitlines() if line.startswith("FOUNDATIONAL AXIOMS USED:"))
tracked = files + [root / "lean-toolchain", root / "lakefile.toml", root / "lake-manifest.json",
                   root / "README.md", root / "AUDIT.md", root / "DEPENDENCIES.md", Path(__file__).resolve()]
tracked += sorted(p for p in (root / "sounio").glob("*") if p.is_file())
tracked += sorted(root.glob("*.md"))
tracked += sorted((root / "docs").glob("*.md"))
tracked += sorted(p for p in (root / "experiments").rglob("*")
                  if p.is_file() and p.suffix in {".md", ".py", ".json"}
                  and "__pycache__" not in p.parts)
tracked += [root / "verification" / "import-provenance.json"]
hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(tracked)}
receipt = {"status": "PASS", "lean": version, "external_packages": [],
           "source_gate": "PASS", "build_exit_code": 0, "axiom_audit_exit_code": 0,
           "summary": summary, "foundational_axioms": foundations, "sha256": hashes}
(out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(version)
print(summary)
print(foundations)
print("PASS: source gate, build, fresh axiom audit; receipt: verification/receipt.json")
