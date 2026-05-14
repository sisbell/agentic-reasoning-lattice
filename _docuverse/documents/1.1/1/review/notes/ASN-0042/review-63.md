# Review of ASN-0042

The ASN decomposes the ownership model into seven transition-discipline axioms (O12, O13, O14, O15, O5, O16, O18), two signature constraints on `pfx` (O1a, O1b), and one primitive relation (`allocated_by_Σ`), with everything else derived. The architectural separation between the two-place predicate `owns(π, a)` (state-free, O0/O1) and the one-place function `ω(a)` (state-relativized, O2) is held consistently throughout — no proof slips between the two by accident.

Verified spots that typically fail:

- **Boundary cases.** Empty user-field segments (T4a violations) excluded explicitly in O10 Form B length analysis. Singleton `Π₀` handled (pairwise non-nesting vacuous). Both `next` branches (field-opening `hwm_0=0` and sibling-advance `hwm_0≥1`) exhibited in the worked example with B6/B1 verification.
- **Equal-length elimination in O3.** Two-line argument explicitly rules out `#pfx(π') = #pfx(ω_Σ(a))` via Prefix → componentwise equality → O1b → contradiction with `π' ∉ Π_Σ`. Not assumed.
- **Form A/B classification in O10.** Exhaustive: Form A excluded by positive component at position `#pfx(π)+1`; length-`#pfx(π)+1` Form B by T4a (trailing zero); length-`#pfx(π)+2` Form B by PrefixBaptismCoupling + B1 (depth-2 component ≤ `hwm_0`); longer Form B by length alone. The `zeros(pfx(π))=1` branch is closed independently — Form B is empty by O1a.
- **Multi-step OwnershipDomainPermanence★.** Induction on path length with proper invocation of B0★ (ASN-0040) for baptismal-registry monotonicity, distinguished from T8 (ASN-0034) which governs allocator-domain monotonicity. The distinction is called out.
- **DelegatorAllocatesPrefix.** Uses O18's freshness conjunct + O16 + O5 + MostSpecificCoveringUnique + O1b to identify the allocator with the delegator. The covering-chain lemma is named once and cited where needed (O2 Step 2, O7(a) case analysis, OwnershipDomainPermanence Step 3, O10 non-coverage), not re-derived per use.
- **SelfOwnershipAtPrefix.** Derived from PrefixBaptismCoupling + O1b + O2; worked example exhibits the concrete witness at `a₆ = pfx(π_A) = [1,0,2]` rather than re-deriving.
- **Worked example.** Each Bop call is annotated with explicit B6 and B1 checks (e.g., the namespace baptisms produce `[1,0,2,1]` and `[1,0,2,2]` with `zeros(p) + (d-1) = 1 ≤ 3` and contiguous-prefix discharge). The bootstrap seed table reconciles cross-stream non-interference with O18 freshness.

The recursive delegation chain in O7(c) is the densest proof and warrants particular scrutiny: the boundary step `π_0 → π_1` (node-to-account, two components appended via TA5(d) with `k=2`) is verified separately from the uniform inductive step `π_k → π_{k+1}` for `k≥1` (single positive component appended via TA5(d) with `k=1`). The covering-set characterization at each `Σ_k` uses NestingByDelegation + covering-chain lemma to exclude non-chain principals via non-nesting, then conditions (ii) and (vi) fall out from prefix-length ordering within the chain.

## OUT_OF_SCOPE

No items.

VERDICT: CONVERGED
