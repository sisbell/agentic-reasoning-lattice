The dependency graph is clean and internally consistent: {AX-1, S0, AX-2} are independent axioms; S1 derives from S0 alone; S3 derives from AX-1, S1, and AX-2 via reachability induction. All Depends sections correctly reflect what each proof actually uses.

The inductive argument for S3 is sound. The two cases — inherited vs. new-or-redirected — are exhaustive and mutually exclusive given `v ∈ dom(Σ'.M(d))`: either `v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v)` (case 1) or its negation (case 2). AX-2's quantifier range is exactly the negation, so the application of AX-2 in case 2 is correctly licensed. S1 discharges case 1 cleanly: J0 gives `a ∈ dom(Σ.C)`, S1 lifts it to `dom(Σ'.C)`. The domain guard in AX-2's formal predicate is correctly motivated — without it, the sub-expression `Σ.M(d)(v)` is evaluated at a point outside `dom(Σ.M(d))` under strict partial-function semantics.

S3 invokes S1 transitively through S0 but does not need to directly cite S0: S1 encapsulates the S0→S1 derivation, and S3's Depends section correctly reflects direct dependencies only. No term shifts meaning across claims.

### S1 presented before its sole dependency S0

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: Document order — AX-2, S1, AX-1, S0, S3; S1 proof body — "By S0 (content immutability)..."
**Issue**: S1's proof cites S0 as its sole premise, but S1 appears before S0 in document order. A reader or linearizing tool traversing the document sequentially encounters S1's proof before S0 is formally stated. The Depends section correctly declares the dependency, so no logical gap exists. The dependency-respecting order for the five claims is: AX-1, S0, AX-2, S1, S3.
**What needs resolving**: N/A — dependency correctly declared; presentation order only.

VERDICT: OBSERVE