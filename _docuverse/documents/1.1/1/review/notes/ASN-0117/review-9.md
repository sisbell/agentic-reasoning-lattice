# Review of ASN-0117

## REVISE

### Issue 1: The K.μ⁻ + K.μ⁺ composite decomposition fails when the suffix is empty (R = ∅)

**ASN-0117, "DELETE(`d`, `p`, `w`)" Effect**: "DELETE is instead the foundation *composite* of two atomic transitions ... a **K.μ⁻** step ... [and] a **K.μ⁺** step that re-places the `N − c − (J − 1)` survivors at the closed-up text positions `{q_J, …, q_{N−c}}`."

**Problem**: The Effect uniformly claims DELETE is the two-step K.μ⁻ + K.μ⁺ composite. But when `R = ∅` — the suffix-delete case `J + c = N + 1` and the delete-everything case `J = 1, c = N`, both of which the ASN treats as worked examples — there are zero survivors to re-place: `N − c − (J − 1) = 0`. The K.μ⁺ step would then add no mappings. K.μ⁺ (ASN-0047, ArrangementExtension) carries the *strict-extension* precondition `dom(M'(d)) ⊃ dom(M(d))`, so an empty K.μ⁺ is not a valid transition. The uniform composite claim therefore has no realization for `R = ∅`.

Note this is exactly where the second step is unnecessary: when `R = ∅`, the survivors are precisely `L = {q_1, …, q_{J−1}}` at their *original* positions (`N − c = J − 1`), which is exactly a prefix-retention K.μ⁻ (retention count `n'_{s_C} = J − 1`) with no re-placement. So the correct statement is a case split: DELETE = K.μ⁻ alone when `R = ∅`, K.μ⁻ + K.μ⁺ when `R ≠ ∅`.

**Required**: Replace the uniform "composite of two atomic transitions" framing with the `R = ∅` / `R ≠ ∅` case split. For the `R = ∅` branch, state DELETE as a single K.μ⁻ transition (which is self-sufficient under J2, ContractionIsolation), and confirm the coupling/frame discharge for that single-step realization.

### Issue 2: The R = ∅ worked examples are inconsistent with the stated Effect

**ASN-0117, "A worked deletion"**: "**Boundary — suffix delete (`J + c = N + 1`)** ... No position is shifted (DEL-SHIFT vacuous)" and "**Boundary — delete everything (`J = 1`, `c = N`)** ... `V_S(d') = ∅`, the empty arrangement."

**Problem**: Both boundary examples have `R = ∅` and are checked directly against the D-clauses, but they silently rely on a single-step (K.μ⁻-only) realization that the Effect section never licenses — the Effect insists DELETE "is the foundation composite of two atomic transitions." P2 (GapClosure) already acknowledges the `R = ∅` case ("the positional reading is vacuous"), so the document is internally inconsistent: P2 and the examples treat `R = ∅`, but the operational decomposition does not. This is the same root as Issue 1 and must be reconciled in both places.

**Required**: Once the case split of Issue 1 is in place, annotate these two worked examples with the K.μ⁻-only realization and confirm the invariant-preservation appeals (S3★, DEL-FENT, DEL-FPROV, P4★, P7a) hold for the single-step case.

## OUT_OF_SCOPE

### Topic 1: Deletion in the link subspace
The precondition fixes `S = subspace(p) = s_C`, so DELETE removes only text-subspace content. Withdrawing a link's V-position from a document's arrangement (subspace `s_L`) is a distinct editing operation and belongs in a future ASN, not here.

**Why out of scope**: The question asks about content deletion; link-arrangement management is separate territory, not an error in this ASN.

### Topic 2: Deletion at element-field depth m ≥ 3
The operation is stated at `m = #p = 2`, inheriting the depth-2 restriction of the cited contraction (ASN-0082 D-SHIFT). Generalizing the left-shift displacement to deeper text subspaces is future displacement-algebra work.

**Why out of scope**: The restriction is correctly inherited from the cited basis; deeper-depth deletion is new territory.

VERDICT: REVISE
