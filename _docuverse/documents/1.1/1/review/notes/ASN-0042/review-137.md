# Review of ASN-0042

I checked the proofs of O1–O18 and the derived claims, traced the State-Axiom inductions, and verified the Worked Example arithmetic against the construction. The mathematical content is sound — the longest-match machinery, the delegation predicate, the O10 fork construction, and the non-coverage analysis all hold under their stated reachability quantifiers. The findings below concern accretion the anti-bloat classifier flags, not logical defects.

## REVISE

### Issue 1: Per-claim forward pointers duplicate the consolidated proof header
**ASN-0042, "Ownership as a Structural Predicate" (O1b) and "The Account-Level Boundary" (O1a)**: O1b's body, after stating the formula, adds: "It is proved by the shared induction in *State Axioms* (*Shared invariant induction*), jointly with O1a and T4-validity." O1a is likewise stated in one section and proven in another, with the same downstream target.
**Problem**: This is forward-reference accretion of the exact flagged shape — "multiple paragraphs in different sections defer to the same downstream location" and "a definition's introduction enumerates downstream consumers." The deferral is doubly redundant: the proof site already announces its inputs in its own header, "**Shared invariant induction (O1a / O1b / T4-validity)**." The claim→proof pointer and the proof→claims enumeration restate the same coupling in both directions; one of them is noise. The sentence does not advance O1b's statement (the formula above it is complete).
**Required**: Drop the per-claim "proved by the shared induction... jointly with..." sentences. The consolidated header in *State Axioms* already names its three discharged invariants; let it be the single site of the coupling.

### Issue 2: Defensive justification of example seed data in a setup slot
**ASN-0042, Worked Example, "Bootstrap seeds"**: "The bootstrap deliberately seeds `[1, 0, 1]` precisely so `[1, 0, 2]` is the next-reachable baptism; without it the stream-predecessor would be missing and O17b's branch could not register `[1, 0, 2]`."
**Problem**: This is a defensive justification pre-empting a reader's "why is this seed present?" rather than advancing the verification. It also duplicates content already discharged downstream: the condition-(v) verification in the *Delegation* milestone computes `children(Σ₀.B, [1], 2) = {[1, 0, 1]}`, `hwm = 1`, `next = [1, 0, 2]` explicitly. The "deliberately seeds... precisely so... without it... could not register" prose restates that computation in essay form in a table-adjacent structural slot.
**Required**: State the seed in the table and let the existing condition-(v) `next(Σ₀.B, [1], 2) = [1, 0, 2]` computation carry the reasoning. Remove the explanatory sentence.

## OUT_OF_SCOPE

None. The ASN stays within ownership state, the delegation operation, and ownership invariants; it does not stray into modification rights, content storage, or the baptism mechanism (it consumes ASN-0040's `next`/`hwm`/B6 as a foundation rather than redeveloping them).

VERDICT: REVISE
