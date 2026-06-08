# Review of ASN-0110

## REVISE

### Issue 1: RE-reveal's degenerate pairing claim and its example are wrong
**ASN-0110, RE-reveal**: "in degenerate states the pairing survives — if exactly one link touches `I` (e.g. the worked instance restricted to `a₁` alone), each role-family `Eᵢ` holds at most one endset and the from/to/type triple is trivially reassembled."

**Problem**: The cited example contradicts the claim. Restricting the worked instance to `a₁ = (F₁, G₁, Θ)` with `I = {c₂, c₃}`: only slot 1 touches (`F₁`), so `E₁ = {F₁}`, `E₂ = ∅`, `E₃ = ∅`. By RE-full the operation returns only *touching* slots, so `G₁` and `Θ` are absent from the result entirely. The from/to/type triple is therefore **not** reassembled — two of its three members never appear. The single-touching-link case the example names is precisely a case where a link touches through only one role, leaving nothing to pair and no triple to recover. The genuine degenerate case (recoverable pairing) is "exactly one touching link that touches through *multiple* roles," and even then only the touching slots are paired, never the full stored triple.

**Required**: Replace the example with one where a single link touches through multiple roles (so a pairing of *returned* endsets exists), and weaken "the from/to/type triple is trivially reassembled" to "the touching endsets returned across roles are trivially attributed to the one link" — the non-touching slots are not in the result and cannot be reassembled.

### Issue 2: RE-anon's "lower bound" is misidentified
**ASN-0110, RE-anon (corollary)**: "the result yields at most a lower bound (the number of distinct endset values present), never the true count."

**Problem**: The number of distinct endset values present is not a lower bound on the contributing-link count. Counterexample: a single arity-3 link with value `(e, e', θ)`, all three slots touching `I` and `e, e', θ` pairwise distinct, gives `E₁ = {e}, E₂ = {e'}, E₃ = {θ}` — three distinct endset values from **one** link. So distinct-value-count (3) exceeds link-count (1); it is not a lower bound. A single link can contribute multiple distinct values (one per role), while distinct links can share values, so the two cardinalities have no general ordering.

**Required**: Drop or correct the parenthetical. If a lower bound is wanted, it must be stated per role (`|Eᵢ|` lower-bounds the number of distinct links touching via slot `i`, since one link contributes at most one slot-`i` value), not as "distinct endset values present" across the whole result.

## OUT_OF_SCOPE

(none — the deferred items in Open Questions, including V-space presentation contract and pairing reconstructibility, are appropriately left to future ASNs.)

VERDICT: REVISE
