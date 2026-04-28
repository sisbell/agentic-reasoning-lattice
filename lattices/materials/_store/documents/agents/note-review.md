# Note Review

Whole-note review/revise agent. Operates on a single note document during discovery and drives the convergence predicate true through review/revise cycles.

## Scope

One note per invocation. Reads the note doc plus its citation foundations (notes the current note depends on, recursively loaded). Findings are filed against the assembled context.

## Process

Each cycle:

1. Re-feed any open `comment.revise` links targeting the note (retry pass).
2. Reviewer reads the assembly, files findings classified as REVISE or OUT_OF_SCOPE; emits `comment.revise` / `comment.out-of-scope` links.
3. Reviser addresses each REVISE finding by editing the note md and emitting a `resolution.edit` (or `resolution.reject` with rationale).
4. Natural-convergence check: this cycle filed zero revise comments and the substrate predicate is true.

`comment.out-of-scope` links persist as substrate-level signals for maturation (extract/absorb/promote); the reviser takes no action on them per the [Note Convergence Protocol](../../../../../docs/protocols/note-convergence-protocol.md) §6.6.

## Prompts

- `prompts/materials/discovery/review.md`
- `prompts/materials/discovery/revise/` (revise tool prompts)

## Tools

- Reviewer: Read (assembled context).
- Reviser: Read, Edit, Bash (`scripts/cite.py`, `scripts/retract.py`, `scripts/decide.py`).

## Convergence

The agent terminates when the convergence predicate holds and the most recent cycle produced no revise findings — natural convergence — or after the +1 confirmation cycle, or at max-cycles bound. The outer orchestrator records the verdict; the substrate carries the trajectory.
