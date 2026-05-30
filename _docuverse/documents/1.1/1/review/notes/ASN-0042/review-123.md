# Review of ASN-0042

## REVISE

### Issue 1: O7(c) imagines prospective states the claim's transition excludes
**ASN-0042, Delegation, O7 postcondition (c)**: "This auto-discharge of (ii) and (iv) is specific to the entry state... at a *later* prospective delegation state `Σ''` — after `π'` may itself have introduced sub-delegates — the most-specific check (ii) ranges over the then-current `Π_{Σ''}`... so both revert to genuine per-state obligations..."
**Problem**: O7's Formal Contract is about the single transition `Σ → Σ'`. This paragraph (≈200 words) reasons about a hypothetical `Σ''` reached after further sub-delegations — a case the claim's carrier does not cover. It is essay content about *when conditions would bind in the future*, not a step in establishing postcondition (c). This is reviser drift: the per-state behavior of (ii)/(iv) is already fixed by their definitions in O15; restating it as narrative around O7 adds nothing the reader cannot read off the predicate.
**Required**: Reduce (c)'s proof to what discharges the recursive right at `Σ'`: conditions (i) fixed by choice of `p''`, (ii)/(iv) auto-discharged because `Π_{Σ'} ∖ Π_Σ = {π'}`, (iii)/(v) genuine obligations. Delete the `Σ''` meditation.

### Issue 2: Freshness of the delegate prefix is asserted/derived four times
**ASN-0042**: condition (v) (`pfx(π') = next(Σ.B, p, d)`, whose `next` semantics already give `∉ Σ.B`); O17b sharpened clause (`next(Σ.B, p, d) = pfx(π') ∧ next(Σ.B, p, d) ∉ Σ.B`); O18 ("`pfx(π') ∈ Σ'.B ∖ Σ.B`"); Freshness-(v) ("(fresh) it is unbaptized — `pfx(π') ∉ Σ.B`... O18 gives...").
**Problem**: The single fact "the delegate prefix is freshly baptized" is stated in four places in four phrasings, with a derivation chain (O17b → O18 → Freshness-(v)) that reproduces what `next`'s `Bop` postcondition (`next(s.B,p,d) ∉ s.B`, ASN-0040) already supplies once condition (v) is in force. This is accretion: multiple paragraphs deferring to the same downstream fact.
**Required**: Pick one source of truth for freshness (the `next` semantics implied by condition (v)) and cite it; collapse O18 and the (fresh) half of Freshness-(v) into a single citation rather than a re-derivation.

### Issue 3: O17b's "sharpened" clause duplicates delegation condition (v)
**ASN-0042, O17b (BaptismalRegistryCoupling)**: "every transition that admits a new principal... the element it baptizes is exactly that principal's prefix, for the B6-valid `(p, d)` named by condition (v) of the delegation predicate: ... `next(Σ.B, p, d) = pfx(π')`..."
**Problem**: This is an axiom restating the content of O15 condition (v) (`pfx(π') = next(Σ.B, p, d)`). Two sources of truth for the same fact (one in the delegation predicate, one in a coupling axiom) is exactly the redundancy the anti-bloat classifier targets, and it leaves ambiguous which is normative. The clause even names "condition (v)" inside the axiom, advertising the overlap.
**Required**: State the registry/principal coupling once. Either O17b owns the "principal-introduction baptizes its prefix" fact and condition (v) cites it, or condition (v) owns it and O17b's first (frame/baptism) branch suffices without the sharpened restatement.

### Issue 4: T4-discharge convention is use-site management prose
**ASN-0042, O17**: "*T4-discharge convention.* Every proof in this ASN that applies a field operation (`fields`, T4b, T4c, FieldStructure) to an allocated address `a ∈ Σ.B` thereby carries the precondition `T4(a)`; we discharge it uniformly by O17 and do not restate the discharge at each use site."
**Problem**: This paragraph manages how later proofs cite O17 rather than advancing any claim. It is the "use-site inventory" pattern. O17 already states `a ∈ Σ.B ⟹ T4(a)`; that a proof may cite it is not itself a fact about ownership.
**Required**: Delete the convention paragraph; let proofs cite O17 where they need `T4(a)`, as they already do (e.g., O6, O9 say "supplied by the T4-discharge convention (O17)" — replace with a direct "by O17").

### Issue 5: Properties table enumerates downstream consumers in a definition slot
**ASN-0042, Properties Introduced, O17b row**: "...with `next(Σ.B, p, d) = pfx(π')` (the primitive from which O18 and Freshness-(v)'s freshness derive) | axiom (coupling)"
**Problem**: The parenthetical names O17b's downstream consumers rather than stating what O17b asserts. Definition/summary slots should advance meaning, not inventory who depends on the entry.
**Required**: Drop "(the primitive from which O18 and Freshness-(v)'s freshness derive)"; the dependency is already recorded in O18's and Freshness-(v)'s own derivations.

### Issue 6: Repeated defensive reachability-precondition parentheticals
**ASN-0042, O3 / O8 / OwnershipDomainPermanence / OwnershipDomainPermanence★**: e.g. "By O3 (OwnershipRefinement) (whose reachability precondition is satisfied by the present hypothesis)..."; "the single-transition OwnershipDomainPermanence applies directly (its reachability precondition is the present hypothesis)..."
**Problem**: These parentheticals defensively re-assert that an already-stated precondition is met. They do not advance the argument; the reader can see the hypothesis is in scope. The pattern recurs verbatim across four proofs.
**Required**: Remove the parentheticals. If a precondition discharge is genuinely non-obvious at one site, state it once there; otherwise let the citation stand.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer / sale of document rights
**Why out of scope**: The ASN correctly defers transfer to an Open Question (Nelson's "bought the document rights"). The refinement-only regime (O3, O8) is the system *as specified*; transfer is genuinely new territory, not an error here.

### Topic 2: Cross-node identity federation consistent with O9
**Why out of scope**: O9 establishes node-locality; federation invariants are listed as an Open Question and are new state/operations, not a gap in this ASN.

VERDICT: REVISE
