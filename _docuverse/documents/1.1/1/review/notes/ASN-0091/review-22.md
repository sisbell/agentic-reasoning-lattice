# Review of ASN-0091

## REVISE

### Issue 1: R-SP application to the unified state needs clarification

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "R-SP (RearrangeSufficientPrecondition) discharges RA-adm with respect to the ASN-0036 foundation invariants at the cut-sequence level by deriving that every such invariant holds at Σ' under the precondition R-PRE(K) ∧ ASN-0036-invariants(Σ, d)."

**Problem**: R-SP's Q includes ASN-0036's S3 ("ran(M'(d)) ⊆ dom(C')"), and R-RI (its sub-lemma) explicitly requires "ASN-0036 S3 holds on the pre-state". In the unified state, ASN-0036's S3 is superseded by S3★ and does not hold for arrangements with link-subspace V-positions (which map to dom(L), not dom(C)). The author then discharges S3★ separately ("from constructive premises rather than from circular appeal to RA-adm"), which is correct, but the framing "R-SP discharges every ASN-0036 invariant" is over-inclusive — it cannot discharge the S3 / S8 clauses in the unified state where they're superseded.

**Required**: Explicitly note that R-SP's S3 and S8 clauses are not load-bearing in the unified state; only the remaining ASN-0036 invariants (S0, S1, S2, S4, S5, S7a-d, S9, S8a, S8-fin, S8-depth, D-CTG, D-MIN, D-SEQ) survive R-SP. Their replacements (S3★, S8★) are discharged separately, as the ASN already does — but the framing should make this division explicit rather than blurring it under "ASN-0036-invariants(Σ, d)".

### Issue 2: Forward reference to RE-sub in early derivations

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "Because CS3 fixes the cut subspace at S = s_C, the link-subspace portion of M(d) is preserved pointwise (RE-sub below): Σ'.M(d)|_{V_{s_L}(d)} = Σ.M(d)|_{V_{s_L}(d)} carries over verbatim, so CL-OWN... and CL-UNIQ... are preserved unchanged at Σ'."

**Problem**: RE-sub is formally introduced later in the "Subspace Frame" section. The discharges of CL-OWN, CL-UNIQ, and S8★'s link-subspace clause cite "RE-sub below" before the label exists, introducing dependency-order confusion. The substantive justification is CS3 + R-FRAME-P/S(a), which is available without RE-sub.

**Required**: Either reorganize so RE-sub is defined before the discharge, or replace the forward-pointer "(RE-sub below)" with direct citation of CS3 + R-FRAME-P/S(a) (the foundation sources that yield the same pointwise preservation).

### Issue 3: E_doc / dom(M) identification asserted parenthetically

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: "ASN-0047's K.μ~ precondition d ∈ E_doc discharges RA-reg (in the unified state, E_doc coincides with dom(M) for documents)."

**Problem**: The identification "E_doc coincides with dom(M)" is asserted parenthetically without proof or citation. It's load-bearing for RA-reg discharge — ASN-0047 quantifies over E_doc, ASN-0093 quantifies over dom(M), and these are introduced as distinct primitives in their respective ASNs. ASN-0091 uses both interchangeably without justification.

**Required**: Either cite a substrate convention establishing the identification, derive it from the unified state's joint document-registration semantics (K.σ updates dom(M) while K.δ-IsDocument adds to E_doc — both must produce the same set), or state it as an explicit unified-state axiom.

## OUT_OF_SCOPE

### Topic 1: Cross-document transclusion fragmentation analysis
**Why out of scope**: The Open Question about what guarantees REARRANGE must preserve when a cut splits a transcluded span is properly framed as future work. The ASN's RE-trans + RE-frag analysis is sufficient for the current ASN.

### Topic 2: Link-subspace REARRANGE semantics
**Why out of scope**: The Open Question about REARRANGE on the link subspace is correctly identified as a future operation. REARRANGE_K's restriction to S = s_C via CS3 is documented; extending to link subspace requires a separate ASN.

### Topic 3: Cardinality upper bound on fragmentation
**Why out of scope**: A theoretical upper bound on RE-frag's cardinality increase is open work. The existential witness suffices for the current ASN.

VERDICT: REVISE
