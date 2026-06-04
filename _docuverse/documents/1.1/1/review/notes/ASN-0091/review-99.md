# Review of ASN-0091

## REVISE

### Issue 1: Redundant per-invariant justification bolted onto the transition-satisfaction principle (anti-bloat drift)

**ASN-0091, "State-Component-Only Invariants"**: "The class — ASN-0036's S0, S1; ASN-0047's P0, P1, P2, L12, P3; ASN-0093's M1, C0 — is therefore discharged uniformly by RA-frame, with no per-invariant argument required. ASN-0047's P3 (ArrangementMutabilityOnly) is included here: it is the synthesis P0 ∧ P1 ∧ P2 ∧ L12, constraining C, L, E, R by monotonicity and value-preservation clauses, all of which RA-frame fixes with equality, so it falls to the same principle."

**Problem**: The third sentence is a use-site justification that re-derives the general principle for a single class member, exactly the accretion pattern the anti-bloat mandate flags. It is either pure redundancy (the preceding general principle and the class enumeration already discharge P3) or a patch for a principle stated too narrowly. The general principle says each invariant "constrains **one** state component (C, L, E, R, or dom(M))." Checking the enumerated class, every member constrains a single component (S0/S1/P0/C0 → C; L12 → L; P1 → E; P2 → R; M1 → dom(M)) **except P3, which constrains four (C, L, E, R)**. So P3 is the sole member that does not fit the stated "one state component" form, and the dedicated sentence exists only to paper over that mismatch. This is precisely "two paragraphs saying the same thing" / a member-specific re-derivation that compounds across cycles.

**Required**: Either (a) generalize the principle's wording to "constrains one or more state components ... by monotonicity or value-preservation clauses" so P3 falls under it directly, then delete the dedicated P3 sentence; or (b) if the per-conjunct reading is intended, state that once and drop the P3-specific restatement. The dedicated P3 sentence should not survive in either case.

VERDICT: REVISE

The mathematics is sound — I verified the RA-π/RE-ran/RE-μ derivations, the K.μ~ clause (i)–(v) discharges, the L-chain lemma, and all six worked examples (the 3-cut pivot fragmentation 2→3, the coalescence 3→2, the equality 2→2, the bijection non-uniqueness, and the net-effect collapse) against concrete values; they check out. The single remaining issue is the redundant P3 justification.
