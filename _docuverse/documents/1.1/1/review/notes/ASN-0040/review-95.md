# Review of ASN-0040

## REVISE

### Issue 1: `s.B` and the foundation's `allocated(s)` are never reconciled in the body

**ASN-0040, "The baptismal registry" / "Unbounded growth" / Open Questions**: B0 is glossed as "irrevocability (analogous to T8 for the registry component)," and `S(p, d)` (c₁ = inc(p, d), cₙ₊₁ = inc(cₙ, 0)) reconstructs exactly T10a's allocator-domain stream.

**Problem**: The foundation already supplies `allocated(s)` (AllocatedSet) — the set of assigned addresses — with permanence T8. This ASN introduces a parallel state component `s.B` with permanence B0/B0★ for the same intuitive notion ("a position that has been assigned"), yet the body never states whether `s.B` *is* `allocated(s)`, a superset, a subset, or a genuinely different abstraction. The entire relationship is punted to a single open question (`allocated(s) ⊆ s.B`). For an ASN whose stated thesis is distinguishing "arithmetic possibility from system fact," this distinction is load-bearing, and a reader of the self-contained ASN cannot tell whether B0/B0★ duplicate T8 or refine it.

**Required**: State the relationship in the body in one or two sentences — e.g. that `s.B` is the committed registry (the *write* in Gregory's two-phase anatomy) while `allocated(s)` is the allocator's realized domain (the *query*), with their alignment deferred. Without this, the parallel permanence machinery reads as reinvention of T8.

### Issue 2: Inconsistent contract labeling of foundation dependencies

**ASN-0040, Formal Contracts of S(p,d), next, hwm, B9 vs S0, S1, B7**: S(p,d) lists "*Axiom:* TA5(b), TA5(c), TA5(d)", next lists "*Axiom:* TA5(c), TA5(d), T1", and B9 lists "*Axiom:* TA5(c), TA5(d) … NAT-closure", while S0, S1, B7 list the same kind of foundation references under "*Depends:*".

**Problem**: TA5, T1, NAT-closure are foundation theorems/axioms this ASN *depends on*, not axioms it *introduces*. Using the "Axiom:" slot for them in some contracts and "Depends:" in others is internally inconsistent and obscures which obligations are genuinely new.

**Required**: Use "*Depends:*" uniformly for foundation references; reserve "*Axiom:*" for genuine design requirements (as B0a and B₀ conf. already are).

## OUT_OF_SCOPE

### Topic 1: B3 (Ghost Validity) and the `Occupied` predicate

**Why out of scope**: B3 introduces `Occupied : T × 𝒮 → {⊤, ⊥}` and a requirement that content appear only at baptized addresses. Content storage is explicitly deferred (scope list: "content storage and retrieval"). B3 is correctly framed as a *forward requirement* on the future content ASN rather than a content-storage operation, and the ghost-element concept (baptized-but-empty) is intrinsic to baptism — so its placement is appropriate, but the `Occupied` machinery itself is future territory, not an obligation this ASN must discharge.

### Topic 2: Concurrent / cross-replica uniqueness

**Why out of scope**: B8 is carefully limited to *co-reachable* (single-path) acts and does not overclaim global uniqueness. Cross-replica baptism ordering is correctly left to an open question and the BEBE scope exclusion.

The proofs of B6 (necessity + sufficiency with full case split), B7 (length-split / equal-length / unequal-length parents, all exhausted), B1, B10, B8, and B9 are complete and case-exhaustive; the "co-reachable" qualifier on B8 and the d=1/d=2 boundary handling in the trace are correct. No technical proof gap found.

VERDICT: REVISE
