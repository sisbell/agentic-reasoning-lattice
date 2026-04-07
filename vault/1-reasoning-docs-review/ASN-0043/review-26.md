# Review of ASN-0043

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: PrefixSpanCoverage belongs in a foundation ASN
PrefixSpanCoverage is a purely tumbler-algebraic result — its proof references only ASN-0034 definitions (T1, T12, OrdinalDisplacement, OrdinalShift, prefix relation) and introduces no link-specific concepts. Placing it in the link ontology ASN means any future ASN needing it (span algebra, arrangement operations, content mapping) would reference ASN-0043 for a tumbler-geometry lemma. Factoring it into ASN-0034 or a dedicated span algebra ASN would give it a semantically appropriate home.
**Why out of scope**: The lemma is correctly stated and proved here; the issue is organizational placement, not correctness.

### Topic 2: Unification of `origin` and `home`
ASN-0036 defines `origin(a)` on `dom(Σ.C)` and this ASN defines `home(a)` on `dom(Σ.L)` using the identical formula `(fields(a).node).0.(fields(a).user).0.(fields(a).document)`. A single `doc_prefix(a)` function for all element-level tumblers would subsume both and simplify cross-store reasoning.
**Why out of scope**: Both functions are correctly defined on their respective domains; unification is a future convenience, not a gap in this ASN.

### Topic 3: Link visibility in arrangements
S3 requires `M(d)(v) ∈ dom(Σ.C)`, and L0 gives `dom(Σ.L) ∩ dom(Σ.C) = ∅`, so links cannot appear in any arrangement. Gregory's implementation puts links in a dedicated V-subspace of the document's permutation matrix (with `deletevspan` removing only the POOM entry while the link's orgl and spanfilade persist). Reconciling the abstract model with this implementation behavior — either by weakening S3 or introducing a parallel arrangement mechanism for links — is needed for the operations layer.
**Why out of scope**: The ASN correctly derives the consequence of S3 + L0 and explicitly acknowledges the tension. Resolution requires extending arrangement semantics, which falls under operations-layer work.

VERDICT: CONVERGED
