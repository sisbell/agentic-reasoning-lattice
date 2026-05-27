# Review of ASN-0099

## REVISE

### Issue 1: τ-link disjointness gap in worked example setup
**ASN-0099, "A Worked Example" section, setup**: "Three type-tumbler addresses `τ_comment`, `τ_reply`, `τ_meta`, pairwise distinct and pairwise disjoint from the content addresses `{α₁, α₂, α₃}` under the prefix order (none is a prefix or extension of any other or of any `αᵢ`)."

**Problem**: The setup establishes prefix-disjointness only (a) pairwise among τ-addresses and (b) between τ-addresses and content addresses α_i. It does NOT establish prefix-disjointness between τ-addresses and link addresses (ℓ, ℓ', ℓ_meta). However:

(a) Query 9's verification of `findlinks({ℓ}, Σ_L)` requires both `τ_comment ⋠ ℓ` (so that ℓ's slot 3, covering `{t : τ_comment ≼ t}`, does not contain ℓ) and `τ_reply ⋠ ℓ` (so that ℓ''s slot 3, covering `{t : τ_reply ≼ t}`, does not contain ℓ). Query 9 itself invokes "τ-disjointness handles slot 3 against `τ_comment` and against link addresses generally" — but this stronger τ-link disjointness is asserted in passing, not established by the setup. Without it, the conclusion `result = {ℓ_meta}` exclusively cannot be reached; ℓ and/or ℓ' might match via their slot 3.

(b) Query 8's parenthetical "`findlinks_filtered({(1, {τ_comment})}, Σ) = ∅` (no link's slot 1 covers `τ_comment`)" requires `ℓ ⋠ τ_comment` (so that ℓ_meta's slot 1, covering `{t : ℓ ≼ t}`, does not contain τ_comment).

**Required**: Strengthen the τ-disjointness clause in the worked example setup to include link addresses — either by explicit extension ("...or of any link address `ℓ, ℓ', ℓ_meta`") or by specifying a concrete allocation context (e.g., "τ-addresses allocated under a separate type registry document `d_τ` distinct from `d_a` and `d_b`") so that CrossDocDisjointness (ASN-0093) and PrefixOrderingExtension (ASN-0034) discharge τ-ℓ non-extension automatically.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
