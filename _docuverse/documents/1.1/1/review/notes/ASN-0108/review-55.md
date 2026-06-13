# Review of ASN-0108

I checked the windowing theory end to end: the wp algebra in W2, the rank-block induction in W4, the sufficiency/necessity hedging in W5, the charge-injectivity bound in W9b, and the four termination walks against the W9/W9a formulas (including the `[N divides m]` term at `m=4`, `m=0`, `m=5`, `N>m`). The arithmetic and the case structure hold; the edge cases the framework demands — empty matching set, exact multiple, first-window-short, orphaned cursor — are all exercised. Cross-ASN citations are confined to the foundation set, and the new symbols (`Match`, `κ`, `≺`, `After`, `Window`) reinvent no foundation notation. Two issues remain.

## REVISE

### Issue 1: The content-position foil key is multi-valued under the adopted discoverability reading

**ASN-0108, "The Enumeration Order" (third candidate key) and its load-bearing uses in W5, W8, W9c**: "the **content-position key**, keyed on the matched content's *current V-position*"; W5 walk: "`κ(x) = ` the *current V-position* of `x`'s matched endpoint content in the consulted arrangement"; W8 walk: "`κ(a₂)` were the *current V-position* of `a₂`'s matched endpoint content."

**Problem**: The note commits to the discoverability reading, under which a link matches `q` at `Σ` exactly when *some* slot's coverage meets `ran(M(d_q))` (ASN-0127 LP12). That intersection can be witnessed by several covered I-addresses, each in turn mapped from several V-positions of `d_q`. So "x's matched endpoint content" does not name a single position — the foil key's *primary* component is multi-valued, and `κ` is undefined as written. The note resolves precisely this multiplicity for *Gregory's* key by keying on the **least** covered I-address of the designated slice (and even cites `onlinklist`'s first-encounter/least-address dedup as the operational resolution), but supplies the V-position foil no analogous selection rule. This matters because the foil is load-bearing, not decorative: the general claims "the content-position key guarantees neither clause" (W5), "It is the content-position key alone … that fails" (W8), and the zero-inflow non-termination construction (W9c) all quantify over *every* matching link, while only the walks' single-endpoint instances make `κ` well-defined.

**Required**: Give the content-position foil a selection rule parallel to Gregory's "least covered I-address" (e.g., the least matched V-position in `d_q`), or scope the foil's general claims to links matching at a unique endpoint. The walks are unaffected by either fix — this is a definitional-precision repair, not a proof repair.

### Issue 2: W8 draws the computability-vs-stability distinction twice

**ASN-0108, W8 preamble vs. W8 body**: The "Two evaluability conditions" preamble opens by positioning the new conditions against W5: "whether `κ(c)` can be evaluated at all — a family of key conditions distinct from W5's comparison-stability family (clause 1, clause 2, state-stability), which governs whether comparisons *move* under evolution rather than whether `κ(c)` can be computed in the first place." The body then re-draws the same line: "The load-bearing property is **computability** of `κ(c)` … *not* value-invariance and *not* state-stability of comparisons; W8 needs only that `κ(c)` remain readable."

**Problem**: The evaluability-vs-comparison-movement distinction is the conceptual axis of W8, and it is stated in full twice within the same claim. The preamble's cross-reference to W5's clause-1/clause-2/state-stability triad is taxonomy the reader parses before reaching the actual definitions (computability, value-totality), which stand on their own; the body then makes the contrast again, concretely, where it is needed. Under the anti-bloat lens this is the forward/cross-reference meta-prose the classifier targets: one of the two statements can go.

**Required**: Keep the definitions of computability and value-totality in the preamble; drop the preamble's cross-claim positioning clause (or reduce it to a parenthetical), since the body already establishes computability ≠ value-invariance ≠ state-stability at the point of use.

## OUT_OF_SCOPE

The deferred territory is already correctly captured by the note's own Open Questions — multi-document enumeration without a global allocation-monotone key (the W6 caveat → OQ1), eventual delivery under a non-allocation-monotone key, the cross-call completeness invariant over a mutating set, the recovery protocol for an uncomputable orphaned cursor (the W8/W9 ambiguity), and progress-sizing correspondence. I raise no new OUT_OF_SCOPE items; these are appropriately scoped out rather than missing.

VERDICT: REVISE
