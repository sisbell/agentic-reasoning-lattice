# Review of ASN-0075

## REVISE

### Issue 1: Implicit content value assumption in D-DISCR construction
**ASN-0075, "Why the Provenance Relation Is Load-Bearing"**: The agreement table states "C value at a: the K.α-supplied value v_a" in column 1 and "same" in column 2, implicitly assuming both K.α calls in Histories 1 and 2 supply identical values v ∈ Val.
**Problem**: K.α takes v ∈ Val as a parameter (a free choice by the caller). The agreement of `C_1 = C_2` at `a` depends on identical values being supplied. This choice is required for the counterexample to work but is not stated explicitly in the construction's prose.
**Required**: Add a sentence to the construction (before the histories) stating that both K.α calls supply the same value v_a ∈ Val, so that C_1(a) = C_2(a) and the agreement on C holds.

### Issue 2: "Immediately following" overstates bundling requirement
**ASN-0075, "Why the Provenance Relation Is Load-Bearing"**: "K.α must be bundled with an immediately-following K.μ⁺/K.ρ pair into a single composite, because K.α's frame leaves M unchanged".
**Problem**: J0 is a composite-boundary coupling, evaluated only between the initial and final states of a composite. The K.μ⁺ must be in the *same composite* as K.α to satisfy J0 at the composite boundary — but it need not "immediately follow"; other elementary steps may intervene within the composite.
**Required**: Replace "immediately-following" with "subsequent within the same composite" (or similar). The bundling requirement is *same-composite*, not *adjacent*.

### Issue 3: Bijection between equivalence classes and witness runs left implicit
**ASN-0075, "Actionability (D-ACT)"**: The decomposition argument establishes that I-adjacency partitions the deletion set into equivalence classes, and that the union over runs recovers the deletion set. The uniqueness of the *run collection* (as opposed to the partition) requires the bijection: each class corresponds to exactly one run.
**Problem**: The text states "the partition is unique" and "conversion in either direction is determinate", but does not explicitly identify how a class maps to a run (i_start = T1-minimum of class; ℓ = |class|), nor that this assignment is a bijection. A reader has to infer the construction.
**Required**: Add a sentence: "Each equivalence class C corresponds to a unique witness run (i_start_C, ℓ_C, origin_C) where i_start_C is the T1-minimum of C, ℓ_C = |C|, and origin_C is the shared origin of C's members; this assignment is a bijection between classes and witness runs."

### Issue 4: D-ORG section heading mismatch with claim table label
**ASN-0075, "Origin Traceability" section heading vs. table**: Section heading uses "D-ORIG" but text refers to "D-ORG" indirectly — actually, all references are consistent. (On re-check, this is not an issue.) [Withdrawn — section uses "D-ORIG" consistently.]

## OUT_OF_SCOPE

None. The ASN appropriately defers DELETE mechanics, fork/COPY mechanics, link semantics, version DAG, and replication to other ASNs (as listed in scope notice and Open Questions).

VERDICT: REVISE
