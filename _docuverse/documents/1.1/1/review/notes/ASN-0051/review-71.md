# Review of ASN-0051

This is a substantial ASN with extensive proofs and witness constructions. I worked through each SV claim, the worked example, and the SV11 attainment witnesses (including the lift schema verifications). Below are my findings.

## REVISE

### Issue 1: SV5b/SV13(e) — reordering proof under K.μ~ stage-level vs endpoint reading
**ASN-0051, SV5 and SV13(e)**: "K.μ~'s ran-preservation corollary (ASN-0047) records that K.μ~ preserves ran(M(d)) as a set when read at the composite endpoints Σ and Σ' bracketing the full K.μ~ composite"
**Problem**: The proof relies on ASN-0047's K.μ~ corollary `ran(M'(d)) = ran(M(d))` as definitional, but ASN-0047 also defines K.μ~ as the *distinguished composite* K.μ⁻ + K.μ⁺. These two framings coexist in the foundation; the ASN should either pick one framing consistently or explicitly state which one drives the proof. As written, the proof appears to use the corollary as primary while the rest of the ASN reasons via composite decomposition, which creates ambiguity about whether the equality is by definition or derived.
**Required**: A single sentence at the start of SV5's proof choosing one framing (e.g., "We read K.μ~'s composite endpoints as the primary equality, justified by the bijection π on dom(M(d))") and a forward pointer to the composite-level scope discussion for the per-step shrinkage explanation.

### Issue 2: Lift schema verifications — "same per-step structural verification" is too compressed
**ASN-0051, SV11 attainment witness, (α_2) and (β_2) lifts**: "The (α_2) lift is the (α) recipe instantiated at p = 2 with the appropriate base-shape relabelling — same per-step structural verification, same SV11 attainment-condition preservation."
**Problem**: Although the parameter changes and offset checks are detailed for the lifted state, the closing "same per-step structural verification" risks being read as a proof-by-similarity for the iterated case. The single-step verification is correct, but inductive iteration from W(3, 2) to arbitrary (m, 2) (and similarly W(2, 3) to (2, p)) is not made explicit — the reader must reconstruct the induction step.
**Required**: One paragraph after the (α_2) and (β_2) verifications stating that iteration is by induction on the parameter (m or p), with the base case being the explicit witness and the step being the verified lift. The induction is a one-liner but currently implicit.

### Issue 3: SV6 sub-claim labelling collides with later schema labels
**ASN-0051, SV6 proof**: Uses "(α) t = s, (β) s ≺ t, (γ) divergence" for proof sub-cases, while the SV11 section uses "(α), (β), (α_2), (β_2)" for lift schemata.
**Problem**: Same Greek letters carry different meanings in different sections; readers cross-referencing may conflate them. Minor but avoidable.
**Required**: Relabel the SV6 sub-cases to numerical (e.g., (1), (2), (3)) or different Greek letters to disambiguate from the lift schema family.

### Issue 4: Worked Example K.μ~ admissibility silent on J1★ across the composite
**ASN-0051, Worked Example, Step 1 admissibility note**: Discharges D-SEQ, D-CTG, D-MIN, S8a for the K.μ~ composite (K.μ⁻ + K.μ⁺), but does not address J1★ (ExtensionRecordsProvenanceContent).
**Problem**: When the K.μ⁺ stage of K.μ~ re-introduces content-subspace mappings with I-addresses already in R (preserved across the K.μ⁻ stage by P2/R monotonicity), J1★ holds trivially. However, the ASN's admissibility framework otherwise discharges each precondition explicitly, and J1★ is the load-bearing coupling for K.μ⁺. Silence here invites the reader to wonder whether the composite is fully ValidCompositeExtended.
**Required**: One sentence noting that J1★ is satisfied across the K.μ~ composite because R-entries for re-added I-addresses persist by P2, without requiring fresh K.ρ steps inside the composite.

### Issue 5: SV11 attainment witness coverage — presentation could be more digestible
**ASN-0051, SV11 attainment witness coverage**: Five witnessed configurations and two non-attainment cases are described in ~3000 words of prose with multiple "Witness shape", "Witness construction", and "Boundary witness shape" subsections.
**Problem**: The reader must track W(m, p) parameters, lift recipes (α, β, α_2, β_2), boundary cases, and saturation verifications across many paragraphs. The structure is correct but hard to navigate; a summary table of (m, p) regions with their witnesses and conditions would let the reader confirm coverage at a glance.
**Required**: A compact table listing each (m, p) region, the witness type (single-block, multi-block, lift), and the structural condition (e.g., `min_k n_k ≥ 2m − 1`) — placed at the start of the attainment section, with the detailed proofs following.

## OUT_OF_SCOPE

### Topic 1: Type endset (Θ) vitality semantics
**Why out of scope**: The ASN deliberately excludes Θ from vitality predicates on semantic grounds (Θ is a type annotation, not an endpoint). What "vital type endset" should mean operationally — and how type-hierarchy ghost references interact with discovery — is a question for a future link-semantics ASN.

### Topic 2: Broader-level span survivability (k ≤ p₃)
**Why out of scope**: The ASN explicitly defers spans with action point at or before the third field separator (cross-document/account/node spans) to ASN-0034's allocator and address-hierarchy machinery. SV6's exclusion is element-level only by design.

VERDICT: REVISE
