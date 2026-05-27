# Review of ASN-0100

## REVISE

### Issue 1: FirstEmissionFreshness citation is too narrow for arbitrary k
**ASN-0100, §Verifying the Invariants — Provenance**: "For Insertion positions, the freshly allocated `a_k` was not in any `ran(M(d))` pre-state (by FirstEmissionFreshness; ASN-0093)"

**Problem**: FirstEmissionFreshness (ASN-0093) addresses only the *first emission* (the boundary case `{a' ∈ dom(C) : origin(a') = d} = ∅`). For arbitrary `k`, including `k ≥ 1` and the boundary case where prior chain emissions exist in `dom(Σ.C)`, the freshness argument requires K.α's general freshness precondition (evaluated against `Σ_k`), then P0 monotonicity to lift the intermediate-state freshness to the operation's pre-state, then pre-state S3★ to conclude `a_k ∉ ran(Σ.M(d))`. The ASN gives the fuller machinery in §Effect One (citing ChainEnumerationInjectivity, ChainMembershipForOrigin, SubAllocatorAxiom.Disjointness), but the terse §Provenance citation collapses this to a lemma that doesn't cover the case.

**Required**: Replace the citation with the chain machinery from §Effect One, or write "by K.α's freshness precondition (ASN-0093) + P0 (ASN-0047) + pre-state S3★".

### Issue 2: L14 citation in Effect One reverses cause and effect
**ASN-0100, §Discovering the Three Effects — Effect One**: "The `a_k ∉ dom(Σ_k.L)` clause holds by L14 (StoreDisjointness; ASN-0093) — equivalently DisjointSubAllocatorChains (ASN-0093)."

**Problem**: L14 is a per-state invariant (`dom(C) ∩ dom(L) = ∅`) that is consistent with `a_k ∉ dom(Σ_k.L)` but does not entail it: at state `Σ_k`, `a_k ∉ dom(Σ_k.C)` (K.α has not yet fired), so L14 in `Σ_k` does not constrain `a_k` against `dom(Σ_k.L)`. The proper discharge — which the ASN provides in the same paragraph — uses SubAllocatorAxiom.Subspace + L0 + SC-NEQ. The "by L14" headline is misleading.

**Required**: Drop the "by L14" framing or qualify it ("consistent with L14"); lead with the SubAllocatorAxiom.Subspace + L0 + SC-NEQ chain that actually discharges the precondition.

### Issue 3: S8★ preservation not explicitly verified
**ASN-0100, §Verifying the Invariants**: The ASN verifies S0, S2, S3★, S8a, S8-depth, S8-fin, D-CTG★, D-MIN★, D-SEQ★, S7a–S7d, L0/L1/L3/L12/L14, P0/P2/P3/P4★/P6/P7/P7a/P8, NodeLineage, CL-OWN/CL-UNIQ — but does not explicitly address S8★ (PerSubspaceSpanDecomposition; ASN-0047), which is a Class (a) per-state invariant.

**Problem**: S8★ is preserved transitively via M2 (DecompositionExistence; ASN-0058) under the verified standing preconditions (S8-fin, S2, S3, S8a, S8-depth, S7b, S7c), but the derivation is implicit. A reader checking that every Class (a) invariant is preserved across INSERT will find an explicit verification for every other one.

**Required**: Add a brief paragraph noting that S8★ follows from M2 on the verified per-state preconditions, with the Insertion region forming a single correspondence run (consecutive shift(p, k) V-positions mapped to the consecutive chain emissions a_0, …, a_{n-1}, which are I-adjacent under TA5(c)).

### Issue 4: shift(p, 0) convention not declared at first use
**ASN-0100, §The Operation: Formal Contract — Effect — Arrangement of d, text subspace — Insertion**: "M'(d)(shift(p, k)) = a_k for 0 ≤ k < n, reading shift(p, 0) = p per OrdinalShiftBase (ASN-0058)"

**Problem**: ASN-0034's OrdinalShift requires `n ≥ 1`, so `shift(t, 0)` is undefined there. ASN-0058's OrdinalShiftBase defines `t + 0 = t` using the `+` notation, but does not itself extend the `shift(t, 0)` notation. The ASN's reading is a notational convention — reasonable and harmless — but presented as a direct foundation derivation rather than a local convention. Across the analysis (S8a verification, OrdAddHom application, INS.M-insert) the convention is silently relied on.

**Required**: At first use, declare the convention `shift(p, 0) := p` explicitly as a notational convenience consistent with OrdinalShiftBase. Or rewrite the Insertion clause as a piecewise: "M'(d)(p) = a_0; for 1 ≤ k < n: M'(d)(shift(p, k)) = a_k".

### Issue 5: Empty-case K.α emission framing implicit about prior chain state
**ASN-0100, §A Worked Example — Empty-document first insertion**: "Let d have V_{s_C}(d) = ∅. Invoke INSERT(d, [1,1], ⟨v₀, v₁, v₂⟩) ..."

**Problem**: `V_{s_C}(d) = ∅` does not imply `dom(C) ∩ {a : origin(a) = d} = ∅` — content addresses with origin `d` can exist in `dom(C)` without being currently arranged. In that scenario, K.α's first-emission predicate is FALSE and the subsequent-emission predicate fires `a_{new0} = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)`, not `[d.0.s_C.1]`. The example's generic notation `a_{new0}` accommodates both, but the reader could mistakenly conclude the first-emission predicate always fires in the "empty case".

**Required**: Add a clause distinguishing "empty arrangement" (V_{s_C}(d) = ∅) from "fresh allocator state" (dom(C) ∩ {origin = d} = ∅) — the ValidFirstInsertionPosition predicate depends on the former; K.α's first-emission predicate depends on the latter. The V-position assignments are determined by the former; the I-address values by the latter.

## OUT_OF_SCOPE

### Topic 1: Concurrent INSERT semantics
The composite-atomicity precondition (INS.pre) rules out interleaved K.α firings from concurrent composites. The post-state when this assumption fails would require a different framework (CRDT-style merge, transaction conflict resolution, or per-document locking specification).

**Why out of scope**: Concurrent execution is environment-level; abstract operation specifications properly assume serialised semantics.

### Topic 2: Closure under composition
The open question "if Σ →INSERT→ Σ_1 →INSERT→ Σ_2, is there always a single INSERT from Σ to Σ_2?" deserves its own treatment, since the answer touches on operation algebra (which generally falls into a separate ASN class).

**Why out of scope**: Operation algebra is a distinct subject.

### Topic 3: Append-specific operation semantics
The ASN observes that the `j = N` case of INSERT is operationally equivalent to a separate APPEND operation, with K.μ⁻ omitted. A standalone APPEND specification (with its own contract, simpler since no Shifted-right region exists) could be derived as a corollary.

**Why out of scope**: A separate ASN for APPEND would either restate INSERT's j=N case or duplicate machinery; neither is a revision of this ASN.

VERDICT: REVISE
