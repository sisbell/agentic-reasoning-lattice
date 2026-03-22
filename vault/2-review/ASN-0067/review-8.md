# Review of ASN-0067

## REVISE

### Issue 1: Incomplete reasoning for J1 vacuity at intermediate state
**ASN-0067, Elementary Decomposition, Case 1**: "(J0, J1, and J1' all hold vacuously: no content is allocated (dom(C) unchanged), no I-address is newly introduced into any arrangement (K.μ⁻ can only reduce the range), and no provenance pair is added (R unchanged))"
**Problem**: The parenthetical explains J1 vacuity by citing K.μ⁻ alone ("K.μ⁻ can only reduce the range"), but the composite (Σ₀, Σ₂) consists of K.μ⁻ *followed by* K.μ⁺. Step 2 is K.μ⁺, which extends the arrangement — a reader checking the reasoning finds that K.μ⁺ adds V→I mappings and would reasonably question whether new I-addresses enter ran(M₂(d)). The correct argument is: Steps 1–2 together form K.μ~, whose corollary (ASN-0047) gives ran(M'(d)) = ran(M(d)). The shifted B_post blocks carry the same I-addresses as the original B_post (only V-positions change), so ran(M₂(d)) = ran(M₀(d)) and ran(M₂(d)) \ ran(M₀(d)) = ∅.
**Required**: Replace the parenthetical with: "Steps 1–2 form K.μ~ whose corollary gives ran(M₂(d)) = ran(M₀(d)); J0 holds because dom(C) is unchanged; J1 holds vacuously because ran(M₂(d)) \ ran(M₀(d)) = ∅; J1' holds because R₂ = R₀."

## OUT_OF_SCOPE

### Topic 1: Formal status of D-CTG as design constraint vs invariant
**Why out of scope**: The ASN correctly observes that D-CTG is violated at intermediate states within a valid composite, and correctly notes it is not in the ReachableStateInvariants list (ASN-0047). Formalizing the distinction between "invariant of reachable states" and "design constraint preserved at operation endpoints" is a foundation-level refinement, not an error in this ASN.

### Topic 2: Cross-subspace COPY semantics
**Why out of scope**: The COPY definition does not restrict the target subspace S — the source resolution discards V-coordinates and carries only I-addresses, so placing content from one subspace into another is structurally valid. Whether cross-subspace placement (e.g., link content into text subspace) should be restricted is a semantic question belonging to future link/arrangement ASNs.

### Topic 3: Serialization of concurrent COPY operations
**Why out of scope**: The ASN correctly notes the ValidComposite framework provides sequential correctness only, and flags concurrency as an open question. A concurrency model is new territory.

VERDICT: REVISE
