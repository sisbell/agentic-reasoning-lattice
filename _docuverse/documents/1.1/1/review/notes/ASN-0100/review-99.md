# Review of ASN-0100

The proofs of the three-region decomposition, the per-subspace sequential invariants, the projection-shift correspondence, and the two wp analyses are carefully constructed and, where I checked the arithmetic (region disjointness, last-component ranges, the empty/append/clearance boundary cases), correct. The ASN meets the depth standard (concrete examples, non-trivial wp). My findings are principally accreted meta-prose flagged by the `anti-bloat` classifier, plus one proof-step elision.

## REVISE

### Issue 1: Irrelevant K.δ aside in the Formal Contract setup
**ASN-0100, §The Operation: Formal Contract**: "The operative substrate is ValidComposite★ (ASN-0047), whose atomic vocabulary is `{…}`. Document registration in this framework is K.δ in its IsDocument sub-case."
**Problem**: INSERT fires no K.δ (the frame `E' = E` is established independently). The sentence describing what K.δ IsDocument does advances none of INSERT's reasoning — it is context-inventory accretion the precise reader must skip past.
**Required**: Delete the document-registration sentence; the frame `E' = E` is already justified at INS.frame.E by "no K.δ fires."

### Issue 2: The full freshness derivation is restated in four sections
**ASN-0100, §Effect One; §Permanence; §Atomicity (S4 bullet); §Provenance (P4★/J1★)**: the `Σ_k`-relative freshness argument ("freshness … is established against the state immediately preceding its K.α firing … `a_k ∉ dom(Σ_k.C) ∪ dom(Σ_k.L)` … exactly the conclusion of SubsequentEmissionFreshness …") appears in full or near-full in each.
**Problem**: One canonical derivation suffices; the others are the same claim reworded. Multiple paragraphs deferring to the same lemma while re-deriving its conclusion is the redundancy the classifier targets.
**Required**: State the derivation once under INS.alloc/Effect One and cite INS.alloc at the three downstream sites without re-deriving.

### Issue 3: Third worked example largely duplicates the first
**ASN-0100, §A Worked Example, "Empty-document re-insertion after full clearance"**: "The V-side invariants (D-MIN★, D-SEQ★, D-CTG★, S8-depth, S8a, S8★) discharge exactly as in the first-insertion example; only the K.α branch and the chain continuation past `a_prev` (step 1 above) differ."
**Problem**: The example itself concedes it parallels the first-insertion example save for the K.α branch, yet reproduces the full composite, post-state, and discharge prose. The genuinely new content is the subsequent-emission-vs-first-emission distinction.
**Required**: Reduce to the differing element — the K.α subsequent-emission branch continuing `A_C(d)` past the persisted frontier — and drop the re-stated invariant discharge.

### Issue 4: Closed-interval reduction proved only between global extremes
**ASN-0100, §Sequential text-subspace structure**: "the set `Pref(m, K) := {…}` satisfies D-CTG★ over the full … slice between its extremes `min` and `max`" — the proof establishes only `min ≤ z ≤ max ⟹ z ∈ Pref`.
**Problem**: D-CTG★ (ASN-0047) quantifies over *every* pair `v_lo, v_hi ∈ V_S(d)`, not just the global extremes. The connecting step — for any pair, `min ≤ v_lo ≤ z ≤ v_hi ≤ max`, hence the extreme result applies — is left unstated.
**Required**: Add the one-line reduction that arbitrary-pair convexity follows from extreme convexity, or restate the lemma over arbitrary pairs.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (K.μ⁺_L semantics)
**Why out of scope**: The ASN explicitly bounds itself to the content subspace and defers link-subspace insertion; this is a future ASN, not a defect here.

### Topic 2: Self-composition closure and concurrent-INSERT serialisation
**Why out of scope**: Raised in Open Questions; both are new territory beyond the single-operation, single-document per-state contract this ASN fixes.

VERDICT: REVISE
