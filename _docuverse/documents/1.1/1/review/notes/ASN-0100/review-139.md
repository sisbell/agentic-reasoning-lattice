# Review of ASN-0100

I checked the proofs case-by-case rather than accepting the structure. The hard parts hold:

- **Tiling without gaps (D-CTG★).** The closed-interval reduction over the *full* depth-`m` slice (not just the shared-prefix run) is the one most specs hand-wave. Here it is done correctly: off-prefix tuples like `[s_C, 2, 1]` are excluded by T1 case (i) at the first divergence, and the arbitrary-pair case is reduced to the extremes via transitivity. The `m_C = 3` worked example exercises exactly this.
- **Forced K.μ⁻ ordering.** The reason interior/prepend require contraction before extension — K.μ⁺'s image-preserving precondition forbids rebinding a still-present Right position like `[1,5]` — is stated explicitly, not assumed.
- **Boundary cases all present and distinct:** append (`Right = ∅`, no K.μ⁻), prepend (forced full clearance `n'_{s_C} = 0`), empty document (first-emission branch), re-insertion into cleared subspace (subsequent-emission branch, V-index/chain-index decoupling), deep subspace.
- **Atomicity** correctly separates per-state invariants (every intermediate, incl. the no-I3-counterpart post-K.μ⁻ state, argued independently) from composite-boundary properties (P4★, P4a, P7a, J0/J1★/J1'★). S4 is discharged against the *growing* `dom(C)` at each K.α intermediate via ChainEnumerationInjectivity — not hand-waved.
- **INS.proj** tracks projection through K.μ⁻ (LP10) then K.μ⁺ (LP9) exactly; the retraction of `P_0^R` and its reintroduction at `shift(v,n)` matches. wp analysis is non-trivial (tight-endset collapse, chain-membership predicate).
- `ran(M'(d)) = ran(M(d)) ∪ {a_k}` (used in the wp) is justified since Left ∪ Shifted-right covers the full pre-state content range.

Concrete examples verify the named postconditions; derived consequences (cross-document allocation independence, discoverability preservation, ghost/resurrection via coverage invariance) are explored.

No missing case, unproven postcondition, or proof-by-checkmark found. References are all to foundation ASNs.

One residual note, non-blocking: the INS.I3-coincide clause "…hold of M'(d) restricted to those two regions, **cited at point of use in the sections that need them**" carries a roadmap pointer rather than logical content, and the downstream sections already cite `(§Effect Three)` directly. This area has been trimmed across the last three commits; the remaining clause is the last trim candidate but does not affect correctness.

VERDICT: CONVERGED
