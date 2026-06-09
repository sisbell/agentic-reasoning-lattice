## Question 3 [theory]

> When a span designates content "exactly," does the design require every named position to be bound — i.e., is a partially-bound span ill-formed — or may COPY designate only the bound subset?

## Short answer

The design does **not** require every named position to be bound. A partially-bound (or even empty) span is **well-formed**. The reason is structural: a Xanadu span designates content by its *boundaries*, not by enumerating occupied positions, and "what lies between... is implicit in the choice of first and last point" (4/25). Because binding was never a well-formedness condition on a span, COPY operates on whatever content the boundaries actually determine — i.e., the bound subset.

Let me show why the question's first horn ("partially-bound span is ill-formed") is ruled out by Nelson's own span semantics.

## A span is boundary-defined, not a list of bound positions

The premise behind "every *named* position must be bound" treats a span as an enumeration of positions. Nelson's model is the opposite — a span names two endpoints and the content is implicit:

> "The first point of a span may designate a server, an account, a document or an element; so may the last point. There is no choice as to what lies between; this is implicit in the choice of first and last point." (4/25)

> "A tumbler-span is not a conventional number, and it does not designate the number of bytes contained. It does not designate a number of anything." (4/24)

Crucially, the design explicitly anticipates spans that bind *nothing*:

> "A span that contains nothing today may at a later time contain a million documents." (4/25)

An empty span is the limiting case of a "partially-bound" span. Since Nelson treats it as a valid, persistent object (its content simply grows over time), partial binding cannot be a well-formedness violation.

## "Exactly" governs exclusion, not completeness of binding

The word "exactly" in the span literature is about *not pulling in unwanted neighbors*, not about requiring every position to be occupied:

> "Note: if you want to designate a separated series of items exactly, including nothing else, you do this by a span-set, which is a series of spans." (4/25)

The phrase is "including nothing *else*" — the span-set machinery exists to **exclude** the intermediate material between discontiguous pieces. It is a precision-of-boundary mechanism, not a binding-completeness requirement. So "designates exactly" never meant "every named position is occupied."

## Unbound positions are first-class in the address space

That tumbler-space contains addressable-but-unbound positions is a deliberate architectural feature, not an error state — these are the **ghost elements**:

> "While servers, accounts and documents logically occupy positions on the developing tumbler line, no specific element need be stored in tumbler-space to correspond to them. Hence we may call them ghost elements." (4/23)

> "However, these elements are virtually present in tumbler-space, since links may be made to them which embrace all the contents below them." (4/23)

And on the link side, the same permissiveness is stated outright:

> "Indeed, there is no need for the presence of elements at the addresses specified. Link types may be ghost elements." (4/45)

So unbound addresses are routinely *embraced* by spans (a link to an account "embraces all the contents below"). The system finds whatever is bound under that span without requiring the span itself to be fully occupied.

## COPY designates the determined (bound) content

COPY's specification is consistent with this — it copies "the material determined by" the spec-set, and "material determined by" a span is precisely the implicit, bound content within the boundaries:

> "COPY: The material determined by <spec set> is copied to the document determined by <doc id> at the address determined by <doc vsa>." (4/67)

There is no clause requiring the spec-set to be densely bound, and no notion of COPY failing on an under-occupied span. It transcludes what is there.

## One caveat about V-space (where the question rarely bites)

Note that *within a single document's Vstream*, the question is largely moot, because Vstream is dense by construction:

> "There are no gaps — if you have 100 bytes, you have addresses 1 through 100." (v-space-addresses, per 4/30/4/66)

So a COPY spec-set expressed over a document's current V-positions is fully bound automatically. The partial-binding scenario is meaningful only in the general tumbler-space case (spans embracing ghost regions, accounts, sparse subtrees), and there the ghost-element design (4/23) governs: the span is valid and the operation acts on the occupied subset.

## Bottom line

- A partially-bound span is **not** ill-formed; the empty span is explicitly a valid, persistent object (4/25).
- "Exactly" is about **excluding** intermediate content (span-sets), not about requiring full occupancy (4/25).
- Unbound positions are intended ("ghost elements," 4/23, 4/45).
- COPY acts on "the material determined by" the spec-set (4/67) — i.e., the bound subset within the boundaries.

One honesty flag: the curated sources establish the span/ghost-element semantics directly, but Nelson does not give a worked example of COPY *over a partially-bound tumbler span* specifically. The conclusion above is a synthesis of the span model (4/24–4/25), ghost elements (4/23, 4/45), and the COPY spec (4/67) rather than a single sentence ruling on COPY-over-ghosts. If you want a verbatim ruling on that exact edge case, NEED_RAW: 4/67, 4/63 (COPY / FINDDOCSCONTAINING surrounding text) and 4/24–4/25.
