# Claim Structural Fix

Refiner for the structural validator's findings. Fires per claim that has unresolved structural violations on its `.md` body — the claim's filename stem matches a finding's `file` field — and walks the apply-mode rule passes in order, dispatching mechanical fixes per (rule, file).

## Scope

One claim per fire. The trigger walks each claim derived from the ASN's source note (CLI mode), or every active `claim`-classified address (daemon mode). Predicate `is_claim_structurally_clean` runs the validator on the claim's directory and returns True (skip) iff zero actionable findings target this claim. Cycle findings (`acyclic-depends`) are excluded — propose mode is retired; the validator surfaces them but they don't make the claim "dirty" under this contract.

## Process

Each fire:

1. Resolve the claim path → derive `asn_label`, `claim_label`, and `claim_dir`.
2. Run the structural validator on `claim_dir` to produce findings.
3. Filter to actionable findings whose `file` stem matches `claim_label` (or whose `detail` mentions the label, for cycle-style findings).
4. For each pass in `PASSES` (body-uniqueness, declaration-label-mismatch, declared-symbols-resolve, depends-agreement, references-resolve):
   - Re-run the validator (state may have changed from previous pass)
   - Filter to this rule's findings on this claim
   - Group findings by file
   - For each (file, findings) group:
     - Copy file to a scratch tempdir
     - Build a substrate-sourced metadata bundle (label · name from substrate `name` links)
     - Invoke `fix_structural_rule` (Claude with Edit/Bash tools per the rule's prompt template)
     - Diff before vs after; for `depends-agreement`, parse the agent's `__decisions.json` sidecar (validates ADD/RETRACT/SKIP decisions per label, raises `DecisionsCorruption` on protocol violation, retries up to 2 attempts)
     - Apply the diff to the real file; commit per-file
     - For `depends-agreement`: emit `retraction` links for RETRACT decisions
     - On declines (no diff and no retractions): record (filename, rule) as declined; subsequent passes skip the pair to avoid re-attempt within this fire
5. Step-commit the agent's fire as a discrete event for audit/log. Per-rule edits commit individually inside the loop; this final commit is a no-op if every per-rule commit already landed.

## Trigger

- Predicate-fired by the runner: `is_claim_structurally_clean(claim_addr)` is the skip signal. Validator runs on every predicate check; cost is bearable because the validator is static (no LLM).
- Re-fires across runner passes if findings remain after a fire (rules that failed, declined, or new findings from prior edits). Decline state is ephemeral within a single fire (the `(filename, rule)` skip-pairs reset between fires); the runner's `max_iterations` cap is the protection against infinite re-fire.

## Inputs

- The structural validator's findings on the claim's directory
- Substrate-sourced metadata (label · name pairs for the claim and its same-ASN dependencies, used in the metadata bundle for depends-agreement / references-resolve prompts)
- The cross-ASN label index (substrate-built; maps every label → claim_addr)

## Outputs

Per-file substrate writes during a fire:
- `retraction` links on `citation.depends` for each RETRACT decision (depends-agreement only)
- File edits to `<claim>.md` applied via diff from the agent's scratch dir
- One `validate-revise(asn): <rule> on <filename>` git commit per per-file edit
- One `claim-structural-fix(asn): <asn_label>/<claim_label>` step commit per fire (no-op if no residue uncommitted)

On corruption (decisions sidecar violates contract): a transcript is written to `_store/_failures/validate-revise/<asn_label>/<filename>.<timestamp>.attempt<n>.txt`.

## Tools

- Reviser (per rule): Read + Edit, plus Bash for `declared-symbols-resolve` (the rule with `Bash` in its `tools` spec).

## Convergence

This agent is a mechanical refiner: it closes structural-validator findings by applying recipe fixes. Quiescence per-claim is the state where `is_claim_structurally_clean` returns True. Quiescence across an ASN is the state where every claim's predicate returns True. The runner walks the trigger until that state is reached, alternating with whatever else is in scope (review/revise) at the producer/refiner level.

## What was retired during the lift

Acyclic-depends propose mode (read-only suggestions for cycle findings) was dropped from the lifted agent. Cycle violations still surface in validator output but aren't actioned. If propose-style proposals come back, they should be designed as a scout caste agent — proposals don't fit the predicate-fire-and-close model the refiner caste uses.

The decline-tracking state was also reduced in scope: the original orchestrator persisted declines across `run_passes` invocations within one CLI run; the lifted agent treats declines as ephemeral within one fire (reset across runner passes). If declines need cross-pass persistence, a substrate marker (parallel to `decomposed`) can be added.
