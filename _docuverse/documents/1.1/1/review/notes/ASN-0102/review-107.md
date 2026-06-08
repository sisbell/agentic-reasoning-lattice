# Review of ASN-0102

## REVISE

### Issue 1: X15 overclaims that COPY's atomicity is "forced" — false for the append and empty-subspace cases

**ASN-0102, X15 (Atomicity)**: "This atomicity is *forced*, not chosen — no multi-step decomposition of COPY is admissible."

**Problem**: The forcing derivation relies entirely on the displaced region producing an intermediate V-gap: "That hole violates D-CTG★ … both of which … demands of *every* state … whenever content is displaced (`p ≤ n_S`) and `W ≥ 1`." But the precondition admits two cases the derivation never revisits, in which **no content is displaced**:

- *Append* (`p = n_S + 1`): the freed region is empty, the copied region extends the tail at `[n_S+1, n_S+W]`. Filling those positions one at a time — `[1,n_S+1]`, then `[1,n_S+2]`, … — keeps `V_{s_C}(d)` contiguous from the minimum at *every* intermediate state (D-CTG★/D-SEQ★ hold), and S2 is never threatened because no position is ever double-bound.
- *Empty subspace* (`n_S = 0`, `p = 1`): identical — the copied positions `[1,1], …, [1,W]` extend an empty subspace contiguously.

In both cases COPY coincides with a contiguous tail extension and is expressible as a valid composite (e.g. one or more `K.μ⁺` extensions followed by the provenance recording, with J1★/J1'★ evaluated initial-to-final). No intermediate state violates a per-state invariant, so `ValidComposite★` clause (1) *is* satisfiable by a decomposition. The blanket claim "no multi-step decomposition is admissible" is therefore false precisely on the boundary cases the ASN otherwise takes care to exhibit (the append and empty-subspace worked examples).

(Separately, the reverse-order argument's phrase "would require two `s_C`-positions to share a last component, violating S2" is imprecise — the actual obstruction is that filling `[v, v+W)` while `[v, n_S]` is still occupied overwrites/loses the displaced binding at a single key, not that two positions share a component. This should be restated.)

**Required**: Restrict the forcing claim to the displacing case (`p ≤ n_S ∧ W ≥ 1`), where the intermediate gap genuinely makes every decomposition inadmissible. For the append (`p = n_S+1`) and empty-subspace (`n_S = 0`) cases, state plainly that COPY coincides with a contiguous extension whose step-by-step or single-`K.μ⁺` realization preserves all per-state invariants, so modeling it as one elementary transition is a *choice* (justified by uniformity with the displacing case), not a forced consequence. Fix the reverse-order S2 wording.

## OUT_OF_SCOPE

### Topic 1: Re-displacement / continued discoverability of copied content
**Why out of scope**: The first open question (what ties origin to discoverability when copied content is later displaced) is downstream operation/projection territory (ASN-0098 family), not a COPY-internal obligation. Correctly left as an open question, not a claim.

VERDICT: REVISE
