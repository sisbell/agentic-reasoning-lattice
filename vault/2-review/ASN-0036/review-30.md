# Rebase Review of ASN-0036

## REVISE

### Issue 1: S7 uniqueness claim incomplete for nesting-prefix allocators

**ASN-0036, Structural attribution (S7)**: "uniquely identifying the allocating document across the system (by T9 and T10, ASN-0034: T9 gives same-allocator monotonicity ensuring distinct documents within an allocator have distinct prefixes; T10 gives cross-allocator disjointness ensuring documents from different allocators cannot share a prefix)"

**Problem**: T10 requires non-nesting prefixes (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). For parent-child document allocators — where a parent spawns a child via `inc(·, k')` per T10a, producing a document whose prefix extends the parent's (e.g., `1.0.1.0.1` spawning `1.0.1.0.1.1`) — T10's premise is violated. S4 correctly handles this identical logical structure by citing T10a (child outputs are deeper), TA5(d) (`#inc(t, k') = #t + k'`), and T3 (different lengths yield different tumblers). S7 makes the same three-case uniqueness argument at the document level but covers only two of the three cases. Reviews 25–26 fixed this gap in S4; S7's parallel argument was not similarly updated.

**Required**: Add the nesting-prefix case to S7's body, following S4's three-case structure: same allocator (T9), non-nesting prefixes (T10), nesting prefixes (T10a + TA5 + T3). Update the registry to: `from S7a, S7b, T4, T9, T10, T10a, TA5, T3 (ASN-0034)`.

VERDICT: REVISE
