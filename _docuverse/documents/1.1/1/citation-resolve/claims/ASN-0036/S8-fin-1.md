# Citation Resolve — ASN-0036/S8-fin — run 1

*2026-06-25T02:27:52Z*
*Model: sonnet*

## Output

The S8-fin prose contains two claim-label tokens: `Σ.M(d)` (used throughout as the object being constrained) and `C` in the Frame clause (shorthand for `Σ.C`, named as the non-constrained counterpart). Let me verify `Σ.C` is the right target.

The `Σ.C.md` file confirms it is a claim in ASN-0036, labeled `Σ.C (ContentStore)`. The Frame's `dom(C)` is clearly that claim's object.

```
CLASSIFICATIONS:
- label: Σ.M(d)
  direction: depends
  bullet: "- Σ.M(d) (Arrangement) — supplies the arrangement partial function `M(d) : T ⇀ T` whose domain finiteness this claim constrains"

- label: Σ.C
  direction: forward
  bullet: "- Σ.C (ContentStore) — named in the Frame as the component whose unbounded growth this claim explicitly does not restrict"

RETRACTIONS: []
```
