# Review of ASN-0077

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Origin projection on entity tumblers (E_doc, E_account, E_node)
**Why out of scope**: O0 explicitly restricts `origin` to `dom(C) ∪ dom(L)`. Whether `origin` should also be defined on entity tumblers (where `origin(d) = d` would hold trivially for d ∈ E_doc) is a separate design question, correctly deferred.

### Topic 2: Cross-subspace I-span lift behavior
**Why out of scope**: The ASN's Open Question 1 records this. The current I-span lift silently drops link addresses by intersecting with dom(C); whether to extend it to dom(L) belongs in a follow-on ASN.

### Topic 3: Native-vs-transcluded distinction at a queried position
**Why out of scope**: Open Question 3 records this. SHOWORIGIN reports the home document, not whether content is native to the queried document — a separate operation per Nelson's design.

### Topic 4: Historical containment operation distinct from current arrangement
**Why out of scope**: Addressed under "What SHOWORIGIN does not promise" and Open Question 5. The R relation grounds a separate operation.

META: (none — the ASN remains firmly in abstract specification territory, defining a state-relative observation operation with structural guarantees independent of implementation mechanism.)

VERDICT: CONVERGED

The ASN is comprehensive and the proofs are careful. O0's extension of `origin` to `dom(L)` is correctly grounded in three pieces (L1c structural identity, K.λ allocation precondition, K.λ-only closure of dom(L)), and the closure argument's reliance on frame-inspection of non-λ transitions is acceptable given ASN-0047's frame conventions. The (F1) ≡ (F2) ≡ (F3) equivalence chain is correctly derived via (F2)=(F3), (F1)⊆(F3), (F3)⊆(F1) with O2 (not M16a alone) handling both content and link blocks via M-sub(a). The singleton I-span derivation correctly excludes #b > #a via K.α's inc(·,0)-only emission algorithm forcing uniform A_C(d) output length. Permanence and monotonicity claims (O5, O6, O7, O11, O11', O8, O12) are correctly derived from foundation invariants (P0, P3, K.μ⁺/K.μ⁺_L effect axioms), and the K.μ~ worked example properly demonstrates why no parallel monotonicity claim exists for arrangement reordering. The wp analysis includes one non-trivial characterization (single-origin spans) and one direct restatement (d_q ∈ result), both correct.
