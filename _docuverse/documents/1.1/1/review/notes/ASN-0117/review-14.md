# Review of ASN-0117

This is a rigorous, largely correct note. The two-layer separation is cleanly maintained, the K.μ⁻/K.μ⁺ composite (and the lone-K.μ⁻ `R = ∅` branch) is exhaustive over the containment cases, the coupling obligations J0/J1★/J1'★ are discharged soundly (all vacuous), the within-document-sharing subtlety in DEL-REMOVE is handled with care, and the wp derivation is genuinely non-trivial with the correct per-link existential quantifier structure. The worked examples cover the multi-position shift, leading-span, suffix, delete-everything, sharing, and cross-document cases. No correctness defects found. The findings below are prose/anti-bloat, consistent with the `review-mode.anti-bloat` classifier this note carries.

## REVISE

### Issue 1: P4★/P7a preservation argument repeated near-verbatim four times
**ASN-0117, Effect section / DEL-FPROV / "suffix delete" example / "delete everything" example**:
- Effect: "P4★ (`Contains_C(Σ') ⊆ R'`) holds because `Contains_C` can only *shrink* under the net contraction while `R' = R` is unchanged, and P7a ... holds because `dom(C') = dom(C)` (P0) and `R' = R` leave every existing `(a, d)` record in place."
- DEL-FPROV: "this preserves P4★ (`Contains_C(Σ') ⊆ R'`, since the content-containment `Contains_C` only shrinks under the net contraction) and P7a..."
- Suffix delete: "P4★ holds because `Contains_C(Σ')` only shrinks while `R' = R`, and P7a because `dom(C') = dom(C)` with `R' = R` leaves every provenance record in place."
- Delete-everything: "P4★ holds since `Contains_C(Σ')` only shrinks while `R' = R`, and P7a since `dom(C') = dom(C)` with `R' = R` preserves every record."

**Problem**: The identical two-clause argument is stated four times in nearly the same words. The worked examples are supposed to *verify* against the established clauses, not re-derive the general preservation argument.
**Required**: State the P4★/P7a preservation argument once (in DEL-FPROV or the Effect section), and have the worked examples cite it (e.g., "frames and couplings as in the Effect section") rather than restate it.

### Issue 2: Well-definedness remark imagines a case the precondition already excludes
**ASN-0117, P3 / "remark on well-definedness"**: "Drop the containment precondition — delete a span beginning before the document's first arranged position — and the subtraction underflows, producing a V-position below the document's origin that no positive query can reach (Q13, Q14). The precondition is not decoration; it is exactly the domain condition that keeps every survivor at a legal, reachable address. An implementation that omits the bound admits leaked, unreachable arrangement state."

**Problem**: The containment precondition (`J ≥ 1`) already excludes this case; the paragraph then imagines dropping it to explain *why* the precondition is needed rather than what it states. The well-definedness fact itself is already discharged in the same section by the OrdinalExceedsDisplacement citation, and the excluded-case scenario is restated verbatim as the first Open Question. This is justification prose layered on an already-established fact.
**Required**: Keep the OrdinalExceedsDisplacement citation establishing well-definedness on `R`; remove the "drop the precondition / leaked unreachable state" essay, which duplicates the Open Question and explains the precondition's motivation rather than advancing the proof.

## OUT_OF_SCOPE

### Topic 1: Reconstructibility / backtrack state requirements
The note repeatedly gestures at "historical backtrack" and reconstructibility but correctly does not specify what state beyond the content store backtrack requires. This is properly deferred to an Open Question and is new territory, not a gap in DELETE.

### Topic 2: Concurrent operations without a serializing authority
Raised as an Open Question; out of scope for the single-operation semantics this note specifies.

VERDICT: REVISE
