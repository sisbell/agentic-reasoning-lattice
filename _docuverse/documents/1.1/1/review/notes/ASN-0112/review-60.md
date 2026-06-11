# Review of ASN-0112

This ASN is in strong shape. The span construction is fully discharged (T12 legality split correctly on endpoint depths; D0/D1 preconditions checked at every application), the V5/V6 dichotomy is now carried by the occupied-depth notion rather than bare strict inclusion, the V9a injectivity argument exhibits an explicit inverse with a correct width-final-component case discriminator, and the four worked configurations (cross-subspace equal-depth, content-only, `m_C > m_L`, `m_C < m_L`) exercise all reachable quadrants of the V-ReachTight/V-LevelUniform square. I verified the arithmetic in the worked report, the depth-divergent variant, and the mirror variant against TumblerSub/TumblerAdd componentwise; all check out, including `extent = [1,2,0]` with overshoot `r⋆ = [2,2,0]` and the mirror's closing round-trip `[1,1] ⊕ [1,1,2] = [2,1,2]`. One precision defect remains.

## REVISE

### Issue 1: The mirror variant misstates the uniqueness of the decoupling regime
**ASN-0112, "A worked report" (mirror variant paragraph)**: "When `m_C = 2 < m_L = 3` — the one regime where V-ReachTight and V-LevelUniform decouple"

**Problem**: By the ASN's own biconditionals, the tight-reach property holds iff `#origin_d ≤ #reach_d` (V-ReachTight) and level-uniformity holds iff `#origin_d ≥ #reach_d` (V-LevelUniform). The two properties therefore come apart in *both* unequal-depth regimes, not one: at `m_C > m_L` the reach overshoots while the span is level-uniform (`#extent_d = #origin_d` — exactly the depth-divergent variant one line earlier, where the ASN itself notes "what lapses is V-ReachTight"), and at `m_C < m_L` the reach is tight while level-uniformity fails. Calling the mirror "the one regime where V-ReachTight and V-LevelUniform decouple" is false on the natural reading of "decouple" (truth values differing). What is actually unique about the mirror regime is the specific combination *tight reach with non-level-uniform span* — the `(Tight, ¬LU)` quadrant — which the closing parenthesis ("the non-level-uniform quadrant") gestures at correctly. The sentence and the parenthesis are in tension.

**Required**: Reword the dash clause to state the unique fact, e.g. "the one regime where V-ReachTight holds while V-LevelUniform fails" (or "where a tight reach coexists with a non-level-uniform span"). Alternatively state that the properties decouple in both unequal-depth regimes and that the mirror realizes the remaining quadrant — the `(¬Tight, ¬LU)` combination being impossible since `#origin_d > #reach_d` and `#origin_d < #reach_d` exclude each other.

## OUT_OF_SCOPE

### Topic 1: Cross-subspace extent-to-count invariant and historical-version reporting
**Why out of scope**: Both are already correctly deferred by the ASN's own Open Questions (the multi-subspace count question and the version-faithfulness question), and per-subspace exact reporting is explicitly assigned to RETRIEVEDOCVSPANSET / ASN-0113 by the scope list. Nothing further to relocate.

VERDICT: REVISE
