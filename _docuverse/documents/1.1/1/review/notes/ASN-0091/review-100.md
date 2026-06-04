# Review of ASN-0091

I read the ASN against the foundations, checked the abstract→REARRANGE_K realisation argument, the RE-* derivations, and all five worked examples. The mathematical core is sound — RA-π/RA-frame derivations (RE-ran, RE-μ, RE-disc, RE-proj) check out, the net-effect split and collapse case are handled correctly, and the worked-example arithmetic verifies. Two findings remain.

## REVISE

### Issue 1: L-chain proof cites TA5(c) for chain-membership preservation
**ASN-0091, "Chain Disjoint-Adjacency Lemma"**: "The chain-adjacency successor `x + 1 = inc(x, 0)` preserves sub-allocator chain membership (TA5(c), ASN-0034), so `x + 1 ∈ dom(A_{s_X}(d_X))`".
**Problem**: TA5(c) states only `#inc(t, 0) = #t` and `t'_{sig(t)} = t_{sig(t)} + 1` — it characterises the increment, not membership in the allocator chain. The fact actually needed (`x ∈ dom(A_{s_X}(d_X)) ⟹ inc(x, 0) ∈ dom(A_{s_X}(d_X))`) follows from the chain being closed under `inc(·, 0)` — i.e. the SiblingStream recurrence `t_{n+1} = inc(t_n, 0)`, which ASN-0093's ChainDiscipline supplies. The whole lemma (and the coalescence/equality run-decomposition witnesses that rest on it) leans on this step, so the citation should be corrected.
**Required**: Cite ASN-0093's ChainDiscipline (the SiblingStream closure of `A_C(d)`/`A_L(d)` under `inc(·, 0)`) for the membership-preservation step; retain TA5-SigValid + OrdinalShiftBase only for the prior identification `x + 1 = inc(x, 0)`.

### Issue 2: Composite-boundary conclusion restated verbatim across consecutive sentences
**ASN-0091, "Composite-Boundary Properties"**: paragraph ends "…so Σ' too is the final state of a trace of valid composites — a reachable composite boundary by construction." The next paragraph opens "Σ' is a reachable composite boundary, so ASN-0047's ExtendedReachableStateInvariants delivers…".
**Problem**: The same conclusion ("Σ' is a reachable composite boundary") is asserted as the close of one paragraph and re-asserted as the premise of the next — the anti-bloat "two sentences say the same thing in different words" pattern. The reader steps over the restatement to reach the actual inference.
**Required**: Collapse the two into a single inference (e.g., end the construction at "…final state of a trace of valid composites" and have the delivery sentence continue from there without re-stating the boundary fact).

## OUT_OF_SCOPE

### Topic 1: Same-source-span reconstitution after a splitting cut
**Why out of scope**: The first Open Question (whether two fragments of a span transcluded from a single source jointly reconstitute the original) is correctly deferred; RE-trans already disclaims it ("Whether the two fragments *jointly reconstitute*… is not established here").

### Topic 2: REARRANGE semantics on the link subspace
**Why out of scope**: CS3 fixes cuts to `s_C`; link-subspace reordering is new operational territory (second Open Question), not a gap in this ASN.

VERDICT: REVISE
