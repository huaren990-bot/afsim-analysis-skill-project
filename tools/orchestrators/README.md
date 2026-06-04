# Orchestrators

Store task orchestration scripts here.

Recommended stages:

1. Run `afsim-source-cognition` to build or refresh the source index.
2. Run `afsim-source-cognition` to generate the architecture draft.
3. Run `afsim-algorithm-extractor` to generate algorithm candidates.
4. Run `afsim-requirement-mapper` to map requirements.
5. Run `afsim-migration-builder` to generate migration plans.
6. Run `afsim-knowledge-curator` to update records and traceability.
7. Run validators.
