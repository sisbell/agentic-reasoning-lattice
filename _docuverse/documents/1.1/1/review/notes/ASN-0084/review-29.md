# Review of ASN-0084

## REVISE

### Issue 1: m_1 = 2 attributed to ASN-0036 but not established there

**ASN-0084, "State and Vocabulary"**: "By the subspace declarations of ASN-0036, the text subspace has depth m_1 = 2, so by S8-depth, every V-position v ∈ V_1(d) satisfies #v = 2 (ordinal depth 1)."

**Problem**: ASN-0036's S8-depth establishes only `m_s ≥ 2` for any subspace, and ValidFirstInsertionPosition explicitly leaves m operator-chosen ("The specific value of `m` beyond the bound `m ≥ 2` is not fixed by the strand model"). The text-subspace depth is therefore not stipulated to be 2 by ASN-0036. This claim is factually incorrect about the foundation.

The depth-2 restriction is load-bearing throughout the ASN: (a) the entire "Identification of singleton tumblers with natural numbers" section requires ord(v) to be a singleton; (b) all arithmetic on cut ordinals (`ord(c₀) + j`, `ord(c₂) − ord(c₁)`) presumes singleton identification; (c) the canonical decomposition argument uses NAT-add/sub on ord values rather than TumblerAdd/Sub. If m_1 > 2, the ASN cannot proceed without substantial reformulation.

**Required**: Replace the unjustified attribution with an explicit assumption — e.g., "We further restrict to documents where the text subspace has been initialized with the minimum depth m_1 = 2 permitted by S8a; documents with m_1 > 2 are outside the scope of this ASN." This makes the load-bearing assumption visible at the precondition level rather than buried as a misattribution.

### Issue 2: R-WP postcondition is trivially true

**ASN-0084, R-WP**: "Let Q be the post-condition 'M'(d) admits a correspondence-run partition' — equivalently, S8(a) and S8(b) hold for M'(d) on V_S(d). Then `wp(REARRANGE_C, Q) ⇐ R-PRE(C) ∧ (M(d) admits a correspondence-run partition)`"

**Problem**: Q is trivially satisfied by any finite arrangement — singleton runs `(v, M'(d)(v), 1)` always satisfy S8(a) and S8(b). The pre-state S8 hypothesis and R-PRE are not load-bearing for the conclusion; the implication is vacuously true. The proof body exhibits B' via R-BLK, which is a meaningful constructive result, but that is R-BLK's content, not a new wp statement. The labelled "Weakest-Precondition Computation" section therefore does no analytical work beyond R-BLK.

**Required**: State a non-trivial wp. Candidates: (a) wp for "the post-state canonical partition has at most |B| + 2·n_cuts maximal runs" (constraining the post-state shape); (b) wp for "any I-adjacency `M(d)(v₁) + 1 = M(d)(v₂)` with v₁, v₂ in the same region is preserved as `M'(d)(π(v₁)) + 1 = M'(d)(π(v₂))`" (characterizing what R-BLK Phase 3 preserves); (c) wp for the conjunction of all ASN-0036 invariants the rearrangement must maintain (making the Invariant Preservation paragraph weakest-precondition-shaped). The current statement should either be strengthened or relabelled as a corollary of R-BLK rather than a wp computation.

## OUT_OF_SCOPE

### Topic 1: Documents with m_1 > 2
**Why out of scope**: Generalizing the cut-sequence arithmetic from singleton ord to multi-component ord (using TumblerAdd/Sub instead of NAT-add/sub) is a separate exercise. This ASN should be explicit that it restricts to m_1 = 2 rather than implicitly assume it.

### Topic 2: Compositions of multiple rearrangements
**Why out of scope**: Acknowledged in Open Questions. Sequential REARRANGE operations and whether they compose to a single rearrangement is a distinct concern.

### Topic 3: k-cut rearrangements for k > 4
**Why out of scope**: Acknowledged in Open Questions. The natural generalization beyond pivot/swap is a separate ASN.

### Topic 4: Bounds on canonical run count after rearrangement
**Why out of scope**: R-BLK explicitly defers characterization of which pre-state run pairs produce post-state mergeability. Bounding the resulting run count requires the deferred analysis.

### Topic 5: Cross-subspace rearrangement
**Why out of scope**: CS3 confines all cuts to subspace 1. Operations that move content between subspaces (text ↔ link) are a different primitive.

VERDICT: REVISE
