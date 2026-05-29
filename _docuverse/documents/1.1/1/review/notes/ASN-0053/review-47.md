# Review of ASN-0053

## REVISE

### Issue 1: "Bijection" asserted as a derived guarantee without derivation, conflating ordered and unordered pairs

**ASN-0053, paragraph following S3b**: "Together with S4a, this establishes that split and merge are exact inverses in both directions... The two operations form a bijection between single spans with a marked interior point and pairs of adjacent spans."

**Problem**: This is a synthesis/commentary paragraph that introduces a *new* claim — a bijection — without deriving it. The two lemmas do not cleanly support it as stated:
- S4 (split) produces an **ordered** pair: a left part λ and a right part ρ.
- S3b explicitly recovers only the **unordered** pair `{α, β}`, and goes out of its way to note that "the left-right assignment is reversed relative to Case A," i.e., the ordering is *not* preserved by merge-then-split.

A bijection requires its domain and codomain to be pinned down. As written, the map from (σ, interior point) lands in *ordered* adjacent pairs, but the round-trip lemma S3b only guarantees recovery of the *unordered* pair. The "bijection" is therefore not established by S4a + S3b; the ordered/unordered mismatch is glossed.

**Required**: Either (a) state and prove the bijection precisely — fix the codomain as ordered adjacent pairs ⟨α, β⟩ with reach(α) = start(β), and show S3b recovers the ordered pair in that restriction (Case A already does; the unordered framing is what muddies it) — or (b) delete the bijection sentence and let S4a and S3b stand as the two inverse directions, which is all the proofs actually deliver. This paragraph is also the clearest instance of the meta-prose the anti-bloat classifier targets: it advances no proof and asserts a guarantee the body does not derive.

## OUT_OF_SCOPE

### Topic 1: Span-set difference bound
The note already records this as an Open Question ("Does the general difference bound extend to span-set difference?"). Correctly deferred; not an error here.

### Topic 2: Cross-level intersection representability
S1's level_compat precondition correctly fences off the different-length case, and the note flags it as an Open Question. Properly scoped.

---

Remaining checks pass. SC exhaustiveness is complete; S0/S1/S3/S4/S5 discharge their foundation preconditions explicitly; S8's loop invariant correctly separates N1 (strict starts) from sortedness and grounds strictness in the emit condition; S9's six-way case split is exhaustive (the shared-start-and-reach configuration is correctly excluded via TA-LC) and each case reaches a clean contradiction; S11/S11a–d cover all five SC cases with the tightness argument for the two-span bound proven by convexity. Concrete examples exercise both branches of every multi-case proof, and the worked examples — including the WR unequal-length failure illustrating why level-uniformity is load-bearing — are legitimate, not bloat.

VERDICT: REVISE
