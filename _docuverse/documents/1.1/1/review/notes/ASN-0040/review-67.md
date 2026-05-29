# Review of ASN-0040

## REVISE

### Issue 1: S2 and B6 necessity restate the same injectivity rationale across two sections
**ASN-0040, S2 prose / B6 sub-case (b)**: S2's trailing paragraph says "The consequence B6(i) draws from this collision — exclusion of such parents to keep the namespace map injective — is argued in B6's necessity discussion below." B6 sub-case (b) then restates it: "Condition (i) excludes such parents here not to avoid a T4 violation but to keep the namespace map injective... This is the sole point where (i) is retained beyond what T4 alone forces."
**Problem**: Two paragraphs in different sections deliver the same argument, with the first deferring forward to the second. This is exactly the "multiple paragraphs deferring to the same downstream location" + duplication pattern.
**Required**: State the injectivity rationale once, at the site where it does work (B6 necessity). Reduce S2's closing paragraph to the bare structural fact (S(p,1)=S(p′,2)) and drop the forward pointer.

### Issue 2: B0b carries defensive "not asserted here" prose with a forward reference to Bop
**ASN-0040, B0b**: "that the union strictly enlarges the set (`next(s.B, p, d) ∉ s.B`, so `|s'.B| = |s.B| + 1`) is the separate freshness claim proved in Bop and is not asserted here."
**Problem**: A clause whose only content is to disclaim what B0b does *not* prove and point at where the proof lives. This advances no reasoning; it is scope-bookkeeping around a forward reference.
**Required**: Delete the disclaimer. B0b's union form stands on its own; freshness is established in Bop where it is used.

### Issue 3: B8 records its scope limitation twice with a forward pointer between them
**ASN-0040, B8 body / postcondition**: Body: "B8 establishes uniqueness only along a single transition path (the scope limitation is recorded in the postcondition note below)." Postcondition: "(The claim is scoped to co-reachable acts: two baptisms on incomparable branches... may compute the same address, but are never jointly observed in any reachable state.)"
**Problem**: The body announces a limitation and points forward to the note; the note then states it. One statement of the scope limitation suffices.
**Required**: Keep the substantive note on the postcondition; remove the body sentence's parenthetical forward pointer (the definition of co-reachable already appears in the opening sentence).

### Issue 4: Condition (iii)'s "binds only at d=2 / subsumed at d=1" is repeated three times
**ASN-0040, B6 statement intro, B6 necessity, B6 postcondition (b)**: The statement intro says "(iii)... it is independently necessary only at d = 2." The necessity proof says "This bites independently only at d = 2... At d = 1... subsumed by (i) rather than independent." Postcondition (b) says "(iii) independently only at d = 2."
**Problem**: The same bookkeeping observation (which condition binds at which depth) appears in three structural slots.
**Required**: Make the binding-depth observation once in the necessity proof; let the statement and postcondition assert the conditions without re-litigating which is "independent."

### Issue 5: next's "Justification of well-definedness" re-derives TA5 totality as essay
**ASN-0040, NextAddress, Justification of well-definedness**: Two full case paragraphs restate that `inc(p,d) ∈ T` (TA5(d)) and `inc(max(...),0) ∈ T` (TA5(c)), plus that a finite subset of a total order has a max.
**Problem**: The non-trivial content is a single sentence — `children` is finite (B_fin) and T1 totally orders it, so `max` exists; both `inc` branches land in T by TA5. The surrounding case-prose re-explains TA5 postconditions that are already cited in the contract.
**Required**: Collapse to the one load-bearing sentence (finiteness + total order ⟹ max exists; TA5 ⟹ both branches in T).

### Issue 6: B9 essay paragraph restates the formal proof's NAT-closure reasoning
**ASN-0040, B9, paragraph before the proof**: "No architectural limit constrains how many children a position may have. The child ordinal occupies a single component, and each baptism advances it by one via inc(·, 0)... Since neither the increment nor successor closure bounds the ordinal, it grows without bound."
**Problem**: This is the proof's argument (TA5(c) totality + NAT-closure ⟹ unbounded ordinal) delivered as essay immediately before the proof delivers it again. Motivation prose that pre-empts the proof.
**Required**: Either cut the paragraph or reduce it to a one-line motivation that does not duplicate the proof's mechanism.

## OUT_OF_SCOPE

### Topic 1: Activation discipline relating allocated(s) to s.B
The Open Questions raise when `allocated(s) ⊆ s.B` holds. This belongs to a future ASN aligning allocator extension with baptism; correctly deferred, not an error here.

### Topic 2: Parent-baptized prerequisite
Bop explicitly imposes no parent-prerequisite, deferring to the ownership model. This is properly scoped out per the Scope section.

VERDICT: REVISE
