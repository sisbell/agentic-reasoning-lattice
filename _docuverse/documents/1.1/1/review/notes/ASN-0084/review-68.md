# Review of ASN-0084

## REVISE

### Issue 1: R-CS3 redundancy claim is false — misses the case where the *first* cut is already in a higher subspace

**ASN-0084, R-CS3 (SubspaceConfinementRedundancy)**: "every cut sequence that violates CS3 ... is already excluded by CS2 together with R-PRE(iv) ... The precondition is then unsatisfiable. Consequently CS3 is redundant with CS2 + R-PRE(iv)."

**Problem**: The proof only establishes unsatisfiability when `c₀` lies in subspace 1. Its unsatisfiability argument writes the R-PRE(iv) range as `subspace(v)=1 ∧ #v=2 ∧ [1,2] ≤ v < [2,1]` and concludes it "contains every [1,k] with k ≥ 2" — but that conclusion requires `c₀` to be a subspace-1 position so that `c₀ ≤ v` has subspace-1 solutions.

Consider instead `K = ([2,1], [2,2], [2,3])` with `V_1(d) ≠ ∅`:
- CS1 (n=3) ✓, CS2 (strictly ordered) ✓, CS4 (depth 2) ✓, CS3 ✗ (all cuts in subspace 2).
- R-PRE(i),(ii) ✓.
- R-PRE(iv): every subspace-1 depth-2 position `v` satisfies `v < [2,1] = c₀` (since `1 < 2` dominates), so **no** `v` satisfies `c₀ ≤ v < c_{n−1}`. The quantification is **vacuously true**, not unsatisfiable.

So this CS3-violating sequence satisfies the entire remainder of R-PRE (the regions simply collapse to `w_α = w_β = 0`, and R-PRE only derives non-degeneracy *from* clause (iii), which includes CS3). CS3 is the **only** clause rejecting it. The lemma's central claim — "no CS3-violating cut sequence satisfies the rest of R-PRE at all" — is therefore false, and the "Every CS3-violating cut sits at c_{n−1}" step does not save the argument: when `c₀` itself is in subspace ≥ 2, R-PRE(iv) degenerates to vacuity rather than to an infinite obligation.

**Required**: Either (a) retract the redundancy claim and present CS3 as load-bearing (it rejects all-higher-subspace cut sequences that the other clauses admit vacuously), or (b) strengthen R-PRE(iv)/the cut-sequence definition so that `c₀` is tied into `V_S(d)` (e.g. `c₀ ∈ V_S(d)`), and then prove the redundancy covers *both* the `c₀`-in-subspace-1 and `c₀`-in-higher-subspace cases explicitly.

### Issue 2: Forward-reference accretion (anti-bloat classifier)

**ASN-0084, R-NS and its table row / R-BLK (NS-run)**: R-NS states "its consequence for the run partition is discharged in place within R-BLK," then "We invoke these four facts ... as *(NS-run)* in Phases 2 and 3"; the Properties table repeats "The verbatim carry of non-S runs into B' is discharged in place within R-BLK as (NS-run)"; R-BLK then re-cites *(NS-run)* in Phases 2 and 3.

**Problem**: A single lemma's downstream consumers are inventoried in three separate locations (lemma prose, table row, consumption site), matching the flagged patterns "a definition's introduction enumerates downstream consumers" and "multiple paragraphs defer to the same downstream location." The reader must hold the deferral across sections to follow what R-NS actually delivers.

**ASN-0084, "Redundancy of CS3" intro + "Redundancy, not necessity"**: Two paragraphs explain the *nature* of the result ("a redundancy observation, not a necessity claim," "an unsatisfiable precondition is benign," "we retain it ... for readability ... but its presence is not load-bearing") rather than advancing the proof — the "explains why the clause is/isn't needed rather than what it asserts" pattern.

**Required**: State R-NS's non-S consequence once at its point of use in R-BLK; drop the table-row and lemma-prose forward inventories. Replace the CS3 meta-commentary with the corrected status (per Issue 1) stated plainly.

## OUT_OF_SCOPE

### Topic 1: Composition of multiple rearrangements
Whether two REARRANGE_K applications compose to a single rearrangement (raised in Open Questions) is genuinely new territory — a future ASN, not a gap here.

### Topic 2: k-cut rearrangements for k > 4
The generalization beyond pivot/swap is correctly deferred.

### Topic 3: Operational recovery of the maximal partition from B'
R-BLK produces a valid (non-maximal) B' and defers the merge-to-canonical reduction to foundation S8 plus a future ASN. This deferral is legitimate, not an error in this ASN.

VERDICT: REVISE
