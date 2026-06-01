# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ admissibility filter omits S3★-aux, which Step (A) silently relies on

**ASN-0047, *Decomposition of K.μ~*, admissibility clause (i) and Step (A)**: Clause (i) states "the induced post-state `M'(d)` would satisfy the full per-state invariant package on `M'(d)` — S8a, S8-depth, S8-fin, D-CTG★, D-MIN★, and S3★, from which the derived D-SEQ★ follows." Step (A) then argues: "S3★-aux constrains `subspace(v) ∈ {s_C, s_L}` everywhere, so a mismatch under π takes exactly one of two complementary forms — `s_C → s_L` or `s_L → s_C`; there is no third case."

**Problem**: The "exactly one of two complementary forms" exhaustiveness presupposes that *both* `subspace(v)` and `subspace(π(v))` lie in `{s_C, s_L}`. For `v` (a pre-state position) this comes from S3★-aux(Σ) by the inductive hypothesis. For the *image* `π(v) ∈ dom(M'(d))`, the restriction `subspace(π(v)) ∈ {s_C, s_L}` is exactly S3★-aux(Σ') — and S3★-aux is **not** in the enumerated admissibility package. It cannot be recovered from the listed clauses: a candidate position `π(v) = [7, 1, 1]` has all-positive components (satisfies S8a) and first component `7 ∉ {s_C, s_L}`; S3★'s two implications (`subspace=s_C ⟹ ...`, `subspace=s_L ⟹ ...`) are then *vacuously* satisfied at `π(v)`, so S3★(Σ') does not exclude it, and D-CTG★/D-MIN★ (quantified per subspace S) say nothing forcing S to be `s_C` or `s_L`. Thus Step (A)'s case analysis is missing the `s_C → (third value)` and `s_L → (third value)` branches, and the L14-driven contradiction does not fire for them. The phrase "full per-state invariant package" contradicts the explicit enumeration that drops S3★-aux.

**Required**: Either add S3★-aux explicitly to admissibility clause (i)'s enumeration (so `subspace(π(v)) ∈ {s_C, s_L}` is a stipulated hypothesis at Σ'), or insert a step in (A) deriving `subspace(π(v)) ∈ {s_C, s_L}` from the listed clauses. Until one of these closes the gap, the "no third case" claim is asserted, not established.

### Issue 2: Duplicated justification prose across K.δ k=0 sites

**ASN-0047, *Elementary transitions* (K.δ case (ii), k=0 bullet) and *K.δ case (ii) discharge and parent-allocator activation***: Both sites carry the same sentence framing the freshness guard and frontier conjunct as "two checkable forms of the same precondition, neither derived from the other." The K.δ k=0 elementary bullet states the FrontierEquivalence equivalence, and the discharge section restates it verbatim in intent.

**Problem**: Per the anti-bloat note, two paragraphs in different sections saying the same thing compound across cycles and force the reader to reconcile near-identical prose. The equivalence is load-bearing once; the second statement advances no new reasoning.

**Required**: State the "two checkable forms, neither derived" framing once (at the FrontierEquivalence lemma or the discharge section) and have the other site point to it without re-asserting the equivalence.

### Issue 3: "Live-depth re-pinning rule" deferral repeated from multiple sites

**ASN-0047, K.μ⁺ amendment / K.μ⁺_L precondition**: Both the content-subspace depth note ("`m_C(d)` is governed by the live-depth re-pinning rule stated once under *V-position depth (operational)*") and the K.μ⁺_L depth precondition ("governed by the live-depth re-pinning rule stated under *V-position depth (operational)*") defer to the same downstream paragraph.

**Problem**: Multiple paragraphs deferring to the same downstream location is one of the accretion patterns flagged for this note. The rule itself is short; the repeated pointer-prose is noise the reader navigates around.

**Required**: Keep a single forward pointer (or inline the one-line rule at the first use site) rather than re-deferring at each subspace's depth clause.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The J4 discharge notes "A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." This is correctly deferred — fork link-inheritance semantics is new territory, not a defect here.

### Topic 2: Concurrency / serialization of link allocation
Raised in Open Questions; concurrency and atomicity beyond the single-event SequentialTransitionAxiom are explicitly out of scope per the Scope section.

VERDICT: REVISE
