# Review of ASN-0110

## REVISE

### Issue 1: RE-conform contradicts RE-arity/RE-zero at the empty store

**ASN-0110, RE-conform (remark) and RE-arity**: RE-arity states "When `dom(Σ.L) = ∅` the tuple is empty" (length `N_max(Σ) = 0`). RE-conform then claims Gregory's fixed three-slot implementation "meets the contract for every store it can represent," reconciled by the clause "the empty-slot-in-position discipline supplies any missing standard slot."

**Problem**: The empty link store is in the conformance sub-class. RE-conform scopes Gregory's conformance to "the sub-class of stores whose links are all arity 3"; the empty store satisfies this vacuously (no link violates arity 3), and it is the initial state `L₀ = ∅` (ASN-0047), hence definitely representable. But on the empty store the spec mandates the *empty tuple* `⟨⟩` (RE-arity, RE-zero: `N_max(Σ) = 0`), whereas a fixed three-slot implementation emits `⟨∅, ∅, ∅⟩` (length 3). These differ, so Gregory does **not** "meet the contract for every store it can represent." The reconciling clause "the empty-slot-in-position discipline supplies any missing standard slot" is itself wrong here: that discipline only fills positions *within* `1..N_max(Σ)` (RE-arity), so at `N_max = 0` it supplies nothing — there are no slot positions in the spec tuple for the discipline to populate. Note also that because L3 forces every link to arity `≥ 3`, a nonempty store always has `N_max ≥ 3`; the only state with `N_max < 3` is the empty store, so the empty store is the precise and sole point where the reconciliation fails.

**Required**: Reconcile the two claims. Either (a) qualify RE-conform to exclude the empty store (restrict the conformance claim to nonempty all-arity-3 stores), or (b) change the length convention in RE-arity so the standard triple is a floor (e.g. length `max(3, N_max(Σ))`, matching Nelson's always-present from/to/type structure and Gregory's emission), updating RE-zero accordingly. In either case, remove or correct the "supplies any missing standard slot" gloss, which does not hold at `N_max = 0`.

## OUT_OF_SCOPE

### Topic 1: Contract for presenting returned endsets back in a querying document's V-coordinates
The ASN explicitly defers (Open Question 1, and the closing paragraph of the V-space section) the lossy V-presentation projection of a returned endset when the document arranges only part of its coverage.
**Why out of scope**: This is a distinct projection layer on top of endset retrieval, properly future work, and the ASN correctly leaves it to the open questions rather than asserting a contract.

VERDICT: REVISE
