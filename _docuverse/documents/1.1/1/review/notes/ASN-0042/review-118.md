# Review of ASN-0042

## REVISE

### Issue 1: "Σ.B is an ASN-0040-reachable registry" is load-bearing but never discharged as a named invariant
**ASN-0042, O10 construction / PrefixBaptismCoupling / Worked Example**: "By O14's bootstrap-registry clause (base case) and O17b (BaptismalRegistryCoupling, inductive step), every reachable Σ.B is an ASN-0040-reachable registry, so `hwm` and `next` are well-defined on it (their B1 and finiteness preconditions hold)."
**Problem**: This fact is invoked repeatedly — every appeal to `hwm`, `next`, B1, and B6 in O10 and in the worked example rests on it — yet it is assembled ad hoc inline ("O14 base case + O17b step") and never stated and proved as a discharged derived invariant. `next` requires `B ⊆ T` finite; `hwm` requires B1 to hold for `(p, d)`. Both preconditions are available *only* if Σ.B is an ASN-0040-reachable registry, so the inductive claim is doing real work in three separate proofs.
**Required**: Promote it to a named derived invariant (e.g., `RegistryReachability`: every reachable Σ.B is an ASN-0040-reachable registry conforming to B₀ conf.) with an explicit base case (O14's bootstrap-registry clause) and step (O17b restricts each registry change to a `Bop(p,d)` edge, which ASN-0040 closes over reachable registries). Cite the named invariant where `hwm`/`next`/B1/B6 are used.

### Issue 2: O7(c) restates the binding/auto-discharged split three times with a cross-slot deferral
**ASN-0042, O7 postcondition (c), proof of (c), and Formal Contract (c)**: "the binding obligations being conditions (iii) and (v) of O15 (condition (i) is fixed by the choice of p'', and conditions (ii) and (iv) are auto-discharged at entry; see the proof and the Formal Contract)."
**Problem**: The same partition of conditions (i fixed; ii, iv auto-discharged; iii, v binding) is stated in the postcondition prose, re-derived in the proof, and restated in the Formal Contract. The parenthetical "see the proof and the Formal Contract" is a same-document deferral to two locations — exactly the accretion pattern flagged for this note. The reader must cross-check three slots to confirm one claim.
**Required**: Derive the (ii)/(iv) auto-discharge once (in the proof), and let the postcondition and Formal Contract reference the result without re-enumerating which conditions are binding.

### Issue 3: Worked Example closing paragraph re-derives O10's general mechanism instead of checking the concrete instance
**ASN-0042, Worked Example, final paragraph**: "The trajectory illustrates Unilateral O10★, which holds for *every* π ∈ Π_Σ by a uniform mechanism: the witness a' = pfx(π).0.{hwm_0 + 1} carries the separator 0 at position #pfx(π) + 1, whereas every Form-A sub-delegate is strictly positive at that position… O10's body (the non-coverage analysis) covers both branches in full."
**Problem**: A worked example should exhibit the postcondition against specific numbers; this paragraph instead restates the general Form-A/Form-B non-coverage argument already proved in O10's body — duplicating the proof in different words. The trailing "O10's body covers both branches in full" is a bare pointer that advances no reasoning.
**Required**: Cut the general re-derivation and the pointer sentence; keep only the concrete verification (the [1,0,3] / [1,0,2,3,0,1] checks already present above it).

### Issue 4: OwnershipDomainPermanence opens with generality/motivation meta-prose
**ASN-0042, OwnershipDomainPermanence statement**: "The property holds at every principal level — node, account, and sub-account along delegation chains — and quantifies over arbitrary π ∈ Π_Σ; the historically motivating instance is the account-level case (Nelson's 'forevermore'), but the formal statement is general."
**Problem**: The formula already quantifies over arbitrary `π ∈ Π_Σ`; the sentence explains *why the statement is general* and supplies historical motivation rather than advancing the claim. This is essay content in a structural slot.
**Required**: Delete; the quantifier carries the generality, and the Nelson grounding already appears in *Permanence and Refinement*.

### Issue 5: O8 "Design confirmation" is defensive epistemic prose about what the implementation does *not* establish
**ASN-0042, O8, Design confirmation**: "Gregory's `validaccount` is a stub that unconditionally returns TRUE, confirming only the *absence of any revocation mechanism*… not the exclusivity conclusion itself. The irrevocability O8 establishes rests on the longest-match rule… a model theorem the stub neither computes nor witnesses."
**Problem**: This is a disclaimer about the limits of an evidence pointer, not a statement of what an operation does. It exists to pre-empt a reader's objection rather than to advance the argument.
**Required**: Reduce to the load-bearing fact ("the implementation provides no revocation path") and drop the meta-commentary on what the stub does/does not witness.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer and provenance/effective-owner divergence
**Why out of scope**: O3/O6 establish a refinement-only regime and inalienable provenance; transfer would let `ω(a)` and `acct(a)` diverge. The ASN correctly defers this to the Open Questions — it is new state-transition territory, not a defect here.

### Topic 2: Cross-node identity federation consistent with O9
**Why out of scope**: O9 fixes node-locality from prefix geometry; federation across node roots introduces new principals and new invariants. Correctly listed as an Open Question.

META: not applicable — the ASN defines ownership state (Π, pfx, ω), the delegation and fork operations, and reachable-state invariants at the abstract level any conforming implementation must satisfy; it has not drifted into implementation mechanics.

VERDICT: REVISE
