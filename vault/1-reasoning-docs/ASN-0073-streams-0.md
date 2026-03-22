# ASN-0073: Streams 0

*2026-03-22*

ASN-0036 defines the arrangement M(d) and the contiguity constraint D-CTG but does not characterize which V-positions are valid targets for content placement. This extension introduces the valid insertion position predicate — the characterization of V-positions at which content may be placed in a document's arrangement while preserving D-CTG and D-MIN. The predicate belongs in the streams domain because it depends solely on the arrangement structure (V_S(d), D-CTG, D-MIN, S8-depth) and constrains all operations that extend an arrangement.


## Valid Insertion Position

We work with the arrangement M(d) and the contiguity constraint D-CTG from ASN-0036. Write V_S(d) = {v ∈ dom(M(d)) : subspace(v) = S} for the V-positions in subspace S of document d.

When V_S(d) is contiguous with |V_S(d)| = N positions, we write its elements as v₀, v₁, ..., v_{N−1} where v₀ is the minimum (D-MIN, ASN-0036) and v_{j+1} = shift(v_j, 1) for 0 ≤ j < N − 1 (D-SEQ, ASN-0036).

**ValidInsertionPosition** — *ValidInsertionPosition* (DEF, predicate). A V-position v is a *valid insertion position* in subspace S of document d satisfying D-CTG when one of two cases holds:

- *Non-empty subspace.* V_S(d) ≠ ∅ with |V_S(d)| = N. Then v = min(V_S(d)) + j for some j with 0 ≤ j ≤ N, and #v equals the existing subspace depth (S8-depth).

- *Empty subspace.* V_S(d) = ∅. Then v = [S, 1, ..., 1] of depth m ≥ 2, establishing the subspace's V-position depth at m. This is the canonical minimum position required by D-MIN (ASN-0036).

In both cases, S = v₁ is the subspace identifier.

There are N + 1 valid insertion positions: N positions targeting existing content (which will be displaced), plus one append position past the end.


## Statement Registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| ValidInsertionPosition | DEF | if V_S(d) ≠ ∅: v = min(V_S(d)) + j with 0 ≤ j ≤ N, #v = subspace depth; if V_S(d) = ∅: v = [S, 1, ..., 1] of depth m ≥ 2 | introduced |
