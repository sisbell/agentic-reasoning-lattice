# ASN-0066 Formal Statements

*Source: ASN-0066-streams-0.md (revised 2026-03-21) — Extracted: 2026-03-21*

## Definition — SubspaceOf

`subspace(v) = v₁` — the first component of the element-field V-position.

## Definition — SubspacePositionSet

`V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S}` — the set of V-positions in subspace S of document d. All V-positions in a given subspace share the same tumbler depth (S8-depth, ASN-0036).

---

## D-CTG — VContiguity (DESIGN, predicate)

For each document d and subspace S, V_S(d) is either empty or occupies every intermediate position between its extremes:

`(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`

## D-MIN — VMinimumPosition (DESIGN, predicate)

For each document d and subspace S with V_S(d) non-empty:

`min(V_S(d)) = [S, 1, ..., 1]`

where the tuple has length m (the common depth of V-positions in subspace S per S8-depth, ASN-0036), and every component after the first is 1.

## D-CTG-depth — SharedPrefixReduction (COROLLARY, lemma; from D-CTG, S8-fin, S8-depth)

For depth m ≥ 3, all positions in a non-empty V_S(d) share components 2 through m − 1. Contiguity reduces to contiguity of the last component alone — structurally identical to the depth 2 case.

## D-SEQ — SequentialPositions (COROLLARY, lemma; from D-CTG, D-MIN, S8-fin, S8-depth)

For each document d and subspace S, if V_S(d) is non-empty then there exists n ≥ 1 such that:

`V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n}`

where the tuple has length m (the common V-position depth in subspace S). At depth 2 this gives V_S(d) = {[S, k] : 1 ≤ k ≤ n}.
