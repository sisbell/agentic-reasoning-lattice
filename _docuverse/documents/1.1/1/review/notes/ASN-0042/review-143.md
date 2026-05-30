# Review of ASN-0042

I checked every O-series claim's proof (O1–O18 plus the derived lemmas), the four-step O2 argument, the inductive O3/O4/NestingByDelegation/PrefixBaptismCoupling/RegistryReachability proofs, the O10 fork construction with its Form-A/Form-B non-coverage analysis, and the worked example's boundary cases. I also ran the additional forward-reference/anti-bloat passes the note requests.

## REVISE

(none)

Findings examined and cleared:

- **O10 fork arithmetic.** `a' = next(Σ.B, pfx(π), 2)` yields `zeros(a') = zeros(pfx(π)) + 1` in both branches (field-opening `hwm_0 = 0` via B5; sibling-advance via B5a), and the closed form `pfx(π).0.{hwm_0+1}` matches both the account-level (`[1,0,2,0,6]`) and node-level (`[1,0,3]`) witnesses. The non-coverage argument is sound: any covering sub-delegate of length `#pfx(π)+2` is itself baptized (PrefixBaptismCoupling), lies in `S(pfx(π),2)`, and is therefore bounded by `hwm_0` (B1), so cannot reach `hwm_0+1`. d=2 (not d=1) is correctly required to descend one tier.
- **O2 well-definedness.** `|C(a)| ≤ #a` via O1b bounds the covering set independently of whether `Π_Σ` is finite; the finite non-empty `≼`-chain has a unique maximum. Solid.
- **Invariant inductions (O1a/O1b/T4, O3, O4, NestingByDelegation).** Bases trace to O14 conjuncts; steps discharge the sole O15 newcomer via the delegation conditions, with O12/O13 carrying existing principals. The O1b length-contradiction (`#pfx(π''') ≤ #pfx(π) < #pfx(π') = #pfx(π''')`) is correct.
- **Anti-bloat scan.** Per-claim Nelson/Gregory justifications are one-liners consistent with the ASN's stated method, not axiom rationale. O17b/O17c/O18 are each used downstream (O7(c), O10, PrefixBaptismCoupling, worked example) and are not mutually redundant — O17c's next-reachable form genuinely narrows the admissible delegate prefixes in O7(c). The single-transition vs. ★ multi-step OwnershipDomainPermanence split is a legitimate derived consequence, not deferral. No use-site inventories, no document-ordering apologetics, no relocated-finding paragraphs found.
- **Cross-ASN references.** Only ASN-0034 and ASN-0040, both foundation; no notation reinvention (deliberate `odom`/`ω` disambiguation against foundation `dom`).

## OUT_OF_SCOPE

(none beyond the topics already deferred to the Open Questions, which are correctly framed as future ASN territory.)

VERDICT: CONVERGED
