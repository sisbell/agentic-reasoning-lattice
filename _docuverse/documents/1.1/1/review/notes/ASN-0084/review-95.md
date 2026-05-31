# Review of ASN-0084

## REVISE

### Issue 1: Per-region displacement uniformity is derived twice
**ASN-0084, "Displacement Analysis" Remark and "R-COMM"**: The Remark states "Read off the explicit R-PPERM and R-SPERM formulas, the offset j within a region cancels, so every position in a region moves by the same direction and distance." R-COMM then proves "π(v + k) = π(v) + k ... Every position in a region receives the same ordinal displacement."

**Problem**: These are the same fact (offset-independence of the per-region map) established by the same argument (associativity of the shift), once informally in the Displacement section and once formally as R-COMM. No proof consumes the Remark — R-BLK cites R-COMM. The two statements in different words are exactly the redundancy the anti-bloat classifier targets.

**Required**: Drop the uniformity claim from the Displacement Remark and have it point to R-COMM, or collapse the informal restatement. Keep only the direction/distance table, which is the genuine derived consequence.

### Issue 2: Phase-3 reassembly content lodged in the Phase-1 (Split) slot
**ASN-0084, "R-BLK," Phase 1**: The labeled paragraph "*Non-S runs are carried verbatim.*" sits under *Phase 1: Split* but asserts a Phase-3 fact ("Phase 3 carries b through unchanged ... which inherits S8-cons under M'(d)"). Phase 2 then says "shown above" and Phase 3 says "carried verbatim, as established in Phase 1."

**Problem**: A reassembly conclusion is stated in the splitting slot, and two later phases defer back to it. Only the "no cut falls in V(b), so Phase 1 never splits b" clause is Phase-1 content; the carry-through and S8-cons claims belong to Phase 3. Bundling them forces the reader to hold a Phase-3 result while reading Phase 1.

**Required**: Keep in Phase 1 only the non-splitting fact (CS3 ⇒ no cut in a non-S run). Move the verbatim-carry and S8-cons-inheritance statements to Phase 3 where they are used, removing the cross-phase deferrals.

## OUT_OF_SCOPE

### Topic 1: Composition of rearrangements and k>4 cuts
**Why out of scope**: Whether two rearrangements compose into one, and the natural permutation class for k>4 cuts, are new territory already captured in the Open Questions, not defects in this ASN's three/four-cut treatment.

VERDICT: REVISE
