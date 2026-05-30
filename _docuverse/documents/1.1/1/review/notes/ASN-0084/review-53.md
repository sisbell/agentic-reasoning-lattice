# Review of ASN-0084

## REVISE

### Issue 1: B' mis-presented as the witness that "discharges the S8 existence clause"
**ASN-0084, R-SP (RearrangeSufficientPrecondition)**: "*…S8 (CorrespondenceRunPartition) with its clauses S8-uniq … and S8-cons … — with the constructive witness B' = R-BLK(B) discharging the S8 existence clause*"

**Problem**: S8 of the foundation states that the **maximal** runs partition `dom(Σ.M(d))` and that the maximal-run decomposition is **unique** — that is its entire content. The ASN itself preserves every precondition S8 requires of the post-state: `dom(M'(d)) = dom(M(d))` (so S8-fin, S8a, S8-depth carry over), S2 via bijectivity of π, and S3 via R-RI. Once those preconditions hold, foundation S8 applies to `M'(d)` directly and gives the unique maximal partition *for free*. Meanwhile R-BLK's `B'` is explicitly **not** maximal ("The partition B' is valid but not necessarily maximal… B' may contain V-adjacent, I-adjacent pairs"). So `B'` neither needs to, nor does, discharge S8 as the foundation states it — it is not the object S8 names. Presenting `B'` as "the constructive witness discharging the S8 existence clause" is a category mismatch: the obligation is already met by the foundation, and the supplied witness is the wrong (non-maximal) object.

**Required**: Reframe the S8 clause of Q. State that post-state S8 (existence + uniqueness of the maximal decomposition) follows directly from foundation S8 because the ASN preserves S8's preconditions. Demote R-BLK from "the S8 witness" to what it actually is — a description of how runs transform that exhibits *a* valid (non-maximal) partition. Remove the claim that `B'` discharges S8.

### Issue 2: Triple-stated "displacement is descriptive, R-COMM does the work"
**ASN-0084, Displacement Analysis (intro), Displacement Analysis (Remark), and R-BLK Phase 3 (commentary)**: the same point is made three times: "*These magnitudes are descriptive… they drive no postcondition… the operational within-region commutation that Phase 3 of R-BLK consumes is supplied by R-COMM, not by the displacement values*"; "*The per-region uniformity recorded here is exactly the same-region commutation that R-COMM (below) establishes operationally*"; "*the operational content Phase 3 consumes is the same-region commutation … supplied by R-COMM, not any arithmetic on the displacement magnitudes.*"

**Problem**: Three paragraphs in three locations assert the identical meta-claim (displacements are descriptive; R-COMM is operational) and all defer to the same downstream location (R-COMM). This is precisely the "multiple paragraphs deferring to the same downstream location" / "two paragraphs say the same thing in different words" accretion pattern.

**Required**: State once (at the Displacement Analysis remark, where the magnitudes are defined) that the magnitudes are descriptive and that R-COMM supplies the operational commutation. Delete the duplicate disclaimers in the intro and in Phase 3.

### Issue 3: Paragraph imagining the w_μ = 0 case the precondition excludes
**ASN-0084, end of "The 4-Cut Swap Permutation"**: "*the 4-cut postcondition formulas (R-S1, R-S2, R-S3) reduce to the 3-cut formulas (R-P1, R-P2) when w_μ is set to zero… However, the preconditions prevent this degenerate case from arising: CS2 requires c₁ < c₂, so w_μ ≥ 1.*"

**Problem**: This constructs a case (w_μ = 0) that CS2 already excludes, then notes it is excluded — the "paragraph imagines a case the precondition already excludes" pattern. It advances no reasoning about the operation as specified.

**Required**: Cut the degenerate-reduction paragraph, or compress to a one-line note that the two forms are distinct primitives (which the surrounding sentence already says).

### Issue 4: R-CS3 conclusion restates its own body
**ASN-0084, R-CS3**: body — "*The genuine load-bearing role of CS3 is that it is the sole clause fixing the single subspace S that R-PRE(iv) quantifies over*"; conclusion — "*CS3 is load-bearing not as a width guard but as the clause that makes 'the subspace S' of R-PRE(iv) well-defined and keeps the cut sequence disjoint from the inert frame.*"

**Problem**: The "Conclusion" paragraph repeats the load-bearing-role sentence already stated mid-lemma, in different words. Same claim, twice.

**Required**: Keep one statement of CS3's role and delete the restating conclusion.

### Issue 5: "Identity convention covers the j = 0 case" re-derived repeatedly
**ASN-0084, Split, Merge, R-COMM, Subspace confinement, Extended Associativity, Reduction of compound shifts**: each re-runs the same j ≥ 1 (via TS3) / j = 0 (via identity convention) bifurcation ("*When k ≥ 1, associativity (TS3) gives…; when k = 0, … by the identity convention*").

**Problem**: The identical two-case split between OrdinalShift (n ≥ 1) and the local `shift(v,0):=v` convention is reconstructed at half a dozen sites. Once Extended Associativity is established (as the ASN does, covering j or k = 0), downstream proofs should cite it rather than re-deriving the j = 0 branch each time.

**Required**: Establish the n ≥ 0 shift algebra once (Extended Associativity already does this for composition; add the analogous one-line closure for the other operators), then cite it. Remove the per-site re-derivations of the j = 0 case.

### Issue 6: Definition/consequence prose enumerating downstream consumers
**ASN-0084, "Consequences of R-PRE — Subspace confinement"**: "*The shifted positions `c₀ + j`, `c₁ + j`, `c₂ + j` named in R-P1, R-P2, R-S1, R-S2, R-S3 retain subspace S…*"; and R-NS(NS-inv) "*Catalogue*" plus "*the content-store invariants (S0, S1, S4, S5, S7a, S7b, S7d)… appear here only for completeness.*"

**Problem**: These passages inventory use-sites and enumerate which invariants are/aren't consumers ("appear here only for completeness" is self-identified filler) rather than advancing the claim. This is the "enumerate downstream consumers" / use-site-inventory accretion pattern.

**Required**: State subspace confinement as the property (cut images stay in S by CS3 + OrdShiftHom(b)) without the R-P1…R-S3 site list. In NS-inv, drop the completeness-only catalogue entries; keep only invariants whose preservation needs an argument.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: The Open Questions correctly defer the k > 4 generalization and the algebra of composing rearrangements; these are new operations, not gaps in the 3-/4-cut specification given here.

### Topic 2: Operational recovery of the maximal (canonical) partition from B'
**Why out of scope**: Characterizing which run pairs in `B'` merge, and proving confluence of exhaustive merging, is legitimately future work — provided Issue 1 is fixed so the ASN does not lean on `B'` to discharge S8 in the first place.

META: The core mathematics (region partition, π, R-COMM, R-BLK transformation, worked examples) defines real state-transition guarantees and stays in-scope; the problems are framing overclaim (Issue 1) and accreted meta-prose, both fixable, so this is not a termination case.

VERDICT: REVISE
