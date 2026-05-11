# Review of ASN-0036

## REVISE

### Issue 1: Auxiliary lemma in S8 — strict inequality `#aⱼ − δⱼ + 1 < #aⱼ` stated, not derived
**ASN-0036, S8 auxiliary lemma, conclusion (i)**: "The strict inequality `#aⱼ − δⱼ + 1 < #aⱼ` is equivalent to `δⱼ > 1`, i.e. `δⱼ ≥ 2` — exactly the bound supplied by S7c."

**Problem**: This is asserted as an algebraic equivalence but no derivation is shown. The position arithmetic crosses NAT-sub territory (`#aⱼ − δⱼ` is partial subtraction), and the route from `δⱼ ≥ 2` to the strict inequality requires explicit citation of NAT-* axioms. Compare with D-CTG-depth's alternative-construction parenthetical, which derives `(v₁)ⱼ₊₁ < (v₁)ⱼ₊₁ + (i + 1)` through a five-step chain. Conclusion (i) is the load-bearing payoff of S7c, so its derivation deserves the same care.

**Required**: Give the explicit derivation. One route: by NAT-sub closure under `#aⱼ ≥ δⱼ`, place `#aⱼ − δⱼ ∈ ℕ`; rewrite `#aⱼ` via the left-inverse `#aⱼ = δⱼ + (#aⱼ − δⱼ)`; apply NAT-order with NAT-addcompat to show `(#aⱼ − δⱼ) + 1 < (#aⱼ − δⱼ) + 2 ≤ (#aⱼ − δⱼ) + δⱼ = #aⱼ`. Or an equivalent NAT-* sequence.

### Issue 2: Auxiliary lemma in S8 — conclusion (iii) silently assumes T4-validity of `shift(aⱼ, k)`
**ASN-0036, S8 auxiliary lemma, conclusion (iii)**: "T4's partition `N(shift(aⱼ, k)).0.U(shift(aⱼ, k)).0.D(shift(aⱼ, k)).0.E(shift(aⱼ, k))` has the same element-field boundary as `aⱼ`'s partition."

**Problem**: T4b's partition requires T4-validity, which has four conjuncts: `zeros ≤ 3`, no adjacent zeros, `t₁ ≠ 0`, `t_{#t} ≠ 0`. The proof verifies the zero-count conjunct (= 3) and the last-component conjunct (via `aⱼ_{#aⱼ} + k ≥ 2`). The no-adjacent-zeros and `t₁ ≠ 0` conjuncts are left implicit. They are recoverable from "zeros sit at the same positions as `aⱼ` and `aⱼ` is T4-valid," but a Dijkstra-style proof states this, especially when invoking T4b's projection.

**Required**: Add one sentence between conclusions (ii) and (iii) stating: since the zero positions of `shift(aⱼ, k)` coincide with those of `aⱼ` (positions strictly less than `#aⱼ`, all copied by the prefix rule), and since `(shift(aⱼ, k))_1 = (aⱼ)_1 ≠ 0` (T4 on `aⱼ`, prefix copy), all four T4-validity conjuncts hold for `shift(aⱼ, k)`, licensing T4b at the new tumbler.

### Issue 3: S7c postconditions stated without derivation
**ASN-0036, S7c Formal Contract postconditions (a), (b), (c)**: Three structural consequences are listed under an "Axiom (design requirement)" entry — most notably (b): "the displacement `δ(k, #a)` has action point `#a`, which falls strictly after the position of `subspace_I(a)` in the full address."

**Problem**: An axiomatic primitive that pins a single quantity (`#E(a) ≥ 2`) should not silently produce a three-part derived consequence without showing the derivation, especially when (b) is what the entire downstream subspace-preservation machinery cites. (a) and (c) follow by inspection of T4b plus T4's positivity, but (b) requires the same position-arithmetic step flagged in Issue 1.

**Required**: Either (i) demote (a), (b), (c) to a separate Consequence with a short derivation paragraph (parallel to how NAT-cancel handles its absorption Consequence), or (ii) add inline justifications for each — particularly (b)'s `#a − #E(a) + 1 < #a` step, citing the same NAT-* chain used to fix Issue 1.

### Issue 4: subspace_I's postcondition (c) circularity with S8's auxiliary lemma
**ASN-0036, subspace_I Formal Contract, Postconditions (c) and Depends**: Postcondition (c) "subspace preservation under shift" cites "S8's auxiliary lemma conclusion (i)" and the Depends entry says "supplies the full derivation behind postcondition (c)."

**Problem**: subspace_I is introduced *before* S8 in the document order; S8's auxiliary lemma in turn invokes `subspace_I` to state its conclusion (i). The forward reference makes the chain feel circular even though it is not — the lemma's proof doesn't actually invoke subspace_I's Postcondition (c). The structure would read more cleanly if subspace_I's Postcondition (c) was either derived inline (a two-line argument: action point of `δ(k, #a)` is `#a`, `subspace_I` sits at position `#a − #E(a) + 1 < #a` by S7c, TumblerAdd prefix rule copies it) or marked explicitly as an exported corollary of the lemma rather than as a postcondition that depends on it.

**Required**: Inline the two-line derivation under subspace_I, or restructure so that the lemma is the source of (c) and subspace_I lists (c) without claiming the lemma "supplies the derivation behind" it (this phrasing reads as `subspace_I depends on auxiliary lemma depends on subspace_I`).

### Issue 5: "observable state" undefined in S3
**ASN-0036, S3 Formal Contract**: "Axiom (well-formedness invariant): In every observable state `Σ`, ..."

**Problem**: "Observable state" appears here for the first and only time, with no definition. The Open Questions section asks "Under what conditions, if any, may the referential integrity invariant S3 be temporarily violated — must it hold at every observable state, or only at quiescent states between operations?" — which suggests the term is doing real work, contrasting with non-observable (intermediate) states. But a strand-level axiom should not depend on an undefined notion. Either every state satisfies S3, or some don't; the axiom needs to commit.

**Required**: Either replace "observable state" with "every state" (and let the Open Question handle the relaxation), or define "observable state" in the body — likely as the state at quiescent moments between operations.

### Issue 6: S5 cross-document construction's `dᵢ` not certified T4-valid where T4-validity is consumed
**ASN-0036, S5 proof, cross-document construction**: "`N + 1` documents `d₁, …, d_{N+1}` with explicit witnesses `dᵢ = [1, 0, 1, 0, i]` for `i = 1, …, N + 1` ... `dᵢ = [1, 0, 1, 0, i]` is a valid document-level tumbler: `zeros(dᵢ) = 2` with no adjacent zeros, positive endpoint components, and the three fields `N(dᵢ) = [1]`, `U(dᵢ) = [1]`, `D(dᵢ) = [i]` populated by strictly positive natural numbers (T4, HierarchicalParsing, ASN-0034)."

**Problem**: The check verifies (no adjacent zeros, positive endpoints) but doesn't separately verify that `i ≥ 1` is required for the `D(dᵢ) = [i]` field to have a strictly positive component — at `i = 0` the field `[0]` is empty after T4-decomposition (the trailing zero becomes a field separator). The construction quietly takes `i ∈ {1, …, N + 1}`. The check should explicitly note that the index-range choice depends on T4's positive-component constraint, since the proof's "natural numbers `1, …, N + 1` exist in ℕ by T0" is the wrong citation (T0 supplies the carrier; `1, …, N + 1 ∈ ℕ` comes from NAT-closure starting at NAT-zero's `0 ∈ ℕ` and NAT-closure's `1 ∈ ℕ`).

**Required**: Fix the citation from "T0, ASN-0034" to "NAT-closure (with `1 ∈ ℕ` from the same axiom and closure under addition), ASN-0034" — and explicitly tie the constraint `i ≥ 1` to T4's positive-component requirement on `D(dᵢ) = [i]`.

## OUT_OF_SCOPE

### Topic 1: How DELETE/INSERT/COPY/REARRANGE preserve D-CTG and D-MIN
**Why out of scope**: This is properly identified in the Open Questions section and the Scope note. Operation-specific frame conditions belong to per-operation ASNs (e.g., ASN for INSERT, ASN for DELETE), not the strand model.

### Topic 2: Link subspace `S = 2` contiguity semantics (tombstone discipline)
**Why out of scope**: The ASN explicitly defers link-subspace contiguity, and properties D-CTG, D-MIN, D-CTG-depth, D-SEQ are bound to text subspace `S = 1` in their Formal Contracts. The link subspace is a separate concern requiring its own properties (tombstones, append-only semantics).

### Topic 3: Subspace alignment between V-positions and I-addresses
**Why out of scope**: The ASN's Remark explicitly treats subspace alignment (`subspace(v) = subspace_I(M(d)(v))`) as an operations-layer preservation obligation. The strand model deliberately does not impose it as a state invariant.

### Topic 4: The choice of `m` beyond `m ≥ 2` in ValidFirstInsertionPosition
**Why out of scope**: The strand model fixes only the lower bound; the specific value (and what nested-hierarchy capabilities a deeper choice unlocks) is an operations-layer convention. Listed under Open Questions.

VERDICT: REVISE
