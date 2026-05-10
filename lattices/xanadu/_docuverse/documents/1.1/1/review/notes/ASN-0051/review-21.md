# Review of ASN-0051

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Link-subspace contribution to endset projection
**Why out of scope**: The ASN explicitly defers link-subspace V-position contributions to π(e, d) — i.e., cases where endset spans reference link addresses that appear via K.μ⁺_L mappings — to the Link Subspace ASN. SV11 correctly restricts its decomposition to π_text. A future ASN should characterize the full projection.

### Topic 2: Canonical fragment ordering and representation
**Why out of scope**: The open questions correctly identify that fragment ordering across mapping blocks is not specified. This is a representation concern for the implementation layer, not a survivability invariant.

### Topic 3: Dormant link reactivation
**Why out of scope**: The mechanism by which a link that has lost vitality in all documents could regain it (e.g., through fork or transclusion of archived content) is a valid question but belongs in the operations layer where composite transitions are sequenced.

---

**Review notes.** The proofs are thorough and correct throughout. I checked every formal claim against the foundation ASNs:

- **SV2/SV3**: The ran monotonicity arguments are sound — K.μ⁺ preserves existing mappings (giving ⊇), K.μ⁻ restricts the domain with preserved values (giving ⊆). Both correctly handle non-injective arrangements where range inclusion can be strict or not.

- **SV5**: The bijection argument correctly uses K.μ~-FIX (dom fixed) and the K.μ~ definition to establish both projection invariance and the locate set transformation. The witness showing locate sets *can* differ is well-chosen.

- **SV6**: The sandwich argument is the proof's core and I verified it step by step. The case split (#t ≥ k, then agreement on positions 1..k−1) is correct, both branches using the same contradiction: any divergence before position k forces t above reach via T1(i). The precondition k > p₃ is exactly right — at k = p₃ the third separator could shift to a nonzero value, breaking the origin argument. The T5 note correctly identifies why the weaker prefix-containment result is insufficient (prefix containment does not force separator alignment when field structures differ in depth). The counterexample (same-origin child-depth entry) is valid and correctly verified.

- **SV7**: The equality (not mere monotonicity) follows from L being entirely in frame for all transitions except K.λ. The proof correctly identifies that both inputs to discover_s — dom(L) and coverage values — are unchanged.

- **SV11**: The contiguity-within-ordinal-sequence argument via S0 (Convexity) is correct. The "cover not partition" qualification for non-injective arrangements is properly stated. The m · p bound holds because each (span, block) pair contributes at most one contiguous fragment.

- **Worked example**: Verified all computations — initial projections, post-removal arrangement via K.μ~ + K.μ⁻, fragment decomposition, and the SV6 explicit tumbler verification. All correct.

- **SV13**: Each clause correctly cites its source property. The synthesis is faithful to the individual results.

VERDICT: CONVERGED
