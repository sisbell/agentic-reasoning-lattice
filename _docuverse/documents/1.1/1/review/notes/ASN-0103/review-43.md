# Review of ASN-0103

I worked the allocation logic, the frontier proof, the worked example, and the full invariant discharge against the foundation contracts. The note is correct and the argument is closed.

## Verification performed

- **Frontier identity `D_A = E ∩ S(A,2)`.** Both inclusions check. The load-bearing direction `D_A ⊆ S(A,2)` is sound: `parent(e) = A` plus `Document(e)` gives `e = A.0.D(e)` via T4b, and `#e = #A+2` forces `#D(e) = 1`, yielding canonical form `[A,0,j]`. The version-exclusion is real and correctly handled — versions carry length `≥ #A+3` (forked one level deeper), so the length filter `#e = #A+2` cleanly separates `A_doc(A)` from `A_v`.
- **Freshness.** `d ∈ S(A,2) \ D_A = S(A,2) \ E` is valid uniformly over `E` (if `d ∈ E` then `d ∈ E ∩ S(A,2) = D_A`, contradicting `d > max(D_A)`). The argument does not assume contiguity of `D_A`, correctly.
- **K.δ legality.** Both branches satisfy K.δ case (ii): `k=2` off `A` (`zeros(A)=1 ≤ 1`), `k=0` off `max(D_A)` (`¬Node`). Zero-count, parent, and T4 identities discharge via B5/B5a, B6, TA5a.
- **Worked example.** `A=[1,0,1]`, `d1=[1,0,1,0,1]`, `v1=[1,0,1,0,1,1]` excluded by length, `d=inc(d1,0)=[1,0,1,0,2]`; the counterfactual collision (`inc(v1,0)` re-baptising `d1`'s next version, violating B8) is correctly derived and B7-disjointness checks.
- **Invariant coverage.** All 35 conjuncts of ExtendedReachableStateInvariants plus P3 and M0 are addressed — directly (S7d, ActivatedEmission via CND.A-act), vacuously on `dom(M'(d))=∅`, or frame-inherited. ActivatedEmission's reliance on the standing assumption CND.A-act for `Activated(A_doc(A))` is a legitimate scoping of account provisioning.

No cross-ASN references outside the foundation set. No correctness gaps, missing boundary cases (first/subsequent document, empty arrangement all covered), or hand-waved invariants.

On anti-bloat: I examined the candidate redundancies — the length-filter motivation appearing in both Effect One (abstract) and the worked example (concrete), and the sub-allocator activation note relative to CND.subAlloc. Both are object-level content (statements of what the operation does, and a concrete counterexample), which the review guidance explicitly excludes from meta-prose. The prose advances reasoning; I do not flag it.

## OUT_OF_SCOPE

### Topic 1: Effective ownership ω(d) of the new document
The note establishes structural ownership `owns(π,d) ≡ pfx(π) ≼ d` and explicitly leaves the effective-owner reading (`ω_Σ'(d)`) open, flagging the required entity-set/baptismal-registry coupling as Open Question 6. This is correctly deferred — `ω` is defined over the ASN-0042 registry `B`, whose coupling to `E_doc` is a genuinely separate concern.

VERDICT: CONVERGED
