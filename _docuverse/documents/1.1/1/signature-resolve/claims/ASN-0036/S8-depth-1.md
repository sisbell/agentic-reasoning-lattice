# Signature Resolve — ASN-0036/S8-depth — run 1

*2026-06-25T01:34:09Z*
*Model: sonnet*

## Output

INTRODUCES:
- bullet: "- `Σ` — the strand model structure; accessed as `Σ.M(d)` to retrieve the V-position mapping for document `d`"
- bullet: "- `M` — the V-position mapping component of `Σ`; `dom(Σ.M(d))` yields the set of all V-positions in document `d`"
- bullet: "- `dom` — domain function on mappings; returns the key set of a mapping, here used to range over all V-positions of a document"
- bullet: "- `subspace` — function from a V-position to its subspace identifier; the axiom's grouping criterion: positions with equal `subspace` values must share a common depth"
- bullet: "- `#` — depth function on tumbler addresses; returns the number of components in an address; the axiom asserts `#u = #w` for all same-subspace positions"

REMOVES: []
