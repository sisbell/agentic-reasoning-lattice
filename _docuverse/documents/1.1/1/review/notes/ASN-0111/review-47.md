# Review of ASN-0111

This review re-derived every load-bearing argument in the revised note: RL0's wp computation and the structural screen's necessity/insufficiency split; the RL4 branched-history witness (K.δ chain from `n₀` through account `[1.0.1]` and document `[1.0.1.0.1]`, the two K.λ branches at the shared frontier `a'`, the identical follow-on step at `c = inc(a', 0)`, and the SOV discharge of J0/J1★/J1'★); RL5's three permanence families (the LP-Sub/`F` depth bound, the P8 + NodeLineage contradiction for `N(a)₁ ≠ 1`, and the account user-field induction over the three K.δ account-producing sub-cases — which I checked is exhaustive: `k = 1` produces only documents, case (i) only nodes); the residual-class exhaustiveness construction through all four field stages (node baptism, account sibling advances, document open-and-advance, link-chain deposit); and the worked read's reachability route (J0/J1★/J1'★ discharge on the content composites, legality of the `n'_{s_C} = 0` contraction, the two-subtree coverage decomposition via PrefixSpanCoverage, and the address arithmetic of `a`, `a'`, `c`). All check out against the foundation contracts. The anti-bloat scan found no pattern crossing the threshold: the single forward deferral ("proved below") resolves in-document, the SOV preamble is one sentence of standard lemma signposting, and the caching paragraph's closing sentence adds the completeness consequence (the (ii) proofs cover *all* permanent absence) rather than restating (ii)/(iii).

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Reader-side discrimination of links with identical recorded values
**Why out of scope**: `readlink` returns the value, and L11b permits distinct addresses to carry equal values; whatever guarantee lets a reader keep two such reads apart is identity/comparison semantics for links, not a defect in the read itself. The ASN correctly parks this as its third Open Question; it belongs to a future ASN.

### Topic 2: Read authorization and access control
**Why out of scope**: the note specifies what any reader obtains; whether a given principal may invoke the read at a given address is an ownership/permission stratum the model has not yet introduced anywhere. New territory, not an omission here.

### Topic 3: Allocation-event notification for residual-class addresses
**Why out of scope**: RL5 establishes that `⊥` at a residual-class address must not be cached because the address may be allocated later; a mechanism by which a waiting reader learns *when* that happens (subscription, polling contract, event protocol) is future operational territory beyond a pure read's contract.

VERDICT: CONVERGED
