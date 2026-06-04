# Review of ASN-0087

## REVISE

### Issue 1: The "state-determined" conclusion about `v_ℓ` is asserted repeatedly across sections

**ASN-0087, Inputs / M-DepthConv**: The *Inputs* lead-in states "the V-position `v_ℓ` is derived from the current state together with the canonical-depth convention M-DepthConv below — its serial component fixed by the link subspace's current cardinality, its depth fixed per M-DepthConv." The M-DepthConv paragraph then closes with "so every subsequent `v_ℓ` MAKELINK places *is* fully state-determined."

**Problem**: Both sentences land on the same conclusion (`v_ℓ` is not a parameter; it is computed from `Σ`). The closing clause of M-DepthConv is rationale prose restating the lead-in's point — it explains *why* the convention matters rather than adding content. This is the "two paragraphs say the same thing" / rationale-accretion pattern the anti-bloat pass targets.

**Required**: Keep M-DepthConv's object-level statement (MAKELINK commits to minimal `m = 2`; S8-depth then pins `m_L(d) = 2`) and delete the trailing "so every subsequent `v_ℓ` … is fully state-determined" clause; let the *Inputs* lead-in carry the state-determinacy observation once.

### Issue 2: `v_ℓ`'s derivation rule is spelled out in four places

**ASN-0087, Inputs, Preconditions, Effect, and M-Pre**: The serial-component-plus-depth rule for `v_ℓ` appears in the *Inputs* lead-in ("serial component fixed by … current cardinality, depth fixed per M-DepthConv"), in *Preconditions* ("`v_ℓ` determined by the link subspace's current cardinality (serial component `n_L + 1` …) together with its depth per M-DepthConv"), in *Effect* (the empty/non-empty case split), and again in the M-Pre claim row ("`v_ℓ` from K.μ⁺_L's positioning rule, serial component `n_L + 1` computed from `Σ`, depth per M-DepthConv").

**Problem**: *Effect* is the rule's natural home (it states the actual positioning) and M-Pre's claim row is the summary; the *Inputs* and *Preconditions* prose restate the computation a third and fourth time. Converging repetition of one mechanical rule.

**Required**: State the `v_ℓ` computation once in *Effect*; reduce the *Inputs* and *Preconditions* mentions to "`v_ℓ` is system-derived (see *Effect*)" without re-deriving the serial/depth components.

## OUT_OF_SCOPE

(none — MAKELINK mechanics are in scope; references to K.μ~/K.μ⁻ in *Permanence of the Binding* are legitimate output-permanence analysis, not reordering/contraction mechanics.)

VERDICT: REVISE
