# Review of ASN-0051

## REVISE

### Issue 1: SV5's π-invariance claim is asserted, not derived

**ASN-0051, SV5 ReorderingProjectionInvariance**: The statement is `π_{Σ'}(e, d) = π_Σ(e, d)`, but the proof block immediately after the statement reads only "Rearrangement cannot change which I-addresses are in the projection. The endset references exactly the same content before and after." Then the labelled "*Proof.*" derives only the locate-transformation `locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)}`.

**Problem**: The π-invariance is asserted colloquially, not derived. SV2 and SV3 each give an explicit three-line derivation for π (coverage invariance + range relation + intersection algebra); SV5's π-invariance deserves the same.

**Required**: Add the explicit derivation before the locate proof: "π_{Σ'}(e, d) = coverage(e) ∩ ran(M'(d)) = coverage(e) ∩ ran(M(d)) = π_Σ(e, d), using L12 for coverage invariance and K.μ~'s ran-preservation corollary `ran(M'(d)) = ran(M(d))`."

### Issue 2: `discover_s(A)` state-dependency notation is inconsistent

**ASN-0051, Definition — Link Discovery**: The definition reads `discover_s(A) = {a ∈ dom(Σ.L) : coverage(Σ.L(a).s) ∩ A ≠ ∅}` — Σ appears only on the right-hand side, leaving the LHS as if it were state-independent. Subsequent claims (SV7, SV8, SV9, SV13(d), SV14) use the phrase `discover_s(A) in Σ` / `in Σ'` to make state-dependence explicit. SV2/SV3/SV5 use the explicit subscript form `π_Σ(e, d)`.

**Problem**: The definition trains the reader to ignore the state, then later claims silently insert "in Σ" — readers must reconcile two conventions. The asymmetry with the π notation (which is subscripted) is unjustified.

**Required**: Pick one convention and apply uniformly. Either subscript discover_s at the definition (e.g., `discover_{s,Σ}(A)`) or open the definition with "For any state Σ, define `discover_s(A) in Σ = ...`".

### Issue 3: TransclusionCouplingAbsence headline overstates the absence

**ASN-0051, Corollary (TransclusionCouplingAbsence)**: "When K.μ⁺ extends M(d₂) with a mapping v ↦ a where a ∈ ran(M(d₁)), the link discoverability through a in d₂ requires no coupling step beyond K.μ⁺ itself."

**Problem**: A valid composite under ASN-0047 J1★ requires K.ρ to record provenance for the extension. The body acknowledges this in a later parenthetical, but the headline reads as if the K.μ⁺ step suffices alone. A reader could carry away the wrong impression of the discipline composites must satisfy.

**Required**: Either qualify the headline ("...requires no *link-store* coupling step beyond K.μ⁺ itself") or lift the K.ρ caveat into the headline rather than burying it in the proof's closing paragraph.

### Issue 4: SV13(g) is missing the state-dependence qualifier in the headline

**ASN-0051, SV13 (SurvivabilityTheorem), clause (g)**: "the surviving text-subspace projection in any document is the union of *exactly* m · p decomposition terms..."

**Problem**: SV11's body has a "Caveat — m · p is state-dependent" paragraph that flags p as a property of the *current* arrangement. SV13(g) — the synthesised theorem statement that downstream consumers will quote — restates the m · p bound without flagging that p varies with state. The caveat appears only further down inside SV13(g)'s expanded text.

**Required**: Add a single qualifier to SV13(g)'s opening: "...the union of *exactly* m · p decomposition terms (at the post-transition state's block count p)..."

### Issue 5: SV6's "subspace-agnostic" rationale and the SV6/L4 broader-span scope are stated as prose only, not summarised in SV13(f)

**ASN-0051, SV13(f)**: "Cross-origin coverage exclusion: new allocations from a different origin cannot enter existing endset spans when the span start is element-level and the span's action point `k` satisfies `k > p₃`..."

**Problem**: The condition `k > p₃` is reproduced, but the *scope* of the result — element-level b only, deferring broader-level spans — is not. A reader of SV13 alone could read SV13(f) as a universal cross-origin exclusion and miss the broader-level deferral that the SV6 proof carefully carves out.

**Required**: Add to SV13(f): "The exclusion applies to element-level allocations (zeros(b) = 3); broader-level spans (k ≤ p₃) are admitted by L4 and deferred to ASN-0034's allocator and address-hierarchy treatment."

## OUT_OF_SCOPE

### Topic 1: Within-document sharing and resolution multiplicity

The first Open Question — "What must the system guarantee about resolution when the same I-address appears at multiple V-positions within a single document through within-document sharing?" — is correctly deferred. The ASN establishes `|locate(e, d)| ≥ |π(e, d)|` and exhibits non-injective cases in the two-span worked example, but doesn't legislate operational semantics for multi-occurrence resolution. Belongs in a downstream ASN on reader-facing operations.

### Topic 2: Vitality across forks

Open Question 7 — "Under what conditions must bilateral vitality be preserved across a fork?" — is appropriately deferred. The TransclusionCouplingAbsence corollary touches forking via J4 but only for discovery monotonicity, not vitality. Fork survivability needs its own treatment.

### Topic 3: Link-subspace endsets (L13 reflexive addressing)

The "Link Subspace ASN" is explicitly named throughout (after SV2, the SV11 parenthetical, the discover_s domain note). Endsets that reference link addresses, the resolution semantics of link-pointing-to-link configurations, and the partial-survival decomposition of link-subspace projection are correctly carved out as a future ASN. SV2's "depends only on monotonic enlargement of ran(M(d))" framing keeps the door open without committing.

### Topic 4: Same-origin coverage growth at element level

The "Content Allocation and Coverage Stability" section explicitly says: "We make no formal SV claim about same-origin coverage growth in this ASN." The descriptive treatment (sequential overshoot, child-depth entry) and the udanax-green implementation correspondence are appropriately scoped as motivation/context for SV6's element-level cross-origin exclusion. The formal characterisation belongs in ASN-0034's allocator-discipline treatment.

VERDICT: REVISE
