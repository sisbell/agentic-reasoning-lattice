# Review of ASN-0093

## REVISE

### Issue 1: Operation Frame clauses carry invariant-preservation rationale that duplicates the discharge matrix
**ASN-0093, K.α (ContentAllocation), Frame**: "`Frame: L' = L; M' = M` (so C2 at `Σ` transfers to `Σ'`: `origin(·) ∈ dom(M)` implies `origin(·) ∈ dom(M')`)" — and identically in K.λ's Frame: "(so L1a at `Σ` transfers to `Σ'`: `origin(·) ∈ dom(M)` implies `origin(·) ∈ dom(M')`)".
**Problem**: The parenthetical is proof rationale (why C2 / L1a survive the transition) placed in the operation's structural Frame slot. The Frame slot's job is to state what is held fixed (`M' = M`), not to re-prove an invariant's preservation. The actual preservation argument already lives in the discharge matrix — the C2/K.α cell ("Preserved at prior keys … M1 extends `dom(M)`") and the L1a/K.λ cell ("Prior keys preserved by M1"). This is the anti-bloat "defensive justification … essay content in structural slots" pattern: the same preservation claim stated in two places, with the operation spec carrying discharge content that belongs in the matrix.
**Required**: Reduce both Frame clauses to the frame assertion (`L' = L; M' = M`, resp. `C' = C; M' = M`) and let the discharge matrix carry the C2/L1a preservation argument.

### Issue 2: The Discharge section's framing paragraph restates what the matrix is rather than advancing the proof
**ASN-0093, "Simultaneous-induction framing"**: "The inductive step for the stated invariants is recorded as a per-(invariant, transition) matrix; entries describe how each transition kind preserves or discharges each invariant."
**Problem**: The non-circularity setup (IH = conjunction of all properties, simultaneous induction) is load-bearing and should stay. But the quoted sentence's second clause — "entries describe how each transition kind preserves or discharges each invariant" — describes the matrix's structure, which the matrix itself makes evident. This is meta-prose narrating the document's own layout, not reasoning.
**Required**: Drop the clause describing matrix entries; keep only the simultaneous-induction justification that the IH is the conjoined set of properties (the part that establishes non-circularity).

## OUT_OF_SCOPE

### Topic 1: Disjointness of `dom(M)` from `dom(C) ∪ dom(L)`
**Why out of scope**: The substrate proves SD (`dom(C) ∩ dom(L) = ∅`) but never asserts that document addresses (`zeros = 2`, M0) are distinct from content/link addresses (`zeros = 3`, C1/L1). It follows immediately from T4c level determination and is not consumed by any proof here (freshness compares only against `dom(C) ∪ dom(L)`), so it is a candidate invariant for a higher layer, not a gap in this note.

VERDICT: REVISE
