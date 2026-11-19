import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "ad-red-scare" / "data"
SOLUTIONS_DIR = BASE_DIR / "solutions"

data_files = sorted(DATA_DIR.rglob("*.txt"))
solution_files = sorted(SOLUTIONS_DIR.rglob("sol.py"))

print("Data files found:", len(data_files))
print("Solutions found:", len(solution_files))

for solution in solution_files:
    print(f"\n{'=' * 50}")
    print(f"Solution: {solution.relative_to(SOLUTIONS_DIR)}")
    print("=" * 50)

    for data_file in data_files:
        print(f"\nInput: {data_file.relative_to(DATA_DIR)}", flush=True)

        with open(data_file, "r") as f:
            try:
                result = subprocess.run(
                    [sys.executable, str(solution)],
                    stdin=f,
                    capture_output=True,
                    text=True,
                    timeout=3600,
                )

                if result.returncode == 0:
                    print("Output:")
                    print(result.stdout)
                else:
                    print("Error:")
                    print(result.stderr)

            except subprocess.TimeoutExpired:
                print("TIMEOUT: Solution exceeded 10 seconds")