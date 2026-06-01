# Review of ASN-0047

## REVISE

### Issue 1: FrontierEquivalence content restated three times
**ASN-0047, FrontierEquivalence lemma + K.δ "Rationale (k = 0 conjuncts)" + K.δ "Freshness discharge" + §K.δ case (ii) discharge, k=0 bullet**: The biconditional "`inc(t, 0) ∉ Σ.E ⟺ t is the frontier`" is proved once as a lemma, then its forward direction is re-explained in prose at least three more times — "FrontierEquivalence (forward direction) above establishes that `inc(t,0) ∉ E` holds iff `(t, 0)` has not yet fired…" (Rationale), "FrontierEquivalence above establishes that this precondition is achievable and stable…" (Freshness discharge), and again "FrontierEquivalence then forces `e = inc(t, 0) ∉ E`" (k=0 bullet).
**Problem**: Same claim in different words across four loci (the "two paragraphs say the same thing" pattern). A reader must reconcile four statements of one lemma to confirm they agree.
**Required**: State the lemma once; at each use site cite it by name with no re-derivation ("by FrontierEquivalence, `inc(t,0) ∉ E`").

### Issue 2: K.δ freshness discharge is duplicated across three sections with circular deferral
**ASN-0047, K.δ definition ("Freshness discharge" paragraph) and §K.δ case (ii) discharge and parent-allocator activation**: The K.δ definition both (a) contains its own "Freshness discharge" paragraph that performs the case (i)/(ii) split, and (b) says the case-(ii) freshness is "discharged per sub-case by the discharge route detailed in §*K.δ case (ii) discharge and parent-allocator activation* below" — while that downstream section performs the same discharge in full again.
**Problem**: The same obligation (`e ∉ E`) is discharged in three places, with the inline paragraph forward-pointing to a section that re-does it. This is the deferral-accretion pattern flagged in the note: prose deferring to a downstream location that duplicates rather than replaces it.
**Required**: Discharge `e ∉ E` in exactly one location. Either keep the inline paragraph and delete the standalone section, or replace the inline paragraph with a single pointer and keep the section — not both.

### Issue 3: Sub-case A2 discharged twice in adjacent paragraphs
**ASN-0047, §K.δ case (ii) discharge, k=2, Sub-case A2 and "Discharge of sub-case A2 via T10a.6"**: Sub-case A2 first establishes `t ∈ dom(A_account(parent(t)))` "via the T10a T1 sibling-increment… placing `t` into `dom(A_account(parent(t)))`," and the immediately following paragraph "Discharge of sub-case A2 via T10a.6" re-derives the same membership "directly, without recursion through prior emissions."
**Problem**: Two consecutive paragraphs establish the identical membership fact by two framings of the same T10a.6 appeal — relocated/duplicated content, not advancing the argument.
**Required**: Collapse to a single discharge of A2's membership obligation.

### Issue 4: LinkVPositionDepthAxiom is redundant given S8-depth + S8a + operational first-insertion
**ASN-0047, LinkVPositionDepthAxiom**: "Each document `d ∈ E_doc` has a fixed link-subspace V-position depth `m_L(d) ≥ 2`, determined at the first link-subspace insertion… and unchanged thereafter," justified as resolving "the underdetermination S8-depth leaves open on an empty link subspace."
**Problem**: Every clause of this axiom is already supplied without an axiom: the lower bound `≥ 2` is S8a; "unchanged thereafter" is exactly S8-depth (uniform depth within a subspace); and "determined at first insertion" is an operational choice made by K.μ⁺_L's precondition (`If V_{s_L}(d) = ∅: v_ℓ = [s_L,1,...,1]` of the chosen depth). The content subspace faces the identical empty-subspace underdetermination and resolves it *operationally* via ASN-0036's `ValidFirstInsertionPosition` predicate with no new axiom — the ASN itself notes "K.μ⁺ realises this predicate directly… just as K.μ⁺_L cites LinkVPositionDepthAxiom." The asymmetry (axiom for links, no axiom for content) is unexplained, and the axiom asserts nothing the operation's precondition plus S8a/S8-depth do not.
**Required**: Either eliminate LinkVPositionDepthAxiom and pin the empty-link-subspace depth operationally in K.μ⁺_L's precondition (mirroring content's treatment), or state precisely what the axiom guarantees that S8a + S8-depth + the operational first-insertion choice do not.

### Issue 5: Properties-Introduced/Inherited entries carry use-site inventory and rationale instead of statement
**ASN-0047, "Inherited from foundation" table, SubspaceConventionAxiom row**: "Pins the subspace identifier values used by Nelson (LM 4/30–4/31) and reproduced in udanax-green (xanadu.h:144–146; granf2.c:162; do2.c:94). The consequence `SC-NEQ ≡ s_C ≠ s_L` (1 ≠ 2) is the structural precondition for every disjointness argument in this ASN."
**Problem**: A table whose purpose is to record label + statement instead carries implementation-citation provenance and a downstream-consumer inventory ("the structural precondition for every disjointness argument") — the "enumerates downstream consumers" pattern. The axiom's content is just `s_C = 1 ∧ s_L = 2`.
**Required**: Reduce the entry to the statement and its foundation source; drop the use-site inventory and implementation citations (these belong, if anywhere, in the body discussion, not the index table).

### Issue 6: P7a cross-layer derivation cites superseded J1 rather than J1★
**ASN-0047, §Cross-layer invariants, P7 a derivation**: "For `a ∈ dom(C') \ dom(C)` (freshly allocated), J0 gives `a ∈ ran(M'(d))` for some d; J1 then gives `(a, d) ∈ R'`."
**Problem**: In the extended two-subspace state J1 is explicitly superseded by J1★ (the ASN states J1 "is superseded by J1★ in the extended state"). The Class (b) verification correctly re-derives P7a from J0 + J1★, but this standalone derivation invokes the retired coupling, leaving two non-identical derivations of the same property and citing a constraint the ASN says no longer governs composites.
**Required**: Cite J1★ (and the S3★ + L14 + S3★-aux step that forces the witnessing V-position to be content-subspace) in the cross-layer P7a derivation, or delete the standalone derivation and point to the Class (b) discharge.

## OUT_OF_SCOPE

### Topic 1: Minimal node-allocation registry protocol
**Why out of scope**: The final Open Question asks what protocol a node-allocation registry must implement to satisfy NodeUniqueAllocation. Registry mechanism (issuing protocol, persistence, concurrency) is allocation-substrate/operations territory, correctly deferred rather than specified here.

### Topic 2: Account-level depth-1 extension
**Why out of scope**: Whether K.δ should admit `k = 1` on accounts is raised as an Open Question and correctly left to a future extension; it is new entity-discipline territory, not an error in the present model.

VERDICT: REVISE
