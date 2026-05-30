# Review of ASN-0042

This ASN is mathematically mature — the core invariants (O2 exclusivity, O3 refinement, O8 irrevocability, O10 fork) are soundly derived, the Form A/Form B non-coverage analysis in O10 is complete, and all cross-references are to foundation ASNs (0034, 0040), so no self-containment violation. My findings are confined to accreted prose and structural weight, which the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: Use-site / "why-needed" prose appended to the O17b axiom
**ASN-0042, State Axioms (O17b)**: "A delegation transition falls in the *baptism* branch, not the frame branch: O18 (DelegationBaptizes) records `pfx(π') ∈ Σ'.B ∖ Σ.B` for the newly introduced principal, and condition (v) fixes that prefix as `next(Σ.B, p, d)`. The frame branch therefore covers only genuine no-op-on-`B` operations."
**Problem**: This paragraph explains how delegation *consumes* the axiom rather than stating what the axiom says — exactly the "new prose around an axiom explaining why it is needed" pattern. The delegation-falls-in-baptism-branch fact is re-derived where it is actually used (DelegatorAllocatesPrefix, O18 itself), so this is a use-site inventory.
**Required**: Delete the trailing paragraph; the axiom's two-branch disjunction stands on its own.

### Issue 2: Duplicated framing prose for O10
**ASN-0042, after O10 statement**: "O10 transforms the ownership boundary from a wall into a fork point. The only 'permission' concept the system needs is prefix containment. Everything else — collaboration, annotation, criticism, derivation — is handled by creating new owned addresses…"
**ASN-0042, end of Worked Example**: "The fork transforms the ownership boundary into a creative act: `π_A` now has a fully owned address `a'`…"
**Problem**: Two paragraphs in different sections deliver the same thematic statement ("the boundary becomes a fork/creative act") in different words. The list of "collaboration, annotation, criticism, derivation" is essay content that advances no reasoning.
**Required**: Keep one. The worked-example sentence is concrete (tied to `a'`/`a₃`); the post-statement essay paragraph is the removable one.

### Issue 3: `R_Σ` / `covers_Σ*` / NestingByDelegation apparatus is heavy machinery with a single worked-example consumer
**ASN-0042, State Axioms (the parent relation `R_Σ`, the "Delegation edges are cover edges (bridge)", and the ~1.5-page NestingByDelegation derivation)**
**Problem**: `covers_Σ*` and `R_Σ` are introduced with a bridge lemma and a full inductive proof, but no O-property uses them formally — OwnershipDomainPermanence states its conclusion as `pfx(π) ≼ pfx(π_d)`, not via `covers`, and O3/O8 do not cite NestingByDelegation. The only consumer is the worked-example unbounded-chain aside ("by NestingByDelegation, any other principal's prefix is non-nesting with the chain"). This is structural accretion: a proof apparatus whose payoff is one descriptive remark plus the prose "principals form a forest under the strict-extension order…".
**Required**: Either route a real downstream property through `covers_Σ*` (the OwnershipDomainPermanence "sub-delegate" informal reading is the natural candidate — formalize it with `covers`), or demote NestingByDelegation/`R_Σ` to a short stated lemma and drop the forest essay.

### Issue 4: Proof-local notation reused across proofs without restatement
**ASN-0042, SelfOwnershipAtPrefix proof**: "For any other `π'' ∈ C(pfx(π))` with `π'' ≠ π`…"
**Problem**: `C(a)` is defined only inside the O2 proof ("define `C(a) = {π ∈ Π : pfx(π) ≼ a}`") as a local abbreviation. SelfOwnershipAtPrefix silently borrows it. A reader following SelfOwnershipAtPrefix in isolation has no definition for `C`.
**Required**: Either inline the set comprehension at the SelfOwnershipAtPrefix use, or promote `C(a)` to a named definition in the Ownership Domains section.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
The Open Questions list (transfer preserving provenance, overlap enforcement, owner-disappearance accessibility, domain density, cross-node federation, delegation-event recording) is correctly deferred — these are future-ASN territory, not defects here, and are appropriately framed as questions rather than claims.

VERDICT: REVISE
