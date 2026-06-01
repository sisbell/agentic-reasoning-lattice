# Review of ASN-0047

## REVISE

### Issue 1: Non-lineage of distinct nodes' account sub-allocators is asserted, not derived
**ASN-0047, *Class (a) → Entity distinctness (derived)***: "two distinct accounts emitted by different account sub-allocators (under distinct parent nodes) are prefix-incomparable by T10a.5 (CrossAllocatorIncomparability), the two account sub-allocators being non-lineage as each is based at its own boundary-baptised node rather than ancestor-descendant of one another."

**Problem**: T10a.5 requires the two allocators to be *non-ancestor-descendant*. The justification offered — "each is based at its own boundary-baptised node" — does not establish this, because NodeBaptism only commits `n₀ ≼ e`; it does **not** forbid one baptised node tumbler from being a prefix of another. Multi-component node addresses are T4-legal (`zeros = 0`, `t₁ ≠ 0`, `t_{#t} ≠ 0`), so `N₁ = [1,2]` and `N₂ = [1,2,3]` are both admissible nodes with `N₁ ≼ N₂`. The conclusion (accounts incomparable) does hold — `A_account(N₂)`'s base `[N₂.0.1]` diverges from `[N₁.0.1]` before the zero separator — but that step (distinct nodes ⟹ prefix-incomparable account-allocator bases, even under node nesting) is exactly what is skipped. "Based at distinct nodes" is silently equated with "non-lineage."

**Required**: Either add the missing derivation (distinct node tumblers yield prefix-incomparable `inc(N,2)` bases, discharging T10a.5's non-ancestor-descendant precondition even when `N₁ ≼ N₂`), or state and justify a discipline restriction that forbids node nesting. The same gap recurs in the K.δ k=2 discharge table's node rows.

### Issue 2: Per-state vs. composite-boundary distinction restated three times
**ASN-0047, *Extended reachable-state invariants* preamble, the proof's Class (a)/(b) headers, and the matrix preambles**: The two-bullet explanation of "per-state invariants hold at every reachable state / composite-boundary properties hold only at boundaries and may transiently fail" is given in full in the section preamble, re-explained verbatim-in-substance at the start of the proof ("per the temporal-scope distinction stated in the preamble"), and partially re-stated again in the *Composite-boundary verification matrix* note and *Temporal decomposition*.

**Problem**: Anti-bloat: the reader must re-read the same scoping lecture three times to follow the proof. The distinction is load-bearing once; the repetitions advance no reasoning.

**Required**: State the per-state/composite-boundary distinction once (the section preamble), and have the proof and matrices reference it without re-explaining.

### Issue 3: P4a discharge mechanism deferred to the same location from three sites
**ASN-0047, P4a definition box, *Class (b)* text, and *Composite-boundary verification matrix***: P4a's "trace property" nature and its "induction-along-the-witnessing-trace" discharge are described in the definition box, then the Class (b) paragraph says it is "discharged by the induction-along-the-witnessing-trace mechanism stated in its definition box," then the matrix row paraphrases the same mechanism again.

**Problem**: Matches the flagged forward-reference-accretion pattern (multiple sections deferring to one downstream location, restating rather than citing). The Class (b) prose and matrix row add nothing beyond pointing back at the box.

**Required**: Discharge P4a once in its definition box; have Class (b) and the matrix cite it by name with no restatement.

### Issue 4: TS-family citation in K.μ⁺_L is imprecise
**ASN-0047, *Link-subspace extension* (K.μ⁺_L, non-empty case)**: "the TS-family shift lemmas (TS1–TS5, ASN-0034) together with S8-depth supply S8-depth preservation."

**Problem**: The needed fact is length preservation under shift (`#shift(v,n) = #v`), supplied by OrdinalShift / TS3's frame alone. Citing all of TS1–TS5 (which include order-preservation, injectivity, composition, strict-increase, amount-monotonicity — none of which bear on depth preservation) is a use-site inventory that obscures which lemma is load-bearing.

**Required**: Cite the single shift length-preservation result actually used.

## OUT_OF_SCOPE

### Topic 1: Concurrent allocation under a shared home document
The Open Questions already isolate "must link address allocation be serialized" and node-baptism coordination. These are correctly deferred — SequentialTransitionAxiom assumes total ordering, and concurrency is new territory, not a defect here.

### Topic 2: Link-withdrawal / tombstoning mechanism
The interior-link withdrawal tension with D-CTG★/D-MIN★ (raised in Open Questions) is genuinely a future ASN: K.μ⁻'s suffix-only contraction is consistent within this ASN's presentational-removal contract; reconciling Nelson's tombstoning is downstream work.

VERDICT: REVISE
