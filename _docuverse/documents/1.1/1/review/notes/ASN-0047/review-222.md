# Review of ASN-0047

## REVISE

### Issue 1: S8★ mislabels and internally contradicts ASN-0036's S8 conditions
**ASN-0047, *Amendments to existing transitions* (S8★ definition)**: "S8★ carries only ASN-0036's S8 conditions (a) (run-cover: every V-position lies in exactly one run) and (b) (lockstep advance with label membership). It intentionally does not carry ASN-0036's S8 condition (c)... For the link subspace it is a *modified* condition (b): ASN-0036's condition (b) carries a label-membership conjunct `aⱼ ∈ dom(Σ.C)` (and `shift(aⱼ, k) ∈ dom(Σ.C)`)..."

**Problem**: The labels do not match the foundation, and the description contradicts itself.
- In ASN-0036, condition **(a)** is *lockstep displacement* (`shift(vⱼ,k) ∈ dom(M(d))`, `M(d)(shift(vⱼ,k)) = shift(aⱼ,k)`, and `shift(aⱼ,k) ∈ dom(Σ.C)`); condition **(b)** is *label well-definedness* (`aⱼ` well-defined by S2, `aⱼ ∈ dom(Σ.C)`); condition **(c)** is uniqueness. "Run-cover" (the partition claim) is the theorem-level statement, not condition (a).
- ASN-0047 first calls (a) "run-cover" and (b) "lockstep advance," i.e. it has swapped lockstep out of (a) and named the partition claim (a). Then, when discharging the link projection, it attributes `shift(aⱼ,k) ∈ dom(Σ.C)` to "condition (b)" — but that conjunct lives in ASN-0036's (a). A reader checking *which* foundation conjuncts S8★ retains versus drops cannot do so against these labels.

**Required**: Relabel against ASN-0036 verbatim. State that S8★ retains the finite-run *partition* (run-cover) together with conditions (a) [lockstep, with the `dom(C)` membership of `shift(aⱼ,k)`] and (b) [label well-definedness with `aⱼ ∈ dom(C)`], drops (c) [uniqueness], and for the link projection substitutes `dom(C) → dom(L)` in the membership conjuncts of *both* (a) and (b). Make the prose use one consistent labeling throughout.

### Issue 2: Redundant pointer table — "Derived structural identities"
**ASN-0047, *Properties Introduced* → "Derived structural identities" table**: all four rows (K.δ-ID.zeros-0/1, zeros-2, parent-0/1, parent-2) carry the derivation column "See K.δ case (ii) catalogue."

**Problem**: The four identities are already stated with full statement *and* derivation in the inline "Structural identities on `e = inc(t, k)`" catalogue under K.δ case (ii). This standalone table restates the statements a second time while its entire derivation column is a back-pointer to the catalogue it duplicates — it advances no reasoning. This is the "pure downstream-deferral" / "two paragraphs say the same thing" pattern the anti-bloat classifier asks to surface at source.

**Required**: Remove the table (the inline catalogue is the single source), or, if a summary index is wanted, fold the four labels into the "New properties" table as one-line entries without a derivation column that only points back.

## OUT_OF_SCOPE

### Topic 1: Forked-arrangement relationship to source arrangement
Whether a fork's initial arrangement must be identical to, or may be a proper subset/reordering of, the source's content arrangement is not constrained by J4. This is already the ASN's own Open Question 1 — new territory, not an error here.

META: not applicable — the ASN defines abstract state, elementary transitions, and invariants stated implementation-independently; it has not drifted into implementation mechanics.

VERDICT: REVISE
