# Review of ASN-0076

I read the note in full and checked each of E0–E11, the K.λ precondition discharges at both composite steps, the boundary cases (orphaning in E11, the k=0 base case in E5), the wp computation, and the worked example.

## REVISE

(none)

The proofs hold up under scrutiny:

- **E0** discharges all four K.λ clauses at *each* step (not "by similar reasoning") — the namespace clauses via the subspace argument (`subspace_I = s_L` vs `s_C` + SC-NEQ), freshness via L11a on the T10a-conforming `A_L(d_new)`, and the `#E ≥ 2` depth bound via an explicit induction grounded in TA5(b)/TA5(c)/TA5-SigValid. The supersession step's reuse of that induction is a reference, not a hand-wave. ValidComposite★ is discharged with J0/J1★/J1'★ each shown vacuous from K.λ's frame.
- **E1/E8** correctly invoke LP13 (multi-step domain+value persistence), which is the right instrument — LP2 (slot-only) would not deliver domain persistence. The prior declined finding on this point was correctly closed.
- **E5** handles the `k=0` base case explicitly (vacuous universal) rather than starting at 1, and threads reachability through ExtendedReachableStateInvariants at each inductive state.
- **E11** is genuine wp analysis on a non-trivial postcondition (discoverability), with the frame pullback through E10 and the `ℓ_new` middle-disjunct vacuity argument fully derived via the F-structure (`#E = 2`, third-zero coincidence, T3 collapse) rather than asserted.
- The worked example instantiates every claim against concrete tumblers (`ℓ_old = [3.0.5.0.7.0.2.1]`, `ℓ_new = [4.0.2.0.3.0.2.1]`, `ℓ_sup = [4.0.2.0.3.0.2.2]`), including the orphan branch of E11.

Anti-bloat pass: the prose is dense but functional. The Foundation Recap, the invariant-inheritance enumeration in E0, and the repeated depth-bound argument all carry proof weight or are legitimate reference-not-repeat. I found no defensive meta-prose, no forward-reference deferral chains, and no relocated-finding residue to flag. The E6 application-layer note states what the model does *not* express, which is permitted.

## OUT_OF_SCOPE

The Open Questions (supersession chains, cycles, retraction conventions, successor-set computation, n-ary supersession) are correctly deferred to future ASNs and are not stated as claims here, so no scope violation.

VERDICT: CONVERGED
