# Baseline Workflow

This workflow is based on the provided AFSIM implementation plan. It uses "knowledge extraction -> requirement mapping -> code migration" as the main line.

## Phase 0: Environment and Project Setup

Create a repository with separate locations for records, architecture, requirements, migration work, tools, and tests. Define templates before generating large analysis outputs.

## Phase 1: AFSIM Source Structure Analysis

Responsible role: source analysis agent.

Inputs:

- AFSIM source directory
- Existing source index, if available

Outputs:

- Architecture overview
- Function index
- Module dependency report

Required evidence:

- Source file path
- Symbol name
- Line range when available
- Local dependencies

## Phase 2: Functional Flow and Math Analysis

Responsible roles: source analysis agent and math analysis agent.

Outputs:

- Functional flow report
- Math formula report
- Function API cards

Each formula explanation must include source location, variable mapping, physical meaning when known, and code-to-math correspondence.

## Phase 3: Own Simulator and Requirement Gap Analysis

Responsible role: requirement analysis agent.

Inputs:

- Own kernel source code
- Requirement documents
- AFSIM capability index

Outputs:

- Requirement gap analysis
- Missing feature specification

Classify each requirement as satisfied, partially satisfied, missing, or unknown.

## Phase 4: AFSIM Feature Location and Adaptation Plan

Responsible role: migration planning agent.

For each missing capability:

- Search the AFSIM index.
- Rank candidate functions and classes.
- Evaluate framework coupling.
- Define adapter interfaces.
- Identify tests and validation data.

## Phase 5: Code Migration and Integration

Responsible roles: migration agent and human reviewer.

Generate code only after the migration plan is clear. Keep generated changes small, testable, and aligned with the target project.

## Phase 6: Documentation and Closure

Responsible role: documentation agent.

Produce a traceability matrix from requirement to AFSIM source to own-project implementation. Archive decisions, assumptions, and validation results.
