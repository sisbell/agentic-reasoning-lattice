# Review of ASN-0118

The technical core of this ASN is sound. I checked the composite exhibition (both the append/empty and displacing decompositions discharge their K.μ⁻/K.μ⁺ elementary preconditions, including the per-subspace retention subtlety and the gap-fill vs. shifted-content split for S8a/S8-depth), the three-branch provenance discharge against J1★/J1'★/P4★/P2, the tiling argument (disjointness by TS1/TS4, gap-freeness by TS3), the ran-equality underlying the CP7b weakest precondition, the exactness of CP4, and the worked example's arithmetic (including the self-transclusion variant). All check out. The remaining findings are accretion patterns this review was explicitly asked to surface, plus one notation inconsistency with a foundation.

## REVISE

### Issue 1: Closure-role commentary stated three times
**ASN-0118, The COPY operation (Effect — domain closure; Frame — entity set) and Claims table (CP12)**: The CP3c paragraph ends "...the same closure role is played by CP6's domain-equality conjunct (for `d`'s non-text subspaces), CP8's `⊆` direction (for `Σ.R`), and CP12 (for `E`)." The CP12 frame paragraph then says "CP12 and CP8's `⊆` direction together bound the two components the remaining clauses constrain only from below." The CP12 table row says it a third time: "with CP8's `⊆` direction, every state component is bounded above by the operation's own clauses."
**Problem**: This is one architectural point — the postconditions upper-bound every state component — made in three places in different words. The CP3c paragraph is additionally a why-the-clause-is-needed justification ("dischargeable from the postconditions alone, not only through the exhibited composite") with an embedded forward deferral ("the tiling argument given later"), wrapped around a postcondition whose content is the displayed equation. This is exactly the cross-cycle accretion the anti-bloat classifier names: prose around a clause explaining why it exists rather than what it says, duplicated at parallel sites.
**Required**: State the closure inventory once — the CP12 frame paragraph is the natural single site, since it is where the "bounded above" observation completes — and reduce the CP3c paragraph to its content: the closure equation plus the I3-V/D-DOM analogue citation. The table row may keep its summary form.

### Issue 2: Self-transclusion mechanism explained twice
**ASN-0118, The COPY operation (frame clauses) and Shared identity across documents (CP9)**: The frame section says "resolution (CP0) reads the *pre-state* `Σ.M(d)`, so the addresses `cᵢ` are fixed before any displacement, and the effect then re-binds them at fresh positions of the same document. We return to this case under CP9." The CP9 section then says "resolution reads the pre-state, so the placed addresses are those the document's own positions bound *before* the displacement; the effect then adds new V-positions, in the same document, referring to the same I-addresses."
**Problem**: The two passages are near-verbatim duplicates separated by a deferral — the "see CP9 below" pointer plus a full re-explanation at the target is the relocated-not-removed pattern. The frame section legitimately needs to note that the `(A d' : d' ≠ d)` clause does not exclude `d_s = d`; it does not need the mechanism, which is CP9's job.
**Required**: At the frame clause, keep only the admissibility note and the pointer ("the case `d_s = d` is admitted; see CP9"); leave the pre-state-read mechanism solely in the CP9 section.

### Issue 3: Composite operation written with the atomic-transition arrow
**ASN-0118, The COPY operation**: "**COPY(`Σ, d, p, R`)** is the transition `Σ → Σ'` with the following effect..."
**Problem**: ASN-0047's SequentialTransitionAxiom reserves `Σ → Σ'` for atomic transitions and `Σ →* Σ'` for composites. COPY is then exhibited as a multi-step composite (K.μ⁻ + K.μ⁺ + K.ρ steps in the displacing case), so the header notation asserts an atomicity the decomposition contradicts — and the document elsewhere leans hard on the atomic/composite-boundary distinction (the P4★ standing precondition, the initial-to-final coupling evaluation). CP10's "across the COPY transition" inherits the same looseness. A reader could wrongly apply per-atomic-step properties to COPY end-to-end.
**Required**: Write the operation as the composite transition `Σ →* Σ'` (or explicitly define an operation-level arrow as ASN-0047 composite shorthand at first use), and align CP10's phrasing.

## OUT_OF_SCOPE

### Topic 1: Correspondence between appearances of shared content
**Why out of scope**: The ASN's fourth open question — how the shared identity COPY establishes relates to a correspondence relation letting one appearance stand for all — is genuinely new machinery (a correspondence/version relation over arrangements), not a missing clause of COPY. Correctly deferred.

### Topic 2: Loss of inherited discoverability under later contraction
**Why out of scope**: What happens when the destination later removes the transcluded positions is DELETE-side behaviour (ASN-0117 territory, with LP12a already supplying the wp machinery); the ASN rightly poses it as an open question rather than specifying it here.

VERDICT: REVISE
