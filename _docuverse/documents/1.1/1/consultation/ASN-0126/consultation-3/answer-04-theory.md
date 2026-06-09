## Question 4 [theory]

> Does "single source" mean a single span as emitted, or a single contiguous coverage — i.e., should two adjacent spans of identical coverage be admissible as a conforming source?

## Answer: "Single source" means single *contiguous coverage*, not a single emitted span

The distinction you're drawing maps directly onto Nelson's separation between a **span** and a **span-set**, and the decisive principle is that in Xanadu **coverage is defined by boundaries, not by enumeration**.

### 1. Coverage is implicit in endpoints, so emission count is not load-bearing

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

Two adjacent spans `[a,b)` and `[b,c)` cover exactly the I-address set that the single span `[a,c)` covers. By Nelson's rule, the *content* of a span is fixed entirely by its endpoints — the act of cutting one contiguous extent into two abutting pieces adds no information and changes no coverage. They are coverage-equivalent. So conformance keyed on coverage cannot distinguish them, and "single source" defined as "exactly one span object as emitted" would be drawing a line Nelson's semantics don't recognize.

### 2. Span-*sets* are reserved specifically for *discontiguity*

Nelson only invokes the multi-span construct when the selection is *broken*:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

The motivating case for "a series of spans" is *separated* items. Adjacency is the opposite of separation. So two adjacent spans of identical coverage are not the thing span-sets exist to express — they are a redundant encoding of what is, semantically, one contiguous span. This is the same reasoning behind a single span being "a degenerate case of a subtree" (`spans` source, 4/24): contiguous coverage has a canonical single-span form.

### 3. Canonical order is an internal mandate — so normalize, don't reject

> "All changes, once made, left the file remaining in canonical order, which was an internal mandate of the system." (1/34, on Barus's enfilade)

This argues against treating the two-adjacent-spans form as a *violation*. The intent is that the system reduces redundant structure to canonical form, not that it refuses input that happens to arrive un-coalesced.

### Recommendation for the spec

- **Define "single source" as single contiguous coverage** (one contiguous I-extent / one coverage-class member), not as "one span as emitted."
- **Admit two adjacent spans of identical/contiguous coverage as a conforming source** — they denote the same I-address set as the merged span and are coverage-equivalent.
- **Have the conformance gate normalize (coalesce adjacent/abutting spans) to the canonical single-span form** before or as part of the check, rather than rejecting. Rejection would penalize a representation choice that carries no semantic difference and contradict the canonical-order mandate.
- The boundary case that *should* fail "single source" is genuine **discontiguity** (a gap between spans) — that is precisely when Nelson says you need a span-set, and it is a different coverage.

### Caveat on terminology

NEED_RAW: none required for Nelson's span semantics — the above is fully grounded in 4/24–4/25 and 1/34. However, flag that **"single source," "conforming source," "coverage," and "coverage-class" are this project's spec terms (cf. the recent ASN-0126 coverage-class registry / K.λ_sh work), not Nelson's own vocabulary.** Nelson never adjudicates adjacent-span coalescence as an admissibility rule directly; I'm deriving the intended answer from his span/span-set distinction and the canonical-order mandate. If the spec's "conforming source" gate is intended to assert a *normalized* invariant (rather than accept-and-normalize), that is a project-level choice consistent with — but not literally stated by — Nelson.
