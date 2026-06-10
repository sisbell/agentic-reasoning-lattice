# Review of ASN-0119

This is a strong, careful note: the imported REARRANGE_K is used correctly, both worked examples (pivot and swap) check out arithmetically against R-PIV/R-SWP/R-PPERM/R-SPERM, the boundary cases (empty exterior vs. degenerate input) are handled, the full ASN-0047 invariant package is discharged, and the depth requirements (concrete example, non-trivial wp via RA7c's contiguity precondition, derived consequences) are met. Two findings remain.

## REVISE

### Issue 1: The P4a trace argument asserts a universal the ASN itself refutes

**ASN-0119, invariant-discharge paragraph (P4a sub-discussion)**: "A valid trace to Σ' is a valid trace to Σ extended by the single REARRANGE step Σ → Σ'."

**Problem**: This is stated as a general fact about Σ' and is the load-bearing step that carries P4a from Σ to Σ'. It is false, and it is contradicted by the ASN's own para-1 observation in "The two streams": "REARRANGE realizes the same net arrangement change as that composite without ever vacating content." REARRANGE's induced π is length-preserving (depth 2 → 2), subspace-preserving (s_C → s_C, identity on s_L), and link-subspace-fixing, and the contiguity paragraph proves the post-state satisfies S8a, S8-depth, D-CTG★, D-MIN★ — i.e. π satisfies every admissibility clause (i)–(v) of ASN-0047's K.μ~, and K.μ~ freezes C, L, E, R exactly as REARRANGE does. So for a non-trivial rearrangement the K.μ~ composite (K.μ⁻ + K.μ⁺) realizes the same π and reaches the very same Σ', yielding a valid trace to Σ' of the form [trace to Σ] + K.μ~ whose final atomic step is K.μ⁺, **not** REARRANGE. Not every trace to Σ' factors through Σ via REARRANGE — and the ASN is the source of the fact that proves it.

The conclusion (P4a holds at Σ') does survive: the non-REARRANGE-ending traces are discharged by their own operations within ASN-0047's induction. But the reasoning as written is wrong.

**Required**: Scope the claim to traces whose final composite is this REARRANGE step ("any valid trace to Σ' *ending in REARRANGE* decomposes as [valid trace to Σ] + REARRANGE"), and state explicitly that traces reaching Σ' by any other route — e.g. the K.μ~ route the ASN itself flags — are that operation's obligation, already discharged. This is the only repair the argument needs.

### Issue 2: Forward-reference / document-structure meta-prose (anti-bloat)

**ASN-0119, RA7a derivation**: "(This derivation re-proves inline, for REARRANGE, ASN-0098's coverage invariance LP3 and reordering bijection LP11 ... so this note reconstructs their conclusions rather than citing them.)"
**ASN-0119, RA1 paragraph**: "We label the pair RA1 for use below."
**ASN-0119, worked pivot**: "the Links section next formalizes this transport as RA7a."

**Problem**: The LP3/LP11 *correspondence* advances understanding; the trailing clause justifying *why* the note re-proves rather than cites is document-structure rationale the derivation does not need (and the kind of defensive prose this review mode is set to catch). "for use below" and the pointer to the Links section are gratuitous signposts a reader skips past to follow the local claim.

**Required**: Drop the "reconstructs ... rather than citing them" justification clause (keep the bare LP3/LP11 correspondence if useful); drop "for use below"; let RA7a stand where it is derived rather than pre-announcing it.

## OUT_OF_SCOPE

The Open Questions section already defers the right topics — cross-document boundary-hood of shared content, unserialized concurrent rearrangements, content-based discovery-index invariants under footprint fragmentation, recoverability of a prior arrangement, and the boundary-preservation guard for a closed-form displacement layer. These are genuine future territory, not gaps in this ASN; the deferral is correct and needs no change.

VERDICT: REVISE
