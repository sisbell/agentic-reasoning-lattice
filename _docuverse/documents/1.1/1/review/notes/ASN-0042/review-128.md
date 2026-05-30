# Review of ASN-0042

## REVISE

### Issue 1: RegistryReachability Corollary is a use-site inventory
**ASN-0042, State Axioms (RegistryReachability)**: "On any reachable `Σ.B`, ASN-0040's `next` ... and `hwm` ... are well-defined, and the invariants B1 (ContiguousPrefix) and B6 (ValidDepth) are available."
**Problem**: The corollary advances no reasoning beyond the claim it follows ("`Σ.B` is an ASN-0040-reachable registry"). It is a catalogue of which downstream sites consume the property — exactly the "definition's introduction enumerates downstream consumers" pattern. The four citations (`next`, `hwm`, B1, B6) already discharge their own preconditions where invoked.
**Required**: Delete the corollary; cite RegistryReachability at the point of use instead.

### Issue 2: O14 prose enumerates downstream invariants rather than stating clauses
**ASN-0042, State Axioms (O14)**: "...the initial principals satisfy the structural constraints that O1a, O1b, T4, and pairwise non-nesting require of all bootstrap principals."
**Problem**: This is meta-prose naming the downstream consumers of the axiom's clauses (O1a, O1b, T4) before the formal clauses — which then restate them anyway. The reader must skip the inventory to reach the actual conjuncts.
**Required**: Drop the consumer enumeration; let the six formal conjuncts stand on their own.

### Issue 3: "Iterate O12 ⟹ Π₀ ⊆ Π_Σ" stated twice
**ASN-0042, State Axioms**: the Reachability-convention paragraph ("The convention licenses iterated application of O12 ... to conclude `Π₀ ⊆ Π_Σ`") and **BootstrapContainment** ("Proof: iterate O12 along the witnessing sequence") assert the identical fact with the identical justification.
**Problem**: Two paragraphs saying the same thing in different words. One is redundant.
**Required**: Keep BootstrapContainment as the derived lemma; reduce the convention paragraph to the reachability definition without re-deriving containment.

### Issue 4: "Refinement-only regime" deferred to O8 from three sites
**ASN-0042**: O3 corollary, O8 *Design confirmation* ("O8 instantiates O3's refinement-only regime"), and O10 closing ("exhibits the refinement-only regime established at O8") each restate and cross-defer the same regime.
**Problem**: Multiple paragraphs in different sections deferring to the same downstream location — the compounding cross-reference pattern.
**Required**: State the regime once (at O3, where it is derived) and let O8/O10 cite without re-narrating.

### Issue 5: Bridge justification appeals to the wrong quantifier
**ASN-0042, State Axioms (Delegation edges are cover edges)**: "condition (ii) makes `π_d` the most-specific principal of `Π_Σ` covering `pfx(π')`, and by O13 (PrefixImmutability) no later transition alters that fact, so `R_{Σ'}(π_d, π')` holds."
**Problem**: `R_{Σ'}` is evaluated at the immediate post-state over `Π_{Σ'} = Π_Σ ∪ {π'}`. The load-bearing step is that the newly added `π'` does not displace `π_d` as most-specific *strict* cover (it cannot, since `pfx(π') ⊀ pfx(π')`). The proof instead cites O13 about *later* transitions, which is not the question being decided at `Σ'`.
**Required**: Justify `R_{Σ'}(π_d, π')` directly — `π'` is not a strict cover of its own prefix, so the most-specific strict cover in `Π_{Σ'}` coincides with that in `Π_Σ`, namely `π_d`. Reserve O13 for persistence into states beyond `Σ'`.

## OUT_OF_SCOPE

The Open Questions section already defers ownership transfer, prefix-overlap enforcement, post-owner accessibility, domain density, cross-node federation, and delegation-event recording. These are correctly out of scope; no action needed. The substantive proof obligations (O2–O10, NestingByDelegation, OwnershipDomainPermanence, the fork construction with both field-opening and sibling-advance branches, node-level and account-level cases) are discharged with explicit case analysis and a concrete worked example, including boundary cases (`zeros(pfx(π)) ∈ {0,1}`, `hwm_0 = 0` vs `> 0`, cross-node ownership).

VERDICT: REVISE
