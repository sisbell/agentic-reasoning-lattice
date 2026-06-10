# Review of ASN-0127

The note is rigorous: every primitive is defined cleanly, the keystone meta-lemma (F-CIL) is properly load-bearing, F-IMG-SWING carries both an injective and a non-injective witness, the worked illustration checks the real postconditions against concrete states (K.α / K.μ⁻ / K.μ⁺ / K.λ, and the existence-vs-discovery zero), and the endset-coverage subtlety (a singleton abbreviates a *subtree*, not a bare address) is handled correctly. The two items below are derivation-completeness gaps, not correctness gaps.

## REVISE

### Issue 1: F-CIL-perlink is stated without a derivation, and is not an instance of F-CIL

**ASN-0127, "The stability keystone" (F-CIL-perlink)**: "*A weaker per-link form supports the inductive step for K.λ:* **F-CIL-perlink** … *For any `a` with `a ∈ dom(Σ.L) ∩ dom(Σ'.L)` and `Σ'.L(a) = Σ.L(a)`: …*"

**Problem**: This is the only lemma in the note given no derivation — every other claim, down to F-IMONO and D-ZERO, carries one. It cannot be silently inherited from F-CIL, because its hypothesis is strictly weaker: F-CIL assumes the *global* store equality `Σ.L = Σ'.L`, whereas F-CIL-perlink assumes only *per-link* value preservation `Σ'.L(a) = Σ.L(a)` for a single `a`. That distinction is load-bearing exactly where the sub-lemma is used. F-LAMBDA invokes it "applied at each `a ∈ dom(Σ.L)`" under K.λ — and under K.λ the global hypothesis of F-CIL *fails* (`dom(Σ'.L) = dom(Σ.L) ∪ {ℓ_new} ≠ dom(Σ.L)`). So F-CIL does not cover the case in which F-CIL-perlink is actually applied; the sub-lemma needs to start its chain from the per-link premise.

**Required**: Give F-CIL-perlink its own (one-line) derivation — the per-link tail of F-CIL's chain, begun from the assumed per-link value equality: from `Σ'.L(a) = Σ.L(a)`, L6 yields arity equality `|Σ'.L(a)| = |Σ.L(a)|` and per-slot endset equality, hence per-slot coverage equality (coverage deterministic); the `matches` existential and the per-slot conjunct are built from exactly these, so each evaluates identically at `Σ` and `Σ'`.

### Issue 2 (minor): D-NONMONO's K.μ⁺ direction is asserted in prose where the symmetric K.μ⁻ direction is proved by formula

**ASN-0127, "Discovery anchoring" (D-NONMONO, K.μ⁺/K.μ⁺_L clause)**: "*These transitions preserve Σ.L (F-PRES), so the comprehension state is again held fixed at Σ (F-INERT); new I-addresses falling in W's positions can then add new link matches, evaluated against the unchanged store.*"

**Problem**: The K.μ⁻ clause discharges its monotone-shrink direction with an explicit inclusion chain and an explicit appeal to F-IMONO. The mirror K.μ⁺ clause supplies the ingredients (F-IMG-MONO, F-INERT) but never chains them — it omits the F-IMONO step and never states the inclusion `findlinks_disc(W,d_q,Σ) ⊆ findlinks_disc(W,d_q,Σ')`. The conclusion is correct and is concretely witnessed by the "Rise under K.μ⁺" illustration, but D-NONMONO itself should match the rigor of its symmetric case.

**Required**: Write the extension-side inclusion mirroring K.μ⁻: `findlinks_disc(W,d_q,Σ) = findlinks(image(W,d_q,Σ), Σ) = findlinks(image(W,d_q,Σ), Σ') ⊆ findlinks(image(W,d_q,Σ'), Σ') = findlinks_disc(W,d_q,Σ')` — middle equality by F-INERT, inclusion by F-IMG-MONO then F-IMONO.

## OUT_OF_SCOPE

### Topic 1: Slot-restricted matching (excluding the type slot)
F-MATCH's existential ranges over *all* slots including the type slot, so a content region whose image happened to meet a link's type endset would match. For content addresses this never fires in practice (type endsets cover s_L/type addresses, not s_C content, as the worked example confirms), and the note already defers slot-filtering to its second open question. Future work, not an error here.

### Topic 2: Composition with ASN-0098's per-link projection
`findlinks_disc` over a full document recovers the discoverable-link set ASN-0098 characterizes per-link (LP12), but the region-keyed / forward-image direction is genuinely new, and the composition is the note's fourth open question. Out of scope.

VERDICT: REVISE
