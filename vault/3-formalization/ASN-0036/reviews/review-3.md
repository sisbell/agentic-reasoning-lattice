# Formalize — ASN-0036 / D-MIN

*2026-04-12 14:27*

**D-MIN (VMinimumPosition).** For each document d and subspace S with V_S(d) non-empty:

`min(V_S(d)) = [S, 1, ..., 1]`

where the tuple has length m (the common depth of V-positions in subspace S per S8-depth), and every component after the first is 1.

D-MIN is a design requirement on valid arrangements. Tumbler components are positive natural numbers (T0(a)), so 1 is the smallest value any component can take. The position [S, 1, …, 1] is therefore the least element of subspace S under lexicographic order (T1): any other position in subspace S shares the first component S but must differ at some subsequent component j, where [S, 1, …, 1] has value 1 and the other position, being a distinct tuple of positive naturals, has value greater than 1 at j — making it strictly larger by T1(i). D-MIN requires that this least position is always present when the subspace is non-empty — every operation that populates or modifies V_S(d) must include [S, 1, …, 1] in the resulting set.

At depth 2 this gives min(V_S(d)) = [S, 1]. Combined with D-CTG and S8-fin, a document with n elements in subspace S occupies V-positions [S, 1] through [S, n] — matching Nelson's "addresses 1 through 100."

We now derive the general form. By D-CTG-depth (when m ≥ 3) or trivially (when m = 2, there is only one post-subspace component), all positions in V_S(d) share components 2 through m − 1. By D-MIN, min(V_S(d)) = [S, 1, …, 1], so those shared components have value 1. Every position is therefore [S, 1, …, 1, k] for varying k. D-CTG restricted to the last component forbids gaps among the k values; D-MIN gives the minimum k = 1; S8-fin bounds the maximum at some finite n. Thus V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n} — a contiguous block from 1 to n at the last component, with all interior components fixed at 1. ∎

*Formal Contract:*
- *Axiom:* `min(V_S(d)) = [S, 1, ..., 1]` — for any non-empty subspace, the minimum V-position is the depth-m tuple with subspace identifier S and every subsequent component equal to 1. This is a design requirement: operations that modify V_S(d) must preserve this minimum.
- *Preconditions:* V_S(d) ≠ ∅; all positions in V_S(d) share depth m (S8-depth).
- *Postconditions:* Combined with D-CTG and S8-fin, `V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}` for some finite n ≥ 1. Positions within a subspace differ only at the last component and form a contiguous range starting at 1.
