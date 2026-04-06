# Formalization Pipeline Design

## Background

The original formalization pipeline was a monolithic 9-step sequence:
stabilize → repair → stabilize → quality → stabilize → audit → verify →
stabilize → assembly → cleanup. Each step ran in order, and cleanup deleted
open-issues.md unconditionally.

This caused several problems:

1. **Silent data loss.** The audit step (surface check, mechanical check,
   extension verification, open-ended audit) produced findings and wrote
   them to open-issues.md, but no step processed them. Cleanup deleted the
   file, silently dropping unresolved findings. In ASN-0040, this caused
   7 findings — including two serious correctness issues (carrier-set
   conflation, broken precondition chain) — to be lost. They were only
   recoverable from git history.

2. **No fix loop for audit findings.** Only the verify step had a
   find → fix → re-verify cycle. Quality had a retry loop for missing
   formal contracts. But audit findings (stale labels, naming mismatches,
   redefinitions, structural issues) had no reviser — they were
   write-only.

3. **Cascading one-at-a-time fixes.** The verify step fixed proofs
   one property at a time. Each fix could change the ASN in ways that
   affected other properties, causing a cascade that prevented convergence.
   ASN-0040 exhibited this behavior.

4. **Coupled steps.** Each step assumed the previous steps had run. The
   `--only` flag existed but steps weren't truly independent — running
   quality alone could fail if format hadn't run first.

5. **Mixed concerns.** Quality did both Dijkstra rewriting and formal
   contract extraction. Audit bundled four unrelated checks (mechanical,
   surface, extension, open-ended) into one step. Repair was a one-time
   setup step mixed into the repeating pipeline.

## Redesigned Pipeline

### Five pipelines with a shared format gate

Every pipeline runs **Format** on entry — normalize structure, populate
names, generate deps. Format is idempotent: if the ASN hasn't changed
since the last clean, it's a no-op (mtime check, instant skip). This
replaces the four explicit stabilize calls in the old pipeline.

Format is not a standalone pipeline. It's infrastructure that every
pipeline invokes as a precondition. Any pipeline can mutate the ASN
(adding properties, changing proofs, updating the dependency table), and
the next pipeline's Format gate re-normalizes before proceeding.

### Pipeline 1: Formalize

**Purpose:** Take each property from informal/semi-formal prose to
rigorous Dijkstra-style proof with a formal contract.

**What it does:**
- If a property section is incomplete or missing its own proof (proof
  embedded in another section), fill it in first (the old "repair" step).
  This is a precondition within Formalize, not a separate pipeline — once
  every property has its own section, repair never runs again.
- Rewrite the proof in Dijkstra's style: prose with embedded formalism,
  explicit cases, no hand-waving.
- Ensure the property section has a `*Formal Contract:*` with the
  applicable fields (Preconditions, Postconditions, Invariant, Frame,
  Axiom, Definition).

**Gate:** Property has a formal contract section that matches its proof.

**Review loop:** Rewrite → check for formal contract → retry if missing
(up to 3 cycles per property).

**Preconditions:** Format gate.

**Why this name:** "Quality" was the old name but sounded like QA
checking. This step IS the formalization — it's the core work of turning
an ASN into a formal specification.

### Pipeline 2: Dependency Audit

**Purpose:** Verify that this ASN's relationship to its upstream
dependencies is correct.

**What it does — three passes, one reviser:**

1. **Mechanical pass** (deterministic, no LLM):
   - Every label in follows_from exists in a dependency's exports
   - Prose citations of foundation labels are in the deps YAML
   - No undeclared cross-ASN references
   - Prose-only citations (cited in text but not in follows_from)

2. **Cross-reference pass** (LLM):
   - Property names match upstream canonical names (e.g., T5 should be
     cited as "ContiguousSubtrees" not "PrefixContiguity")
   - No local redefinitions of upstream properties (e.g., B8
     re-deriving GlobalUniqueness that ASN-0034 already exports)

3. **Extension pass** (LLM):
   - When a property claims to extend or parallel an upstream property,
     verify the semantic relationship actually holds

**Gate:** All three passes clean.

**Review loop:** Find issues → reviser applies fix (guided by the
finding's Required section) → re-run the relevant pass. One reviser
for all three passes.

**Preconditions:** Format gate. Upstream ASNs must have run Assembly
(formal-statements.md must exist for each dependency).

**Why one pipeline:** All three passes check the same concern — does
this ASN's contract with its dependencies hold? Stale labels,
wrong names, and broken semantic claims are all dependency issues.
The reviser needs the same context for all of them.

### Pipeline 3: Open-ended Audit

**Purpose:** Find structural and semantic issues that the other
pipelines can't catch.

**What it does:** Reads the whole ASN and looks for cross-cutting
problems:
- Carrier-set conflation (using T where T4-valid subset is meant)
- Precondition chain gaps (caller doesn't satisfy callee's contract)
- Ambiguous invariants
- Proof strategies that work but use incorrect justifications

These are issues that span multiple properties or involve the
relationship between the ASN's language and the foundation's
definitions. The structured checks in Proof Review and Dependency
Audit can't find them because they check one property or one
reference at a time.

**Gate:** No findings, or all findings addressed.

**Review loop:** Find issues → reviser applies fix → re-run audit.

**Preconditions:** Format gate. Should run after Formalize (no point
auditing un-formalized prose).

### Pipeline 4: Proof Review

**Purpose:** Check each proof for correctness against a rigorous
checklist.

**What it does — per property, in dependency order:**

1. Precondition completeness — are all required inputs stated?
2. Case coverage — is the case analysis exhaustive?
3. Postcondition establishment — does the proof actually establish
   what the formal contract claims?
4. All conjuncts addressed — every part of the postcondition proven?
5. Dependency correctness — are all used properties declared?
6. Formal contract match — does the contract reflect the proof?
7. Missing guarantees — does the proof establish something not
   captured in the contract?

**Gate:** Property passes all 7 checks (VERIFIED).

**Review loop:** Verify → if FOUND, reviser applies fix (guided by
finding) → re-verify (up to 10 cycles per property).

**Preconditions:** Format gate. Should run after Formalize (needs
formal contracts to check against).

**Why "Proof Review" not "Verify":** "Verify" sounds like it just
confirms something. This step is doing the work of a formal methods
reviewer — evaluating proof soundness, completeness, and contract
fidelity.

### Pipeline 5: Assembly

**Purpose:** Produce the pipeline's output artifacts.

**What it does:**
- Generate formal-statements.md from the formalized property sections
- Regenerate dependency-graph.yaml
- Run dafny_modules coverage check (if bucket mapping exists)

**Gate:** Files produced, coverage check passes.

**Review loop:** None — mechanical output generation.

**Preconditions:** Format gate. Should run after Formalize (needs
formalized properties to extract).

## Ordering constraints

```
Format gate (runs on entry to every pipeline)
    │
    ├── Formalize
    │       │
    │       ├── Proof Review
    │       ├── Open-ended Audit
    │       └── Assembly
    │
    └── Dependency Audit (independent of Formalize)
```

- **Formalize** requires only the Format gate.
- **Dependency Audit** requires only the Format gate and upstream
  ASNs having Assembly output. It can run in parallel with Formalize.
- **Proof Review** requires Formalize (needs formal contracts).
- **Open-ended Audit** requires Formalize (reviews formalized prose).
- **Assembly** requires Formalize (extracts from formalized sections).
- **Proof Review** and **Open-ended Audit** are independent of each
  other and of Dependency Audit.

## Convergence modes

The three per-property pipelines (Formalize, Dependency Audit, Proof
Review) share a convergence mechanism. Each pipeline runs over a set
of properties, may change some of them, and needs to determine when
to stop. There are two modes:

### Incremental convergence

Track which properties changed ("dirty set") and narrow each pass
to only those properties plus their downstream dependents.

```
dirty_set = all properties
while dirty_set is not empty and cycle < max_cycles:
    run pipeline on dirty_set
    changed = properties that were modified
    dirty_set = changed ∪ downstream_dependents(changed)
    cycle += 1
if dirty_set is not empty:
    flag non-convergence with remaining dirty set
```

This is efficient — each pass does less work than the last, and the
dirty set shrinks toward empty. The dependency graph propagation
ensures that if fixing property A affects property B (which depends
on A), B gets re-checked even though the pipeline didn't directly
touch it.

### Full sweep convergence

Every pass runs across all properties. Keeps going until a full pass
produces zero changes, or the cycle limit is reached.

```
while cycle < max_cycles:
    run pipeline on all properties
    if nothing changed:
        converged
        break
    cycle += 1
if not converged:
    flag non-convergence
```

More expensive but catches issues that incremental might miss — for
example, a property that wasn't in the dirty set but has a latent
issue exposed by changes elsewhere that the dependency graph doesn't
capture.

### Which mode for which pipeline

Both modes require a cycle limit (always enforced, never optional).

- **Formalize** — default incremental. Expensive per property (LLM
  rewrite), so minimizing the set matters. The dependency graph
  reliably propagates: if a formal contract changes, dependents
  need re-checking.

- **Dependency Audit** — default full sweep. The mechanical pass is
  cheap, so running across all properties costs little. Cross-reference
  and extension passes are more expensive but the finding set is
  typically small.

- **Proof Review** — default incremental. Expensive per property
  (Opus verification call). Dependency-ordered processing already
  ensures upstream fixes are visible to downstream checks.

The mode can be overridden per invocation (e.g., force full sweep
on Formalize when incremental isn't converging, or force incremental
on Dependency Audit for a targeted re-check).

### No separate fix verification

The current pipeline has a loop within a loop: verify a property →
fix it → immediately re-verify the same property → if still broken,
fix again (up to 10 inner cycles). This inner verification step is
removed in the new design.

Under the convergence loop, the pipeline itself is the verification.
If the reviser fails to fix an issue, the next pass finds the same
issue — the property stays in the dirty set. If the reviser makes a
bad fix that introduces a new problem, the next pass catches it.
The outcome is the same but the mechanism is simpler: one loop, not
a loop within a loop.

The cycle limit protects against the case where the reviser keeps
making bad fixes or where two properties keep dirtying each other.
Instead of an inner loop retrying N times nested inside an outer
loop, there is one convergence loop with one limit. This also means
every property in the dirty set gets equal attention on each pass —
the pipeline doesn't spend 10 cycles on one stuck property while
others wait.

## Reviser design

All four review pipelines share one principle: the reviser is
finding-driven. The reviewer produces a finding with a `**Problem**`
section (what's wrong) and a `**Required**` section (what to do).
The reviser executes the Required instruction against the specific
property section.

The revise prompt is: Dijkstra methodology priming + property section
context + the reviewer's finding. The reviewer tells the reviser
*what* to change. The methodology tells the reviser *how* to write.
The revise prompt does not hard-code fix rules — different pipelines
produce different kinds of findings, and the reviser handles them
all through the same finding-driven mechanism.

## What was removed

- **open-issues.md** as an accumulator. Each pipeline's review loop
  tracks its own findings through the find → fix → re-check cycle.
  Review files in `vault/2-review/` remain as the persistent audit
  trail.

- **Cleanup step** that deleted open-issues.md. Replaced by each
  pipeline managing its own state.

- **Repair** as a separate pipeline. Folded into Formalize as a
  precondition — if a property section is incomplete, fill it in
  before formalizing.

- **Stabilize** as an explicit pipeline step. Replaced by the Format
  gate that every pipeline runs on entry.
