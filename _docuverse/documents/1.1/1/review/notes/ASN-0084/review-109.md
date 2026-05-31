# Review of ASN-0084

## REVISE

### Issue 1: Displacement Analysis Remark duplicates its own bullet derivation
**ASN-0084, "Displacement Analysis," Remark**: "*Remark (per-region displacement uniformity).* Read off the explicit R-PPERM and R-SPERM formulas, the offset j within a region cancels, so every position in a region moves by the same direction and distance — the displacement depends only on the region widths…"

**Problem**: The remark's load-bearing claim ("the offset j within a region cancels") is then re-asserted verbatim at the end of every bullet that follows it ("In each case j cancels," "In every case j cancels"). This is the two-paragraphs-say-the-same-thing pattern: the topic sentence and the per-bullet conclusions state the identical fact. The remark adds no reasoning the bullets do not already carry.

**Required**: Either delete the remark and let the bullets stand, or delete the per-bullet "j cancels" tails and let the remark cover them once. Do not keep both.

### Issue 2: A trivially-answerable question is left open, weakening the precondition analysis
**ASN-0084, "Open Questions"**: "what does R-PRE(iv) guarantee beyond what D-SEQ already supplies — given that D-SEQ alone makes every region a well-defined cardinality and keeps source references within V_S(d)?"

**Problem**: This is posed as open territory, but it is a one-line consequence of material already in the ASN. By D-SEQ, V_S(d) = {[S,k] : 1 ≤ k ≤ N}; R-PRE(iv) quantifies over depth-2 subspace-S positions in [c₀, c_{n−1}). Given D-SEQ, R-PRE(iv) is satisfied **iff** every ordinal in [ord(c₀), ord(c_{n−1})) is ≤ N, i.e. iff `ord(c_{n−1}) ≤ N + 1`. So R-PRE(iv) adds exactly the bound that the affected range not exceed existing content by more than one position — the EXT-VAC case being its boundary. The depth standard requires resolving non-trivial precondition relationships, and this one resolves in a sentence; leaving it as "open" understates the analysis the ASN has already done. (The full wp for the invariant suite Q is genuinely open — see below — but this sub-question is not.)

**Required**: State inline (e.g., in "Consequences of R-PRE" or beside R-PRE(iv)) that, under D-SEQ, R-PRE(iv) is equivalent to the single bound `ord(c_{n−1}) ≤ N + 1`. Remove this from Open Questions or narrow it to the genuinely-open wp question.

## OUT_OF_SCOPE

### Topic 1: Weakest precondition for the full invariant suite Q
**Why out of scope**: Computing the complete wp for REARRANGE_K against the post-state invariant suite (including any future link/version invariants) is new analytical territory, not a defect in the present operation's proof. R-PRE is shown *sufficient* throughout; *weakest* is a separate obligation, correctly deferred.

### Topic 2: k-cut rearrangements (k > 4) and composition of rearrangements
**Why out of scope**: The generalization and the algebra of composing rearrangements are genuinely new operations, appropriately left to a future ASN.

VERDICT: REVISE

The mathematical core is sound: I verified the pivot/swap tilings, R-PIV/R-SWP well-definedness, R-PPERM/R-SPERM bijectivity (finite self-injection ⇒ bijection), R-COMM's per-region commutation, R-BLK's split-classify-reassemble (every interior cut splits, so no run straddles a region), and R-CANON's forward/backward no-extension argument. The six worked examples each check out against the postconditions, and the prior declined findings (OrdShiftHom citation, Phase-1/Phase-3 misplacement) are no longer present. The two REVISE items are a prose duplication and an under-stated precondition consequence, not correctness defects.
