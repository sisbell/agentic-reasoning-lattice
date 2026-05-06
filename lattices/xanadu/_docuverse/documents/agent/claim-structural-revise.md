# Claim Structural Revise

Refiner that closes `comment.violation` findings emitted by the structural-audit scout. Fires per claim that has unresolved violations and walks the apply-mode rule passes in order, dispatching mechanical fixes per (rule, file) and emitting `resolution.<kind>` per closed comment. Naming follows the `*_revise` refiner convention (note_revise, claim_revise, claim_structural_revise) — refiners that close `comment.<kind>` via `resolution.<kind>` share the verb regardless of the input subtype.

## Scope

One claim per fire. The trigger walks each claim derived from the ASN's source note (CLI mode), or every active `claim`-classified address (daemon mode). Predicate `is_claim_structurally_clean(claim_addr)` is a substrate read: True (skip) iff every `comment.violation` link targeting the claim has a `resolution.<kind>`. False (fire) when at least one violation is unresolved.

## Process

Each fire:

1. Resolve the claim path → derive `asn_label`, `claim_label`, `asn_num`, `claim_dir`.
2. Read substrate findings: walk active `comment.violation` links targeting the claim, filter to those without resolutions, walk back to each finding doc, parse the body for `rule`, `file`, `line`, `detail`. Each finding dict carries `comment_addr` for downstream resolution emission.
3. For each pass in `PASSES` (body-uniqueness, declaration-label-mismatch, declared-symbols-resolve, depends-agreement, references-resolve):
   - Filter substrate findings to this rule's findings on this claim
   - Group findings by file
   - For each (file, findings) group:
     - Copy file to a scratch tempdir
     - Build a substrate-sourced metadata bundle (label · name from substrate `name` links)
     - Invoke `fix_structural_rule` (Claude with Edit/Bash tools per the rule's prompt template)
     - Diff before vs after; for `depends-agreement`, parse the agent's `__decisions.json` sidecar (validates ADD/RETRACT/SKIP decisions per label, raises `DecisionsCorruption` on protocol violation, retries up to 2 attempts)
     - Apply the diff to the real file; commit per-file
     - For `depends-agreement`: emit `retraction` links for RETRACT decisions
     - Emit `resolution.edit` (claim_addr → comment_addr) per closed comment in the group when fix lands; emit `resolution.reject` per comment when the group declines (no diff, no retracts)
4. Step-commit the agent's fire as a discrete event. Per-rule edits commit individually inside the loop; this final commit is a no-op if every per-rule commit already landed.

## Trigger

- Predicate-fired by the runner: `is_claim_structurally_clean(claim_addr)` is the skip signal. Pure substrate read; no validator runs from inside the predicate (the structural-audit scout owns detection).
- Decline state across fires now persists naturally via `resolution.reject` — the predicate sees declined comments as resolved and the trigger skips them on next fire. No more ephemeral skip_pairs across runner passes.
- Re-fires across runner passes when fresh `comment.violation` links emerge from a subsequent audit-scout fire on post-edit state.

## Inputs

- Unresolved `comment.violation` links targeting the claim (read from substrate)
- Per-finding doc bodies with `rule`, `file`, `line`, `detail` (parsed)
- Substrate-sourced metadata (label · name pairs for the claim and its same-ASN dependencies, used in the metadata bundle for depends-agreement / references-resolve prompts)
- The cross-ASN label index (substrate-built; maps every label → claim_addr)

## Outputs

Per-file substrate writes during a fire:
- `resolution.edit` from claim → comment_addr per comment whose group's fix landed
- `resolution.reject` from claim → comment_addr per comment whose group declined
- `retraction` links on `citation.depends` for each RETRACT decision (depends-agreement only)
- File edits to `<claim>.md` applied via diff from the agent's scratch dir
- One `validate-revise(asn): <rule> on <filename>` git commit per per-file edit
- One `claim-structural-revise(asn): <asn_label>/<claim_label>` step commit per fire (no-op if no residue uncommitted)

On corruption (decisions sidecar violates contract): a transcript is written to `_store/_failures/validate-revise/<asn_label>/<filename>.<timestamp>.attempt<n>.txt`.

## Tools

- Reviser (per rule): Read + Edit, plus Bash for `declared-symbols-resolve` (the rule with `Bash` in its `tools` spec).

## Convergence

This agent is a mechanical refiner: it closes structural-validator findings (via the audit scout) by applying recipe fixes. Quiescence per-claim is the state where `is_claim_structurally_clean` returns True (every `comment.violation` has a resolution). Quiescence across an ASN is the state where every claim's predicate returns True. The runner walks both this trigger and `claim-structural-audit` until that state is reached.

The Producer→Refiner cycle:

```
ClaimStructuralAuditAgent (scout)        →   ClaimStructuralReviseAgent (refiner)
runs validator,                              reads comment.violation from substrate,
emits audit doc + per-violation findings     applies per-rule fix per (rule, file),
+ comment.violation                          emits resolution.<kind> per closed comment
```

Refiner edits invalidate the audit's coverage (latest audit's violations resolved → audit re-fires on post-fix state). Eventually: latest audit clean (zero violations) AND no unresolved comment.violation. Both predicates True → quiescence.

## What was retired during the lift

Acyclic-depends propose mode (read-only suggestions for cycle findings) was dropped during the orchestrator lift. Cycle violations surface in validator output but aren't actioned. If propose-style proposals come back, they should be designed as a scout-caste agent — proposals don't fit the predicate-fire-and-close model the refiner caste uses.

The validator no longer runs inside this agent — it lives in the structural-audit scout, which detects violations and emits substrate. The refiner is pure closure: substrate read → fix → resolution emission.
