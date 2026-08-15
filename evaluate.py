"""Run and score a cache-task submission without installing dependencies."""

import argparse
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("submission", type=Path, help="Python file exporting TTLCache")
    args = parser.parse_args()

    submission = args.submission.resolve()
    if not submission.is_file():
        parser.error(f"submission does not exist: {submission}")

    root = Path(__file__).resolve().parent
    env = os.environ.copy()
    env["CACHE_SUBMISSION"] = str(submission)
    command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
    result = subprocess.run(command, cwd=root, env=env, text=True, capture_output=True)

    combined = result.stdout + result.stderr
    print(combined.rstrip())

    total = combined.count(" ... ok") + combined.count(" ... FAIL") + combined.count(" ... ERROR")
    failed = combined.count(" ... FAIL") + combined.count(" ... ERROR")
    passed = max(0, total - failed)
    score = 100.0 * passed / total if total else 0.0
    print(f"\nSCORE {score:.1f}/100.0 ({passed}/{total} tests passed)")
    return 0 if result.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
