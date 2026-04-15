# Cone Review — ASN-0036/D-SEQ (cycle 3)

*2026-04-15 02:49*

I need to read the actual property files to verify the current state against the provided ASN content.

### D-MIN's formal contract uses lexicographic order (via `min` and "least element") without citing T1 or the T-membership chain

**Foundation**: T1 (LexicographicOrder, ASN-0034) — defines the total order on T; Σ.M(d) — provides `dom(Σ.M(d)) ⊆ T`
**ASN**: D-MIN (VMinimumPosition) — axiom: `min(V_S(d)) = [S, 1, ..., 1]`; postcondition: "`min(V_S(d)) = [S, 1, ..., 1]` is the least element of V_S(d) under lexicographic order. Since every V-position component is at least 1 (S8a) and the tuple `[S, 1, …, 1]` has the minimum possible value at every post-subspace component, no element of V_S(d) can precede it."
**Issue**: D-MIN's axiom uses `min(V_S(d))`, which presupposes a total order on V_S(d) to identify the least element. The postcondition explicitly invokes the lexicographic order and reasons "no element of V_S(d) can precede it" — a claim that depends on T1 to define "precede." The body text confirms this with "making it strictly larger by T1(i)." Yet T1 appears nowhere in D-MIN's formal preconditions. Every sibling property that uses the lexicographic order cites it: D-CTG ("the lexicographic order `<` (T1, ASN-0034) is well-defined on V-positions"), D-CTG-depth ("T1 (LexicographicOrder, ASN-0034) — every ordering comparison…"), D-SEQ ("providing carrier-set membership for T1"). D-MIN also omits the T-membership chain — `V_S(d) ⊆ dom(Σ.M(d))` (V_S(d), SubspaceVPositionSet) and `dom(Σ.M(d)) ⊆ T` (Σ.M(d)) — that D-CTG and D-SEQ cite to establish that T1's order applies to V-positions. Without T1, `min` is undefined on tumblers; without the T-membership chain, T1 cannot be applied to V_S(d). D-MIN's preconditions list S8-depth, S8-vdepth, and S8a but not the order or the carrier-set membership that its axiom and postcondition both require.
**What needs resolving**: D-MIN's formal preconditions must cite T1 (LexicographicOrder, ASN-0034) and the T-membership chain (`V_S(d) ⊆ dom(M(d)) ⊆ T` via V_S(d) and Σ.M(d)), matching the convention established by D-CTG, D-CTG-depth, and D-SEQ.
