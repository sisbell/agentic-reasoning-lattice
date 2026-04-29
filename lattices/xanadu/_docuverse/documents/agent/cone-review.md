# Cone Review

Focused review/revise agent operating on a *dependency cone* — an apex claim plus its transitive dependency closure. Runs when a single claim is being repeatedly revised against (relatively) stable dependencies, where whole-ASN review's broad lens may miss the apex-specific reasoning gap.

## Scope

One cone per invocation:
- An apex claim (the focus of attention)
- Its transitive dependency closure (claims the apex cites, directly and indirectly, within the same ASN)

Scope is assembled by the orchestrator: the apex label plus the list of dep labels. The cone-review agent reads the apex's full content plus its dependency claims as context.

## Process

Each cycle:

1. Re-feed any open `comment.revise` links targeting the apex (retry pass).
2. Validator gate on the cone.
3. Reviewer reads the cone, files findings narrowly focused on the apex's reasoning relative to its dependencies; emits `comment.revise` / `comment.observe`.
4. Reviser addresses REVISE findings on the apex md, files `resolution.edit` (or `resolution.reject` with rationale).

Up to 3 cycles per invocation by default — cones converge faster than whole-ASN reviews because the scope is tight.

## Trigger

- Detected automatically by full-review: an apex with high recent revise activity while its deps are stable.
- Explicit invocation: `python scripts/claim-full-review.py <asn> --cone <apex>`.
- Bulk sweep: `python scripts/claim-cone-sweep.py <asn>` walks high-dependency cones in DAG order.

## Prompts

Cone-review reuses the full-review prompts:
- `prompts/shared/claim-convergence/full-review/review.md`
- `prompts/shared/claim-convergence/full-review/revise.md`

The same prompts are scoped differently — cone-review's assembled context is the cone, not the whole ASN. The reviewer's output classifications and the reviser's tool surface are identical to full-review.

## Tools

- Reviewer: Read (cone context).
- Reviser: Read, Edit, Bash (`scripts/convergence-link-cite.py`, `scripts/substrate/retract.py`, `scripts/claim-link-contract.py`, `scripts/substrate/name.py`, `scripts/substrate/label.py`).

## Convergence

The cone-review agent terminates when its reviewer files zero revise findings on the cone and the substrate predicate is true for the cone's claims. Per A3, "did the most recent cone-review on this apex converge?" is a substrate query against this agent's `manages` links.
