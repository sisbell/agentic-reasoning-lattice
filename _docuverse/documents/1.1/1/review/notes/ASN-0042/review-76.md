# Review of ASN-0042

## REVISE

### Issue 1: The delegation predicate is claimed complete but O18 imposes an unlisted seventh condition

**ASN-0042, O15 / O18 / DelegatorAllocatesPrefix**: O15 states principals enter Π "subject to six structural conditions, named the *delegation predicate*" and "no other mechanism introduces principals." The `delegated` definition lists exactly (i)–(vi). None requires `pfx(π') ∉ Σ.B`. Yet O18 (axiom) asserts `pfx(π') ∈ Σ'.B ∖ Σ.B` — a freshness requirement on every introducing transition.

**Problem**: The predicate is presented as the complete admission gate, but freshness lives entirely in O18 and is not among (i)–(vi). DelegatorAllocatesPrefix's "Freshness" step does not derive freshness from the delegation conditions — it cites O18: "By the strengthened O18 ... gives `pfx(π') ∈ Σ'.B ∖ Σ.B` directly." So the gate that actually decides which `π'` may enter is the conjunction of the six predicate conditions *and* O18, not the predicate alone. A delegation targeting an already-baptized namespace prefix satisfies (i)–(vi) but violates O18; the ASN never reconciles this except informally in the Worked Example ("mutually exclusive futures"), which itself appeals to O18 rather than the predicate.

**Required**: Either add freshness as condition (vii) of `delegated`, or prove that (i)–(vi) plus the baptism discipline entail `pfx(π') ∉ Σ.B`. Stop calling the six-condition predicate the complete admission criterion if O18 adds a seventh.

### Issue 2: "Why the axiom is needed" prose attached to O14

**ASN-0042, O14**: "The non-nesting conjunct (sixth clause) is load-bearing: without it, a bootstrapped principal could nest within another's domain ... and the Account-level permanence Corollary would fail. The baptized-prefix conjunct (seventh clause) is independent of the coverage conjunct of the first clause, which runs in the opposite direction ... The seventh clause closes that gap."

**Problem**: This is precisely the flagged anti-bloat pattern — prose around an axiom explaining *why each clause is needed* rather than stating what the axiom says. It defends the clause selection against an imagined weaker version instead of advancing the contract. The reader must skip it to reach the next claim.

**Required**: Delete the load-bearing/independence justification. The clauses stand on their own; their necessity belongs in the proofs that consume them (O8, PrefixBaptismCoupling), not in the axiom statement.

### Issue 3: Multiple sections defer to the Delegation section for the same content

**ASN-0042, O15 and the `delegated_Σ*` definition**: O15 says conditions (ii) and (vi) are "both developed in the *Delegation* section below." The `delegated` definition says the reflexive-transitive closure is "built from the structural parent relation `R_Σ` ... defined alongside NestingByDelegation below." O5's authorization is likewise cross-referenced to the same later material.

**Problem**: Several paragraphs in different sections defer to one downstream location — the compounding forward-reference pattern the classifier names. The conditions (ii)/(vi) discussion then appears a third time, restated, in the Delegation section ("Condition (ii) is the authorization constraint..."; "Condition (vi) enforces top-down delegation order...").

**Required**: State each condition's content once, at its definition. Remove the "developed below" pointers and the duplicate Delegation-section restatement of (ii)/(vi).

### Issue 4: Worked-example fork analysis duplicated for π_B

**ASN-0042, "The Fork as Ownership Boundary" (Worked Example), Forking by π_B**: "the user-field-separator argument articulated below for `π_A` transposes to `π_B` by substituting `pfx(π_B)` for `pfx(π_A)`, and applies identically to both branch outputs."

**Problem**: This is a second pass over a verification already done for π_A, acknowledged as a substitution. It is the "two paragraphs saying the same thing" pattern. The field-opening branch (`hwm_0 = 0`) is the only new element; the rest restates the π_A non-coverage argument.

**Required**: Keep only the field-opening branch verification (the genuinely new case) and drop the transposed restatement of the sibling-advance argument.

### Issue 5: Excluded-case parentheticals (reviser drift)

**ASN-0042, O3 Corollary**: "(The corollary makes no claim about addresses `a ∈ Σ'.B ∖ Σ.B` newly baptized in the transition — for such addresses, `ω_Σ(a)` is undefined and the inequality is ill-formed.)"

**Problem**: The corollary's precondition is already `a ∈ Σ.B`, which excludes newly baptized addresses. The parenthetical defends against a case the precondition forecloses — a paragraph imagining a case the carrier already excludes. The same pattern recurs in OwnershipDomainPermanence's closing paragraph ("When `π` has not yet exercised delegation authority at `Σ` ...").

**Required**: Remove the parenthetical; `a ∈ Σ.B` carries the restriction. Trim the OwnershipDomainPermanence tail to the NestingByDelegation citation if it is load-bearing, else drop it.

### Issue 6: Essay content in the O10 Postconditions slot

**ASN-0042, O10 Formal Contract, Postconditions**: The Postconditions field runs for a full paragraph — "The construction satisfies O5 ... The single-tier guarantee is exact: O10 does not promise content-bearing depth ... descent to content placement requires further baptisms inside `dom(a')`, each its own O5-authorized step under `π`'s continuing sovereignty."

**Problem**: The structural Postconditions slot holds a postcondition formula plus an essay re-explaining the construction, the B6 bound, and the depth caveat — all already established in the proof body. Flag the placement, not the content.

**Required**: Reduce the Postconditions field to the formula and the `zeros(a')` clause. Move the depth/sovereignty commentary out of the contract slot (or delete as duplicative of the proof).

### Issue 7: `allocated_by_Σ` introduction enumerates downstream consumers

**ASN-0042, `allocated_by_Σ(π, a)` (AllocatedBy)**: "What the ownership model constrains is its signature and the properties it must satisfy (O5, O16) ... Constraints: O5 (SubdivisionAuthority) — allocator is most-specific covering principal; O16 (AllocationClosure) — every new address has an allocator."

**Problem**: The definition's introduction lists which downstream properties consume it rather than advancing the relation's meaning — the flagged "enumerates downstream consumers" pattern. The semantics (a baptism produced `a` on behalf of `π`) is the only content; the O5/O16 inventory is consumer-side.

**Required**: State the signature and semantics; drop the "properties it must satisfy (O5, O16)" inventory from the introduction. O5 and O16 already reference this relation at their own sites.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer machinery
**Why out of scope**: The ASN correctly records transfer as an open question (Open Questions; the O3 discussion of "bought the document rights"). Specifying transfer invariants and the provenance/authority divergence is new territory for a future ASN, not a defect here.

### Topic 2: Authentication / session-to-prefix binding
**Why out of scope**: The "Principal Identity and the Trust Boundary" section explicitly externalizes the `session.account = pfx(π)` binding. Concrete authentication mechanisms are listed as out of scope, and the ASN treats the binding as exogenous — correct.

VERDICT: REVISE
