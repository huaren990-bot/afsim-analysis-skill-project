# Scripts

Place deterministic helper scripts here.

Recommended scripts:

- `index_cpp_source.py`: scan C/C++ source and emit JSONL symbol index.
- `summarize_index.py`: aggregate function and class summaries into module reports.
- `detect_formula_hotspots.py`: find formula-heavy code regions.
- `validate_traceability.py`: check that reports cite source evidence.

Scripts should write generated outputs to `workspace/` and should not overwrite human-edited reports unless explicitly requested.
