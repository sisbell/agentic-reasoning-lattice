# Review of ASN-0071

## REVISE

### Issue 1: Malformed set-containment chain in the codomain argument

**ASN-0071, "The operation"**: "Therefore `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ dom(Σ.L) ∩ dom(Σ.C) ∪ dom(Σ.C) = dom(Σ.C)`"

**Problem**: The displayed expression does not type-check as a derivation. Read with standard precedence (∩ before ∪), `dom(Σ.L) ∩ dom(Σ.C) ∪ dom(Σ.C)` parses as `(dom(L) ∩ dom(C)) ∪ dom(C) = ∅ ∪ dom(C) = dom(C)` — so the final value is right, but the *middle term is not an upper bound the left side was shown to sit inside*. The correct bounding set is `(dom(C) ∪ dom(L)) ∩ dom(C)`, obtained from `ran(M(d)) ⊆ dom(C) ∪ dom(L)` (S3★) intersected with `iaddrs(Q) ⊆ dom(C)`. The chain as written transposes the union and intersection. The subsequent "more precisely" sentence gives the actually-valid one-line argument (any `a` in the intersection is in `iaddrs(Q) ⊆ dom(C)`), which makes the entire displayed chain both wrong and redundant.

**Required**: Delete the malformed displayed containment and keep only the "more precisely" argument, or rewrite the chain as `ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ⊆ (dom(Σ.C) ∪ dom(Σ.L)) ∩ dom(Σ.C) = dom(Σ.C)` with the two inclusions named (S3★ for the left factor, the subspace-confinement subset claim for the right).

### Issue 2: find(Q)(Σ) is undefined when a queried source document is absent from Σ.E_doc

**ASN-0071, "The query" / "The operation"**: vspec is defined as "a pair `(d_s, σ)` where `d_s ∈ Σ.E_doc`", but the operation has signature `find : VSpecSet × Σ → P(E_doc)` with `Q` and `Σ` as independent inputs.

**Problem**: `iaddrs_one(d_s, σ)(Σ)` references `dom(Σ.M(d_s))`. By M1, `dom(Σ.M) = Σ.E_doc`, so if `d_s ∉ Σ.E_doc` then `Σ.M(d_s)` is undefined and the intersection `⟦σ⟧ ∩ dom(Σ.M(d_s))` has no meaning. The type signature presents `Q` as a free argument decoupled from the evaluation state, yet nothing in the `find` definition states the precondition `(A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)`. Entity permanence (P1) makes the gap benign only when `Q` is formed at a state no later than the evaluation state; the spec never restricts to that case. A Dijkstra-grade definition of a partial function must name its domain.

**Required**: State an explicit well-definedness precondition on `find(Q)(Σ)` — `(A (d_s, σ) ∈ Q :: d_s ∈ Σ.E_doc)` — or make the vspec's `Σ`-binding identical to `find`'s evaluation state and say so. Either resolves the coupling; leaving the type signature as two independent arguments without the precondition does not.

## OUT_OF_SCOPE

### Topic 1: R-based historical containment query

**Why out of scope**: The ASN correctly defers "what documents EVER contained this" to a separate `R`-based operation (Open Questions, "Permanence and currency reconciled"). This is new territory, properly a future ASN, not a defect here.

### Topic 2: Visibility filtering and replica freshness

**Why out of scope**: "What we do not specify" (ii)–(iii) appropriately defer access-control filtering and distributed-replica consistency. These are separable policy/deployment layers, not omissions in the abstract operation.

VERDICT: REVISE
