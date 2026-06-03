# Review of ASN-0077

I checked the pointwise origin development (O0–O5★), the I-span and V-span lifts and their equivalence chain (F1≡F2≡F3), the preservation lemmas (O7, O11/O11′/O11★/O11′★/O11★★, O11.1) with their well-formedness side conditions, the negative bounding claims (O13/O14), the boundary cases, and both wp analyses against the worked example.

The proofs hold up under scrutiny:

- **O11 sub-case (a)** correctly derives the contradiction via `m' = m` (forced by S8-depth at Σ′ over the non-empty pre-state content positions guaranteed by precondition (iii)), so K.μ⁺ cannot introduce a depth-`m` content position inside `⟦σ⟧` that precondition (vi) didn't already require — the crux is sound.
- **O2 / equivalence chain** handle both subspaces uniformly (M16a for content blocks, CL-OWN bridged by M-int for link blocks); the link case is not silently folded into M16a.
- **Singleton I-span** rigorously disposes of `#b<#a` (T1), `#b=#a` (T3), and `#b>#a` (zero-count balance forcing document-prefix coincidence), and correctly stops short of the `dom(C)`-length-2 closure it would otherwise need.
- **Boundary cases** (empty intersection, cross-subspace I-span, empty document, empty-restriction, link-subspace V-span) are each addressed with the correct admissible/inadmissible distinction.
- **O13/O14** are backed by concrete witnesses (σ_{1..7} contraction; the [1,1,3]↔[1,1,7] swap), with K.μ~ admissibility discharged clause-by-clause.
- The multi-step exhaustiveness rests on a binary modifies-`M(d)`/fixes-`M(d)` partition, not on enumerating the vocabulary — valid given each lemma's stated hypothesis.
- All cross-ASN references are to foundation ASNs (0034, 0036, 0047, 0053, 0058, 0098); no improper references. O0's link extension is supported by L1c directly (the A_L routing is supplementary, not load-bearing).

No hand-waves, missing conjuncts, or improper references found. Depth requirements (worked example, two wp analyses, derived consequences, negative bounds) are met.

## REVISE

None.

## OUT_OF_SCOPE

### Topic 1: Link-origin reporting from an I-span
The I-span lift restricts to `dom(C)`, silently dropping link addresses (Open Question 1). This is correctly deferred to a future ASN rather than forced into this one.

### Topic 2: Historical-containment operation over Σ.R
Distinguishing current-arrangement origin from ever-contained provenance is appropriately left as an open question, not an error here.

VERDICT: CONVERGED
