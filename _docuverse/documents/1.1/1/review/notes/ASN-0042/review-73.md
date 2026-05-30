# Review of ASN-0042

This ASN carries the `review-mode.anti-bloat` classifier. The mathematical core (O0–O10, the derived invariants, and the worked example) is sound and thorough — I found no correctness defect in the proofs. The findings below are accreted meta-prose and forward-reference patterns flagged at source, plus two redundancy items.

## REVISE

### Issue 1: Notation-justification prose in O8
**ASN-0042, IrrevocableDelegation (O8)**: "We state O8 with the four-place `delegated(Σ_d, Σ_d^{post}, π, π')`, naming the single introducing edge ... because the reachability quantifier `Σ_d^{post} →* Σ'` ranges over multi-step trajectories: the subscript abbreviation `delegated_{Σ_d}(π, π')` resolves only against a single named successor, so it would be malformed under a `→*` binder where `Σ'` is the path endpoint..."
**Problem**: This paragraph explains *why the four-place form is used instead of the abbreviation* — a justification of notation, not an advance of the claim. The reader does not need the malformedness argument to apply O8.
**Required**: Use the four-place predicate in the statement and delete the justification paragraph. If a one-clause reminder is needed, fold it into the precondition list, not a free-standing essay.

### Issue 2: Signature-justification prose in the delegation definition
**ASN-0042, Definition (delegated)**: "Both transition endpoints are explicit parameters; condition (iii) pins which successor `Σ'` introduces `π'`, so the predicate's meaning never depends on a contextually-supplied successor."
**Problem**: Meta-prose explaining why the signature is well-formed rather than what the predicate asserts. Conditions (i)–(vi) already carry the content.
**Required**: Delete. The abbreviation rule ("we write `delegated_Σ(π, π')` when `Σ'` is named in the surrounding formula") is sufficient.

### Issue 3: Redundant scope-status declarations around the identity note
**ASN-0042, Principal Identity and the Trust Boundary**: "We record this as a scope boundary of the ownership model, not as a property." ... *Scope note (Identity is exogenous)* ... "This scope note records a boundary the model does not cross; it makes no verifiable claim about reachable states and so is not listed among the model's axioms or derived properties."
**Problem**: Three separate sentences in one short section all assert the same fact — "this is a scope boundary, not a property." This is exactly the flagged pattern of prose justifying why something is *not listed*.
**Required**: Keep one statement of the scope boundary; delete the framing sentence before the note and the status-justification sentence after it.

### Issue 4: Forward-reference / use-site framing at FieldStructure and the covering-chain lemma
**ASN-0042, Account-Level Boundary**: "We record once the field-structure facts that both the well-formedness of `acct(a)` and the prefix relation `acct(a) ≼ a` (AccountPrefix, *Structural Provenance* below) rely on."
**ASN-0042, Ownership Domains**: "Before developing ownership domains' nesting structure, we extract a structural fact about the prefix relation `≼` that the subsequent proofs invoke repeatedly. ... we state it once as a named lemma."
**Problem**: Both lead with a use-site inventory ("relied on by X and Y below," "invoked repeatedly") and ordering justification ("we record once," "we state it once") rather than the lemma content. The lemmas stand on their own.
**Required**: State FieldStructure and the covering-chain lemma directly. Drop the "relied on below / stated once / invoked repeatedly" framing.

### Issue 5: Downstream-consumer enumeration in NestingByDelegation
**ASN-0042, State Axioms (NestingByDelegation)**: "The proofs of O10 (sub-delegate prefix maxima) and OwnershipDomainPermanence★ (sub-delegate inheritance) tacitly rely on this geometry — sub-delegates of a principal `π` are precisely the descendants of `π` in the forest..."
**Problem**: A use-site inventory naming downstream consumers of the lemma — flagged pattern. The forest characterization is the content; the list of who uses it is not.
**Required**: Keep the structural statement ("principals form a forest under strict-extension order, rooted at bootstrap principals"); delete the "the proofs of O10 and ★ tacitly rely on this" clause.

### Issue 6: Design-intent prose ("forevermore") restated across five sections
**ASN-0042**: Nelson's "once assigned a User account, the user will have full control over its subdivision forevermore" (LM 4/29) and the accompanying "not that `ω` is static ... but that no external act can alter it" gloss appear in *Account-Level Boundary*, *Permanence and Refinement* (intro), *OwnershipDomainPermanence* discussion, *O8 design confirmation*, and *Unilateral O10★*.
**Problem**: The same design rationale is re-derived in prose five times. Two paragraphs (Permanence-and-Refinement intro and the OwnershipDomainPermanence corollary discussion) say substantially the same thing in different words — flagged duplication.
**Required**: Anchor the "forevermore = no external act, refinement-only" reading once (at its tightest home, OwnershipDomainPermanence) and cite it elsewhere rather than re-arguing it.

### Issue 7: O0 adds no content beyond O1's decidability postcondition
**ASN-0042, Ownership as a Structural Predicate (O0)** and **O1**: O0 asserts `owns(π, a)` is "decidable from `pfx(π)` and `a` alone," and O1's *Decidability* paragraph re-establishes exactly this ("consulting no mutable system state. This satisfies the design requirement O0").
**Problem**: O0 is stated as a separate property but is discharged entirely as a corollary of O1's definition; the summary table itself labels it "verification target of O1's definition." It introduces no obligation O1 does not already carry. This is a definition/requirement split that doubles the surface without doubling the content.
**Required**: Either fold O0 into O1 as a named postcondition (decidability) of the definition, or justify what O0 constrains that O1's decidability clause does not.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer machinery
**Why out of scope**: The tension between transferable "document rights" (LM 2/29) and inalienable provenance (O6) is correctly logged as an Open Question, not modeled. Transfer would require an address-external registry, which belongs to a future ASN.

### Topic 2: Cross-node identity federation
**Why out of scope**: O9 establishes node-locality; what invariants a federation must satisfy to coexist with O9 is new territory, properly deferred to the Open Questions.

VERDICT: REVISE
