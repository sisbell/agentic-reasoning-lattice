# Cone Review — ASN-0034/T8 (cycle 1)

*2026-04-15 20:49*

### TumblerSub contract weakens zpd-component inequality, breaking actionPoint = zpd across property boundary

**Foundation**: T1 (LexicographicOrder), ZPD, Divergence — used in TumblerSub's precondition consequence derivation
**ASN**: TumblerSub formal contract — "Consequence (by Divergence case analysis via T1, Divergence, ZPD): when zpd(a, w) is defined, aₖ ≥ wₖ at k = zpd(a, w)"
**Issue**: The proof establishes the strict inequality aₖ > wₖ in both Divergence cases: case (i) yields `wₖ < aₖ`, case (ii) yields `aₖ > 0 = wₖ`. But the contract exports only `aₖ ≥ wₖ`. This weakening is load-bearing downstream: the TumblerSub narrative asserts `actionPoint(b ⊖ a) = zpd(b, a)`, which requires `(b ⊖ a)ₖ = bₖ - aₖ > 0` at the zpd point — i.e., the subtraction result's first nonzero component is at exactly the zpd position. The non-strict `≥` permits `(b ⊖ a)ₖ = 0`, which would place the action point *after* the zpd position, making `actionPoint ≠ zpd`. The roundtrip condition (referenced via D0) substitutes `zpd(b, a) ≤ #a` for TumblerAdd's precondition `actionPoint(w) ≤ #a` — a substitution valid only when the equation `actionPoint(b ⊖ a) = zpd(b, a)` holds.
**What needs resolving**: The contract's consequence must export the strict inequality `aₖ > wₖ` (not `≥`) at k = zpd(a, w) when zpd is defined. Alternatively, a postcondition must assert that when zpd(a, w) is defined, `(a ⊖ w)ₖ > 0` at k = zpd(a, w), so that the actionPoint = zpd equation is grounded in the contract and available to D0.

---

### T10a.2 prefix-incomparability claim ungrounded — Prefix (PrefixRelation) absent from formal contract

**Foundation**: Prefix (PrefixRelation) — "tumblers of equal length are prefix-related only if identical"
**ASN**: T10a formal contract, postcondition T10a.2 — "For all siblings a, b from the same allocator, same\_allocator(a, b) ∧ a ≠ b → a and b are prefix-incomparable, satisfying the precondition of T10"
**Issue**: The proof path for T10a.2 is: T10a.1 (all siblings have equal length) → Prefix (equal-length tumblers are prefix-related only if identical) → distinct equal-length siblings are prefix-incomparable. The justification section correctly lists Prefix among six foundations. But the formal contract for T10a.2 references neither T10a.1 nor Prefix — it states the conclusion (prefix-incomparable) without declaring the dependencies that bridge from "same length and distinct" to "prefix-incomparable." A contract reader sees the claim but cannot trace its justification without reading the proof body.
**What needs resolving**: The formal contract for T10a.2 must declare its dependency on T10a.1 (uniform sibling length) and Prefix (PrefixRelation), or T10a needs a Depends field aggregating the six foundations its postconditions require — analogous to T8's "Depends: NoDeallocation."
