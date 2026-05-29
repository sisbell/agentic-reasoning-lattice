# Review of ASN-0040

## REVISE

### Issue 1: B8's headline guarantee is unconditional but only proved under single authority
**ASN-0040, B8 (Uniqueness)**: "Distinct baptismal acts produce distinct addresses: `(A a, b : produced by distinct baptismal acts : a ≠ b)`."
**Problem**: The bold statement and the Properties-Introduced entry ("Distinct baptisms produce distinct addresses — uniqueness") assert an unconditional invariant, but Case 1 (same namespace) is discharged entirely by B-Seq and holds only *under a single baptismal authority*. The closing paragraph concedes this: "two concurrent commits reading the same hwm would both compute c_{m+1} and collide — so this clause does not extend across authorities." So the unconditional headline is not merely imprecise — the author demonstrates it is false in general. Only Case 2 (cross-namespace, via B7) is authority-independent.
**Required**: Scope the headline and table entry: state the cross-namespace clause unconditionally and the same-namespace clause under single authority. The formal-contract precondition already carries the qualifier; the prose-level claim must match it.

### Issue 2: B8 Case 1 relabeling asserts "WLOG" without discharging the obligation
**ASN-0040, B8, Case 1**: "By B-Seq the realized states are totally ordered by →*, so s₁' and s₂ are comparable: either s₁' →* s₂ or s₂ →* s₁'. Relabel ... so that s₁' →* s₂ ... this relabeling is without loss of generality."
**Problem**: The proof needs s₁'→*s₂ but comparability also admits s₂→*s₁'. The "WLOG" silently assumes the relabeling can always force the wanted direction. Closing it requires two facts not invoked here: B4 (atomicity) rules out a read-state strictly inside β₁'s single edge s₁→s₁', and B-Seq's no-fork clause rules out s₂ = s₁ (a shared read-state). Only with both does s₂→*s₁' collapse to s₂ = s₁', re-establishing s₁'→*s₂. As written, this is "follows from comparability" — a claim, not a proof.
**Required**: Show the relabeling explicitly: cite B4 to exclude an intermediate read-state and B-Seq's no-fork to exclude a shared read-state, then conclude s₁'→*s₂ in every case.

### Issue 3: B8 closing paragraph is reviser drift around an excluded case
**ASN-0040, B8, final paragraph**: "The two clauses ... rest on different foundations and carry different strengths ... two concurrent commits reading the same hwm would both compute c_{m+1} and collide — so this clause does not extend across authorities (see Open Question 6)."
**Problem**: This is essay content imagining the concurrency scenario that the claim's own precondition (single authority) excludes, then deferring to Open Question 6. The genuine scope-limit belongs in the contract precondition (where it already lives once Issue 1 is fixed); the speculative collision narrative and the downstream pointer add no step to the argument and force the reader past meta-prose. This is exactly the forward-reference accretion the anti-bloat classifier targets.
**Required**: Delete the paragraph. The per-clause strength distinction is fully captured by stating Case 2 unconditionally and Case 1 under single authority (Issue 1).

### Issue 4: B3's closing sentence reaches into out-of-scope content storage
**ASN-0040, B3 (Ghost Validity)**: "Content presupposes baptism: any content-storage layer built atop this model may store content at an address only after that address is baptized."
**Problem**: Content storage and retrieval are explicitly out of scope. The three admissible-configuration bullets characterize the registry and are in scope; this trailing sentence imposes a constraint on a future content-storage layer — a forward gesture that the body of B3 does not use and that this ASN cannot discharge.
**Required**: Remove the sentence, or relocate the ordering constraint to the relevant future ASN. B3's in-scope content is "baptism (membership in s.B) is independent of whether content is stored" — that stands without the forward constraint.

## OUT_OF_SCOPE

### Topic 1: Multi-authority / concurrent baptism in a shared namespace
**Why out of scope**: Already named in Open Question 6. B-Seq deliberately restricts to a single serialized commit path; cross-replica ordering in a shared namespace is new territory, not a defect here. (Issue 1 is about correctly *scoping* the existing claim, not about covering this topic.)

### Topic 2: Which seed sets B₀ are valid for genesis
**Why out of scope**: B₀ conformance is taken as a design requirement; enumerating viable root configurations is deferred (Open Question 3) and is not an error in this ASN.

VERDICT: REVISE
