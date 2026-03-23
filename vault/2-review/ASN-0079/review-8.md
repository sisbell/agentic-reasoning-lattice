# Review of ASN-0079

## REVISE

### Issue 1: F10 proof cites wrong foundation for functional-dependency claim
**ASN-0079, ArrangementIndependence proof**: "The endset coverages coverage(Σ.L(a).eᵢ) depend on Σ.L alone (L12, LinkImmutability, ASN-0043)."
**Problem**: L12 establishes that link values are preserved across state transitions. The claim here is about functional dependency at a single fixed state — that computing coverage requires only the endset value stored in L, not M(d) or any other state component. That is a definitional observation about the coverage function (ASN-0043), not an immutability property. A reader following the citation to verify the proof would find L12 irrelevant to the argument being made.
**Required**: Replace the L12 citation with a reference to the definition of coverage (ASN-0043): coverage is a function of the span set in the endset, which is read from Σ.L(a).eᵢ — no other state component is consulted. The claim is definitional.

### Issue 2: F19 formalization does not match its prose
**ASN-0079, ScaleIndependence**: "the overhead from the non-matching population, which must not grow linearly with |dom(Σ.L)| − |FindLinks(Q)|. Formally, the total cost is O(f(|FindLinks(Q)|) + g(|dom(Σ.L)|)) where g is o(n). This correctly captures Nelson's constraint"
**Problem**: The prose identifies the relevant quantity as the *non-matching* population |dom(Σ.L)| − |FindLinks(Q)|, but the formula applies g to the *total* population |dom(Σ.L)|. These diverge when |FindLinks(Q)| is large relative to |dom(Σ.L)|: the formula permits up to o(|dom(Σ.L)|) overhead even when only a handful of links fail to match, whereas the prose (and Nelson's statement) targets the non-matching count specifically. The sentence "This correctly captures Nelson's constraint" overclaims — the formalization is conservative in the important regime (|FindLinks(Q)| ≪ |dom(Σ.L)|) but strictly weaker than the prose in the complementary regime.
**Required**: Either (a) align the formula with the prose by writing g(|dom(Σ.L)| − |FindLinks(Q)|) where g is o(n), or (b) keep the current formula but soften the "correctly captures" claim to acknowledge it is a conservative bound that coincides with Nelson's constraint when the matching set is a vanishing fraction of the total.

## OUT_OF_SCOPE

### Topic 1: Access control model
**Why out of scope**: The ASN introduces accessible(u) as an abstract function and derives F15/F16 from it. The definition of users, permissions, and the state governing access belongs in a future ASN on document privacy and access control. The interface between link discovery and access control is correctly specified here without presupposing the access model.

### Topic 2: Monotonic discoverability under access filtering
**Why out of scope**: F18 establishes monotonic discoverability for FindLinks(Q) but not for FindLinks_u(Q). Whether the access-filtered result is monotonic depends on whether accessible(u) can shrink (access revocation), which is a property of the access control model — not of link discovery.

VERDICT: REVISE
