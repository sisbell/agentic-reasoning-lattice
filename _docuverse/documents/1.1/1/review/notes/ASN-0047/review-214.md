# Review of ASN-0047

This is a heavily-developed ASN and the core arguments — the D-SEQ★ derivation, the K.μ~ link-subspace fixity proof, GlobalLineage, the K.δ allocator-dispatch tree — are rigorous. I checked the boundary cases the rubric demands (full-document clearance via K.μ⁻ with all `n'_S = 0`; empty-arrangement fork reducing to ex nihilo; first/subsequent emission freshness; empty `e₁`/`e₂` endsets) and found them handled. The findings below are localized: one incorrect justification in a worked example, and two instances of the forward-reference/use-site accretion the `review-mode.anti-bloat` classifier solicits.

## REVISE

### Issue 1: Fork worked example justifies S8-depth by appeal to the source document
**ASN-0047, *Worked example: fork with subsequent insertion*, K.μ⁺ step**: "The V-positions [1,1] and [1,2] satisfy S8a (all components strictly positive, zeros = 0) and S8-depth (uniform depth 2 within subspace s_C, *matching the pre-existing arrangement of d₁*)."

**Problem**: The parenthetical reasoning is wrong. S8-depth is a per-(document, subspace) uniformity property: it constrains `V_{s_C}(d₂)` to share a common depth *among d₂'s own positions*, not to match `d₁`'s depth. `d₂` is freshly created with `M₂(d₂) = ∅`, so its content-subspace depth is re-pinned from scratch by the first insertion (`ValidFirstInsertionPosition`) at *any* value `m ≥ 2` (S8a) — the transclusion copies `d₁`'s I-addresses, not its V-position depths. The justification as written contradicts the design freedom the ASN itself reserves in its first Open Question ("must it be identical, or may it be a proper subset?"), implying forks must inherit the source's V-structure.

**Required**: Drop "matching the pre-existing arrangement of d₁." S8-depth holds because the two new positions `[1,1]`, `[1,2]` share depth 2 among themselves; the depth is `d₂`'s own free choice ≥ 2, independent of `d₁`.

### Issue 2: Derivation prose in the Notation slot
**ASN-0047, *Notation*, "Subspace-position correspondence"**: "For `v ∈ dom(M(d))` with `M(d)(v) = a`, `subspace(v) = subspace_I(a)` (S3★ + L0). The equality is a two-step chain: S3★ routes the value to the correct store by subspace … (S3★ alone yields only store *membership*, not equality of subspace identifiers; L0 supplies the second step.)"

**Problem**: A notation section should fix one notation per concept and point to its defining ASN. This entry instead carries a multi-sentence derivation (a two-step S3★/L0 argument plus a parenthetical defending why one premise alone is insufficient) of a *result* whose premises (S3★, L0) are not even introduced until later in the body. This is essay/derivation content occupying a structural slot, and it forward-references definitions the reader has not yet seen.

**Required**: Reduce to the notation fact and a pointer (e.g., "`subspace(v) = subspace_I(a)` for `M(d)(v) = a`; see S3★ + L0"). Move the two-step derivation and the defensive parenthetical to the S3★/L0 discussion in the body, or delete it if the chain is restated there (it largely is, under *Generalized referential integrity*).

### Issue 3: Use-site inventories enumerating downstream consumers in the Properties tables
**ASN-0047, *Properties Introduced***, two rows:
- *Local extensions* table: "K.α's `E(a)₁ = s_C` precondition (inherited) | Pins `subspace_I(a) = s_C`, **cited downstream to preserve L0's C-clause and L14** in the extended state."
- *Inherited from foundation* table, C-fin: "**Load-bearing for K.α's subsequent-emission case formula** `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)` — the indexed set is a subset of the finite `dom(C)`, so `max` is well-defined…"

**Problem**: Both rows describe *where the property is consumed downstream* rather than stating the property. This is the use-site-inventory pattern the anti-bloat classifier flags: the consumer list (L0's C-clause, L14, K.α's `max`-well-definedness) belongs at the consuming site, where the discharge already cites the premise, and rots if those sites are renamed or restructured. The table entries should carry the statement and its source, not a manifest of dependents.

**Required**: Trim each row to the property statement and foundation source. The consuming sites (L0/L14 matrix cells; K.α's subsequent-emission precondition) already cite these premises, so the inventory is redundant.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The fork composite (J4) deliberately starts the forked document's link subspace empty and notes "A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope." This is correctly deferred — it is new operational territory, not a gap in the present transition taxonomy.

### Topic 2: Concurrency and address-space exhaustion
The Open Questions on serialization of concurrent allocations under a shared home document, and on link-allocation failure due to exhaustion, are genuinely future work. They depend on a concurrency model and a finiteness/quota model this ASN does not (and per its scope list, should not) introduce; T0(a)/T0(b) guarantee unbounded address space at the abstract level, so exhaustion is an implementation concern.

VERDICT: REVISE
