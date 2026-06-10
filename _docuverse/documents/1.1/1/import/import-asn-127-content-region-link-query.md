---
create_note: 127
title: "Content-Region Link Query"
source_doc: "_workspace/asn-new-content-region-link-query-draft.md"
depends: [34, 36, 43, 47, 58, 93, 98]
---

# Why I'm importing this doc

ASN-0099 (FINDLINKS Operation) was authored as an operation note but
ended up developing foundation-grade content along the way: a two-phase
factoring of content-region link queries (`image(R, d, Σ)` + per-link
matching), a stability meta-lemma over comprehensions consulting only
`Σ.L`, and a characterization of which K-transitions preserve the link
store. That foundation theory was then borrowed wholesale by ASN-0110
(RETRIEVEENDSETS) via 10 load-bearing claim citations, locking in an
operation-on-operation dependency the architecture does not condone.

ASN-0107 (FINDNUMOFLINKSFROMTOTHREE) re-derived the same machinery
locally under different labels (E1-E4, D1-D3, `Qᵢ(Σ)`); ASN-0108
(FINDNEXTNLINKSFROMTOTHREE) deferred it as a hand-waved "discoverability
reading" that the windowing layer depends on. ASN-0121 (the FINDLINKS
reframe) avoids the algebra deliberately via an I-address-only regime —
correct architecturally, but its FL-STB stability claim is identifiably
an instance of the same meta-lemma.

The pattern is a missed factoring. The content-region link query
algebra is foundation-grade content that should have existed before
any of the find-links family was drafted. Three of four content-region
link query operations currently re-derive, defer, or borrow it; one
deliberately avoids it. None can cite it cleanly because it has no
foundation home.

This note supplies that home and only that. It names the projection
primitive `image(R, d, Σ)`, the per-link match predicate, the two-phase
combinator `findlinks_V`, and the stability keystone
ComprehensionInvariantUnderΣL (with its per-link sub-lemma). On top of
those it states A1a (which K-transitions preserve `Σ.L`), F9 (Σ.L-
fixity ⟹ result invariance), and F9-λ (the unique store-modifying
transition's per-step effect, fully characterized). The anchoring
taxonomy distinguishes existence-anchored requests (fixed I-addresses
in the permanent space) from discovery-anchored requests (state-
resolved through `M(d_q)`), surfacing the monotonicity / non-monotonicity
asymmetry the operations layer needs to reason about reader-facing
stability.

The note explicitly does not address: operation-specific filtering
duality (filtered/unfiltered, per-slot universal vs per-link
existential), content-keyed queries that name addresses through `Σ.C`
rather than `Σ.M`, or composition with link projection displacement
(ASN-0098's territory). Those layer on top via successor work.

Importing now because:

- The dependent revisions (ASN-0110 reframe, ASN-0107 reframe, ASN-0108
  in-place revise, ASN-0121 two-citation revise) all need this
  foundation to exist before they can re-cite cleanly.
- ASN-0099's full retirement (currently retired-but-still-cited) is
  blocked on the foundation existing so the borrowed citations have
  somewhere to land.
- Future content-region link query operations should cite this rather
  than re-derive.

Direct deps `[34, 36, 43, 47, 58, 93, 98]` — no transitivity
assumption:
- ASN-0034 supplies the tumbler address space `T` and total order T1.
- ASN-0036 supplies S0 (content-store append-only).
- ASN-0043 supplies L3/L4/L6/L12/L-fin and the `coverage` definition.
- ASN-0047 supplies the extended state `Σ = (C, L, E, M, R)`, the
  K-transition vocabulary, and S3★.
- ASN-0058 supplies B1+B2 mapping-block decomposition (for the
  contiguous-V-span case of the image).
- ASN-0093 supplies K.λ's freshness precondition.
- ASN-0098 supplies LP3★ (coverage permanence), LP11 (total-range
  preservation under reorder), and store monotonicity.
