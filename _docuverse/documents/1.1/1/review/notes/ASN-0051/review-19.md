# Review of ASN-0051

## REVISE

### Issue 1: SV7 formal statement scope narrower than Properties table
**ASN-0051, SV7 (TransclusionCouplingAbsence)**: "Formally, for any K.μ⁺ or K.μ⁺_L transition Σ → Σ' and any set of I-addresses A: discover_s(A) in Σ' = discover_s(A) in Σ"
**Problem**: The labeled formal statement restricts to K.μ⁺/K.μ⁺_L, but the Properties table describes SV7 as holding "for all L-preserving transitions (all except K.λ)." The body text establishes the generalization ("The same equality holds for every elementary transition that holds L in frame"), and the proof depends solely on L being invariant — so the broader claim is correct. But the formal statement under the SV7 label does not match the Properties table entry under the same label.
**Required**: Either generalize the formal statement to "for any transition Σ → Σ' that holds L in frame" (which the proof already supports), or restrict the Properties table entry to match the formal statement and note the generalization separately.

### Issue 2: SV13 remark contradicts the ASN's own analysis
**ASN-0051, SV13 Remark (same-origin coverage growth)**: "At the byte level, sequential sibling allocation closes existing spans to future allocations"
**Problem**: The detailed analysis in "Content Allocation and Coverage Stability" identifies *sequential overshoot* — "If a span's reach extends beyond the current allocation maximum [...] future sibling allocations (TA5(c)) will enter the span as they advance through the ordinal sequence." The same section provides an explicit counterexample where child-depth allocation enters an existing span. The SV13 remark's blanket claim that sibling allocation "closes existing spans" contradicts both mechanisms. The detailed analysis correctly says the intersection is "*typically* closed at creation" (emphasis on *typically*), but the SV13 remark drops this qualification.
**Required**: Qualify the remark: "At the byte level, sequential sibling allocation closes existing spans *whose coverage is fully allocated* to future allocations" or "closes *tight* existing spans," matching the nuance in the detailed analysis. The remark should not assert universal closure when the same ASN demonstrates exceptions.

## OUT_OF_SCOPE

### Topic 1: Fork survivability
**Why out of scope**: The ASN briefly notes that forks share I-addresses via K.μ⁺ and thus inherit discovery (SV7 discussion). But the formal characterization of how bilateral vitality propagates across a fork (J4) — given that the fork copies only a subset of the source's arrangement — is a distinct question. The ASN's own open questions list this explicitly. It requires reasoning about J4's composite structure and the relationship between ran(M(d_src)) and ran(M'(d_new)), which belongs in a version or fork ASN.

### Topic 2: Link-subspace contribution to projection
**Why out of scope**: The ASN explicitly restricts SV11 to the text-subspace projection π_text(e, d) and defers the link-subspace contribution. When endset spans reference link addresses (L13, ReflexiveAddressing) and K.μ⁺_L creates link-subspace V-positions, the full projection π(e, d) may include link addresses not captured by π_text. The ASN correctly identifies this deferral ("deferred to the Link Subspace ASN") and SV13(g) is scoped accordingly.

VERDICT: REVISE
