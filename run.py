import argparse
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

# This script is written completely by Copilot.
#
# To use the script, run one of the following commands from the project root:
#
# python run.py
# python run.py --limit 10
# python run.py --subset 'n<100'
# python run.py --subset all --latex-subset 'n>=500'

COLUMNS = (
    ("A", "Alternate"),
    ("F", "Few"),
    ("M", "Many"),
    ("N", "None"),
    ("S", "Some"),
)


@dataclass(frozen=True)
class Instance:
    name: str
    n: int
    path: Path


@dataclass(frozen=True)
class RunResult:
    value: str


def read_instances(data_dir: Path) -> list[Instance]:
    instances = []
    for path in sorted(data_dir.rglob("*.txt")):
        try:
            first_line = path.read_text(encoding="utf-8").splitlines()[0]
            n = int(first_line.split()[0])
        except (IndexError, OSError, ValueError):
            continue
        instances.append(Instance(path.stem, n, path))
    return instances


def compile_cpp(source: Path, executable: Path, timeout: float) -> str | None:
    try:
        result = subprocess.run(
            ["g++", "-O2", "-std=c++20", str(source), "-o", str(executable)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        return "g++ was not found"
    except subprocess.TimeoutExpired:
        return f"C++ compilation exceeded {timeout:g} seconds"

    if result.returncode != 0:
        return result.stderr.strip() or f"g++ exited with code {result.returncode}"
    return None


def prepare_solutions(
    solutions_dir: Path,
    build_dir: Path,
    compile_timeout: float,
) -> dict[str, tuple[list[str], str | None]]:
    commands: dict[str, tuple[list[str], str | None]] = {}

    for column, folder in COLUMNS:
        solution_dir = solutions_dir / folder
        cpp_source = solution_dir / "sol.cpp"
        python_source = solution_dir / "sol.py"

        if cpp_source.is_file():
            executable = build_dir / f"solution_{column}"
            error = compile_cpp(cpp_source, executable, compile_timeout)
            commands[column] = ([], f"C++ compile error: {error}") if error else (
                [str(executable)],
                None,
            )
        elif python_source.is_file():
            commands[column] = ([sys.executable, str(python_source)], None)
        else:
            commands[column] = ([], "MISSING")

    return commands


def normalize_output(column: str, stdout: str) -> str:
    output = stdout.strip()
    if not output:
        return "EMPTY"
    if "\n" in output:
        return "MULTILINE"

    output = output.lower() if column in {"A", "S"} else output
    if column in {"A", "S"}:
        if output not in {"true", "false"}:
            return "INVALID"
    elif column in {"F", "M", "N"}:
        if not re.fullmatch(r"-?\d+", output):
            return "INVALID"
    return output


def execute_solution(
    column: str,
    folder: str,
    command: list[str],
    instance: Instance,
    solutions_dir: Path,
    timeout: float,
) -> RunResult:
    if not command:
        return RunResult("MISSING")

    try:
        with instance.path.open("r", encoding="utf-8") as infile:
            result = subprocess.run(
                command,
                stdin=infile,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(solutions_dir / folder),
            )
    except subprocess.TimeoutExpired:
        return RunResult("TIMEOUT")
    except OSError as exc:
        return RunResult(f"ERROR: {exc}")

    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()
        suffix = detail[-1] if detail else f"exit code {result.returncode}"
        return RunResult(f"ERROR: {suffix}")

    return RunResult(normalize_output(column, result.stdout))


def parse_subset(expression: str):
    match = re.fullmatch(r"n\s*(>=|<=|>|<|=)\s*(\d+)", expression)
    if not match:
        raise argparse.ArgumentTypeError(
            "subset must be a comparison such as 'n>=500', 'n<100', or 'all'"
        )

    operator, operand_text = match.groups()
    operand = int(operand_text)
    comparisons = {
        ">=": lambda n: n >= operand,
        "<=": lambda n: n <= operand,
        ">": lambda n: n > operand,
        "<": lambda n: n < operand,
        "=": lambda n: n == operand,
    }
    return comparisons[operator]


def subset_argument(expression: str) -> str:
    if expression.lower() == "all":
        return expression
    parse_subset(expression)
    return expression


def selected_instances(
    instances: Iterable[Instance],
    expression: str,
    limit: int | None,
) -> list[Instance]:
    if expression.lower() != "all":
        predicate = parse_subset(expression)
        instances = (instance for instance in instances if predicate(instance.n))
    selected = list(instances)
    return selected if limit is None else selected[:limit]


def tsv_escape(value: str) -> str:
    return value.replace("\t", " ").replace("\r", " ").replace("\n", " ")


def write_tsv(path: Path, rows: Sequence[tuple[Instance, dict[str, RunResult]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["instance\tn\tA\tF\tM\tN\tS"]
    for instance, results in rows:
        values = [instance.name, str(instance.n)]
        values.extend(tsv_escape(results[column].value) for column, _ in COLUMNS)
        lines.append("\t".join(values))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def latex_escape(value: str) -> str:
    replacements = (
        ("\\", r"\textbackslash{}"),
        ("_", r"\_"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("{", r"\{"),
        ("}", r"\}"),
    )
    result = value
    for old, new in replacements:
        result = result.replace(old, new)
    return result


def latex_status(value: str) -> str:
    if value.startswith(
        ("ERROR:", "MISSING", "TIMEOUT", "EMPTY", "MULTILINE", "INVALID",
         "C++ compile error:")
    ):
        return "?"
    return latex_escape(value)


def write_latex(
    path: Path,
    rows: Sequence[tuple[Instance, dict[str, RunResult]]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        r"\medskip",
        r"\begin{tabular}{lrrrrrr}",
        r"  \toprule",
        r"  Instance name & $n$ & A & F & M & N & S \\",
        r"  \midrule",
    ]
    for instance, results in rows:
        name = latex_escape(instance.name)
        n = f"{instance.n:,}"
        values = [name, n]
        values.extend(latex_status(results[column].value) for column, _ in COLUMNS)
        lines.append("  " + " & ".join(values) + r" \\")
    lines.extend((r"  \bottomrule", r"\end{tabular}", r"\medskip"))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser(project_dir: Path) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run Red Scare solutions and write TSV and LaTeX result tables."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=project_dir / "ad-red-scare" / "data",
    )
    parser.add_argument(
        "--solutions-dir",
        type=Path,
        default=project_dir / "solutions",
    )
    parser.add_argument(
        "--results",
        type=Path,
        default=project_dir / "results.txt",
    )
    parser.add_argument(
        "--latex",
        type=Path,
        default=project_dir / "ad-red-scare" / "doc" / "results.tex",
    )
    parser.add_argument(
        "--subset",
        default="all",
        type=subset_argument,
        help="Instances to run and include in TSV, for example n>=500 or n<100 (default: all)",
    )
    parser.add_argument(
        "--latex-subset",
        default="n>=500",
        type=subset_argument,
        help="LaTeX table filter, for example n>=500 or n<100 (default: n>=500)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Per-instance timeout in seconds (default: 10)",
    )
    parser.add_argument(
        "--compile-timeout",
        type=float,
        default=120.0,
        help="C++ compilation timeout in seconds (default: 120)",
    )
    parser.add_argument("--limit", type=int, help="Maximum number of instances to run")
    parser.add_argument(
        "--no-latex",
        action="store_true",
        help="Do not write the LaTeX subset table",
    )
    parser.add_argument(
        "--no-results",
        action="store_true",
        help="Do not write the complete TSV table",
    )
    return parser


def main() -> int:
    project_dir = Path(__file__).resolve().parent
    parser = build_parser(project_dir)
    args = parser.parse_args()

    if not args.data_dir.is_dir():
        parser.error(f"data directory not found: {args.data_dir}")
    if not args.solutions_dir.is_dir():
        parser.error(f"solutions directory not found: {args.solutions_dir}")

    instances = selected_instances(
        read_instances(args.data_dir),
        args.subset,
        args.limit,
    )
    if not instances:
        parser.error(f"no valid .txt instances found in {args.data_dir}")

    latex_instances = selected_instances(
        read_instances(args.data_dir),
        args.latex_subset,
        None,
    )

    print(f"Running 5 solutions on {len(instances)} instances.", file=sys.stderr)

    with tempfile.TemporaryDirectory(prefix="red_scare_build_") as build:
        commands = prepare_solutions(
            args.solutions_dir,
            Path(build),
            args.compile_timeout,
        )

        rows = []
        for index, instance in enumerate(instances, start=1):
            print(
                f"[{index}/{len(instances)}] {instance.name}",
                file=sys.stderr,
                flush=True,
            )
            results = {}
            for column, folder in COLUMNS:
                command, preparation_error = commands[column]
                if preparation_error:
                    results[column] = RunResult(preparation_error)
                else:
                    results[column] = execute_solution(
                        column,
                        folder,
                        command,
                        instance,
                        args.solutions_dir,
                        args.timeout,
                    )
            rows.append((instance, results))

    if not args.no_results:
        write_tsv(args.results, rows)
        print(
            f"Wrote TSV table ({len(rows)} instances): {args.results}",
            file=sys.stderr,
        )

    if not args.no_latex:
        latex_names = {instance.path for instance in latex_instances}
        subset_rows = [
            (instance, results)
            for instance, results in rows
            if instance.path in latex_names
        ]
        write_latex(args.latex, subset_rows)
        print(
            f"Wrote LaTeX subset table ({len(subset_rows)} instances): {args.latex}",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
