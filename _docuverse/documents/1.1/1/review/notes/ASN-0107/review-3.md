# Review of ASN-0107

## REVISE

### Issue 1: R1 asserts an exact −1 decrement that its own conditions don't guarantee

**ASN-0107, §"How the Count Changes: Links Retracted", R1**: "contracting away a single consulted entry that is the last consulted V-position mapping to its resolved I-address ... where that I-address is reached, in the relevant slot, by exactly one matching link — the discovery count drops by exactly one: `Δnum_disc = −1`."

**Problem**: The stated conditions constrain how many *links* reach the removed address `a`, but not whether the one matching link `ℓ` has *alternate* reach into `Qᵢ`. The link drops only if `coverage(ℓ.eᵢ) ∩ Qᵢ(Σ') = ∅`, i.e. only if `coverage(ℓ.eᵢ) ∩ Qᵢ(Σ) = {a}`. If `ℓ`'s slot-`i` coverage also meets `Qᵢ(Σ)` at some surviving address `a' ≠ a` (permitted, and exactly the situation R3 describes), then `ℓ` survives and `Δnum_disc = 0`. R1 omits the condition that excludes this. The overclaim is also internally inconsistent: R1 calls itself "the `k = 1` case of R2," and R2 gives `Δ ∈ {−k, …, 0}` — so the `k = 1` specialization is `Δ ∈ {−1, 0}`, not the asserted `= −1`.

**Required**: Add the missing condition (the matching link's slot-`i` coverage meets `Qᵢ(Σ)` only at `a`), or restate the conclusion as `Δnum_disc ∈ {−1, 0}` with `−1` attained precisely under that condition — consistent with R2 and R3.

### Issue 2: A1's discovery-count clause states a condition inconsistent with its own premise

**ASN-0107, §"How the Count Changes: Content Added", A1**: premise "new I-addresses carrying no incoming links"; conclusion "for the discovery count it holds whenever the inserted content lies outside the resolved region `Qᵢ(Σ)`."

**Problem**: Under the premise that the fresh address `a_new` has *no incoming links*, no stored link has `a_new ∈ coverage(eᵢ)`, so arranging `a_new` into the query region (a `K.μ⁺` step, which is what "inserting into an arrangement" requires) cannot create a new match — even when `a_new` enters `Qᵢ(Σ')`. Neutrality therefore holds *regardless* of whether the content lies inside or outside the region; the operative reason is the no-incoming-links premise, not the location. The qualifier "lies outside the resolved region" is thus both unnecessary and incorrect as a sufficient condition, and it conflates the existence-count argument (fixed `Q`) with the discovery-count argument (resolved `Qᵢ` that the insertion changes). It is also imprecisely worded: `Qᵢ(Σ)` is an address set evaluated at the pre-state, and `a_new` is fresh, so "`a_new` lies outside `Qᵢ(Σ)`" is trivially and vacuously true.

**Required**: Restate the discovery clause so neutrality follows from the no-incoming-links premise directly (no link covers `a_new`, so no new match), independent of where the content is arranged; or, if the intended scenario is content *with* incoming links (resurrection, LP18), drop the "no incoming links" premise and condition on the V-position relative to `Wᵢ`.

### Issue 3: D2's arrangement-change enumeration omits K.μ⁺_L

**ASN-0107, §"Two Anchorings", D2**: the case analysis covers "Extension (K.μ⁺)", "Contraction (K.μ⁻)", "Reordering (K.μ~)".

**Problem**: A query part may resolve to link-subspace addresses — `Wᵢ` may contain link-subspace V-positions whose images are link addresses (link-to-link references, L4(c); S3★ maps such positions into `dom(Σ.L)`). The link-subspace extension `K.μ⁺_L` then alters `Qᵢ(Σ)` exactly as `K.μ⁺` does for the content subspace, yet D2 never names it. E3 correctly lists `K.μ⁺_L` among the arrangement transitions; D2's enumeration should match.

**Required**: Either extend D2's extension bullet to cover `K.μ⁺_L` (the strict-domain-extension + prior-domain-agreement argument transfers unchanged), or state explicitly that D2's `Wᵢ` is confined to the content subspace and justify that confinement.

## OUT_OF_SCOPE

### Topic 1: Independently-anchored multi-document requests
The first Open Question (three parts anchored to separately-evolving documents) is correctly deferred; the monotonicity interaction is genuinely new territory, not a gap in this ASN's single-request treatment.

### Topic 2: Coincidence of discovery and existence counts
The conditions under which every resident matching link is currently discoverable are a future-ASN concern, appropriately listed as open.

META: (not applicable — the ASN stays at the level of abstract count semantics and state-transition guarantees, not implementation mechanics)

VERDICT: REVISE
