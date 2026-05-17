# Review of ASN-0047

## REVISE

### Issue 1: S9 restatement contradicts admitted composites

**ASN-0047, ExtendedTransitionInvariants**: "Every valid composite transition Σ → Σ' between reachable states satisfies P0 ∧ P1 ∧ P2 ∧ P3★ ∧ P5★ ∧ S9 ∧ L12."

The proof states S9 as: `(A Σ → Σ' : (E d : M'(d) ≠ M(d)) : dom(C') = dom(C) ∧ (A a ∈ dom(C) : C'(a) = C(a)))`

**Problem**: This restatement is strictly stronger than the foundation S9, which only requires value preservation (`(A a ∈ dom(C) : a ∈ dom(C') ∧ C'(a) = C(a))`), allowing dom(C) to extend. For the standard content-insertion composite K.α + K.μ⁺ + K.ρ:
- Antecedent: M(d) changes (true)
- Consequent: dom(C') = dom(C) ∪ {a} ≠ dom(C) — **FALSE**

The proof's "transitivity of equality over a finite composite preserves the consequent" argument fails: K.α extends C but holds M in frame (antecedent vacuous at that step), then K.μ⁺ changes M but holds C in frame (consequent holds *only at that step*). At the composite boundary, both C has extended *and* M has changed, so the implication is genuinely violated.

**Required**: Either (a) use the foundation S9 verbatim (value preservation only), under which K.α + K.μ⁺ + K.ρ trivially satisfies S9 because existing entries persist; or (b) move S9 out of ExtendedTransitionInvariants and explicitly scope it to elementary transitions only.

### Issue 2: ShiftPreservation cited for the wrong property

**ASN-0047, K.μ⁺_L "Shift-lemma applicability" and "Per-subspace arrangement invariants"**: "S8a is supplied by ShiftPreservation (ASN-0036), which preserves the all-positive-components property under shift uniformly in v₁"

**Problem**: Foundation ShiftPreservation is stated for `a ∈ dom(Σ.C)` (I-addresses with `zeros = 3`) and preserves (i) `zeros(shift(a, k)) = 3`, (ii) T4-validity, (iii) `#E` preservation, (iv) `subspace_I` preservation. It does **not** establish S8a (which is about V-positions with `zeros = 0`). The characterisation as "stated parametrically in v₁" is also wrong — the foundation lemma's hypothesis is `a ∈ dom(C)`, not a parametric V-position.

The correct citation for S8a preservation on V-positions is **OrdShiftHom (c)** (ASN-0036): "When `v` satisfies S8a, `shift(v, n)` satisfies S8a unconditionally" — or equivalently OrdAddS8a with `w = δ(1, m)` whose action-point-tail condition is vacuously satisfied.

**Required**: Replace ShiftPreservation citations for V-position S8a with OrdShiftHom (c) or OrdAddS8a; remove the inaccurate "parametric in v₁" characterisation of ShiftPreservation.

### Issue 3: NodeLineage missing from per-state invariants theorem

**ASN-0047, ExtendedReachableStateInvariants**: lists S2 ∧ S3★ ∧ ... ∧ CL-UNIQ but does not include NodeLineage.

**Problem**: NodeLineage is asserted as an axiom (`(A e ∈ E : IsNode(e) : n₀ ≼ e)`) and discharged inductively: it holds at Σ₀ by reflexivity (E₀ = {n₀}, `n₀ ≼ n₀`), and K.δ case (i) preserves it via the precondition `n₀ ≼ e`. It is a per-state property of every reachable state. Its absence from the theorem leaves the inductive invariant unstated.

**Required**: Add NodeLineage to ExtendedReachableStateInvariants' conjunction (and verify the induction step in the proof, which is straightforward given K.δ's case-(i) precondition).

### Issue 4: `fields(a)` notation reinvents foundation E(a)

**ASN-0047, Notation section**: "`fields(a)` (ASN-0034, T4b): the element-field truncation of the tumbler"

**Problem**: T4b (ASN-0034) defines the partial projection `E(a)` for element-level addresses. There is no `fields` function in T4b. ASN-0036 uses `E(a)ᵢ` notation directly (e.g., "the within-subspace ordinal `[E(a)₂, ..., E(a)_δ]`"). This ASN's `fields(a).E₁` notation is a renaming of the foundation's `E(a)₁`.

The instructions are explicit: "If an ASN invents its own notation for something a foundation already defines, flag it as a REVISE item."

**Required**: Either (a) use `E(a)` and `E(a)₁` from T4b directly throughout, or (b) explicitly state `fields(a) := E(a)` as a local abbreviation for readability without claiming foundation attribution.

### Issue 5: SubAllocatorAxiom needs explicit reconciliation with L1c

**ASN-0047, "Allocator hierarchy under documents"**: SubAllocatorAxiom asserts that link anchors `b_L(d)` are "outside T10a's per-owner inc tree rooted at `d`" and that the first link `[d.0.s_L.1]` is admitted by axiom rather than T10a.

**Problem**: ASN-0043's L1c (LinkAllocatorConformance) requires the existence of a T10a-conforming inc chain from a T4-valid document seed `s` to every link address, with `k₁ = 2`. For `ℓ = [d.0.s_L.1]` with `s_L = 2`, a pure inc-chain exists (`inc(d,2) → inc(_,0) → inc(_,1)`) reaching `ℓ` through intermediates `[d.0.1]`, `[d.0.2]` that are not actually allocated. The ASN doesn't reconcile whether (a) these intermediates count as "T10a-conforming chain steps" (in which case SubAllocatorAxiom is a structural abstraction over the inc-chain, not "outside T10a"), or (b) SubAllocatorAxiom genuinely admits chains that L1c forbids.

**Required**: Clarify how SubAllocatorAxiom relates to L1c — either by exhibiting the constructive inc-chain that L1c demands and noting SubAllocatorAxiom abstracts over it, or by explicitly amending L1c (which would require a separate revision of ASN-0043).

### Issue 6: K.μ~ status oscillates between "distinguished composite" and "transition kind"

**ASN-0047, multiple sections**: K.μ~ is declared "a distinguished composite, not a primitive transition" but appears in the elementary catalogue, in the Frame extension table with its own derived frame, in the elementary case-analysis of ExtendedReachableStateInvariants, and in the ValidComposite★ definition as a "shorthand for its decomposition."

**Problem**: The treatment is internally consistent under the explicit "shorthand" reading, but the ASN never names K.μ~ at the level of its actual status — is it an elementary transition, a named composite (like J4 Fork), or something in between? The structural sufficiency claim says "seven elementary transitions ... plus the distinguished composite K.μ~" — which suggests it's not elementary; but it appears in the elementary-case proof.

**Required**: Pick one position consistently. Either treat K.μ~ as a named composite (like J4) with no elementary status, and verify invariant preservation strictly via its decomposition without listing it as a separate "case" in elementary proofs; or admit it as an elementary transition with its own contract and frame, deriving the decomposition account as a realisation theorem rather than a definition.

## OUT_OF_SCOPE

The ASN explicitly defers these to future work; they are correctly excluded:

### Topic 1: Tombstone-style link withdrawal
**Why out of scope**: Nelson's "not currently addressable" status mechanism (LM 4/9) requires per-link liveness state outside the present five-component model. The ASN names this as the principal known gap and defers it to a withdrawal-invariants question.

### Topic 2: Version-management semantics
**Why out of scope**: The K.δ k=1 sub-case admits version allocations structurally, but arrangement-transition invariants between versions, content-allocator linkage, version lineage acyclicity, etc., belong to a future version-management ASN.

### Topic 3: Account-level k=1 and non-T10a allocators
**Why out of scope**: Both are deliberate scope exclusions noted in the structural sufficiency section, deferred to future ASNs that might widen the allocator discipline.

META: The ASN is firmly on-mission — it specifies state, elementary transitions, invariants, and coupling constraints at the abstract level, with implementation mechanics correctly relegated to scope exclusions.

VERDICT: REVISE
