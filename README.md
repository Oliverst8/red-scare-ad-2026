# Red Scare
![hippo](https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3OXZkYzhtYnpvZHBxMnd4a3VyODdyM3lvajN0Y2kxeWgxbjB2bXUxdiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/pdoygq9c9fZwuNJPHL/giphy.gif)

Run the benchmark suite from the repository root:

```bash
python run.py
```

This creates:

- `results.txt`: a tab-separated table for the selected `--subset` of valid input instances.
- `timings.txt`: optional tab-separated solution execution times in seconds.
- `ad-red-scare/doc/results.tex`: a LaTeX table fragment for instances with at least 500 vertices.

Useful options:

```bash
python run.py --limit 10
python run.py --subset 'n<100' --no-latex
python run.py --subset all --latex-subset 'n>=500'
python run.py --timeout 30
python run.py --no-latex
python run.py --timings
python run.py --timings --timings-file timings-small.txt --subset 'n<100'
```
