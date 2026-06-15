# Review of ASN-0133

I checked the core results against the foundations. Q0's abstract rebuild, Q1, Q3's Marker pattern (including the idem=⊤ dedup and born-nullified sub-cases), Q-EXT, Q5's W(σ) injection, Q5a's domain bound, and Q6's regime/case analysis are sound. The two issues below are a flawed central demonstration and an out-of-scope essay.

## REVISE

### Issue 1: The "heterogeneous" worked example R′ is single-view; the note never concretely exhibits the view-incompatibility its rebuild exists for

**ASN-0133, "Heterogeneous rewrite, worked"**: "The case Q0's rewrite is built for is the *heterogeneous-view* registry, where the per-rule conjuncts read incompatible views and the merge is not the naive one." … "so all view-sensitivity lives in the triggers, and they split." … "the lone default-view succs must be rebuilt to the audit view the rest of the term carries."

**Problem**: R′ = {ρ_walk, ρ_mark} is not heterogeneous, and its conjuncts do not read incompatible views. ρ_mark's conjunct — domain `L_obs`, trigger `¬(∃ m ∈ L_mark :: (∃ a ∈ addrs_F(c) :: a ∈ coverage_F(m)))` — reads only fixed-view audit bases (`L_obs`, `L_mark`) and V-TUP projections (`addrs_F`, `coverage_F`). By PC3 each such constituent denotes the same slice at *every* term view, so the entire ρ_mark conjunct is **view-independent**: its value is identical at audit, active, and default. ρ_walk's only view-sensitive atom is `succs` at default.

Therefore `quiescent_{R′}` is expressible at top-level view = **default** with no rebuild: ρ_walk's `succs` is UV-filtered correctly at default, ρ_mark (view-independent) evaluates correctly at default, and the two PC0-conjoin at the common view default — one PL term. So:
- "incompatible views" is false — default is a common view;
- "the merge is not the naive one" is false — the naive default merge is well-formed and correct;
- "must be rebuilt to the audit view the rest of the term carries" is false — the rest of the term is view-independent and carries no view; the audit rebuild is one valid rendering, not a forced one;
- "all view-sensitivity lives in the triggers, and they split" is false — only ρ_walk's trigger is view-sensitive; ρ_mark's is view-independent.

The root slip is treating ρ_mark's *fixed-view audit-slice read* (view-independent) as if it forced an audit term view. (The value-preservation computation at Σ* is itself correct — the rebuilt audit spelling and the default spelling both yield ∅; only the characterization is wrong.) Consequently the note proves Q0's rebuild necessary for genuinely heterogeneous registries but never concretely exhibits one — its sole "heterogeneous" instance is single-view, so the load-bearing demonstration that the rebuild is required is absent.

**Required**: Either (a) replace R′ with a genuinely view-incompatible registry — two view-sensitive constituents forced to different, incompatible views, e.g. one trigger reading `members(K, active)` (which forces active because `members` differs across all three views) conjoined with one reading `succs` at default; no single top-level view renders both, so the rebuild is genuinely required and value-preservation against the *naive default* and *naive active* merges both matter — or (b) keep R′ but state plainly it is single-view (renderable at default without rebuild), present the audit rebuild as illustrative re-spelling, and drop the "incompatible views" / "merge is not the naive one" / "must be rebuilt" / "view-sensitivity splits" claims.

### Issue 2: "Satisfiability is environment-conditional" develops the turn-fairness model the note declares out of scope

**ASN-0133, "Satisfiability is environment-conditional" (under H-SFAIR)** vs. **"What this note doesn't cover"**: the former builds out weak turn-fairness, joint turn-fairness, a scheduler-starvation counterexample, and an add-remove-around-each-turn counterexample; the latter states that "the turn/serialization model H-SFAIR's satisfiability needs … [is] operational machinery this corpus deliberately leaves at the implementation layer."

**Problem**: The paragraph develops precisely the turn-fairness/satisfiability model the scope statement defers. None of its conditions feed a theorem — Q5/Q5a/Q6 *assume* H-FAIR/H-SFAIR, never their satisfiability — and its single load-bearing output, "H-SFAIR is a distinct route from regime (i) (idleness vs cooperation)," is what Q6 uses and restates verbatim there ("two distinct routes (idleness versus cooperation), not one condition under two names"). The remaining ~80% (the two counterexamples, the weak-vs-joint turn-fairness construction) is essay on material the note itself places at the implementation layer.

**Required**: Trim to the load-bearing conclusion — H-SFAIR is a distinct sufficient route, not reducible to regime (i) — and remove or relocate the turn-fairness construction so the section no longer develops what "What this note doesn't cover" defers.

## OUT_OF_SCOPE

None to add — the note's deferrals (Open Questions 1–5, "What this note doesn't cover": scheduler, environment model, stochastic bodies, activation binding) are correctly scoped above this layer.

VERDICT: REVISE
