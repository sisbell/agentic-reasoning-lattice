# Review of ASN-0099

## REVISE

### Issue 1: F4 realizability discharge — parametric witness construction is implicit
**ASN-0099, F4 (MatchFormulaMinimality), Realizability discharge**: "any pair `(a, I)` satisfying F1's existential at some slot `i` ... is realizable as a conforming state extending some base via a single K.λ step"

**Problem**: The discharge argues that "any pair (a, I)" is realizable, but the link address `a` is not freely chosen — it is determined by K.λ's chain discipline (the subsequent-emission formula `inc(ℓ_prev, 0)` ranging over `A_L(d)` for some `d ∈ E_doc`). What is actually parametric in the construction is the (endset configuration, I-set) pair: K.λ at the final step accepts any well-formed endset sequence (L4 places no constraint on referenced addresses, K.λ requires only `N ≥ 3` and non-empty slot 3), and `I ⊆ T` is unconstrained query data. Since `matches(a, I, Σ)` factors through the endset tuple (two addresses with identical endsets have identical match status), the discharge's substance is correct under this implicit factoring — but a reader auditing F4 may misread "any pair (a, I)" as licensing free choice of address.

**Required**: Make the parametric factoring explicit. State that the witness's address `a` is realized by K.λ's chain discipline rather than freely chosen; that endsets at the realizing K.λ step are the free parameter; and that the witness's (endset configuration, I-set) shape is what the realization preserves. Note that L1c (LinkAllocatorConformance) supplies the closure: every F1-admitted address inhabits some `A_L(d)` chain and is therefore K.λ-reachable, so the realization space covers the F1-admission space.

### Issue 2: F4 "single K.λ step" understates the base construction
**ASN-0099, F4 (MatchFormulaMinimality), Realizability discharge**: "is realizable as a conforming state extending some base via a single K.λ step"

**Problem**: K.λ produces the chain element at the *next* index of `A_L(d)`. To realize a link at chain index `k` (i.e., address `[d.0.s_L.k]` with `k ≥ 2`), the base state must have already received `k − 1` prior K.λ allocations under `d`. The phrase "single K.λ step" elides this. The preceding paragraph addresses the K.δ entity-creation prelude needed to make `dom(M)` non-empty but does not address the K.λ prelude needed for chain advancement. For chain index 1 the wording is correct (first-emission predicate fires); for chain indices ≥ 2 the wording is imprecise.

**Required**: Clarify that "extending some base" includes prior K.λ allocations under `d` to advance `A_L(d)` to chain index `k − 1`, and the witness link is then realized at the final K.λ step at chain index `k`. Equivalently, state the discharge as "extending an appropriately-set-up base via a final K.λ step that produces the link with the desired endsets".

## OUT_OF_SCOPE

### Topic 1: Phantom-address query semantics, replication, access control, concurrency model, I→V resolution
**Why out of scope**: The ASN explicitly lists these in its "Open Questions" section, deferring them to future ASNs. The boundaries are correctly drawn — each topic introduces independent state or protocol commitments not needed for the abstract specification of FINDLINKS over a single state.

### Topic 2: Promoting A1 to a substrate axiom
**Why out of scope**: A1 (LinkStoreInertOfNonAllocatingOperations) is derived in this ASN via the closed-world reading of substrate effect clauses, grounded in transparently-cited consultative evidence (Nelson's design intent; Gregory's implementation evidence). The ASN labels this as a load-bearing interpretive choice and discharges A1 within its own scope. Whether to axiomatize this in ASN-0047 or ASN-0093 directly is a substrate-revision question, not a defect of this ASN.

### Topic 3: A "strict K.λ additions" companion to F19
**Why out of scope**: F19 captures monotonicity (`findlinks(I, Σ) ⊆ findlinks(I, Σ')`) under reachable sequences. The strict additions under K.λ (a newly-allocated matching link entering the result set) follow directly from K.λ's published effect `L' = L ∪ {ℓ ↦ ...}` together with F1's evaluation at Σ', and are demonstrated in the worked example (Query 11's F19 verification). A separately-named claim would be redundant rather than load-bearing for this ASN's scope.

VERDICT: REVISE
