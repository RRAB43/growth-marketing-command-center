"""Run all deterministic analyses and generate the executive brief."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    "analysis/ab_test_analysis.py",
    "analysis/customer_segmentation.py",
    "analysis/attribution_models.py",
    "ai-automation/generate_brief.py",
]

for script in SCRIPTS:
    print(f"\n=== Running {script} ===")
    subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=True)

print("\nAll analyses completed. Review outputs/ and WEEKLY_BRIEF.md.")
