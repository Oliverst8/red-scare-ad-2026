import subprocess
import sys
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
COLUMNS = {
    "A": "Alternate",
    "F": "Few",
    "M": "Many",
    "N": "None",
    "S": "Some",
}
TIMEOUT = 10

# Works whether this script is in the project root or in solutions/.
SOLUTIONS_DIR = BASE_DIR if (BASE_DIR / "Alternate").is_dir() else BASE_DIR / "solutions"
PROJECT_DIR = SOLUTIONS_DIR.parent
DATA_DIR = PROJECT_DIR / "ad-red-scare" / "data"

if not DATA_DIR.is_dir():
    sys.exit(f"ERROR: Data directory not found: {DATA_DIR}")
if not SOLUTIONS_DIR.is_dir():
    sys.exit(f"ERROR: Solutions directory not found: {SOLUTIONS_DIR}")

data_files = sorted(DATA_DIR.rglob("*.txt"))
if not data_files:
    sys.exit(f"ERROR: No input .txt files in {DATA_DIR}")

print(f"Found {len(data_files)} input files in {DATA_DIR}", file=sys.stderr)


def prepare_solutions(build_dir):
    commands = {}
    for col, folder in COLUMNS.items():
        solution_dir = SOLUTIONS_DIR / folder
        py_file = solution_dir / "sol.py"
        cpp_file = solution_dir / "sol.cpp"

        if py_file.is_file():
            commands[col] = [sys.executable, str(py_file)]
            print(f"{col}: Python ({py_file})", file=sys.stderr)
        elif cpp_file.is_file():
            executable = build_dir / f"solution_{col}"
            print(f"{col}: Compiling {cpp_file}", file=sys.stderr)
            try:
                compiled = subprocess.run(
                    ["g++", "-O2", "-std=c++17", str(cpp_file), "-o", str(executable)],
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if compiled.returncode != 0:
                    print(f"COMPILE ERROR for {col}:\n{compiled.stderr}", file=sys.stderr)
                    commands[col] = None
                else:
                    commands[col] = [str(executable)]
            except (OSError, subprocess.TimeoutExpired) as exc:
                print(f"COMPILE ERROR for {col}: {exc}", file=sys.stderr)
                commands[col] = None
        else:
            print(f"MISSING: {solution_dir}/sol.py or sol.cpp", file=sys.stderr)
            commands[col] = None
    return commands


def run_solution(command, data_file, col):
    if command is None:
        return r"--"
    try:
        with data_file.open("r") as infile:
            result = subprocess.run(
                command,
                stdin=infile,
                capture_output=True,
                text=True,
                timeout=TIMEOUT,
                cwd=str(SOLUTIONS_DIR / COLUMNS[col]),
            )
        if result.returncode != 0:
            print(f"ERROR {col} / {data_file.name} (exit {result.returncode}): "
                  f"{result.stderr.strip()}", file=sys.stderr)
            return "?"
        output = result.stdout.strip()
        if not output:
            print(f"EMPTY OUTPUT {col} / {data_file.name}", file=sys.stderr)
            return "?"
        if "\n" in output:
            print(f"MULTILINE OUTPUT {col} / {data_file.name}: {output!r}", file=sys.stderr)
            return "?"
        return output.replace("&", r"\&").replace("%", r"\%")
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT {col} / {data_file.name} ({TIMEOUT}s)", file=sys.stderr)
        return "?"
    except OSError as exc:
        print(f"EXECUTION ERROR {col} / {data_file.name}: {exc}", file=sys.stderr)
        return "?"


def get_n(data_file):
    with data_file.open() as infile:
        return int(infile.readline().split()[0])


with tempfile.TemporaryDirectory(prefix="red_scare_build_") as build:
    commands = prepare_solutions(Path(build))
    print(r"\medskip")
    print(r"\begin{tabular}{lrrrrrr}")
    print(r"  \toprule")
    print(r"  Instance name & $n$ & A & F & M & N & S \\")
    print(r"  \midrule")

    for data_file in data_files:
        try:
            n = get_n(data_file)
        except (ValueError, IndexError) as exc:
            print(f"INVALID INPUT {data_file}: {exc}", file=sys.stderr)
            continue
        name = data_file.stem.replace("_", r"\_")
        results = [run_solution(commands[col], data_file, col) for col in COLUMNS]
        print("  " + " & ".join([name, f"{n:,}", *results]) + r" \\")

    print(r"  \bottomrule")
    print(r"\end{tabular}")
    print(r"\medskip")