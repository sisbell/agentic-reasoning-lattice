# Review of ASN-0042

This ASN carries the `review-mode.anti-bloat` classifier, and the dominant problem is exactly that: prior revision cycles (notably the recent O1a/O1b reclassification) have left rationale, use-site inventories, and duplicated derivations scattered through the prose. The mathematics is largely sound and properly abstract — but the argument is buried. Findings below are mostly source-level noise; one is a stated-but-unused lemma.

## REVISE

### Issue 1: O1a/O1b "derived invariant" rationale stated three times
**ASN-0042, `pfx(π)` axiom and State Axioms intro**: pfx axiom — *"injectivity is O1b; the account-level boundary ... is O1a. Neither is part of this axiom — both are established by induction over reachable states (base cases O14(iii)/(iv), preserved by delegation)..."*; State Axioms ¶2 — *"O1a ... and O1b ... are derived invariants, not constraints on the `pfx` primitive: the `pfx` axiom fixes only the codomain..."*; then re-derived in full in *Delegation*.
**Problem**: The same fact (these are derived, with base cases O14(iii)/(iv), preserved by delegation) is restated in three sections. The first two are pure meta-prose explaining *why the axiom is structured this way* rather than advancing reasoning — residue of the reclassification commit.
**Required**: Keep the actual derivation in *Delegation* (and the one-line entries in the Properties table). Delete the explanatory clauses from the `pfx` axiom and the State Axioms intro.

### Issue 2: MostSpecificCoveringUnique is stated, proved, and never used
**ASN-0042, Ownership Domains**: *"MostSpecificCoveringUnique (derived) ... supports the most-specific covering arguments in O7(a) and OwnershipDomainPermanence (Step 3)."*
**Problem**: This is a use-site inventory that is false. O2 Step 4 re-derives the identical argument inline; O7(a), DelegatorAllocatesPrefix, and OwnershipDomainPermanence invoke the *covering-chain lemma* + O1b directly, not this corollary. The lemma is dead weight whose advertised consumers don't cite it.
**Required**: Either invoke it at the named sites (and remove the inline duplication in O2 Step 4) or delete the corollary and the inventory sentence.

### Issue 3: O18 body is rationale and implementation narrative, not an axiom statement
**ASN-0042, O18**: *"This is the structural coupling ... The freshness conjunct ... records the design commitment that principal prefixes are reserved — Gregory's `findpreviousisagr` ... the registries are two views of the same act, not independent ledgers..."*
**Problem**: An axiom's prose should say what it asserts. Here the bulk explains *why the axiom is needed* and narrates implementation, exactly the flagged pattern. The base/inductive roles are the only load-bearing content.
**Required**: Reduce to the formula plus the base-case (O14 seventh clause) and inductive-step roles; drop the "two views," "design commitment," and `findpreviousisagr` essay (or move one sentence to a design-justification line).

### Issue 4: Roadmap inventory in State Axioms
**ASN-0042, State Axioms opening**: *"The ownership model rests on seven transition-discipline axioms (O12, O13, O14, O15, O5, O16, O18) together with the primitive allocation relation ... from which we derive six further properties ..."*
**Problem**: An enumeration of which labels are axioms vs. derived. It advances no reasoning and duplicates the Properties table.
**Required**: Remove; the per-property Status column already carries this.

### Issue 5: Defensive "what is NOT used" citations
**ASN-0042, Ownership Domains (Domains nest proof)**: *"(T5 ContiguousSubtrees plays no role here — its content is the lexicographic contiguity of prefix-defined intervals, not the componentwise expansion)."*
**Problem**: Negative-citation meta-prose explaining why a foundation property is *absent*. The reader does not need to be told what was not used. The same defensive style recurs (e.g., O0's "tight"-ness paragraph distinguishing the stranger handed `(pfx(π),a)` vs. only `a`).
**Required**: State the derivation from Prefix; drop the parenthetical disclaimers.

### Issue 6: Worked-example and O10 meta-prose about what each paragraph is doing
**ASN-0042, Worked Example / O10**: *"Concrete witness for SelfOwnershipAtPrefix. This paragraph exhibits a concrete instance ...; it does not re-derive the general fact."*; O10 *"Scope. This is trajectory-specific, not delegation-intrinsic..."*; *"The field-opening branch is ... one possible exhibition of a fresh delegate's first fork, not a structurally forced consequence."*
**Problem**: Sub-paragraphs labeled "Scope" and prose narrating what the example is/isn't establishing are noise the reader works around — flagged patterns. The verification itself (the ✓ checks) is fine; the commentary framing it is not.
**Required**: Keep the concrete checks; delete the sentences describing the paragraph's evidentiary status.

### Issue 7: Disproportionate existence essays in O7(c) and O8 precondition
**ASN-0042, O7(c) and O8**: O7(c)'s unbounded-chain construction (`π_0, π_1, ...` with boundary step, inductive extension, coverage/exhaustiveness sub-arguments) runs many paragraphs to witness "the right is recursive"; O8 carries two precondition paragraphs (*"The added hypothesis `π' ∈ Π_{Σ'}` constrains the trajectory..."* and *"Here `delegated_{Σ_d}(π, π')` abbreviates the four-place..."*) plus a three-step "delegate persists" argument that re-derives introduction-event uniqueness already implied by O15+O12.
**Problem**: Existence of an arbitrarily long account-level chain and the four-place-abbreviation reading are over-argued for what the contracts claim. The defensive precondition justification is reviser drift.
**Required**: Compress O7(c)'s witness to the boundary step + uniform inductive step (the coverage/exhaustiveness recursion can cite NestingByDelegation in one line). Reduce O8's precondition discussion to one sentence and fold the redundant uniqueness sub-argument into a citation of O15/O12.

## OUT_OF_SCOPE

### Topic 1: Whether `owns`-based authorization lets a parent act on delegated content
O0 remarks *"Authorization decisions reduce to prefix comparison"*, and the cited implementation predicate `isthisusersdocument`/`tumbleraccounteq` computes account-level containment (the non-exclusive `owns`), not longest-match `ω`. This raises a real tension with O8's irrevocability *as enforced*, but it lands in access control / what an owner may do — explicitly out of scope. The model correctly separates `owns` (O0/O1) from `ω` (O2), so this is not an error in the ASN's stated claims. Worth a one-line cross-reference to the enforcement scope note, not a fix here.

META: not applicable — the ASN defines ownership state, delegation operations, and reachable-state invariants at the right level of abstraction; it has not drifted into implementation mechanics.

VERDICT: REVISE
