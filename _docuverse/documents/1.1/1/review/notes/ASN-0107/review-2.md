# Review of ASN-0107

## REVISE

### Issue 1: `Q = (T, T, T)` does not count every stored link
**ASN-0107, "State and the Counting Request"**: "The fully-unconstrained request `Q = (T, T, T)` is a legitimate — if maximally broad — query: it counts every stored link, since every link carries three non-empty endsets (L3)."
**Problem**: L3 (ASN-0043/0093) guarantees only that the *type* endset is non-empty (`e₃ ≠ ∅`); it does **not** require `e₁` or `e₂` to be non-empty, and `Endset = 𝒫_fin(Span)` explicitly admits `∅`. A link with an empty from-endset has `coverage(e₁) = ∅`, so `coverage(e₁) ∩ T = ∅` and `sat` fails on slot 1. Such a link is **not** counted by `Q = (T, T, T)`. The same paragraph already states the correct rule two sentences earlier ("satisfied by any link with a *non-empty* i-th endset"), so the claim is internally contradictory.
**Required**: Strike "since every link carries three non-empty endsets." `Q = (T, T, T)` counts exactly the stored links whose first two endsets are also non-empty (the type endset always is). State this restriction, or note that under the standard triple only `e₃` non-emptiness is guaranteed.

### Issue 2: A1's justification is false
**ASN-0107, A1 (FreshContentNeutrality)**: "The new addresses are not in the coverage of any existing link's endset (endsets were fixed against earlier addresses), so they introduce no new satisfier."
**Problem**: An endset span denotes an *interval* of the address space (PrefixSpanCoverage, ASN-0098), and that interval can contain addresses allocated *later* — this is exactly the orphan/resurrection mechanism (LP17, LP18, L9): a fixed endset's coverage may include a freshly-allocated address. So "new addresses are not in the coverage of any existing link's endset" is wrong. It is also unnecessary: K.α adds no link, so trivially no new satisfier; and for the existence count, neither `coverage` nor the fixed permanent `Q` changes (this is just E3), regardless of whether the new content address happens to fall inside some link's coverage.
**Required**: Replace the parenthetical with the correct reasoning: K.α adds no element to `dom(Σ.L)` and leaves every `coverage` and the fixed `Q` unchanged (E3); the new content address is irrelevant unless it lies in `Q`, which a request denoting unchanged content excludes.

### Issue 3: The reordering worked instance is incompletely computed and inconsistent
**ASN-0107, "A Worked Instance" (reordering paragraph)**: "Sharpen the query to `W₁ = {v₁}` alone ... the links whose from-coverage is exactly `{a₁}` — `ℓ₁` and `ℓ₂` — drop on slot 1 ... so the count moves."
**Problem**: The example tracks only slot 1. Under the natural reading that `W₂ = {v₂}` and `W₃ = {v_τ}` are retained, the swap `π` (which exchanges the *images* of `v₁` and `v₂`) also moves slot 2: `M'(d)(v₂) = a₁`, so `Q₂(Σ') = {a₁}`. Then `ℓ₃`'s to-endset `{a₂}` fails slot 2 (`{a₂} ∩ {a₁} = ∅`), so the true post-swap count is `num_disc = 0`, not the implied `3 → 1`. The worked instance therefore does not faithfully verify the D2-reordering clause and is self-inconsistent.
**Required**: Either fix `W₂`, `W₃` as unconstrained (`T`) so slot 1 alone governs and `num_disc` moves `3 → 1` cleanly, or carry the full three-slot count through the swap (showing `ℓ₃` also drops on slot 2, `num_disc = 0`). State the resulting number explicitly.

### Issue 4: R1's minimal-decrement case omits a precondition
**ASN-0107, R1 (MinimalDecrementNoStoreRetraction)**: "contracting away a single consulted entry whose resolved I-address is reached, in the relevant slot, by exactly one matching link — the discovery count drops by exactly one: `Δnum_disc = −1`."
**Problem**: Content sharing is permitted — distinct V-positions may map to the same I-address (M13/S5, ASN-0058/0036). If another consulted V-position in `Wᵢ` also maps to that I-address, contracting one entry leaves the I-address in `Qᵢ(Σ')`, the link still matches, and `Δnum_disc = 0`. The "exactly one matching link" condition constrains the link side but not the V-position side, so `Δnum_disc = −1` is not guaranteed.
**Required**: Add the missing condition that the contracted entry is the last consulted V-position mapping to that I-address (equivalently, the I-address leaves `Qᵢ` under the contraction), making the decrement-by-one the genuine floor case of R2.

## OUT_OF_SCOPE

(none — the open-questions section already routes future topics, and `match` is correctly kept internal rather than returned)

VERDICT: REVISE
