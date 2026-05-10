# Claim Structural Audit

The system's first scout-caste agent. Patrols claim md files to detect structural-validator violations and emits per-finding substrate so the structural-fix refiner can close them via existing resolution machinery. Identifies, classifies, signals — does not author content, does not edit claims.

## Scope

One claim per fire. The trigger walks each claim derived from the ASN's source note (CLI mode), or every active `claim`-classified address (daemon mode). The predicate `is_claim_audit_fresh` is closure-style staleness:

- True (skip) iff the latest audit covering this claim was clean (zero violations) OR the latest audit's violations include at least one unresolved `comment.violation` (refiner is still working).
- False (fire) iff no audit covers this claim yet, OR all violations from the latest audit have been resolved (need re-audit on post-fix state).

No verb-flag classifiers, no marker state. The substrate (audit doc + `review.coverage` + per-violation findings + their resolution status) carries everything the predicate needs.

## Process

Each fire:

1. Resolve claim path → derive `asn_label`, `claim_label`, `asn_num`.
2. Run the structural validator on the claim's directory; filter findings to those whose `file` stem matches `claim_label`.
3. Emit the audit doc:
   - Path: `_docuverse/documents/audit/claims/<asn>/<claim>-<n>.md`
   - Body: timestamp + per-rule outcomes (clean / N violations) for every rule the validator checks
   - `review.structural` classifier on the audit doc
   - `review.coverage` link from audit doc → claim
4. For each violation found, emit:
   - Per-finding doc at `_docuverse/documents/finding/claims/<asn>/audit-<n>/<rule>-<i>.md`, body = rule + file + line + detail
   - `finding` classifier on the per-finding doc
   - `comment.violation` link from per-finding doc → claim (the open issue the refiner reads)
   - `provenance.derivation` from audit doc → per-finding doc
5. Step commit + return AgentResult.

## Caste justification

- **Working surface:** structural form. The validator's checks (body-uniqueness, declaration-label-mismatch, declared-symbols-resolve, depends-agreement, references-resolve) are about structural conformance — invariants over the claim's form, not assessments of its reasoning. Reading prose to check structural form is scout territory under the agent-castes axis "what aspect of the artifact you analyze."
- **Detection happens here:** the validator runs *inside* this agent. The findings emitted to substrate aren't persisted from upstream LLM output; they're discovered by this agent's run. Distinguishes scouts (detect) from producers (author content) and from `claim_findings` (parses pre-existing LLM-detected findings into substrate).
- **Identity grant:** scouts share the create-side cut with producers. Audit docs and per-finding docs are new substrate identities. What separates the castes is working surface, not predicate-direction.

## Trigger

Predicate-fired by the runner. Closure-style staleness; re-fires when refiner has closed all violations from the latest audit (need to verify post-fix state). Per-claim granularity matches the structural-fix refiner; runner walks both triggers in alternation until quiescence.

## Inputs

- The structural validator's findings (returned in-memory by `claim-validate.py`'s `run_all_checks`)
- Cross-ASN label index (built from substrate; available via `lib.lattice.labels.build_cross_asn_label_index` if needed for finding-body context)

## Outputs

Per fire:
- One audit doc with `review.structural` classifier + `review.coverage` link to the claim
- Zero or more per-finding docs (one per violation), each with `finding` classifier + `comment.violation` link to the claim + `provenance.derivation` from audit doc
- One git commit (`claim-structural-audit(asn): <asn_label>/<claim_label> audit-<n> violations=<N>`)

## Tools

None — the validator runs in-process (no LLM, no Bash). Pure static analysis dispatched via `importlib`.

## Convergence

This agent is a scout. Its complement is the `ClaimStructuralReviseAgent` refiner, which reads `comment.violation` from substrate and closes via `resolution.<kind>`. Cycle:

```
1. Audit fires → emits audit doc + per-violation findings + comment.violation
2. Refiner fires per comment.violation → fixes (resolution.edit) or rejects
   (resolution.reject); edits claim md as needed
3. After all violations closed, audit's predicate flips False → re-fire
4. New audit on post-fix state — clean (quiescence) or new findings (loop)
5. Equilibrium: latest audit was clean → predicate True → quiescence
```

## What this isn't

- **Not a content reviewer.** Doesn't read the claim's reasoning, doesn't judge argument quality, doesn't author critique prose. The LLM reviewer (claim_review producer / cone_review / full_review) handles content critique; this scout handles structural form.
- **Not a fixer.** Emits open issues; doesn't close them. The structural-fix refiner closes via existing resolution machinery.
- **Not the validator.** The validator is `claim-validate.py` — a static-analysis module. This scout is the substrate-bearing wrapper that runs the validator and persists its output.
