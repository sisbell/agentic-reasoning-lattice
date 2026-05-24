# Review of ASN-0097

## REVISE

### Issue 1: Π15a's stratified-S3 axioms modify a foundation invariant
**ASN-0097, §Independence from Arrangement, Π15a proof**: "We adopt this stratification locally as a strengthening of S3."

**Problem**: The original S3 (as cited from ASN-0036) reads `ran(Σ.M(d)) ⊆ dom(Σ.C)`. The introduced S3-link permits `ran(Σ.M(d))` to include addresses from `dom(Σ.L)`, which — given the cited disjointness `dom(Σ.L) ∩ dom(Σ.C)|_{s_C} = ∅` — is consistent only if `dom(Σ.C)` is interpreted to encompass link addresses, an interpretation never spelled out. As written, this is not a strengthening of S3 but a substantive re-stratification that contradicts the literal foundation constraint. Π15a is load-bearing for the cross-document independence story, so the gap matters.

**Required**: Either (a) derive the stratification from existing foundation axioms by exhibiting the precise relation between `dom(Σ.C)` and the subspace partition, (b) explicitly propose this as a foundation-level revision rather than a local axiom and document the consequences for other ASNs depending on the original S3, or (c) restate Π15a so the proof does not require modifying S3.

### Issue 2: Proof justification by "consultation evidence"
**ASN-0097, §Independence from Arrangement, Π15a proof and §The Coverage-at-Creation Rule**: "The consultation evidence (Nelson on design intent, Gregory on the implementation's POOM) supports a subspace-stratified reading of S3"; "The consultation evidence indicates that the design intent (Nelson) is CCR-open..."

**Problem**: Formal proofs and structural-axiom selections must rest on stated axioms, defined types, and previously established claims — not on appeals to design discussions or implementation observations external to the specification. "Consultation evidence" cannot discharge a proof obligation.

**Required**: Remove all "consultation evidence" appeals from proof bodies and axiom selections. Where intent is load-bearing (the stratified S3 reading, the CCR choice), state the premise as a local axiom or derive it from the foundations directly.

### Issue 3: Π4 invokes an undeclared external interpretation function
**ASN-0097, §Permanence of Link Structure, Π4 proof**: "the directional role assigned to slot `i` is a function of the slot index `i` alone, supplied by the link type's external interpretation; this role-by-index function lives outside Σ.L and is not in the write set of any operation in the transition vocabulary."

**Problem**: The "role-by-index function" is a Σ-external constant function on which Π4 depends. It is invoked mid-proof without prior declaration in this ASN. If L7 of ASN-0043 introduces it, the proof should name it (e.g., `Role : LinkType × ℕ → Direction`) and cite L7 as its source. As written, the proof's invariance premise is unstated.

**Required**: Name the interpretation function explicitly, state its type, and either cite the foundation that introduces it or declare it as a local structural premise of this ASN. The "outside Σ" claim must be substantiated against named structure.

### Issue 4: Empty endset / empty coverage boundary unaddressed
**ASN-0097, §The Projection and §Behavior Under State Transitions**

**Problem**: The review rubric mandates checking "MAKELINK with empty endsets" as a boundary case. The ASN does not address `cov(e) = ∅` — which can arise if an endset has no spans or if every span has zero width. All Π5–Π11 claims hold vacuously, but the ASN neither verifies this nor precludes it via a non-emptiness precondition on K.λ.

**Required**: Either (a) verify that proj/iproj definitions and Π5–Π11 proofs survive `cov(e) = ∅` (vacuously) with an explicit note in the relevant proof, or (b) add a non-emptiness precondition to K.λ excluding empty endsets and exhibit it in the link-allocation axiom.

### Issue 5: R13 (CCR-conditional) not exemplified in the worked example
**ASN-0097, §A Worked Example**: the trace verifies R9, R10, R11 against concrete states but never exhibits R13's conditional behavior.

**Problem**: R13 is the most subtle synthesized guarantee — it depends explicitly on the open CCR choice, and the two policies diverge on whether `K.α + K.μ⁺` can enlarge an existing projection. The example does not distinguish them. Per the rubric, the ASN should verify key postconditions against concrete scenarios; R13's two-mode behavior is the most informative non-trivial case.

**Required**: Add a sub-trace illustrating each CCR policy — (i) CCR-restricted: a fresh `a_new` from K.α placed adjacent to a linked region by K.μ⁺ does not enter any existing projection (`a_new ∉ cov(eᵢ)` by freshness + S1); (ii) CCR-open: a ghost endset created before `a_new`'s allocation gains `a_new` upon arrangement. The example as-is cannot distinguish the policies.

### Issue 6: Heavy reliance on cross-ASN labels with no foundations listed in this review
**ASN-0097, throughout**: references to L0, L6, L7, L12, L14, L0a (ASN-0043); S0, S1, S3, S8a (ASN-0036); K.α, K.λ, K.μ⁺, K.μ⁻, K.μ~, K.μ~-FIX (ASN-0047); T10a (ASN-0006).

**Problem**: Per rule 7, cross-ASN references should be flagged unless those ASNs are listed foundations. The Foundation section of this review is empty. As presented, every label citation is an unverifiable cross-reference. Even granting that ASN-0036/0043/0047 are foundations in context, several proofs (Π0, Π2, Π4, Π10, Π13, Π14, Π15a, Π15b) name labels (L0, L6, L7, L12, K.μ~-FIX, frame conditions) whose content is not restated, so a reader cannot verify the proofs from this ASN alone.

**Required**: Either (a) establish ASN-0036/0043/0047 as foundations explicitly in the foundation list, or (b) restate the load-bearing foundation contracts (L12 immutability, S0/S1 store monotonicity, K.μ⁻/μ⁺/μ~ frame conditions and contracts, K.α freshness, K.λ frame) inline so each proof is independently checkable.

## OUT_OF_SCOPE

### Topic 1: CCR's final settlement
**Why out of scope**: The ASN explicitly leaves the Coverage-at-Creation Rule as an open structural axiom with two consistent policies. Settling between CCR-restricted, CCR-open, or a hybrid is a separate structural decision that belongs in a future ASN — not a revision of this one. The Open Questions section appropriately surfaces this.

### Topic 2: VA's derivation from a versioning foundation
**Why out of scope**: VA (Versioning Assumption) is introduced as a local axiom because no versioning ASN currently exists. The ASN acknowledges this. Deriving VA from a more primitive versioning contract belongs in a future versioning ASN; Mode II claims here are properly conditioned on VA holding.

VERDICT: REVISE
