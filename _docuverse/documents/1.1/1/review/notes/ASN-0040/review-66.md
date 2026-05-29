# Review of ASN-0040

## REVISE

### Issue 1: B0b claims "exactly one new element" as immediate from B0a, but freshness is not

**ASN-0040, B0b (Transition Dichotomy)**: "or it is *baptismal*, induced by `baptize(p, d)` ... with `s'.B = s.B ∪ {next(s.B, p, d)}` — the addition of exactly one new element. This is immediate from B0a's partition of Σ."

**Problem**: B0a establishes only the set-union *form* `s'.B = s.B ∪ {next(s.B, p, d)}`. That this union actually *adds* an element — i.e. `next(s.B, p, d) ∉ s.B`, so the cardinality strictly increases — is the freshness claim proved separately in Bop, and that freshness proof depends on B1. So "the addition of exactly one new element" is **not** immediate from B0a's partition; it imports freshness. The phrasing also risks the appearance of circularity, since B0b is the induction skeleton for B1.

You are saved from an actual circularity only because the three consumers (B1, B_fin, B10) each use the union form, not the cardinality claim: B_fin needs only "finite set ∪ singleton is finite," B1 recomputes the child set directly, B10 reasons over `B ∪ {a}`. The "exactly one new element" wording is therefore both unsupported at its stated source and unused by its consumers.

**Required**: Either weaken B0b to the union form (`s'.B = s.B ∪ {next(s.B, p, d)}`, immediate from B0a) and drop the "exactly one new element" gloss, or state explicitly that the strictness (`|s'.B| = |s.B| + 1`) follows from Bop freshness (B1), not from B0a.

### Issue 2: B8 cross-branch limitation stated twice

**ASN-0040, B8**: body — "B8 establishes uniqueness only along a single transition path; cross-branch uniqueness — whether two baptisms on incomparable branches of the reachability relation produce distinct addresses — is unaddressed." Postcondition — "(The claim is scoped to co-reachable acts: two baptisms on incomparable branches of the reachability relation may compute the same address, but are never jointly observed in any reachable state.)"

**Problem**: Two paragraphs in the same property say the same thing. This is the duplication pattern the anti-bloat classifier flags.

**Required**: Keep one statement of the scope limitation (the postcondition note is the natural home) and remove the other.

### Issue 3: B6(i) injectivity rationale duplicated across S2 and B6

**ASN-0040, S2 discussion**: "so B6(i) excludes such parents to keep the namespace map injective — the one point where (i) is retained beyond what T4 alone forces." **B6 necessity / postcondition (b)**: "the d = 1 trailing-zero case, where (i) is retained for injectivity (S2)."

**Problem**: The same rationale (B6(i) retained at the d=1 trailing-zero case for namespace injectivity) appears in two sections, each deferring to the other. Defer-to-same-location duplication.

**Required**: State the injectivity reason once — it belongs with B6's necessity argument, where the d=1 exception is actually carved out — and have S2 simply note the stream-collision fact without re-arguing the B6 consequence.

### Issue 4: B9 carries meta-commentary on its own proof

**ASN-0040, B9 proof**: "No ceiling is consulted ... so the construction may be iterated through every natural number ... the unboundedness of the component is *derived* here, not imported as a premise." **B9 prose**: "The design guarantees infinite headroom, leaving capacity as a pure engineering concern."

**Problem**: "derived here, not imported as a premise" is rhetoric about the proof's stance rather than a step of the proof; "pure engineering concern" is essay editorializing. Neither advances the reasoning. The substantive content (NAT-closure gives `n+1 ∈ ℕ` at every step) is already present and sufficient.

**Required**: Delete the self-referential and editorial sentences; retain the NAT-closure step.

## OUT_OF_SCOPE

None beyond the topics already enumerated in the Scope section. The parent-prerequisite question, `allocated(s) ⊆ s.B` activation discipline, valid seed sets, ghost/structural distinction, bulk allocation, cross-replica ordering, and per-subspace contiguity are correctly parked in Open Questions.

VERDICT: REVISE
