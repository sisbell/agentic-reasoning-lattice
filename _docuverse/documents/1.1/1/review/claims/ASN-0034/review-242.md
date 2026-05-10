# Cone Review — ASN-0034/T10a.8 (cycle 7)

*2026-04-18 05:33*

### T10a.1, T10a.2, T10a.3, T10a.6 summary Depends omit T10a despite consuming its constitutive clauses
**Foundation**: The citation pattern established by T10a.4 (cycle 1 Finding 3, cycle 4 Finding 11), T10a.5, T10a.7, and T10a.8 requires that every postcondition consuming an axiom clause of T10a (sibling production restricted to `inc(·, 0)`, child-spawning bounded to `k' ∈ {1, 2}`, the tree/identity/domain structure that makes "allocator" and "sibling" well-defined, the at-most-once constraint, or the root-initialization clause) cite T10a in its Depends — naming the specific clause consumed.

**ASN**: Four sibling postconditions under T10a's Formal Contract Postconditions block omit T10a:

- **T10a.1 (Uniform sibling length)** Depends: "TA5 (TA5(c): `#inc(t, 0) = #t`)." The statement quantifies over "every allocator with base address b" and "all sibling outputs" — the restriction of sibling production to `inc(·, 0)` is an axiom clause of T10a, not a consequence of TA5.

- **T10a.2 (Non-nesting sibling prefixes)** Depends: "T10a.1 (`#a = #b`) and Prefix (equal-length tumblers are prefix-related only if identical)." The predicate `same_allocator(a, b)` and the very notion of "siblings from the same allocator" are defined by T10a.

- **T10a.3 (Length separation)** Depends: "T10a.1 (uniform sibling length) and TA5 (TA5(d): `#inc(t, k') = #t + k'` for `k' > 0`)." The bound `k' ∈ {1, 2}` that the statement uses and the child-spawning / nesting-level structure are axiom clauses of T10a.

- **T10a.6 (Domain disjointness)** Depends: "T10a.1 (uniform sibling length), T10a.3 (length separation), T10a.5 (cross-allocator prefix-incomparability), Prefix (reflexivity of `≼`)." The notions of "two distinct allocators", `dom(·)`, and `same_allocator(·, ·)` whose witness-uniqueness the corollary asserts are all fixed by T10a's definitional clauses.

By contrast, T10a.5 Depends opens with "T10a (at-most-once constraint)", T10a.7 with "T10a (enumeration definition)", and T10a.8 with "T10a (sibling production restricted to `inc(·, 0)`)" — each naming the specific axiom clause its proof consumes.

**Issue**: A reader reconstructing the dependency DAG from the summary listings sees four postconditions that quantify over T10a-defined objects (allocators, siblings, domains, child spawns) yet list no edge to T10a. This is the same citation-omission pattern cycle 1's Finding 3 and cycle 4's Finding 11 flagged for T10a.4, generalized to four further postconditions. The inconsistency is cross-cutting: for readers and extractors, the T10a-axiom edge appears for T10a.4 (once standalone is aligned), T10a.5, T10a.7, T10a.8, and T10a-N (orientation), but not for T10a.1, T10a.2, T10a.3, T10a.6 — breaking the per-clause sourcing discipline the ASN otherwise applies.

**What needs resolving**: T10a.1, T10a.2, T10a.3, and T10a.6 must each cite T10a (AllocatorDiscipline) in their summary Depends, naming the specific axiom clause consumed — sibling restriction to `inc(·, 0)` (for T10a.1), the "same-allocator" / sibling notion (for T10a.2), the `k' ∈ {1, 2}` child-spawning bound (for T10a.3), and the tree/identity/domain structure (for T10a.6) — matching the pattern T10a.5, T10a.7, and T10a.8 follow.

### Consequence 8 body prose retains "(T0's carrier ℕ)" handwave that standalone T10a.8 has already resolved
**Foundation**: Cycle 1 Finding 1 required the "non-zero ⇒ strictly positive on ℕ" step in T10a.8 to be sourced jointly from T0 + NAT-zero + NAT-discrete rather than from "(T0's carrier ℕ)" alone; the standalone T10a.8 now does so explicitly. Cycle 4 Finding 10 required the summary listing of T10a.8 inside T10a's Formal Contract to match. The body prose under the numbered consequences is a third, distinct location for the same inference.

**ASN**: Consequence 8 body prose (under the numbered consequences inside T10a's body, not the Formal Contract summary block): "Since T10a restricts sibling production to `inc(·, 0)` and every output of a conforming allocator satisfies T4 (Consequence 4), TA5-SigValid fixes `sig(tₙ) = #tₙ` at every step; **T4's field-segment constraint forces the terminal component non-zero, hence strictly positive (T0's carrier ℕ).**" The body also writes "`(tₙ)_{sig(tₙ)} + 1 > (tₙ)_{sig(tₙ)} ≥ 0`" citing only NAT-addcompat — the lower-bound step `(tₙ)_{sig(tₙ)} ≥ 0` is not attributed.

**Issue**: The "hence strictly positive (T0's carrier ℕ)" phrasing is exactly the handwave Finding 1 flagged and that the standalone T10a.8 has replaced with joint T0 + NAT-zero + NAT-discrete citation. The body prose retains the original wording, and it omits NAT-zero for the `≥ 0` lower bound used in the post-increment chain. Finding 10 addresses the summary listing (inline proof sketch inside the Formal Contract); the body prose under Consequence 8 is a distinct textual location that carries the same unresolved handwave — a reader who reads the numbered consequences as the canonical proof presentation sees an argument the standalone and (once aligned) the summary no longer endorse.

**What needs resolving**: Consequence 8 body prose — inside T10a's body text under the numbered-consequences enumeration — must source the "non-zero ⇒ strictly positive" step from T0 + NAT-zero + NAT-discrete jointly (pre-increment) and attribute the `(tₙ)_{sig(tₙ)} ≥ 0` lower bound to NAT-zero (post-increment), so all three locations stating this inference (body prose, Formal Contract summary listing, standalone T10a.8) use the identical per-step trio/quartet citation the document has committed to.
