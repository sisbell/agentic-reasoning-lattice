# Review of ASN-0133

I checked the proofs in Q0 (PL-membership, including the heterogeneous-view rewrite and the `chain`/`elems` handling), Q1, X-DEF/Q3 (the Marker pattern and its idem=⊤ dedup-hit subtlety), Q-EXT, Q5/Q5a (the injection bound and the closed-case degeneracy), Q6 (all three regimes plus the holding-failure and reaching-failure counterexamples and their closure by H-SFAIR's regime form), and the scope section's S-monotonicity argument. The worked composition's class check, extinction discharge, acyclic-coupling argument, cyclic counterexample, and the Σ₀→Σ₁→Σ₂ terminal-state trace all check out. The mathematics is sound. One anti-bloat item remains.

## REVISE

### Issue 1: H-FAIR's real-fired-discharge sentence restates a point already made and forward-references H-RF
**ASN-0133, H-FAIR (FairnessHypothesis)**: "The real-fired discharge is *effective* — it consumes the occurrence's trigger — only under extinction discipline, which forces the post-state falsification (X-DEF); a *vacuous* real fire, advancing neither, would re-arm its trigger at once, but H-RF excludes any loop of them, each iteration being a real fire."

**Problem**: Two sentences earlier the same paragraph already establishes the decoupling from consumption — "'Fired' here means real-fired … decoupled from both state-change and trigger-consumption … a fire of a non-extinction-disciplined rule need not falsify its own trigger." The flagged clause "effective … only under extinction discipline" is that identical fact re-spelled in the positive direction (extinction discipline ⟺ a real fire falsifies its own trigger). The remaining clause — "a vacuous real fire … but H-RF excludes any loop of them" — forward-references H-RF, which is not defined until two hypotheses later in the same section, and previews the H-RF-necessity argument that Q6 already delivers in full: "drop H-RF and rules can re-arm each other forever, each re-fire a fresh real fire without bound." Neither clause advances H-FAIR's definition (every trigger-true occurrence discharged one of three ways); a reader following the definition skips past both. This is the forward-reference accretion in an axiom slot that the note's anti-bloat classifier targets.

**Required**: Drop the sentence. Its consumption-decoupling content is already stated in the same paragraph; its H-RF-necessity content belongs to — and is present in — Q6's proof.

## OUT_OF_SCOPE

None. The deferred topics (scheduler construction, stochastic rule bodies, activation binding, environment model) are correctly placed in "What this note doesn't cover," and Open Questions 1–5 are genuine future work rather than gaps in this note.

VERDICT: REVISE
