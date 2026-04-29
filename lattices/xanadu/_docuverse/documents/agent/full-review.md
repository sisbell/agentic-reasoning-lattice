# Full Review

Whole-ASN review/revise agent. Operates on an entire ASN's claim files at once and drives the convergence predicate true through cycles.

## Scope

One ASN per invocation. Reads every claim md in `lattices/xanadu/claim-convergence/<asn>/` plus the ASN's foundation (recursively-loaded dependency claims). Reviews are filed against the assembled whole-ASN view.

## Process

Each cycle:

1. Re-feed any open `comment.revise` links from prior cycles to the reviser (retry pass).
2. Run the validator gate; halt if structural violations remain.
3. Assemble the ASN's claim files (read-only) plus its foundation.
4. Reviewer reads the assembly, files findings classified as REVISE or OBSERVE; emits `comment.revise` / `comment.observe` links.
5. Reviser addresses each REVISE finding by editing the affected claim md and emitting a `resolution.edit` (or `resolution.reject` with rationale).
6. Optionally invoke the cone-review agent on a detected dependency cone.
7. Natural-convergence check: this cycle filed zero revise comments and the substrate predicate is true.

Up to 8 cycles per invocation by default. The +1 confirmation runs if the work loop exhausted N cycles without observing natural convergence.

## Prompts

- `prompts/shared/claim-convergence/full-review/review.md`
- `prompts/shared/claim-convergence/full-review/revise.md`

## Tools

- Reviewer: Read (assembled context).
- Reviser: Read, Edit, Bash (`scripts/convergence-cite.py`, `scripts/link/retract.py`, `scripts/claim-classify.py`, `scripts/link/name.py`, `scripts/link/label.py`).

## Convergence

The agent terminates when the convergence predicate holds and the most recent cycle produced no revise findings — natural convergence — or after the +1 confirmation cycle, or at max-cycles bound. The outer orchestrator records the verdict; the substrate carries the trajectory.
