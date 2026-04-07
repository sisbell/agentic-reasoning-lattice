# Review of ASN-0054

## REVISE

### Issue 1: Decomposition effect paragraph misplaced under COPY
**ASN-0054, Preservation Under Operations / COPY**: "**Effect on the canonical decomposition.** A run whose V-positions lie entirely within one region moves as a unit — its V-span shifts but its I-span is unchanged. A run straddling a cut boundary splits at the cut point..."
**Problem**: This paragraph describes REARRANGE's decomposition effects — it references regions, cuts, `rearrangend`, and "no coalescing pass follows the rearrangement." It is placed under the COPY heading. REARRANGE has no decomposition-effect paragraph of its own, and COPY's actual decomposition effect (identical to INSERT's: at most one existing run splits, transcluded content introduces new runs) is never stated.
**Required**: Move this paragraph to the REARRANGE section. Add a brief decomposition-effect paragraph for COPY noting that its V-space mechanics and decomposition effects are identical to INSERT's (differing only in I-address provenance).

### Issue 2: A0 invariant status not formally declared
**ASN-0054, A0 (V-Domain Contiguity)**: "This is the fundamental structural property of arrangements."
**Problem**: A0 is described as fundamental but never formally declared as a per-state invariant alongside S2, S3, S8a, S8-depth, and S8-fin. The operations section verifies preservation for four specific composites, but A0 is not integrated into the transition system. A raw K.μ⁺ that adds a non-contiguous V-position would satisfy all of ASN-0047's preconditions (S8a, S8-depth, S8-fin, referential integrity) while violating A0. Without declaring A0 as a required postcondition of K.μ⁺ and K.μ~, the invariant floats outside the formal system it depends on.
**Required**: State explicitly that A0 is a per-state invariant of all reachable states (in the same category as S2, S3, etc.). Note that K.μ⁺ and K.μ~ preconditions must be extended to require that the resulting arrangement satisfies A0 — this is the formal mechanism that closes the gap between "FEBE operations preserve A0" and "all reachable states satisfy A0."

### Issue 3: No concrete worked example
**ASN-0054, entire note**
**Problem**: Twelve properties and four operation effects are introduced without verifying any against a specific numerical scenario. The Shakespeare example is a narrative illustration, not a verification. None of A0–A12 is checked against a concrete arrangement.
**Required**: At minimum, one worked example: a specific document with named V-positions and I-addresses, its canonical decomposition computed explicitly, and one operation (INSERT or DELETE) applied with the post-state decomposition verified against A3–A7. For instance: document d with M mapping [1,1]→[3,0,1,0,5], [1,2]→[3,0,1,0,6], [1,3]→[3,0,1,0,8] — show that the break set is {v₂}, the canonical decomposition is two runs R₁=([1,1],[3,0,1,0,5],2) and R₂=([1,3],[3,0,1,0,8],1), and verify A6 partition and A7 width preservation concretely.

### Issue 4: DELETE decomposition omits single-run-spanning-both-boundaries case
**ASN-0054, DELETE / Effect on the canonical decomposition**: "A run straddling the left boundary of the deletion is truncated (its right portion is removed). A run straddling the right boundary is truncated (its left portion is removed). At most two runs are truncated — one at each boundary."
**Problem**: When a single run R = (v_s, a, r) contains the entire deleted range (s < j and s + r > j + w), that one run is affected at both boundaries, producing a left survivor [s, j) and a right survivor [j+w, s+r). These survivors are never I-adjacent (the gap of w deleted I-positions separates them), so they remain distinct runs in the post-state. The phrasing "at most two runs are truncated — one at each boundary" suggests two different runs are involved; the single-run case where one run produces two survivors is not stated.
**Required**: Add an explicit note: when a single run spans both deletion boundaries, it splits into two I-non-adjacent survivors (since the w deleted I-positions create an I-gap of width w between them).

### Issue 5: "FEBE operations" undefined
**ASN-0054, Preservation Under Operations**: "We verify that the FEBE operations preserve A0."
**Problem**: The term "FEBE operations" is used without definition. Whether this means exactly {INSERT, DELETE, REARRANGE, COPY} or includes MAKELINK and others is ambiguous. Formal claims should not depend on undefined terms.
**Required**: Define "FEBE operations" on first use, or replace with an explicit enumeration: "the four arrangement-modifying operations: INSERT, DELETE, REARRANGE, and COPY."

## OUT_OF_SCOPE

### Topic 1: Formal definition of editing operations as composite transitions
**Why out of scope**: The ASN correctly treats INSERT, DELETE, REARRANGE, and COPY as informally described composites and verifies A0 preservation. The formal decomposition of each operation into elementary transitions (K.α, K.μ⁺, K.μ⁻, K.μ~, K.ρ) with explicit precondition threading is a future ASN's work.

### Topic 2: Link subspace invariants
**Why out of scope**: The ASN explicitly restricts to the text subspace (v₁ ≥ 1) and lists link subspace invariants as an open question. Link addresses may have different structural properties (permanent, gap-tolerant) requiring separate treatment.

VERDICT: REVISE
