# Review of ASN-0042

The ASN is exceptionally thorough. State axioms (O12–O18) are clearly identified, derived properties have explicit proofs, the worked example concretely verifies each postcondition against specific principals and addresses, and the case analyses are exhaustive (O10's Form A/B classification with `hwm_0 = 0` field-opening boundary; AccountField's four-case proof over `zeros(a) ∈ {0,1,2,3}`; NestingByDelegation's sub-case proof of `pfx(π_d) = pfx(π_1)` via O1b). I traced:

- The fork trajectory in *Verifying O10*: seeds, Bop calls (1)–(3), hwm computation, B6 discharge, O5 authorization, B1 contiguity prerequisites — every step checks out.
- The structural forcing of `hwm_0 = 0` at the freshly-delegated `π_B` — the granfilade-anchoring argument is correct.
- The chain construction in O7(c) — `pfx(π_0) = [1]`, `pfx(π_k) = [1, 0, 1, ..., 1]` for `k ≥ 1`. T4, condition (iv), the most-specific-covering check via NestingByDelegation, prefix-length sequence `1, 3, 4, ..., k+2`. All verify.
- The covering-chain lemma, O3's strict-extension argument, O8's irrevocability via length-permanence, O9's case analysis on `zeros(pfx(π))`, OwnershipDomainPermanence★'s induction with first-delegator form.
- The two-registry coupling: O18 (freshness) ↔ ASN-0040 `next` (next-slot semantics) ↔ DelegatorAllocatesPrefix (single-allocator coupling).

Edge cases addressed: `hwm_0 = 0`, `zeros(pfx(π))` ∈ {0,1}, single-node vs multi-node bootstrap, sub-delegation chains, self-ownership at the prefix boundary (`a₆ = pfx(π_A)`), and the namespace-vs-delegation mutual exclusion via O18 freshness. The reachability convention is correctly threaded — every property invoking iterated O12/O13/B0★ restates the precondition.

The recommendation in `ownership-divergence.md` (Gregory's `tumbleraccounteq` ignoring components past the second zero) describes an implementation deviation from this spec, not a defect in the spec — the spec correctly forbids that behavior via O2/O3/O8.

## REVISE

(none)

## OUT_OF_SCOPE

(none — the ASN's Scope section and Open Questions explicitly enumerate the boundaries)

VERDICT: CONVERGED
