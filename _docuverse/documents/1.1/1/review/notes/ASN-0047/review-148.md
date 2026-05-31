# Review of ASN-0047

## REVISE

### Issue 1: First content V-position depth is not pinned by K.μ⁺'s precondition
**ASN-0047, *Elementary transitions* (K.μ⁺) and *Link-subspace extension* (LinkVPositionDepthAxiom)**: K.μ⁺'s precondition lists "S8a, S8-depth, S8-fin, D-CTG, D-MIN" but nothing fixing the *depth* of the first content V-position when `V_{s_C}(d) = ∅`. The LinkVPositionDepthAxiom section asserts the content side "already carries a foundation predicate governing its first insertion: ASN-0036's `ValidFirstInsertionPosition(d, v, m)` ... K.μ⁺ realises it directly."

**Problem**: The link subspace gets an explicit axiom (LinkVPositionDepthAxiom) wired into K.μ⁺_L's precondition; the content subspace gets only an assertion of inheritance in a *different* section. K.μ⁺'s own precondition list never cites `ValidFirstInsertionPosition`. The ASN itself concedes "K.μ⁺'s preconditions (S8a + S8-depth + D-MIN★) do not pin the depth of the first content insertion." So a reader checking K.μ⁺ in isolation cannot determine the first content position's depth — the claim "K.μ⁺ realises it directly" is stated, not established. This is an internal inconsistency: the ASN took the trouble to discharge the link-side underdetermination with an axiom but left the structurally identical content-side underdetermination as prose.

**Required**: Cite `ValidFirstInsertionPosition` explicitly inside K.μ⁺'s precondition for the `V_{s_C}(d) = ∅` case (as K.μ⁺_L cites LinkVPositionDepthAxiom for `V_{s_L}(d) = ∅`), so the realisation is wired in rather than asserted at a distance.

### Issue 2: Within-account entity-distinctness discharge is too narrow
**ASN-0047, *Extended reachable-state invariants*, "Entity distinctness" prose**: "Within a single account, T10a GlobalUniqueness on the account's document sub-allocator chain discharges directly."

**Problem**: Two documents sharing a parent account need not lie on the same chain. A version `inc(d_src, 1)` preserves `parent(d_new) = parent(d_src)` (K.δ-ID.parent-0/1), so a direct document `[A.0.1]` (on `A_doc(A)`) and a version `[A.0.1.1]` (on `A_v([A.0.1])`) both have parent `A` yet inhabit *different* sub-allocator chains. "GlobalUniqueness on the account's document sub-allocator chain" names only `A_doc(A)` and does not cover the version, which is not on that chain. The same-parent-account case is therefore incompletely discharged.

**Required**: Discharge same-parent-account distinctness by plain GlobalUniqueness across distinct allocation events (which covers cross-chain pairs), or by T10a.6 domain-disjointness between `A_doc(A)` and the relevant `A_v(·)`, rather than restricting to a single chain.

### Issue 3: Essay prose around LinkVPositionDepthAxiom explaining why no companion axiom exists
**ASN-0047, *Link-subspace extension***: The second paragraph of LinkVPositionDepthAxiom ("The same vacuity afflicts the content subspace ... We introduce no `ContentVPositionDepthAxiom`, however, because ... the asymmetry between the two subspaces is therefore one of *where the discipline is stated* ... not a gap left open for content.")

**Problem**: This is meta-prose explaining *why the axiom is needed* and *why a companion axiom is not*, rather than advancing what the axiom says (matches the flagged drift pattern "new prose around an axiom explains why the axiom is needed rather than what it says"). The substantive content — that the content side's first-insertion depth is governed by `ValidFirstInsertionPosition` — belongs at K.μ⁺'s precondition (Issue 1), not as a defensive justification appended to the link axiom.

**Required**: Delete the companion-axiom justification paragraph; move the one load-bearing fact (content first-insertion depth comes from `ValidFirstInsertionPosition`) into K.μ⁺'s precondition.

### Issue 4: Forward-reference accretion — repeated deferral and axiom-discharge meta-commentary
**ASN-0047, multiple sites**:
- CL-OWN, CL-UNIQ, and NodeLineage each say "Proved as part of ExtendedReachableStateInvariants below" — three separate paragraphs deferring to the same downstream location (matches "multiple paragraphs in different sections defer to the same downstream location").
- NodeUniqueAllocation sub-case B discharge contains: "(The structural derivation through '...' is the *content* of clause (c); the clause names the closure explicitly so the discharge cites the axiom directly without reconstructing the chain at each invocation.)" — meta-prose explaining why the clause is structured as a named closure rather than advancing the discharge.

**Problem**: These are noise the precise reader must skip past. The triple-deferral adds nothing the index in ExtendedReachableStateInvariants does not already carry; the parenthetical justifies the axiom's *shape* rather than applying it.

**Required**: Drop the "Proved as part of … below" stubs (the invariant list already enumerates them) and delete the clause-(c) self-justification parenthetical, leaving the direct citation.

### Issue 5: K.α "no local amendment" downstream use-site inventory
**ASN-0047, *Amendments to existing transitions*, K.α paragraph**: "Downstream sites in this ASN — verification matrix, body prose, and the *Properties Introduced* tables — cite this inherited precondition by name as **K.α's `E(a)₁ = s_C` precondition** ..."

**Problem**: Enumerating downstream consumers of an inherited precondition (matches "a definition's introduction enumerates downstream consumers rather than advancing meaning"). The fact that the precondition is inherited from ASN-0093 is the load-bearing point; the catalogue of where it is later cited is bookkeeping.

**Required**: State that K.α's content-subspace precondition is inherited from ASN-0093 and stop; remove the use-site inventory.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal / tombstone mechanism
**Why out of scope**: The ASN correctly defers a status-flag/retraction mechanism for withdrawing an interior link without suffix-removing its successors (catalogued in Open Questions). This is a separate mechanism over `dom(L)`, legitimately future work.

### Topic 2: Node-allocation registry protocol
**Why out of scope**: The abstract boundary at NodeUniqueAllocation / NodeRegistryBootstrap is defensible; specifying the registry's issuing protocol and concurrency discipline belongs in a future ASN, as the Open Questions note.

META: (not applicable — the ASN defines abstract state, transitions, and invariants that an alternative implementation would also have to satisfy; it has not drifted into implementation mechanics.)

VERDICT: REVISE
