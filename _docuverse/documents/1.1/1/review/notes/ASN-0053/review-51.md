# Review of ASN-0053

## REVISE

### Issue 1: Use-site inventory and blanket forward justification in "The reach function"
**ASN-0053, The reach function**: "Existence of a width w with a ⊕ w = b — and the identity w = b ⊖ a — holds exactly when the additional length condition #a ≤ #b is met (D1, ASN-0034); uniqueness of that width is D2 (ASN-0034). Every use in this ASN is level-uniform (#a = #b), so all three conditions hold throughout."

**Problem**: The closing sentence is a use-site inventory — a blanket pre-assertion that all downstream proofs satisfy D0/D1/D2's conditions. It advances no reasoning here, and it is redundant: WF, WR, S4, S5, S11, S11c each re-state and locally discharge exactly these conditions (#s = #r, divergence ≤ #s, etc.) at their own proof sites. This is the accretion pattern where an introduction enumerates its downstream consumers rather than the local discharges carrying the burden. The reader must skip the blanket claim to follow each proof, then re-encounter the same fact discharged properly in situ.

**Required**: Drop the "Every use in this ASN is level-uniform... so all three conditions hold throughout" sentence. Each theorem already discharges D0/D1/D2 preconditions where it uses them; the global assertion adds nothing the local proofs don't establish more precisely.

### Issue 2: Defensive narration of a foundation postcondition
**ASN-0053, The reach function**: "The subtraction itself is well-defined when a < b and divergence(a, b) ≤ #a (D0, ASN-0034); but D0's own postcondition shows the round-trip can fail (#a > #b → a ⊕ (b ⊖ a) ≠ b), so well-definedness of the subtraction does not by itself guarantee a width carrying a to b."

**Problem**: This re-derives and re-justifies foundation content (D0's conditional postcondition) defensively, to motivate why D1 is then cited. The worked counterexample after WR ("σ = ([1, 3, 5], [0, 2])... ≠ [0, 2]") already demonstrates the same failure mode concretely and is the legitimate vehicle for it. The prose narration duplicates that demonstration in abstract form.

**Required**: Collapse to a single sentence: the displacement is w = b ⊖ a, well-defined and round-tripping exactly when #a ≤ #b (D1) with uniqueness by D2. Let the WR counterexample carry the necessity of the length condition.

## OUT_OF_SCOPE

### Topic 1: Span-set difference bound (Open Question 7)
**Why out of scope**: The tight bound on |normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)| for general span-sets is correctly deferred; S11d closes only the two-span case, and the generalization is genuinely new territory.

### Topic 2: Cross-level intersection and subspace-boundary guarantees (Open Questions 2, 5)
**Why out of scope**: Every theorem here is gated on level-uniformity/level-compatibility, and that constraint is load-bearing (it is what licenses WF in S1, S3, S4, S11). Intersection/difference across hierarchical levels is a separate algebra, not a gap in this one.

---

The mathematics is sound. I verified SC exhaustiveness, the S1/S3 membership equalities, the S5 TA-assoc/TA-LC discharge chain, the S8 loop invariant (initialization, merge, emit, finalization) and its N1/N2 derivation, the full six-case S9 uniqueness argument, and the S11 boundary characterization plus its convexity-based tightness. All hold. Worked examples exercise both branches where it matters (S8 hits merge and emit; S11d covers all five SC cases). The only findings are accreted meta-prose flagged by the anti-bloat classifier.

VERDICT: REVISE
