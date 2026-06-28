# Signature Resolve — ASN-0036/Strand — run 1

*2026-06-28T02:53:16Z*
*Model: sonnet*

## Output

INTRODUCES:
- bullet: "- `Σ.C` — the content store component of the strand; a partial function `T ⇀ Val` mapping Istream addresses to content values, held immutable across state transitions"
- bullet: "- `Σ.M` — the arrangement family component of the strand; maps each document `d` to its arrangement `Σ.M(d) : T ⇀ T`, a partial function from Vstream positions to Istream addresses, freely mutable"
- bullet: "- `T` — the carrier set used for both Istream addresses and Vstream positions; the shared domain/codomain type for the strand's two components"
- bullet: "- `Val` — the carrier set of content values; the codomain of the content store `Σ.C`"
- bullet: "- `⇀` — partial-function arrow; used to type both `Σ.C : T ⇀ Val` and each arrangement `Σ.M(d) : T ⇀ T`"

REMOVES: []
