# Traceability Rules

## Evidence Levels

Use one of these evidence levels for important claims:

- `source-cited`: backed by source path and symbol or line range.
- `document-cited`: backed by a user-provided requirement or design document.
- `index-derived`: backed by generated source index output.
- `inferred`: reasoned from nearby evidence but not directly stated.
- `unknown`: not enough evidence.

## Required Links

For architecture claims:

- Link to modules, classes, functions, or configuration files.

For algorithm claims:

- Link to the exact source function or code block.
- Include variable mapping.

For migration claims:

- Link requirement ID to AFSIM source candidate and target-project insertion point.

## Records

Each major run should create or update a record in `docs/records/` containing:

- Date
- Inputs
- Commands or tools used
- Outputs changed
- Review decisions
- Open questions

Do not include hidden chain-of-thought. Keep records focused on reviewable evidence and decisions.
