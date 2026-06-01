# Review of ASN-0086

## REVISE

### Issue 1: Emit_K function-ness misattributes max-uniqueness to R0a-Cor1

**ASN-0086, Lemma — Emit_K function-ness** (and the parallel passage in Definition — `a_emit(Σ, d)`): "`ℓ_prev` is `max{ℓ' ∈ dom(Σ.L) : origin(ℓ') = d}` — a unique extremum because, by R0a-Cor1, the homed set is a contiguous prefix of `A_L(d)`'s chain enumeration and so admits a unique maximum under T1."

**Problem**: The uniqueness of the maximum is not "because" of R0a-Cor1. Any finite, non-empty subset of a strictly totally ordered set has a unique maximum by T1 trichotomy alone (the set is finite by L-fin restricted to `origin(·) = d`, non-empty in the subsequent branch). Contiguity contributes nothing to uniqueness. This is not merely over-citation: Emit_K function-ness is asserted over the *full* state space Σ ("every state reachable from Σ_init"), whereas R0a-Cor1 is proved only at *substrate-conforming* states. Threading R0a-Cor1 into the function-ness proof imports a conformance hypothesis the conclusion does not actually require, and would make the proof fail at any non-conforming state in Σ even though `max` is well-defined there regardless.

**Required**: Discharge uniqueness from T1 (strict total order) plus finiteness (L-fin) directly, and drop the R0a-Cor1 appeal — or restate Emit_K's domain as substrate-conforming states if the conformance dependency is intended. Fix both the Lemma and the `a_emit` definition that inherits it.

### Issue 2: "substrate-conforming state" and "substrate-conforming layer" definitions duplicate and then diverge, while claiming exact equivalence

**ASN-0086, Definition — substrate-conforming layer**: clause "(a) Invariant Catalog. The full L/S/M/C invariant list ... together with the Link-record value-shape commitments L5 (EndsetSetSemantics), L6 (SlotDistinction), and L8 (TypeByAddress)" — followed by "Clauses (a) and (b) here are **exactly the two conditions** of the Definition — substrate-conforming state."

**Problem**: The earlier Definition — substrate-conforming state states clause (a) as "preserve the full L/S/M/C invariant catalog." If that catalog already contains L5/L6/L8 (they are ASN-0043 invariants), the layer definition's explicit re-enumeration is redundant restatement of the same condition in different words. If it does not, then the layer's clause (a) is strictly stronger and the claim "exactly the two conditions" is false — the equivalence that licenses "every `↝`-reachable post-state of a substrate-conforming layer is itself a substrate-conforming state" then does not hold as stated. Either way the two definitions are not in the asserted exact correspondence.

**Required**: Make the two clause-(a) catalogs literally identical (state which invariants the "full catalog" comprises once, in one place), or, if L5/L6/L8 are a genuine addition at the layer level, drop the "exactly the two conditions" claim and re-justify the state-conformance of `↝`-post-states against the stronger layer condition.

## OUT_OF_SCOPE

### Topic 1: Substrate-level enforcement of the unit-depth retraction discipline

The Open Question on elevating the unit-depth retraction discipline to a substrate guarantee (a dedicated retraction K-operation with a shape constraint) is correctly deferred — it would require a new K-operation contract in ASN-0093, not a revision here. The current treatment as a layer convention, with the direct-K.λ crafted-span regime honestly retained in the WP, is sound for this note.

### Topic 2: Concurrency/atomicity model for Emit vs Observe

The interaction between concurrent Observe and Emit, and the consistency model for observing `A_K` transitions, is genuinely new territory (no concurrency model exists in the adopted foundation). Belongs in a future ASN.

VERDICT: REVISE
