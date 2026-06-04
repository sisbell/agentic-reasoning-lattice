# Review of ASN-0100

This ASN carries the `review-mode.anti-bloat` classifier. The technical content is sound and the proofs are largely complete — I found no correctness defect rising to REVISE. The findings below concern accreted meta-prose and duplicated argument, which is exactly what the classifier flags.

## REVISE

### Issue 1: Cross-document projection invariance proved twice

**ASN-0100, §Cross-document independence (Q3) and §Coverage and link discoverability (INS.proj, the `d' ≠ d` bullet)**:

§Cross-document independence: "for any link `ℓ ∈ dom(L)` and any document `d' ≠ d`, the projection from `d'` is unchanged... Every elementary step... carries the cross-document frame... so `M(d')` is unmodified... and `L' = L`... so coverage is composite-invariant (LP3★)... Both determinants are unchanged, so the projection is unchanged."

INS.proj `d' ≠ d` bullet: "Each elementary step... carries the explicit cross-document frame... LP4 applied at each step... composing across the finite step sequence... yields `project(ℓ, i, d', Σ') = project(ℓ, i, d', Σ)`. Equivalently and directly: `project(ℓ, i, d', ·)` depends only on `M(d')` (composite-invariant) and on `coverage(e_i)` (composite-invariant by LP3★)..."

**Problem**: The same chain-the-frame-across-elementary-steps argument is given in full in two sections, reaching the identical conclusion. This is "two paragraphs in the same document say the same thing in different words."
**Required**: State the cross-document projection invariance once (it belongs with INS.proj's case split) and have the other site reference it, or drop the §Cross-document independence restatement.

### Issue 2: Defensive meta-prose and a second redundant proof inside INS.proj

**ASN-0100, §Coverage and link discoverability, INS.proj `d' ≠ d` bullet**: "Equivalently and directly: ... so it is unchanged across the composite. This matches the step-by-step rigor of the `d' = d` case below; no unproved 'LP4★/LP5★' closure is invoked."

**Problem**: The bullet first gives the per-step chaining proof, then gives a second "Equivalently and directly" proof of the same fact, then appends prose justifying that the argument is rigorous ("matches the step-by-step rigor," "no unproved closure is invoked"). The justification-of-rigor sentence is reviser drift — prose explaining why the proof is acceptable rather than advancing the proof, almost certainly relocated from a prior finding's resolution.
**Required**: Keep one derivation. Delete the rigor-justification sentence; rigor is demonstrated by the proof, not asserted alongside it.

### Issue 3: Organizational/use-site inventory framing in §Atomicity

**ASN-0100, §Atomicity and Canonical Order**: "ASN-0047's ExtendedReachableStateInvariants enumerates ~28 per-state invariants. Many are trivially preserved by frame... We group these by the state component they range over:" ... "These invariants are not re-verified in the per-step analysis below, which focuses on the invariants whose preservation requires non-trivial argument under INSERT's specific composition."

**Problem**: The per-invariant discharges that follow are real work, but the surrounding bookkeeping prose (the "~28," the "we group these," the closing "are not re-verified below... focuses on") is organizational scaffolding describing the structure of the argument rather than making it. This is the use-site-inventory pattern around a frame-preservation claim.
**Required**: Let the grouped discharges stand on their own. Remove the inventory count and the meta-sentences announcing what is and isn't re-verified.

### Issue 4: Repeated forward deferral to §Provenance

**ASN-0100, §The Operation: Formal Contract (Effect — Provenance) and §Discovering the Three Effects (Effect Three)**: "The composite-boundary couplings J0, J1★, J1'★ (ASN-0047) hold at the boundary `Σ →* Σ'`; the discharge is given in §Provenance." and "INSERT grows `dom(C)`, so the post-state invariants are re-derived directly in §Verifying the Invariants."

**Problem**: Multiple earlier sections defer the same obligations to the same downstream sections. The provenance contract is stated in the formal-contract block, restated in the worked example's discharge paragraphs, and discharged in §Provenance — three touch-points for one obligation.
**Required**: State the provenance effect once in the contract and discharge once; drop the intermediate "the discharge is given in §X" pointers.

## OUT_OF_SCOPE

### Topic 1: Link-subspace insertion (K.μ⁺_L) semantics
**Why out of scope**: The ASN explicitly bounds itself to the content subspace; the Open Question on link-subspace insertion correctly defers this to a future ASN.

### Topic 2: Self-composition closure of INSERT
**Why out of scope**: Whether `Σ →INSERT→ Σ₁ →INSERT→ Σ₂` collapses to a single INSERT is a genuine algebraic question, but it is new territory listed under Open Questions, not a gap in the present per-operation contract.

VERDICT: REVISE
