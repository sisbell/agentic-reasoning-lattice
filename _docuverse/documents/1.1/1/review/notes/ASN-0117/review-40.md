# Review of ASN-0117

The ASN's technical core is sound. I checked the composite realisation against K.μ⁻/K.μ⁺'s preconditions (strict contraction `J − 1 < N`; strict extension `N − c − (J − 1) ≥ 1` exactly when `R ≠ ∅`; placement images in `dom(C)` via S3★; D-CTG★/D-MIN★ at the rebuilt run), the coupling discharges (J0, J1★, J1'★ all vacuous or one-directional as claimed), the range identity `ran(M'(d)) = ran(M(d)) \ A_del^{excl}` (verified by direct set computation; the SD appeal correctly protects the `s_L` images), the wp's per-link existential (correctly weakest — a per-slot universal would be merely sufficient), and the arithmetic of every worked example (`σ(q_5) = q_3`, the three-position uniform shift, the `n'_{s_C} = 0` boundary, the suffix-delete vacuity of D-SEP(b)). All check out. Three items remain.

## REVISE

### Issue 1: undefined label "F0"
**ASN-0117, "Invariants the operation must preserve" (cross-document isolation paragraph)**: "This is the F0 cross-document frame the evidence confirms structurally — DELETE resolves exactly one document's arrangement and reaches no other (Q17)."
**Problem**: `F0` is a label that appears nowhere else in this ASN and in none of the foundation ASNs (the cross-document frame is named D-CD in ASN-0082 and DEL-FDOC here). A self-contained specification cannot use a claim label it never introduces; as written, the reader must guess whether F0 is a consultation artifact, a sibling-ASN label, or a typo.
**Required**: Either drop the label ("This is the cross-document frame the evidence confirms structurally…") or, if F0 is the consultation's own designation, gloss it as such with its citation.

### Issue 2: within-document sharing example silently forces `a_2 = a_5`
**ASN-0117, "A worked deletion" (Within-document sharing)**: "Suppose additionally `M(d)(q_2) = a_5` — `d` arranges the content `a_5` at *two* positions."
**Problem**: The base scenario fixes `M(d)(q_k) = a_k` for `k = 1, …, 5`. By S2 (ArrangementFunctionality), `q_2` has exactly one image, so "additionally `M(d)(q_2) = a_5`" is not an additional mapping — it is the stipulation `a_2 = a_5`, which is consistent only because the `a_k` were never declared distinct. As worded, the example reads as adding a second image to `q_2`, which S2 forbids. The downstream computation (`A_del^{excl} = ∅` because `a_5 ∈ M(d)(L ∪ R)` via `q_2`) is correct under the `a_2 = a_5` reading, but the reader has to repair the setup to reach it.
**Required**: State the stipulation explicitly — e.g., "modify the scenario so that `a_2 = a_5`, i.e. the images of `q_2` and `q_5` coincide (the `a_k` were not assumed distinct); `d` then arranges the content `a_5` at two positions" — so the example visibly respects S2.

### Issue 3: J1★ parenthetical defends a case the predicate already excludes
**ASN-0117, "Effect" (coupling paragraph)**: "(J1★ asks only that the post-state range introduce nothing new; what *leaves* the range — exactly `A_del^{excl}` of the wp section below, under within-document sharing a possibly proper subset of `A_del` — plays no part in the discharge.)"
**Problem**: J1★'s trigger conjunct, quoted immediately before, is already one-directional — departures from the range cannot fire it, so the parenthetical defends against a misreading the formula does not admit. It also pulls wp-section content (`A_del^{excl}`, the sharing qualification) forward into the coupling discharge, where it does no work; that material is fully developed in its proper place. This is the defensive-justification / forward-deferral pattern flagged for this review mode.
**Required**: Delete the parenthetical, or reduce it to its first clause if the directional reminder is judged load-bearing; the `A_del^{excl}` identification belongs solely to the wp section.

## OUT_OF_SCOPE

### Topic 1: DELETE at text-subspace depths m > 2
**Why out of scope**: The precondition fixes `m = #p = 2`, matching the depth-2 scope of the foundation contraction (ASN-0082's `#p = 2` precondition). A general-depth deletion has no foundation displacement to instantiate and would be new territory, not a defect here.

### Topic 2: de-arranging link-subspace positions
**Why out of scope**: DELETE is fixed to `S = s_C`. Contracting a document's link subspace (withdrawing a link placement) is admitted by K.μ⁻'s vocabulary but is a distinct operation with its own discoverability semantics, properly a future ASN.

### Topic 3: totalization, concurrency, backtrack reconstructibility, discovery indexing
**Why out of scope**: Already correctly deferred by the ASN's own Open Questions; none is an error in the present operation.

VERDICT: REVISE
