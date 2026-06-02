# Review of ASN-0069

## REVISE

### Issue 1: Empty-source trigger condition stated against `d_src` instead of `d_op`

The ASN takes great care, throughout §"What Must Be Constructed" and onward, to distinguish the *identity source* `d_src` from the *content source operand* `d_op` (= `d_src` on a first fork, = `d_prev` on a subsequent fork), and §"The Empty-Source Case" correctly states that "on a subsequent fork `d_op = d_prev`, so the relevant emptiness is that of the prior version, which may be empty even when `d_src` is not." V4, V8, V7's formal statement, and V0's Effects all correctly key on `V_{s_C}(d_op)`.

But three downstream statements slip back to `d_src`, which produces *wrong* claims for subsequent forks (where `d_op = d_prev` can be empty while `d_src` is non-empty, or vice versa):

**ASN-0069, §"The Empty-Source Case", paragraph after V7**: "V4 and V8 are vacuous when `V_{s_C}(d_src) = ∅` (their universal quantifiers range over an empty set)."
**Problem**: V4 and V8 quantify over `V_{s_C}(d_op)`, so they are vacuous precisely when `V_{s_C}(d_op) = ∅`, not `V_{s_C}(d_src) = ∅`. On a subsequent fork with an emptied prior version but non-empty `d_src`, this statement is false.

**ASN-0069, Properties Introduced table, V7 row**: "fork of `d_src` with `V_{s_C}(d_src) = ∅` reduces to K.δ alone".
**Problem**: Contradicts the formal V7 statement ("fork of `d_src` with `V_{s_C}(d_op) = ∅`"). For a subsequent fork these differ.

**ASN-0069, §"The Fork Composite", K.δ-alone verification header**: "When `V_{s_C}(d_src) = ∅`, V7 reduces V0 to a single elementary K.δ step".
**Problem**: The composite reduces to K.δ alone iff K.μ⁺ cannot fire, i.e. iff `V_{s_C}(d_op) = ∅`. Keyed on `d_src`, a subsequent fork of a content-bearing `d_src` whose `d_prev` was emptied would be misclassified as the non-empty branch.

**Required**: Replace `V_{s_C}(d_src)` with `V_{s_C}(d_op)` in all three locations, matching the formal V7 statement, V0, and §"The Empty-Source Case"'s own opening. (Note the worked-example "Empty source" vignette is a *first* fork, where `d_op = d_src`, so it remains correct as written.)

## OUT_OF_SCOPE

None. The Open Questions section appropriately defers concurrency, snapshot-vs-living forks, descendant enumeration, transcludent sources, and version-collection coherence to future ASNs.

VERDICT: REVISE
