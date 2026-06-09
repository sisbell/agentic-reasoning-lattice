# Review of ASN-0116

I worked the algebra, the composite-validity argument, the link-survival/discoverability claims, and all three worked scenarios. The two-layer separation is clean, the K.α → K.μ⁻ → K.μ⁺ → K.ρ decomposition discharges its intermediate-state preconditions correctly, the range identity (RAN) drives J0/J1★/J1'★ soundly, and IP6's weakest precondition is genuinely non-trivial (containment, not emptiness) with the worked "IP6 trap" numbers checking out. The boundary care at `k = 0` (OrdShiftHom needs `n ≥ 1`, so `shift(p,0) = p` falls back to the precondition) is exactly right. The technical core is, to my reading, correct.

The findings below are modest and live at the prose/coverage level, not the mathematics.

## REVISE

### Issue 1: Clause-2 discharge is forward-deferred three times to the same location
**ASN-0116, "INSERT as a valid composite"**: the section repeats, in three separate paragraphs, that the coupling constraints are checked only at the boundary and proved later — "we discharge clause 2 at the boundary below"; "the coupling constraints (clause 2) are checked only at the composite boundary, discharged in the provenance section below"; "with clause 1 verified step-by-step and clause 2 at the boundary, INSERT is a valid composite."
**Problem**: This is the flagged accretion pattern — multiple paragraphs deferring to one downstream location (the provenance section's J0/J1★/J1'★ discharge). The three restatements add no reasoning; a reader following the clause-1 verification has to skip past the same forward pointer repeatedly.
**Required**: State once, at the section's close, that clause 1 is verified here and clause 2 is discharged in the provenance section; delete the two redundant restatements.

### Issue 2: Filler paragraph stating that S8★ "carries no obligation"
**ASN-0116, "Per-subspace run decomposition"**: "S8★ ... holds at the filled post-state directly by ExtendedReachableStateInvariants ... It is a post-state invariant, not a precondition of any composite step, so it carries no INSERT-specific obligation."
**Problem**: This is "why the work isn't needed" meta-prose rather than reasoning that advances the argument — the second sentence explains the absence of an obligation, which is degrade-around noise.
**Required**: Compress to the single load-bearing citation (S8★ holds at the post-state by ExtendedReachableStateInvariants, ASN-0047); drop the obligation-disclaimer sentence.

### Issue 3: Worked example omits the front-insertion (J=1) into a non-empty document
**ASN-0116, "A worked insertion"**: the example covers interior (`J=3`), append (`J=N+1`), and empty subspace (`V_S(d)=∅`).
**Problem**: The prose specifically distinguishes the front-insertion-with-suffix case as the path where K.μ⁻ fires with `n'_{s_C}=0` and clears the entire content subspace — "distinct from the append case (where K.μ⁻ is dropped) and the empty subspace (where there is no suffix to shift)." This is the genuine "first" boundary (insert before all existing content of a non-empty document), and it is the only branch exercising the `n'_{s_C}=0` strict-contraction precondition. The empty-subspace example is `J=1` but trivial (no suffix moves), so it does not exercise this path.
**Required**: Add a short worked instance — e.g., insert `XY` at `p = q_1` into the `N=5` document — verifying that K.μ⁻ clears `V_{s_C}(d)` (retain count 0, strict contraction `0 < 5`) and K.μ⁺ reinstalls `{q_1,…,q_7}` with `min(V_S(d')) = q_1` (D-MIN★).

## OUT_OF_SCOPE

### Topic 1: Insertion at a transclusion-shared V-position; concurrent-insertion freshness; transclusion provenance; post-edit fragmentation
**Why out of scope**: These are exactly the four Open Questions the ASN already files for future ASNs (transclusion = ASN-0118, concurrency, provenance-of-transcluded-content, fragmentation under later editing). Correctly deferred, not errors here.

VERDICT: REVISE
