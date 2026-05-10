# Review of ASN-0081

## REVISE

### Issue 1: Local axioms VD, VP, VC duplicate foundation properties

**ASN-0081, Local Axioms**: "VD — UniformVPositionDepth (AXIOM, local)… VP — PositiveSubspace (AXIOM, local)… VC — SubspaceContiguity (AXIOM, local)"

**Problem**: All three are established in ASN-0036 and should be cited, not reintroduced:

- VD = S8-depth (FixedDepthVPositions): `(A d, v₁, v₂ : v₁ ∈ dom(M(d)) ∧ v₂ ∈ dom(M(d)) ∧ (v₁)₁ = (v₂)₁ : #v₁ = #v₂)`
- VP is a sub-property of S8a (VPositionWellFormedness): `zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0` — strictly stronger than VP
- VC = D-CTG (VContiguity), stated with a closed interval (`v₁ ≤ v ≤ v₂`) versus D-CTG's open interval (`u < v < q`), but logically equivalent since the endpoints are already known members

Additionally, VC's justification references implementation internals (`findvsatoappend`, `acceptablevsa`, enfilade walking). D-CTG is a system invariant — its justification belongs in ASN-0036, not here. The note that "the backend does not enforce contiguity structurally" undermines the invariant status that D-CTG already has.

**Required**: Replace VD, VP, VC with citations to S8-depth, S8a, D-CTG (ASN-0036). Remove implementation-level justifications.

### Issue 2: Contraction preconditions not formalized; positivity argument cites wrong property

**ASN-0081, Contraction Setup**: "The contraction span lies entirely within the current arrangement."

**Problem (a) — scattered preconditions**: The contraction's applicability conditions are spread across prose, per-property precondition lists, and implicit assumptions. No unified formal contract collects them. The critical condition `p ∈ V_S(d)` never appears as a formal precondition anywhere — it is assumed but unstated.

**Problem (b) — incorrect citation in D-SHIFT**: The proof claims "The shifted ordinal is positive: the minimum shifted ordinal is ord(r) ⊖ w_ord = ord(p)… which is positive by VP." VP establishes `subspace(v) = v₁ ≥ 1` — that the *subspace identifier* is positive. It says nothing about the ordinal `ord(p) = [p₂]` being positive. Positivity of `ord(p)` requires `p₂ ≥ 1`, which follows from `p ∈ V_S(d)` and S8a (`v > 0` — all components positive), not from VP. Without `p ∈ V_S(d)` as a precondition, nothing prevents `p = [S, 0]`, which would yield `min(Q₃) = [S, 0]`, violating S8a in the post-state.

**Required**: (a) State a unified formal contract for the contraction: `p ∈ V_S(d)`, `w > 0`, `#w = #p`, `w₁ = 0`, and the containment condition (at depth 2 with D-SEQ: `ord(p)₁ + c − 1 ≤ |V_S(d)|`). (b) Fix the D-SHIFT positivity argument to cite `p ∈ V_S(d)` and S8a, not VP.

### Issue 3: Missing Istream frame condition

**ASN-0081, Region Postconditions**: D-L, D-DOM, D-CS, D-CD characterize the post-state arrangement. No formal statement addresses the content store.

**Problem**: D-SHIFT's prose notes "the content store is unchanged" but this appears as expository text, not as a formal frame condition. The ASN defines frame conditions for cross-subspace positions (D-CS) and cross-document arrangements (D-CD), yet omits the most fundamental frame: content immutability. Without `Σ'.C = Σ.C` stated formally, the S3 (referential integrity) argument for the post-state has no anchor — shifted positions map to pre-state I-addresses, but those I-addresses must still be in `dom(Σ'.C)`.

**Required**: Add a frame condition for the content store: `(A a ∈ dom(Σ.C) : a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))`, or cite S0 directly.

### Issue 4: Post-state invariant preservation not derived

**ASN-0081, Statement Registry**: Lists postconditions (D-SHIFT, D-DOM) and frame conditions (D-L, D-CS, D-CD) — the standard components of an operation specification — but no statement verifies that the post-state satisfies system invariants.

**Problem**: The following invariants are not addressed:

- **S2 (ArrangementFunctionality)**: M'(d) is a function. Follows from D-BJ (σ injective) + D-DP(a) (L ∩ Q₃ = ∅) + D-L and D-SHIFT assigning unique values. Two-line derivation, not stated.
- **S3 (ReferentialIntegrity)**: `ran(M'(d)) ⊆ dom(Σ'.C)`. Follows from D-L and D-SHIFT (all post-state I-addresses were pre-state I-addresses) + S3 on the pre-state + Istream frame (Issue 3). Not stated, and the Istream frame is itself missing.
- **D-CTG preservation**: Post-state `V_S(d)` is contiguous. D-DP shows the boundary between L and Q₃ is tight, but does not derive that L is contiguous (it's a prefix of a contiguous set) or that Q₃ is contiguous (order-preserving image of a suffix). The union L ∪ Q₃ is therefore contiguous, but this chain isn't shown.
- **D-MIN preservation**: When L ≠ ∅, inherited. When L = ∅, then p = min V_S(d) = [S, 1, …, 1] by D-MIN, so min Q₃ = [S, 1, …, 1] by D-SEP(b). Neither case derived.

These all follow from stated results in one or two steps. The derivations are short but non-trivial (especially D-CTG, which chains D-DP with individual region contiguity). Without them, a downstream ASN cannot cite this ASN for invariant preservation — it would need to re-derive each invariant.

**Required**: Add a section deriving that the post-state preserves S2, S3, D-CTG, and D-MIN. Alternatively, explicitly scope the ASN as algebraic tools (removing operational framing from the statement registry) and defer invariant preservation to the operation ASN — but then D-L, D-DOM, D-CS, D-CD should not be labeled "frame" and "postcondition."

### Issue 5: Worked example omits boundary cases

**ASN-0081, Worked Example**: Verifies a middle-of-arrangement contraction where L = {[1,1]}, X = {[1,2],[1,3]}, R = {[1,4],[1,5]}.

**Problem**: This covers only L ≠ ∅ ∧ R ≠ ∅. Two boundary configurations go unchecked:

- **L = ∅** (contraction starts at min V_S(d)): e.g., p = [1,1], w = [0,2], r = [1,3] on V_S(d) = {[1,1],…,[1,5]}. Post-state is Q₃ = {[1,1],[1,2],[1,3]} only. This exercises D-SEP(b) at the minimum boundary and D-MIN preservation — the shifted minimum must equal [S,1].
- **R = ∅** (contraction runs to end): e.g., p = [1,3], w = [0,3], r = [1,6] on V_S(d) = {[1,1],…,[1,5]}. Post-state is L = {[1,1],[1,2]} only. D-SEP(b), D-BJ, and D-DP(b) are vacuously satisfied. Verify that D-DOM, D-CTG, D-MIN hold for L alone.

**Required**: Add at least one boundary case to the worked example, verifying all postconditions.

## OUT_OF_SCOPE

### Topic 1: Generalization to ordinal depth > 1
**Why out of scope**: The depth-2 scoping axiom is stated explicitly and generalization is listed as an open question. The deeper case introduces genuine complexity — TA4's zero-prefix condition is no longer vacuous, TA3-strict's equal-length precondition must be checked against multi-component displacements, and the round-trip `(ord(p) ⊕ w_ord) ⊖ w_ord = ord(p)` needs its full precondition chain verified. This merits separate treatment.

### Topic 2: Full DELETE operation specification
**Why out of scope**: This ASN provides algebraic characterizations of contraction effects. A DELETE operation would compose these with precondition validation, version management, link-endset updates, and cross-subspace coordination — each requiring analysis beyond span algebra.

VERDICT: REVISE
