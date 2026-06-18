# Module Interface Export

You are extracting the **consumer-facing interface** from a converged module
detailed-design. The full design is the system of record; this extract is what a
*dependent* module's design loop reads in its place — the contract it builds
against, with the producing module's internal reasoning stripped out. It is to a
module design what claim-statements are to a note: the condensed, authoritative
contract, nothing else.

A dependent does not need (and is actively diluted by) this module's internal
data model, its algorithm internals, its resolved cross-note conflicts, its open
build decisions, or its rationale. It needs the **types and signatures it will
call**, the **obligations on the caller**, the **guarantees it may rely on**, the
**seams this module exposes to it**, and the **boundary** (what it must NOT expect
here). Extract exactly that.

## The module design

{{design}}

## Task

Produce the interface a downstream module builds against. Preserve every public
type and signature **verbatim** — names, parameters, return types, and the
generic/trait bounds — because a dependent's design must reference them exactly.
Around each, keep only the caller-relevant contract.

## Output format

Start directly with `# {{module_id}} — Interface (for dependents)` and a one-line
statement of what this module owns. Then these sections, in order:

```
## Public interface

[Every public type, trait, enum, and function signature, VERBATIM from the
design — in code blocks, exactly as written. Keep each item's one-line
precondition/contract comment when the design has one; drop multi-line internal
commentary.]

## Caller contracts & obligations

[For the items a dependent calls: the precondition the CALLER must discharge,
the guarantee/postcondition it may rely on, the error/None cases, and any
invariant a caller leans on (e.g. "every Address returned is T4-valid"). Bullet
form, one line each. This is the part that prevents a dependent from misusing
the seam.]

## Seams exposed downstream

[The contracts this module publishes for specific neighbors — e.g. "→ M5: ...",
"→ everyone: ...". Copy the design's "exposes downstream" seam list if present;
otherwise synthesize it from the signatures.]

## Boundary — NOT provided here

[The one-line list of what this module deliberately does NOT own, so a dependent
does not build against a non-existent seam.]
```

## What to include

- Public type/trait/enum/function signatures — **verbatim**, with bounds intact.
- The caller's precondition for each callable seam, and what it must discharge itself.
- Guarantees/invariants a caller may rely on.
- Error and absence (`None`/`Err`) cases a caller must handle.
- The downstream seam contracts (the "→ Mx" list).
- The boundary list (what is out of scope for this module).

## What to exclude

- The internal data model and storage representation.
- Algorithm internals and worked examples.
- "Conflicts resolved", "Open build decisions", and design rationale.
- Cross-note citation trails and historical context.
- Anything a dependent cannot observe through the public interface.

## Critical constraint

Do **not** rename, re-type, or "improve" any signature — a dependent references
them exactly, so a drifted name or bound is a defect. Copy signatures verbatim;
extract the contract, do not editorialize or redesign. If the design leaves a
seam's precondition implicit, state it as you find it — do not invent new
guarantees the design does not make.
