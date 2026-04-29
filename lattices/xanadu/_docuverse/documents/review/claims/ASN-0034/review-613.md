# Cone Review — ASN-0034/TA3 (cycle 7)

*2026-04-26 08:08*

I'll carefully re-read TA3 and the supporting claims, focusing on what may have escaped previous cycles.

Tracing through Sub-case A2's revised padded notation, the Case B preamble's two new direct-derivation arguments (for `dₐ ≤ #a` and `d_b ≤ #b`), and the restructured proof of `d_b` defined (now using Case B's witness `j` directly without routing through `dₐ`), each previous finding has been addressed:

- **Finding 1** (TumblerSub's exported divergence-point inequality): TumblerSub's Postconditions list now includes `â_{zpd(a,w)} > ŵ_{zpd(a,w)}` on padded projections.
- **Finding 2** (A2 padded notation): A2 now uses `â_d`, `ŵ_d`, `b̂_d` throughout the divergence-point and tail steps.
- **Finding 3** (preamble bound derived inside contradiction block): Both `dₐ ≤ #a` and `d_b ≤ #b` are now derived by hypothesis-free contradiction from the padding clause + TumblerSub's exported postcondition.
- **Finding 4** (B1 native at potentially-padding indices): B1 now cases on `j ≤ #w` vs `j > #w` with padded projections throughout.
- **Finding 5** (`d_b` defined: instantiating ZPD at index not yet shown to lie in `1..L_{b,w}`): proof now instantiates at `j ≤ #b ≤ L_{b,w}` directly.
- **Finding 6** (T1-witness-to-`dₐ` leap): replaced with the direct padding-clause argument.

The case-structure, padded/native conversions, prefix/length-comparison branches, and the trichotomy on `(dₐ, d_b)` all walk soundly. Depends list (TA2, TumblerSub, ZPD, T1, T3, TA-Pos, TA-PosDom, NAT-sub, NAT-zero, NAT-order, NAT-discrete, NAT-closure) matches the proof's invocations.

VERDICT: CONVERGED

## Result

Cone review converged.

*Elapsed: 7888s*
