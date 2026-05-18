## Question 6 [theory]

> Was the link design ever intended to admit more than three endsets, or has the structure always been exactly the triple (F, G, Θ) — from-set, to-set, type-set?

# On Link Endsets: Always Three

The link structure has always been exactly the triple (F, G, Θ). The three-endset design is canonical throughout Literary Machines, and richer relational structures emerge through **composition** (link-to-link), not through adding endsets.

## Direct Evidence for the Triple

The FEBE protocol's `MAKELINK` operation specifies precisely three sets:

> "This creates a link in document <doc id> from <from set> to <to set> connected to <three set>." (4/68)

The search operation is correspondingly `FINDLINKSFROMTOTHREE` — three constraints, no more.

## Symmetric, Not Extensible

Nelson presents the type endset as a *generalization* of the from/to endsets to a symmetric triple — explicitly closing the design at three:

> "A link's type is specified by yet another end-set, pointing anywhere in the docuverse. This is symmetrical with the other endsets." (4/44)

> "The from-set may be an arbitrary collection of spans, pointing anywhere in the docuverse. Similarly, the to-set may be an arbitrary collection of spans pointing anywhere in the docuverse. We adopt the same convention for link types." (4/43)

The "Tumbler Square" visualization on 4/46-4/47 shows the link's home on one side and exactly three endsets mapping to the other three sides — a four-sided figure (home + 3 endsets), not n-sided.

## How N-ary Relations Are Handled: Composition

When Nelson needs structures richer than three-way (e.g., faceted classifications, hierarchical types), he composes links rather than extending the link signature:

> "Complex relational structures, such as the faceted link (discussed in Chapter 2), may be constructed with links to links. These use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." (4/51)

The CONS analogy is telling: just as LISP builds arbitrarily complex data from pairs, Xanadu builds arbitrarily complex relations from triples via link-to-link.

## Variation Within the Triple, Not Beyond It

The one variation Nelson discusses is *fewer* than three meaningful endsets, not more:

> "One-Sided Links: An important variation where a link has only one side - something pointing to material, but not from other material." (cited from 4/48)

So the design space Nelson explored was 1–3 active endsets within a triple, with extensibility achieved by linking links — never by widening the signature.

## Summary

The triple (F, G, Θ) is invariant in the specification. Nelson's design strategy was to keep the primitive minimal and symmetric, then let users compose: link-to-link gives you n-ary relations, compound links give you faceted structures, and ghost-element type endsets give you unbounded extensibility on the third axis. Adding a fourth endset would have violated the "minimal powerful mechanism" pattern that runs through the whole architecture.

NEED_RAW: 2/24-2/25 (faceted link discussion in Chapter 2, referenced from 4/51 but not in curated sources) if the user wants the original framing of compound/faceted links.
