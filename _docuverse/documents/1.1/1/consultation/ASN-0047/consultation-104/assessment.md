# Channel Assignment — ASN-0047 review-104

**Date:** 2026-05-18 05:07

## Issue 1: K.μ~ admissibility necessary-vs-sufficient confusion
Reason: Fix is internal — derivable from K.μ~-FIX (which forces per-subspace cardinality preservation) combined with admissibility clause (iii)'s `π ≠ id`. Tightening to `|dom_C(M(d))| ≥ 2` follows from observing that singleton dom_C forces π = id on that singleton, which (with link-subspace fixity) forces π = id overall.

## Issue 2: K.α discharge inconsistent with K.λ case-split structure
Reason: Fix is internal — purely an editorial restructuring to mirror K.λ's existing two-bullet first-emission / subsequent-emission form. The structural reasoning (SubAllocatorAxiom.FirstEmission for first, T10a GlobalUniqueness for subsequent, SC-NEQ + T7 + L14 for cross-store) is already present in the ASN; the fix recasts it into parallel form.

## Issue 3: GlobalLineage's TA5(c) prefix preservation claim is imprecise
Reason: Fix is internal — derivable from TA5(c)'s precise postcondition as stated in ASN-0034 (the foundation). The corrected argument requires observing that the chain's structural shape (starting with `inc(origin(ℓ), 2)`) places `sig(tᵢ) > #origin(ℓ)` at every step, so each TA5(c) k=0 step preserves the *prefix `origin(ℓ)`* even though it does not preserve the *current operand* as a prefix.

## Issue 4: Bootstrap node's status in node-allocation registry is implicit
Reason: Fix is internal — a formalization choice within the ASN's abstraction boundary. NodeUniqueAllocation already declares registry mechanism details out of scope; the fix adds one explicit clause (`n₀ ∈ dom(registry)` at Σ₀) to close the T2 spawn discharge for the first K.δ k=2 event with `t = n₀`.

## Issue 5: K.μ⁻ effect strict-subset clause non-emptiness preconditions
Reason: Fix is internal — editorial clarification of precondition vs. consequence. The strict-contraction conjunct in clause (2) is logically equivalent to the strict-subset effect, derivable by checking that `dom(M'(d)) ⊂ dom(M(d))` decomposes into `∪_S V_S(d') ⊊ ∪_S V_S(d)` under the per-subspace patterns of clause (1).

## Issue 6: K.μ~ partial-suffix vs. full-clearance forms - admissibility constraint not stated
Reason: Fix is internal — derivable from K.μ⁻'s value-preservation clause and K.μ⁺'s amended preconditions. If π disturbs any position below k₀, K.μ⁻ at `n'_{s_C} = k₀ − 1` would leave those positions in dom(M_int(d)) with original values, and K.μ⁺'s value-preservation clause then forbids altering them — making the partial-suffix expansion inadmissible. The constraint can be stated explicitly without external input.
