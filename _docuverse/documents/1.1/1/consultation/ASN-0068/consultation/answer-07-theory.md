## Question 7 [theory]

> What must the design guarantee about the symmetry of the comparison — does the order of the two documents affect the result?

# Symmetry of Comparison

The design must guarantee **two distinct properties**, which are easy to conflate:

## 1. The correspondence relation is symmetric

Correspondence is a structural property of the spans themselves, derived from shared Istream origin. If span X in document A corresponds to span Y in document B, that fact is intrinsic to the spans — not to which document you happen to name first. The Istream addresses are permanent and non-directional; the relation simply *is* what it is.

This follows from the foundational claim that correspondence enables intercomparison:

> "Of course, a facility that holds multiple versions of the same material, and allows historical backtrack, is not terribly useful unless it can help you intercompare them in detail—unless it can show you, word for word, what parts of two versions are the same." [LM 2/20]

"What parts are the same" is an inherently symmetric question. The answer cannot legitimately depend on argument order.

## 2. The returned ordered pairs preserve argument order

The protocol response, however, is *ordered* — and this is intentional. From SHOWRELATIONOF2VERSIONS:

> "This returns a list of ordered pairs of the spans of the two spec-sets that correspond." [LM 4/70]

So `SHOWRELATIONOF2VERSIONS(A, B)` returns pairs `(a_span, b_span)`; reversing the arguments returns `(b_span, a_span)`. The pairs are swapped, but the underlying matching is identical. The caller must be able to interpret which element of each pair belongs to which document — hence the ordering.

## The guarantee

**Information-equivalence under reversal**: `SHOWRELATIONOF2VERSIONS(A, B)` and `SHOWRELATIONOF2VERSIONS(B, A)` must convey identical content — same set of correspondences, same span boundaries — differing only in the order within each pair. No correspondence may appear in one direction and be hidden in the other. No span boundary may shift based on argument order.

This is what makes the operation *meaningful* as a basis for intercomparison and for refractive link-following:

> "Links may be refractively followed from a point or span in one version to corresponding places in any other version. Thus a link to one version of a Prismatic Document is a link to all versions." [LM 2/26]

If the relation were asymmetric, a link from A could lead to B, but the same link from B might not lead back to A — and the whole prismatic-link guarantee collapses.

## What is *not* symmetric

The **comment** on a counterpart link can carry directional commentary added by the linker. That's commentary metadata, not the correspondence relation itself.

> "The counterpart link shows that there are correspondences between two equivalent documents, sections or passages. (This has also been called a collateral or correspondence link. Note that a counterpart link will typically have a comment attached to it." [LM 4/53]

The link's *commentary* may say "A is the translation of B" rather than "B is the translation of A." But the structural correspondence — which spans match which — must be the same either way.

---

**NEED_RAW: 4/70** — Nelson defines the protocol as returning "ordered pairs" but does not, in the curated material, *explicitly* state the symmetry guarantee as a design requirement. The symmetry follows necessarily from the architecture (shared Istream origin, refractive link-following), but if you want Nelson's own words stipulating "reversing arguments must yield equivalent results," the full 4/70 protocol description should be consulted to confirm whether any directional asymmetry is specified.
