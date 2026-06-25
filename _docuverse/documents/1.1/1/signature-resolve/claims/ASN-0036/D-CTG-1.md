# Signature Resolve — ASN-0036/D-CTG — run 1

*2026-06-25T19:45:50Z*
*Model: sonnet*

## Output

The formal contract is fully in the prompt. Analyzing the quantified expression and prose:

- `V_1` — set-valued function `V_1(d)` returning text-subspace positions for document `d`
- `<` — strict ordering on V-positions (not in notation primitives list)
- `subspace` — function extracting the subspace index of a V-position
- `#` — operator extracting the ordinal component from a V-position (`#v`, `#u`)
- `zeros` — function mapping a V-position to its zero-count (depth indicator)

INTRODUCES:
- bullet: "- `V_1` — set-valued function mapping a document to the set of V-positions in its text subspace (subspace index 1)"
- bullet: "- `<` — strict ordering relation on V-positions; used to express gap-freeness between extremes"
- bullet: "- `subspace` — function extracting the subspace index from a V-position; guards the inner quantifier to depth-1 positions"
- bullet: "- `#` — operator extracting the ordinal component from a V-position; equality `#v = #u` selects same-depth peers"
- bullet: "- `zeros` — function mapping a V-position to its count of leading zeros; `zeros(v) = 0` pins v to depth 1"

REMOVES: []
