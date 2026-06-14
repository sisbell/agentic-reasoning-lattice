## Assessment

This is a strong, builder-actionable digest that stays at design altitude and gets the note's hardest content right. Several sections are genuinely excellent and I'll flag them so the reviser doesn't touch them:

- The **T4c-separability analysis** (in *Implementation approaches* and *How it fits*) is faithful to the note's most subtle move: that Partition does *not* premise T4c, that mutual-exclusion needs no injectivity ("unnecessary, not circular"), that reading membership off the bijection's domain *would* be circular, and that the per-predicate correspondence postconditions are semantic-equivalence theorems — not "reporting only." This is the part most digests would botch; this one nails it.
- The **sum-type-makes-the-lemmas-true-by-construction** insight, and the reduction of Partition to "the scan computes `zeros` and the clauses correctly," is the right load-bearing engineering call.
- **"Scan, not a parse; the bound is on zero-count, not length; a Node is unbounded"** correctly preempts the natural misread that addresses are tiny.
- The **one-place `Account(t)` vs. two-place containment (`tumbleraccounteq`) vs. ownership (`isthisusersdocument`)** layering, and locating the "structural ≠ ownership" hazard at the *containment* layer, is precise and well-grounded in the evidence.
- The **empty-tumbler escalation** (well-formed ≠ decided; surface to T0/T4, don't silently resolve) is a real upstream gap handled at the right altitude.

All Green claims are grounded in the evidence; no fabrication. Forced-vs-conventional is correctly assigned throughout. I found no material defects — only sharpenings.

## Revision list

1. **`[SHARPENING]` *Guarantees to uphold* omits name-faithfulness from the checklist.** The section lists totality, Partition, Off-Domain Vacuity, level stability, and depth ceiling — but not the level-correspondence guarantee (`Account(t) ⟺ t is a T4c account address` on the valid subdomain), which the digest itself elsewhere calls load-bearing ("relied on by any consumer trusting that `Account(t)` denotes a T4c account address"). A builder treating this section as the contract checklist will miss it. Add a line: *Name faithfulness — the four labels genuinely denote T4c's address classes (semantic-equivalence theorems); largely inherited from T4c given a correct `zeros` computation, but it is the warrant that `Account` etc. mean what consumers assume.*

2. **`[SHARPENING]` Green-interop clause attribution is imprecise and mildly self-inconsistent.** "Scan such an array raw and it trips the leading-zero clause immediately … long before any trailing zeros could read as an adjacent-zero pair; the firing clause is leading-zero, not adjacent-zero" — but the leading `{0,0,0,0}` block is *itself* a run of adjacent zeros, so adjacent-zero fires at the front too (and `zeros ≤ 3` is blown). This also sits in tension with the digest's own *Decisions* point that violations co-occur (`[0,0]` violates leading, trailing, *and* adjacent). Restate as: *leading-zero is detected first in a left-to-right scan, but adjacent-zero and over-depth fail too — the takeaway is unchanged: decode the encoding before scanning, since a raw Green array never satisfies T4-valid.* Keep the (correct) point that the trailing pair is not the operative failure.

3. **`[SHARPENING]` *How it fits* opening lumps T4c with the always-consumed inputs.** "It consumes `zeros(t)`, T4's validity clauses, and T4c's level↔zero-count correspondence" reads as if the core classification depends on T4c. The next two sentences correct it, but scope the opening to match: the core (validity + level) consumes `zeros(t)` and T4's clauses only; **T4c is consumed solely by the correspondence postconditions** (via T4b/T3), and Partition is derived here without it.

(Optional, not worth a numbered item: the "four-zero leading header" framing is an inference from two literals — both *do* start with exactly four zeros, so it's consistent with the evidence; leaving it as-is is fine, though "a fixed leading zero block" would hedge the header semantics the evidence doesn't spell out.)

VERDICT: CONVERGED
