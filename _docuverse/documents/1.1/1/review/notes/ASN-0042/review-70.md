# Review of ASN-0042

## REVISE

### Issue 1: MostSpecificCoveringUnique is stated but never consumed
**ASN-0042, Ownership Domains**: "**MostSpecificCoveringUnique (derived).** Whenever a principal achieves the maximum prefix length among the covering principals of a tumbler, that principal is unique."
**Problem**: This corollary is proved, then never cited. Every site that needs the fact re-derives it inline instead: O2 Step 4, NestingByDelegation's `R_Σ` uniqueness ("the covering principals … are ≼-comparable … and have pairwise distinct prefixes (O1b)"), and DelegatorAllocatesPrefix all reconstruct the covering-chain + O1b argument from scratch rather than invoking MostSpecificCoveringUnique. A derived property with no consumer is dead weight.
**Required**: Either cite MostSpecificCoveringUnique at the re-derivation sites (NestingByDelegation, DelegatorAllocatesPrefix, O2 Step 4) and delete the inline repetitions, or remove the corollary.

### Issue 2: O14 misattributes why FiniteRegistry is needed
**ASN-0042, O14 commentary**: "This is the base case for the finiteness invariant `|Π_Σ| < ∞` (FiniteRegistry, derived below), **which the O10 fork argument relies on**."
**Problem**: O10's fork proof relies on no such thing. Its non-coverage analysis is universally quantified ("Every sub-delegate `π_i` … for each such `π_i ∈ Π_Σ`") and concludes π is longest-match by showing *every* other covering principal is strictly shorter — no maximum over a finite set is taken, so finiteness is never invoked. FiniteRegistry is actually used where a *maximum* must exist: NestingByDelegation's `R_Σ` ("a single maximal-length one exists") and MostSpecificCoveringUnique. The attribution to O10 is simply wrong.
**Required**: Correct the use-site to name NestingByDelegation (and MostSpecificCoveringUnique if retained), or drop the attribution clause entirely.

### Issue 3: "Why the axiom is needed" prose around the state axioms
**ASN-0042, O12 / O15 / O16 / O18**: e.g. O12 "removing a principal would reverse the refinement of `ω` … (violating O3's monotonic refinement below) and undo a delegation act (violating O8's irrevocability below)"; O15 "Without this closure, O12 permits arbitrary growth of Π — a mechanism … could introduce a principal at document level (violating O1a)"; O16 "Without this closure, addresses could appear … the derivation of O4 requires …"; O18's multi-clause "records the design commitment" paragraph.
**Problem**: These passages argue why each axiom must exist (with forward references to downstream properties) rather than stating what the axiom asserts. This is exactly the accreted defensive justification the anti-bloat classifier targets; the reader must skip past it to reach the axiom content.
**Required**: Reduce each axiom to its statement plus, at most, a one-line design citation (Nelson/Gregory). Move necessity arguments, if genuinely load-bearing, into the proofs that consume them.

### Issue 4: Document-ordering prose pairing O5 across two sections
**ASN-0042, State Axioms / Subdivision Authority**: State Axioms: "The consequences of O5 … are developed in the *Subdivision Authority* section below." Subdivision Authority: "O5 (SubdivisionAuthority) was stated in *State Axioms* above …"
**Problem**: A matched forward/backward pointer pair whose sole content is justifying where O5 lives. It advances no reasoning.
**Required**: State O5 once where its consequences are developed; drop the cross-pointers.

### Issue 5: Duplicated `acct(a)` definition and contract
**ASN-0042, Account-Level Boundary vs. Structural Provenance**: The `acct(a)` definition, four-case `zeros(a) ∈ {0,1,2,3}` well-formedness argument, and Formal Contract appear in *The Account-Level Boundary*; the AccountPrefix Formal Contract in *Structural Provenance* then restates the same `acct(a) = a when zeros(a)=0; … when zeros(a) ≥ 1` definition line, and AccountPrefix repeats a near-identical four-case analysis on `zeros(a)`.
**Problem**: Two paragraphs perform the same case split on the same value, and the definition is transcribed twice. One claim (well-definedness) and the other (prefix relation) are distinct, but the shared scaffolding is duplicated verbatim.
**Required**: Prove the field-structure facts (segment positivity, separator position by zero-count) once and have both AccountField well-formedness and AccountPrefix cite that single case analysis.

### Issue 6: Repeated deferral and repeated "forevermore" elaboration
**ASN-0042, OwnershipDomainPermanence / first-delegator Remark / surrounding prose**: The single-transition body, the OwnershipDomainPermanence★ corollary, the "Remark (first-delegator form)", and the trailing "The first-delegator form yields Nelson's 'forevermore' in its multi-step form" each restate that the delegation chain inducing changes inside `dom(π)` begins with π's own act and no external party can insert into it. Separately, both SelfOwnershipAtPrefix and OwnershipDomainPermanence defer their concrete verification to the same downstream Worked Example.
**Problem**: Multiple paragraphs in different slots state the same conclusion in different words, and multiple sections defer to one downstream location — both flagged compounding patterns.
**Required**: State the "forevermore" reading once (the corollary is the natural home); collapse the Remark into it or delete. Consolidate the Worked-Example deferrals into a single pointer.

### Issue 7: Meta-prose about citation and roadmap bookkeeping
**ASN-0042, State Axioms**: "On registry monotonicity … We state the distinction once here and cite B0 directly at each use site below." and the opening inventory "rests on seven transition-discipline axioms (O12, O13, O14, O15, O5, O16, O18) … from which we derive six further properties (O1a, O1b, FiniteRegistry, NestingByDelegation, O17, PrefixBaptismCoupling)".
**Problem**: Prose describing the document's own citation discipline and enumerating its derivation roster is bookkeeping, not reasoning. The roster duplicates the Properties Introduced table.
**Required**: Drop the citation-practice note (cite B0 at use sites silently); let the Properties table carry the inventory.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer, cross-node federation, content accessibility on owner deletion
**Why out of scope**: These are correctly confined to the Open Questions list and the exogenous-identity Scope note; the ASN raises them without specifying claims, which is the right treatment. No revision needed — flagged only to confirm the scoping is sound, not drifted.

VERDICT: REVISE
