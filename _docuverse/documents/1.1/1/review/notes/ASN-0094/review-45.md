# Review of ASN-0094

## REVISE

### Issue 1: Provenance walkthrough pre-allocation list incomplete

**ASN-0094, Additional Worked Examples → Provenance (partial G-slot)**:

> "Pre-allocate `s, t, t' ∈ A^{Σ_0}` (any allocated addresses; `t_F = t_G = A` admits both content and relation addresses)."

Then Form 2 introduces an unallocated symbol:

> "`Emit_K(Σ_P1, home_prov, {(s', δ(1, #s'))}, ∅)` with `s' ∈ A^{Σ_P1}` (... we use a fresh `s' ∈ A^{Σ_0}` distinct from `s` for clarity)"

**Problem**: The walkthrough states `s' ∈ A^{Σ_0}` but `s'` is not in the pre-allocation list. The parenthetical implicitly extends pre-allocation without updating the explicit list. Forms 3 and 5 then depend on the slot-address-set inequality `{s'} ≠ {s}`, which is load-bearing for the candidate-set filtering in those Forms' Sh4-contract analyses. A reader who follows the explicit pre-allocation list would be unable to instantiate Form 2.

**Required**: Either extend the pre-allocation list to `Pre-allocate s, s', t, t' ∈ A^{Σ_0}`, or make Form 2's parenthetical clearer that `s'` is pre-allocated independently of the opening list (e.g., move the `s'` allocation into a dedicated pre-allocation paragraph between Form 1 and Form 2).

## OUT_OF_SCOPE

### Topic 1: (Peano-rec) is a foundation extension, not an ASN-0094 concern

**Why out of scope**: The appendix introduces `m + (n + 1) = (m + n) + 1` as a "Peano-core upstream supplement to NAT-closure" — required for NAT-sub's derivation but absent from the foundation's listed NAT axioms (NAT-closure, NAT-order, NAT-discrete, NAT-addcompat, NAT-wellorder). The framework acknowledges this and proposes a future foundation extension. Fixing this belongs in the foundation ASN, not in ASN-0094 — the appendix's discharge is sufficient for ASN-0094's local needs.

### Topic 2: Multi-process substrate consistency

**Why out of scope**: The *Sh4 idempotency contract* and *FDD functional-dependency contract* commit to single-process substrates by design. The Open Questions section flags this as a scope boundary requiring a coordination protocol extension; not an ASN-0094 gap to repair.

### Topic 3: Per-shape body-shape uniformity sharpening

**Why out of scope**: The Sh5(a) status downgrades per-shape body-shape uniformity from commitment to aspiration. Sharpening to a procedural recipe (e.g., body-shape derivation procedure keyed off shape components) is recorded as future work. The current catalog meets the aspiration by hand-curation; this is acknowledged scope, not a defect.

### Topic 4: Mechanical catalog-extension tooling

**Why out of scope**: Sh5(b)'s discipline is enforced by manual review per the *Catalog extension is a manual review process* paragraph. The framework declines to commit additional artifacts (auditor role, periodic re-audit cadence, automated tooling). This is a scope decision, not a defect.

VERDICT: REVISE
