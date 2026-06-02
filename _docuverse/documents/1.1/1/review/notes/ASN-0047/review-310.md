# Review of ASN-0047

## REVISE

### Issue 1: Dangling reference to an undefined property "P4"
**ASN-0047, *Extended reachable-state invariants*, Base case**: "L₀ = ∅ satisfies link invariants vacuously, including L3; **S3★ and P4★ reduce to S3 and P4** ... S3★ and P4★ reduce to S3 and P4".

**Problem**: This ASN defines `P4★` (ProvenanceBounds, content-subspace) but never defines an unstarred `P4`. `S3` is a foundation property (ASN-0036) and may be cited, but `P4` is not in any foundation table and is not introduced anywhere in this ASN. The token reads as residue from a prior version that carried an unstarred provenance bound. A reader cannot resolve what `P4★` is being said to "reduce to." (The unscoped bound `Contains(Σ) ⊆ R` is described later in the J4 section but is never labeled `P4`.)

**Required**: Either define/label the unscoped bound and cite it consistently, or rewrite the sentence to say "`P4★` reduces to the unscoped bound `Contains(Σ) ⊆ R`" without the phantom label.

### Issue 2: The "imposed (not derived) / K.α-alone" justification is restated near-verbatim in three sites
**ASN-0047, J0 box**: "A clause-(1)-satisfying elementary sequence in which K.α executes alone — every elementary precondition holding at each intermediate state — does exist; J0 is precisely what excludes it from the *valid* composites."
**ASN-0047, ValidComposite★ clause (2)**: "A composite that satisfies clause (1) but violates clause (2) — for instance, K.α alone without an accompanying K.μ⁺ and K.ρ — is not a valid composite even though every elementary precondition holds at every intermediate state."
**ASN-0047, *Scoped coupling constraints* preamble**: "J1★ and J1'★ are imposed (not derived); the wp derivations below give the motivating obligation."

**Problem**: The note carries the `review-mode.anti-bloat` classifier. The "K.α executes alone, every elementary precondition holds, yet the composite is invalid" illustration is the same point made twice in nearly identical words (J0 box and ValidComposite★ clause (2)), with the "imposed not derived" framing echoed a third time. This is the "two paragraphs say the same thing in different words" accretion pattern — distinct from a structural split, this is repeated meta-prose at source. The reader who has absorbed the point at J0 must re-skip it at ValidComposite★.

**Required**: State the "imposed, not an elementary-system axiom" status and the K.α-alone counterexample once (the natural home is the ValidComposite★ clause-(2) definition), and have the J0 box cross-reference it rather than re-illustrate.

### Issue 3: J3 self-sufficiency leans on K.μ~-RANGE without surfacing the intermediate-state P4★ behavior it shares with the composite-boundary analysis
**ASN-0047, J3 (Reordering isolation)**: "By **K.μ~-RANGE** (range-invariance), Contains(Σ') = Contains(Σ). All invariants are trivially maintained; no co-occurring transition is needed."

**Problem**: K.μ~ is a *composite* (K.μ⁻ + K.μ⁺), and the per-state-invariant induction (Class (a)) is explicitly stated to run over *elementary* steps that reach the intermediate state. At that intermediate state (post-K.μ⁻, pre-K.μ⁺), `Contains_C` has shrunk and the link subspace is retained, but J3 asserts isolation only at the composite boundary. The claim "all invariants are trivially maintained" is stated at the boundary granularity while the surrounding proof framework demands the elementary granularity. The discharge is almost certainly correct (the K.μ⁺ step re-adds only already-ranged addresses, so no R-extension is needed), but J3 states the conclusion without naming that the intermediate K.μ⁺ adds no range-new address — the exact fact that makes "no co-occurring K.ρ" sound.

**Required**: Add one clause to J3 stating that the K.μ⁺ step of the decomposition introduces no range-new content I-address (ran preserved by K.μ~-RANGE), so J1★ is vacuous at that step and no K.ρ is required — making the "no coupling" claim hold at the elementary granularity the Class (a) induction uses, not only at the boundary.

## OUT_OF_SCOPE

### Topic 1: Prepend / interior INSERT expressed through elementary transitions
The elementary model fixes `min(V_S(d)) = [S, 1, …, 1]` (D-MIN★) and contiguity (D-CTG★), and K.μ⁺ is pure addition with existing values unchanged. Consequently inserting *before* the minimum or *between* two existing positions is impossible via K.μ⁺ alone and requires a K.μ⁻ + K.μ⁺ composite that renumbers the suffix. The ASN shows split/merge and interior *replacement* composing from the elementary set but never demonstrates prepend/interior *insertion* composing similarly.

**Why out of scope**: INSERT is a named operation explicitly excluded from this ASN's scope; the elementary transitions provably suffice to express it as a composite. Demonstrating that composition belongs to the operations ASN, not here.

### Topic 2: Renumbering-aware interior link withdrawal
K.μ⁻ contracts each subspace by suffix removal only; interior withdrawal with compaction is unmodeled.

**Why out of scope**: The ASN itself flags this as an Open Question; modeling the implementation's `DELETEVSPAN` compaction is future-ASN territory, not a defect in the present elementary set.

META: The ASN defines abstract state (C, L, E, M, R), elementary transitions on it, and reachable-state invariants stated independently of any implementation — it has not drifted into implementation mechanics.

VERDICT: REVISE
