# Review of ASN-0125

I checked the two operations (`assert_sup`, `editlink`) against their preconditions, frame, and postconditions; traced every boundary the de-listing/standoff/fork constructions touch; verified the inductive structure of EL-DM for circularity; and confirmed the foundation citations resolve against the listed verified ASNs. Notes on what I verified are folded into the OUT_OF_SCOPE section. The note carries `review-mode.anti-bloat`; I scanned for forward-reference accretion and reviser drift specifically.

## REVISE

None.

The technical spine holds under scrutiny:

- **The impossibility result (EL0) is exact, not rhetorical.** `J = a ∈ dom(L) ∧ L(a) = ℓ₀` persists by L12 closed under `→*` (LP13), `J ⟹ ¬R_mut`, so `wp(S, R_mut)` is `false` at `Σ₀` for every program — sound, and the dual ("readable at its address forever") is the same fact read positively.
- **Boundaries are handled, not skipped.** Empty store `Σ₀` grounds EL-DM's base (`S^{Σ₀} = L_R^{Σ₀} = ∅`, vacuous). The de-list construction (EL9(2)) correctly confronts that `K.μ⁻` drops only a *suffix*: it drops `a` with the tail at `n'_{s_L} = j−1`, re-seats the `n−j` survivors one position down via `K.μ⁺_L`, and degenerates cleanly at `j = n` (last/only). The standoff `current = ∅` (EL14(c)) and its reachability *inside* the disciplined layer (EL14(e)) are both constructed, not asserted.
- **The frame-on-activity split in EL6(iv)/EL7(iv) is correct in both tiers.** The unconditional `nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` rides on `coverage(K_sup) ≠ coverage(R)` (no `[R]`-slice growth); the conditional `nullified(Σ') = nullified(Σ)` discharges wp Case 2's third conjunct by R0a *at `Σ'`* — both fresh address and pre-existing retraction target sit in the `Σ'` antichain, forcing prefix-incomparability. That derivation is self-contained, not a bare appeal.
- **DC(ℓ') is exactly the guard discipline-preservation needs (EL7(vi)).** Its schema clause fires precisely on the `|ℓ'| = 3 ∧ coverage = K_sup` slice ASN-0086 admits into `S^{Σ₁}`; the `|ℓ'| > 3` and off-coverage cases land in the vacuous branch, and the leading conjunct bars a retraction-class successor. A non-canonical `[K_sup]` successor makes DC false, so `editlink` cannot mint a schema-violating claim.
- **EL11(a)'s coverage trace is fully worked.** "No content address extends a link address" is proven from C1 (three zeros) + L0 + SC-NEQ, not waved; the antichain (R0a) collapses link-side extension to equality; `listed only at home` follows from CL-OWN + HomeOriginCoincidence. EL13's cross-home commutation is proven via `a_emit` locality + distinct fresh keys.
- **Cross-references are confined to foundation ASNs** (0034/0036/0040/0042/0043/0045/0047/0053/0058/0086/0093/0098); no non-foundation dependency is load-bearing.

On the anti-bloat axis: the prose is *dense* but I could not isolate a passage that, removed, costs the argument nothing. The implementation notes are concrete code-grounding (explicitly not meta-prose); the `Ŝ^Σ`/`S^Σ` distinction is defensive robustness for multi-layer coexistence, not padding; the currency section's cross-reference cluster (Df-CUR ↔ EL14(e) ↔ EL9(3) ↔ EL15(d)) points to substance, not noise the reader must route around. The intro's preview of EL3's "menu collapses" is roadmap-then-deliver, within convention.

## OUT_OF_SCOPE

The Open Questions are genuinely future work, and — importantly — the note's core results do not silently depend on resolving them; it leaves them open rather than smuggling in partial answers.

### Topic 1: Retraction authority and meta-claim currency stratification
**Why out of scope**: Authority over who may retract a claim is placed outside `Σ` by EL8(b) (the state carries no principal set; ownership is ASN-0042's office). Currency over supersession-claims-of-supersession-claims is reachable by the construction but its stratification semantics is correctly deferred — `current(y)` remains well-defined (a finite closure) even with meta-claims; only the desired interpretation is open.

### Topic 2: Span-level correspondence under endset reshaping
**Why out of scope**: `editlink` treats `ℓ'` as an opaque whole value. Carrying correspondence between old and new *spans* of a reshaped endset is a refinement of the record, not a gap in the supersession relation this ASN defines.

### Topic 3: Disciplines guaranteeing non-empty / temporally-witnessed currency
**Why out of scope**: EL14(c) demonstrates `current = ∅` is reachable and EL13 proves cross-home order is unrecoverable from state. Whether some assertion discipline forces non-emptiness, or attaches a temporal witness, is new design territory — the note correctly reports the negative facts rather than inventing the missing structure.

VERDICT: CONVERGED
