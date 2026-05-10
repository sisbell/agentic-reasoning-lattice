# Claim Findings

Decomposes a claim-review doc into per-finding substrate. Owns the second stage of the review → findings → revise chain: the upstream review producer (cone-review or full-review) emits the review doc as prose; this agent reads it, extracts each finding, runs the classifier-override sub-routine, and emits the per-finding substrate plus the `decomposed` marker.

## Scope

One review doc per fire. The scope walker yields every active `review` classifier whose target is a review under the requested ASN's claim-review namespace (`_docuverse/documents/review/claims/<asn_label>/`). Daemon mode walks every active review.

## Process

Each fire:

1. Resolve the review_addr to its file path; read the review prose verbatim from disk.
2. `extract_findings` parses each `### `-prefixed section into a `(title, cls, body)` tuple. The reviewer's class (REVISE / OBSERVE) is captured from the body's `**Class**:` line.
3. `apply_classifier_verdict` runs the override sub-routine — a separate Sonnet call per finding that re-classifies on disagreement. The agent's empirical justification: across observed disagreements, the classifier was right ~73% of the time and the reviewer's failure mode is severe (under-flagging real defects). The list is mutated in place; downstream sees the corrected classes.
4. `record_findings` emits the per-finding substrate for each finding:
   - Writes the finding-body verbatim to `_docuverse/documents/finding/claims/<asn>/review-N/<n>.md`.
   - Emits `finding` classifier on the per-finding doc.
   - Emits `comment.<cls>` (revise or observe) from finding doc → target claim.
   - Emits `provenance.derivation` from review doc → finding doc.
5. Emits `decomposed` classifier on the review doc — the fire-once marker that closes the trigger predicate. Emitted whether the review yielded zero findings (CONVERGED verdict) or many.

## Trigger

- Predicate-fired by the runner: `is_decomposed(review_addr)` is the skip signal. Fires once per review.
- The substrate-readable signal `decomposed` distinguishes "review hasn't been processed" from "review was processed and produced no findings." Without it, a CONVERGED review with zero findings would re-fire forever.

## Inputs

- The review doc's file content (prose, including each `### `-prefixed finding section)
- Cross-ASN label index built from substrate (resolves `**ASN**:` / `**Foundation**:` headers in finding bodies to claim addresses)

## Outputs

- One `<n>.md` finding doc per emitted finding under `_docuverse/documents/finding/claims/<asn>/review-N/`
- `finding` classifier on each per-finding doc
- `comment.revise` or `comment.observe` from each per-finding doc to its target claim
- `provenance.derivation` from review_addr to each finding_addr
- `decomposed` classifier on the review doc (always, even with zero findings)

## Tools

None. The agent reads the review file directly and emits substrate via the `lib.lattice.findings` and `lib.backend.emit` helpers; it doesn't drive an LLM session beyond the override sub-routine, which is internal to its run.

## Convergence

Per the create/close framing in the agent-castes taxonomy, this agent is a producer — it grants substrate identity (per-finding docs + their classifier links). It closes the predicate it fires on by *creating* substrate, not by editing or resolving. After fire, downstream refiners (claim-revise) pick up the per-finding `comment.revise` links and close them; quiescence is reached when every emitted comment has a resolution.
