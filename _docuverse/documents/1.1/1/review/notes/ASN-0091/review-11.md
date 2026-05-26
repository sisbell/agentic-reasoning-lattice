# Review of ASN-0091

## REVISE

### Issue 1: Citation error for K.μ~ admissibility
**ASN-0091, Section 1 (REARRANGE as Vstream-Only Operation)**: "ASN-0084's K.μ~ admissibility clause (ii) (`π ≠ id`) is the formal vehicle confirming this property"
**Problem**: K.μ~ is defined in ASN-0047 (transition model), not ASN-0084. ASN-0084 defines REARRANGE_K, which realises K.μ~. The admissibility clauses (i) and (ii) are in ASN-0047's K.μ~ definition.
**Required**: Change citation to "ASN-0047's K.μ~ admissibility clause (ii)".

### Issue 2: RA-adm discharge incomplete for ASN-0047 extended invariants
**ASN-0091, Section 1**: "ASN-0084's R-SP (RearrangeSufficientPrecondition) discharges RA-adm at the cut-sequence level by deriving that every ASN-0036 foundation invariant carried by an arrangement transition holds at Σ' under the precondition R-PRE(K) ∧ ASN-0036-invariants(Σ, d)."
**Problem**: R-SP explicitly covers only ASN-0036 invariants. ASN-0047 introduces extended invariants — S3★, S3★-aux, CL-OWN, CL-UNIQ, P4★ — that are necessary for the unified state. RA-adm asks for "every foundation invariant satisfied by Σ" preserved at Σ'. The ASN discusses S3★ + L14 forcing subspace preservation but does not address CL-OWN, CL-UNIQ, P4★, S3★-aux. The worked example's admissibility check also omits these. The discharge is true by inspection (link subspace fixed for S = s_C preserves CL-OWN and CL-UNIQ; subspace-preserving content permutation preserves P4★ via the bijection of pre-image sets carrying Contains_C(Σ) onto Contains_C(Σ') with RE-R unchanged), but the argument needs to be in the ASN.
**Required**: Either (a) add an explicit paragraph showing how REARRANGE_K's specific structure (link-subspace fixity for S = s_C, content-subspace bijection) preserves CL-OWN, CL-UNIQ, P4★, and S3★-aux, or (b) augment R-SP's named scope to include the extended invariants and cite that augmentation. The worked example admissibility check should also be extended to verify these invariants concretely.

### Issue 3: Informal subtraction notation on tumblers
**ASN-0091, Section 8 (Run Decomposition Is Not Invariant), coalescence and equality witnesses**: "c ∉ {a − 1, a + 1}"
**Problem**: ASN-0034's OrdinalShiftBase convention defines `t + k` only for `k ≥ 0`. The notation `a − 1` is used informally to mean "the chain predecessor of `a`". When `a` is the first emission of its chain, `a − 1` does not exist and the constraint is vacuous — but this is not addressed. The proof's chain-structural argument is correct (addresses from distinct chains cannot be chain-adjacent on either side), but the notation is not licensed by the foundation conventions.
**Required**: Rephrase using chain-structural language without invoking subtraction: "c is not chain-adjacent to a on either side — neither c + 1 = a nor a + 1 = c can hold, because chain-adjacency under TA5(c) requires both addresses to belong to the same sub-allocator chain, and c, a come from distinct chains (d_X ≠ d_Y forces disagreement on positions 1–5)."

### Issue 4: RA-dom redundancy not noted
**ASN-0091, Section 1**: RA-dom is stated as part of the abstract class definition.
**Problem**: As discussed informally near the bijection characterisation, RA-dom is *derivable* from RA-π (equicardinality of dom(M(d)) and dom(M'(d))) + RA-adm (forcing subspace preservation via S3★ + L14) + foundation D-SEQ★ (which pins V_S(d) uniquely from its cardinality). Including RA-dom as definitional is not wrong, but the ASN should either note the derivability for clarity or justify why it is taken as definitional rather than derived.
**Required**: Add a short remark either deriving RA-dom from the other clauses, or noting that it is included for ease of reference and is in fact derivable.

## OUT_OF_SCOPE

### Topic 1: Link-subspace REARRANGE_K semantics
**Why out of scope**: ASN-0084's CS3 fixes the cut subspace at S = s_C. The Open Questions section explicitly identifies link-subspace rearrangement semantics as future work.

### Topic 2: Universal realisation of admissible bijections by cut-sequence compositions
**Why out of scope**: The Open Questions section asks whether every admissible bijection of dom(M(d)) can be realised by finite compositions of cut-sequence rearrangements. This is a completeness question for the operation vocabulary, separate from this ASN's consequence derivations.

### Topic 3: Quantitative bound on run-decomposition cardinality increase
**Why out of scope**: The Open Questions section asks for an upper bound on cardinality increase. This is quantitative analysis distinct from the qualitative RE-frag/coal/eq results.

VERDICT: REVISE
