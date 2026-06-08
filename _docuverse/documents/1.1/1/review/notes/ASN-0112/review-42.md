# Review of ASN-0112

This is a carefully constructed query specification, and the formal content holds up: I checked the V2 coverage proof in both depth cases (including the depth-divergent worked variant `origin_d = [1,1,1]`, `reach_d = [2,2]`, `extent_d = [1,2,0]`, `r⋆ = [2,2,0]`), the V3 same-depth tightness argument via `inc(w,0)`/TA5, the V6 strictness witness `w⋆ = [s_C,1,…,1,n_C+1]`, and the two wp derivations — all sound. The findings below are about accreted meta-prose, which is the flagged concern for this note.

## REVISE

### Issue 1: The `reach_d` vs `r⋆` distinction is re-litigated across five sites

**ASN-0112, V2 / V3 / V-ReachTight / worked variant / Claims table**: The single fact "the constructed endpoint `reach_d` equals the delivered span's denotational reach `r⋆` only when `#origin_d ≤ #reach_d`" is stated and re-disambiguated in: the V2 prose (two covering cases), the V3 prose (`reach_d` "not the least admissible reach over all of `T`"), the standalone V-ReachTight claim, the depth-divergent worked variant ("what lapses is V-ReachTight … V3's same-depth tightness … is intact"), and three separate table entries (V2, V3, V-ReachTight), V3's entry carrying a nested parenthetical "(which attains `reach_d` only under V-ReachTight)".

**Problem**: A reader tracking the actual reach must reconcile the same caveat restated in six places; each new slot re-defends against confusing `reach_d` with `r⋆`. This is exactly the cross-cycle accretion the anti-bloat mode targets (and the recent revise commits to "V-ReachTight wp prose and V2 table entry" show it is still churning).

**Required**: Make V-ReachTight the single home for the `reach_d` vs `r⋆` biconditional. Let V2 state coverage and cite V-ReachTight for the reach value; let V3 state its same-depth bound on `reach_d` and stop disclaiming `r⋆`; drop the parenthetical re-explanations from the table entries.

### Issue 2: Claims-table entries carry proof-method and defensive prose instead of claim statements

**ASN-0112, Claims table, V2**: "`O(d) ⊆ ⟦σ_d⟧` (coverage), **proved unconditionally via D0/D1 without assuming level-uniformity**; the actual reach `r⋆ = … ≥ reach_d = … > max O(d)` (the reach-equality condition is carried by V-ReachTight) …"
**ASN-0112, Claims table, V3**: the entry embeds "(`= #reach_d`; the deeper zero-extension `max O(d).0` is a smaller upper bound but lies at greater depth) — a bound on `reach_d`, not on the delivered span's denotational reach `r⋆` …"

**Problem**: The table is a claim summary; these entries instead record *how* the claim was proved ("via D0/D1 without assuming level-uniformity") and pre-empt a specific misreading. "Without assuming level-uniformity" is meta about the proof, not part of the claim. This is proof-rationale relocated into a structural summary slot.

**Required**: Reduce V2 and V3 to their claim statements (coverage; `origin_d` is glb and `reach_d` is the least same-depth strict upper bound of `max O(d)`). The proof method belongs in the body, not the table.

### Issue 3: Defensive "not an artifact / forced rather than incidental" framing

**ASN-0112, "Exact cover … bounding box" intro**: "the divergence is not an implementation artifact — it is forced by the demand for *one* origin-and-extent pair."
**ASN-0112, V6 prose**: "The enclosure is forced rather than incidental …"

**Problem**: The convexity-plus-separated-series argument in V6 already establishes that enclosure is forced; the "not an artifact / forced rather than incidental" clauses add insistence without adding reasoning. They are defensive residue.

**Required**: Keep the V6 convexity argument; delete the "not an implementation artifact" and "forced rather than incidental" framing clauses.

## OUT_OF_SCOPE

### Topic 1: Multi-subspace extent-to-count relationship (first Open Question)
**Why out of scope**: The dense-run count coincidence is correctly confined to the single-subspace case (V5/V12); relating extent to occupied count across the inter-subspace void is genuinely new territory and properly left to a future ASN. Noted only to confirm it is not a gap in this note.

### Topic 2: Depth-divergent reachability under editing arithmetic (fifth Open Question)
**Why out of scope**: Origin/extent behavior when V-position arithmetic is driven outside the well-formed range is downstream of this query's value semantics; deferring it is appropriate.

VERDICT: REVISE
