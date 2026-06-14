# Review of ASN-0134

This is a careful, self-aware note, and most of its proofs hold up under scrutiny: H0/H1/H2 cover the frontier conflict structure (including the first-emission boundary and nesting homes), A4/A5 keep step-tearing and batch-tearing properly separated, A6's per-state/transition-clause split is correct, the V2 banking argument and its §8 trace are sound, and the H3 disjoint-write vs distinct-element distinction is right. Two issues remain.

## REVISE

### Issue 1: The idem=⊤ duplicate is presented as a cross-home phenomenon, but it is home-independent

**ASN-0134, §9 clause 8 / M1(b) / §4 instance (i)**: 
> "Drop it and per-home MIC permits the duplicate: two **cross-home** coverage-equal idem = ⊤ emits may each read a stale A_K, both miss, and both deposit at their own home frontiers (no allocation collision, H1)…" (clause 8)
> "per-home clauses 1–7 alone permit a **cross-home** idem = ⊤ duplicate" (M1(b))

**Problem**: Every counterexample motivating clause 8 — §4 instance (i), M1(b)(ii), the clause-8 body — fixes two *distinct* homes. But the duplicate is not specific to the cross-home axis, and the note's own architecture entails this. Clause 2 is per-home and is scoped precisely to "the **frontier-read-and-deposit** of any two S-allocations to d." The dedup check is a global read of `A_K` that *precedes* the deposit and is not an allocation, so clause 2 does not serialize it — indeed *cannot*, since the dedup-read is global and clause 2 is the per-home clause (if clause 2 covered it, clause 2 would not be per-home, collapsing the very distinction the note builds on).

Consequently two **same-home** coverage-equal idem=⊤ emits X, Y into one `(d, s_L)` also both-miss-and-duplicate under clauses 1–7: X dedup-reads `A_K` (miss), Y dedup-reads a stale `A_K` before X's deposit (miss), then clause 2 serializes the two *deposits* to distinct slots φ, φ+1 — distinct addresses, no collision — leaving two coverage-equal active tuples at one home. The note's own I1a-breaking argument ("the second deposit's own pre-state already carries the first's coverage-equal tuple, so it is not a miss-against-its-own-pre-state — I1a's induction breaks exactly there") is stated in the cross-home scenario but is *entirely home-independent*; it applies verbatim to the same-home pair, where clause-2 spacing supplies the distinct addresses that H1 supplies cross-home.

This matters because same-home is the *primary* idem=⊤ use case (a retry, or two concurrent workers asserting the same edge in the same document). As written, the cross-home-only framing invites an implementer to conclude that clause 2's per-home serialization already suppresses same-home idem=⊤ duplicates — it does not.

**Required**: State the idem=⊤ duplicate as home-independent. Correct M1(b), §4 instance (i), and clause 8 to say clauses 1–7 permit an idem=⊤ duplicate *regardless of home* (cross-home via H1-distinctness of the two deposits; same-home via clause-2 spacing of the two deposits), with clause 8 required in both. The I1a-breaking argument is already general enough to carry the same-home case directly.

### Issue 2: Off-by-one in the anchor-separator index

**ASN-0134, §7 (and the H1 proof parenthetical)**:
> "b_C(d) = [1.0.1.0.1.0.1] carries the field-separator 0 at **index #d = 5**, whereas b_C(d') = [1.0.1.0.1.1.0.1] continues there with the nonzero digit 1 … so the anchors **diverge at index #d**." (§7)
> "b_S(d) carries the field-separator 0 **at index #d** … the anchors diverge at index #d." (H1)

**Problem**: Under the 1-indexed convention the foundation uses — ASN-0093's `DisjointSubAllocatorChains` places s_C at position `#d + 2`, so the field-separator preceding it sits at `#d + 1` — the separator is at `#d+1`, not `#d`. Checked against the note's own nesting pair (d = [1.0.1.0.1], #d = 5; d' = [1.0.1.0.1.1]): b_C(d) and b_C(d') both carry the document digit `1` at position 5 and therefore **agree** at index #d; they first diverge at position 6 = #d+1, where b_C(d) has the separator `0` and b_C(d') has the continuation `1`. So the stated divergence index points at a position where the anchors actually coincide. (The claim is correct only under a 0-indexed reading, which would silently conflict with ASN-0093's `#d+2`.)

This is in the parenthetical/illustrative route; the load-bearing argument (origin) is unaffected. But §7 is a worked example meant to be checkable, and the index as printed is false at the value given.

**Required**: Align the separator index to `#d+1` (consistent with ASN-0093's s_C-at-`#d+2`), or, if 0-indexed positions are intended, declare that convention and reconcile it with the foundation's `#d+2`.

## OUT_OF_SCOPE

None. The deferred territory the note gestures at — batch read-atomicity, cross-server composition of per-home orders, weakest exclusion primitives for clauses 2/7/8 — is correctly carried as Open Questions rather than smuggled in as claims, and the "What this note does not cover" / Scope boundaries match.

VERDICT: REVISE
