# Review of ASN-0133

This is a careful, self-aware note — it names its hypotheses, separates registration-checkable from meta-level conditions, and correctly identifies several places where folklore (no-retraction-implies-flip-once, H-W as a route) is unsound on the shipped machinery. Q0/Q1 (recognizability, absorption), Q5/Q5a (the bound), Q-EXT, and Q-FLIP all check out against ASN-0086/0126/0128/0129. I found one substantive error, and it sits on the note's own headline claim.

## REVISE

### Issue 1: REACHING quiescence (non-grow-only) is wrongly attributed to weak fairness; Q6's case analysis omits bounded out-of-phase cycling

**ASN-0133, "What this note commits" (Conditional termination) and Worked composition (Quiescence):**
- Summary: "Quiescence is then **reached** after finitely many real fires under H-RF and the fairness hypothesis (H-FAIR); **holding** it is environment-conditional"
- Worked example: "**reached** after finitely many real fires given a bounded flagged population and any fair scheduler, … the producer (non-grow-only domain) **holding** once the environment stops re-flagging uncommented targets, or under strong fairness (H-SFAIR, Q6)."

**Problem.** Both passages split *reaching* (attributed to H-RF + weak H-FAIR + bounded growth) from *holding* (attributed to H-SFAIR / environment-idle, for non-grow-only). That split is false: for a non-grow-only registry, **reaching** a quiescent state needs the same H-SFAIR-or-environment-idle hypothesis as holding it. A weak-fair scheduler facing an environment that cycles finitely many trigger-true arguments out of phase reaches *no* quiescent state, with H-RF, bounded growth, and weak H-FAIR all satisfied.

Concrete counterexample (the note's own producer `ρ_P`, domain `{t ∈ M_tgt : is_attn(t)}` at active view, `T_P` an SF audit-spelling):

- Environment flags two targets `t1, t2` via `attn`, deposits no `cmt`; the scheduler issues **zero** fires (every trigger-true target is removed by the environment before it would fire, so weak H-FAIR is discharged by *removal*, not firing — exactly what H-FAIR permits).
- The environment keeps "≥1 of `{t1,t2}` flagged-and-uncommitted at every state" by re-flagging one *before* unflagging the other (overlap, no all-empty gap).
- Then **H-RF holds** (zero real fires), **bounded growth holds** (`⋃_k [D_{ρ_P}] = {t1,t2}`), **weak H-FAIR holds** — yet **no state is quiescent** (`T_P` true on the standing uncommitted target). Quiescence is not reached.
- H-SFAIR forbids this σ (`t1, t2` are each trigger-true at infinitely many indices and never fired) and forces their commits, reaching quiescence. So reaching here is exactly an H-SFAIR fact, not a weak-H-FAIR fact.

Note this is consistent with the note's own closed-case observation ("`{t ∈ M_tgt : is_attn(t)}` static … terminates unconditionally under fairness"): it is precisely the environment's power to *remove* an argument before firing that breaks reaching, and that is a non-grow-only/open-model phenomenon — the same phenomenon the note correctly assigns to *holding* but not to *reaching*.

**Root cause — Q6, "Where neither regime applies":** "an environment **alternating fresh** trigger-true arguments … keeps every state non-quiescent — quiescence not even reached — while an environment **oscillating one** non-grow-only argument's domain membership … quiescent only in the gaps." This dichotomy treats the only bounded obstruction to reaching as *single-argument* oscillation (which does leave gaps). It omits the bounded **multi-argument out-of-phase cycling** case above, which has no gaps and is not "fresh" (the arguments are a fixed finite set, re-presented). Because bounded growth excludes "alternating *fresh*" (that needs unboundedly many distinct arguments), the case split as written wrongly implies that under bounded growth the worst case is "gaps" — i.e., reached intermittently. That is what licenses the incorrect reached/held split in the summary and worked example.

(Q6's *top-level statement* is, by contrast, accurate: "the non-grow-only domains being where an environment hypothesis remains." The defect is the detailed case analysis and the two prose summaries built on it.)

**Required.**
1. Correct the summary and worked example so that, for non-grow-only registries, **reaching** (not only holding) is conditioned on H-SFAIR or environment-idle; weak H-FAIR + bounded growth delivers only the *registry-side* guarantee (finitely many real fires, registry-inert past N), not a reached quiescent state.
2. Extend Q6's "neither regime applies" analysis with the third obstruction — bounded out-of-phase cycling of finitely many trigger-true arguments — and show it defeats reaching under weak H-FAIR while satisfying H-RF and bounded growth, with H-SFAIR as the closing hypothesis. The grow-only sub-case is unaffected (removal is impossible, so weak H-FAIR collapses to firing, and reaching+holding both follow — keep that as the clean contrast).

## OUT_OF_SCOPE

### Topic 1: A scheduler discharging H-FAIR / H-SFAIR
The note correctly defers scheduler construction and fairness proofs ("What this note doesn't cover"). Issue 1 sharpens the requirement the deferred scheduler must meet — non-grow-only coordination needs a *strongly*-fair discipline (priority-with-aging across recurrences) to reach quiescence, not merely weak fairness. Building and proving such a scheduler belongs to the operational layer, not here.

### Topic 2: A formal stratification termination theorem
Stratification appears only as a heuristic (H-W discussion, worked example's repair) with the honest caveat that per-stratum bounds are themselves a decomposition of H-RF. A genuine stratified-registry termination theorem (legality condition "no emission enlarges a strictly lower stratum's domain," plus its discharge) is future work, not a gap in this note's stated scope.

### Topic 3: The `pd_extinct` (SF) certificate class
Q-EXT/Q5a make SF membership the load-bearing *uncertified* registration check; the note's Open Question 1 already routes the actual designated-class specification to a future ASN extending ASN-0130. Correctly deferred.

VERDICT: REVISE
