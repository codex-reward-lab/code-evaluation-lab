# Deterministic Code Evaluation Lab

A compact, reproducible software-engineering evaluation environment. The task
asks a candidate to turn a minimal key/value cache into a bounded TTL/LRU
cache. The repository includes:

- a precise behavioral specification;
- an intentionally incomplete baseline;
- a separate golden reference implementation;
- deterministic tests driven by a fake clock;
- a dependency-free scoring harness; and
- a container recipe for reproducible execution.

The environment demonstrates how a real feature request can be converted into
an automatically gradable coding task without relying on network access,
sleeping tests, or timing-sensitive assertions.

## Quick start

```bash
python evaluate.py challenge/cache.py
python evaluate.py reference/cache.py
```

Expected results:

- baseline: partial score because basic storage works but TTL/LRU behavior does
  not;
- reference: `100.0/100.0`.

Run the reference in a clean container:

```bash
docker build -t code-evaluation-lab .
docker run --rm code-evaluation-lab
```

## Task contract

See [TASK.md](TASK.md) for the candidate-facing specification and
[`task.json`](task.json) for machine-readable metadata. The evaluator accepts a
single Python file that exports `TTLCache`.

## Design choices

- **Deterministic time:** tests inject a fake monotonic clock.
- **No hidden infrastructure:** Python's standard library is sufficient.
- **Observable rubric:** every test has equal weight and failures are printed.
- **Isolation:** a candidate submission is loaded by file path, not installed.
- **Golden solution:** the reference implementation documents one valid answer;
  alternate correct implementations receive the same score.

## License

MIT. See [LICENSE](LICENSE).
