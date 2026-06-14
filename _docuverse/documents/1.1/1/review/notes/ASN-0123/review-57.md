# Review of ASN-0123

I checked the load-bearing proofs against the foundation contracts, traced every clause of the operation, and worked the edge cases. The note is sound. Recording what I verified, then the verdict.

**Apparatus proofs.**
- **SA** (StoredAddressAntichain): correct. The `a ≺ b` argument places three distinct zeros (`d₀`'s two + the separator at `#d₀+1`) inside `b`'s document prefix `d'`, contradicting `zeros(d') = 2`. The separator is at a position disjoint from `d₀`'s zeros, so the count is genuine.
- **VN-B1** (VersionNamespaceContiguity): airtight. The induction's case split is exhaustive — Node (excluded by `zeros=2`), base-tier spawn `k=g` (forces `t=p, j=1`, only when `m=0` by IH+freshness), other inter-tier spawn `k=3−g` (excluded by penultimate component: `0` vs nonzero), sibling `k=0` (forces `t=c_{j−1}∈E`, hence `j=m+1`). I confirmed `c₁` cannot arrive via `k=0` (would require `t_{#t}=0`, breaking T4), so the base-tier and sibling cases partition arrivals cleanly. The unified `(p,g)` treatment covering both `S(d,1)` and `S(pfx(π),2)` holds.
- **Z-mono, trunc, nextv/nextd**: correct; `nextd` is properly scoped to account-tier `π`.

**Operation and V-WF.** Both ValidComposite★ clauses discharge for both in-domain branches. I verified the K.δ operand preconditions (owned: version/sibling frontier with `parent(v)=parent(d_src)∈E`; cross-owner: `k=2` descent off `pfx(π)` or `k=0` sibling off the prior document frontier, with `parent(v)=pfx(π)∈E` via PS incumbency), the single-K.μ⁺ transcription onto canonical positions (S8a/S8-depth/D-CTG★/D-MIN★ immediate, images in `dom(C)` by S3★ at Σ with `C` framed), and the `|A|` K.ρ steps. The couplings reduce exactly to the `R'` clause; `n=0` makes them vacuous. Delegation of the per-state invariants to ExtendedReachableStateInvariants is legitimate once validity is shown.

**V9 severance.** The O5(ii) maximality discharge is a genuine theorem: any coverer of `v` longer than `pfx(π)` would contain the length-`(#pfx(π)+1)` prefix `[pfx(π),0]` with `zeros=2`, contradicting O1a. The severance proof `¬(d_src ≼ v)` closes both comparability branches correctly. V8's coverer-set equality and V7's "every address-encoded descendant is owned by `ω(d)`" both check out via the same Z-mono/O1a mechanism.

**Edge cases.** Empty source (`n=0`), shared content within the source (`|A|<n`, the worked instance's repeat at `[1,3]`), owned vs. account-tier cross-owner, first vs. subsequent fork (`hwm=0` vs `≥1`), node-tier forker (excluded by P-tier), links-only source (`A=∅`) — all handled. The two worked instances are arithmetically correct (verified the divergence at position 4 in the cross-owner case, and `a₁⋠a₂` for the SA step in carry-through).

**Foundation hygiene.** No non-foundation cross-references in the body. The inline reproofs (VN-B1, the frontier identity, V0's same-allocator distinctness via GlobalUniqueness) are cross-transition-system non-transfers, each justified at its site.

## REVISE

None.

## OUT_OF_SCOPE

### The note's deferrals are correctly placed
Concurrency serialization of competing forks, derivation-direction recovery under symmetric provenance, link-subspace versioning, location-fixed windowing, withdrawal/supersession semantics, and provenance-vs-derivation separation are all routed to Open Questions rather than half-specified — the right call. The atomicity remark honestly bounds what the foundation supplies (atomic steps, not composite atomicity) and does not overclaim. No topic is improperly pulled in-scope.

VERDICT: CONVERGED
