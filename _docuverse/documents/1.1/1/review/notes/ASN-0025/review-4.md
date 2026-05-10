# Review of ASN-0025

## REVISE

### Issue 1: INSERT freshness derivation cites T9 alone
**ASN-0025, INSERT**: "Freshness (B ∩ Σ.A = ∅) is guaranteed by T9 (forward allocation): new addresses are strictly greater than all existing ones under T1."
**Problem**: T9 guarantees monotonicity *within a single allocator's sequential stream*. It does not guarantee that a new address from allocator A₁ is distinct from an existing address produced by allocator A₂. The claim "strictly greater than all existing ones" overclaims T9. Cross-allocator freshness requires T10 (partition independence) or GlobalUniqueness.
**Required**: Cite the full chain: T9 (intra-allocator monotonicity) + T10 (inter-allocator disjointness), or cite GlobalUniqueness directly. The same fix applies wherever freshness is asserted for CREATE LINK, CREATE VERSION, and CREATE DOCUMENT — all cite only "o ∉ Σ.A" or "l ∉ Σ.A" without naming the guarantee.

### Issue 2: V-space postconditions for INSERT and DELETE are informal
**ASN-0025, INSERT**: "All V-positions at or beyond p shift forward by width n. The I-addresses of the shifted entries are unchanged — only their V-positions move."
**Problem**: The J0 preservation proof for INSERT relies on the claim "Shifted V-entries retain their original I-addresses, which are in Σ.A ⊆ Σ'.A." This is stated in prose, not as a formal postcondition. The same issue applies to DELETE ("Subsequent V-positions shift backward... The I-addresses of shifted entries remain unchanged"). The ASN introduces J0 as a formal well-formedness invariant with quantifiers and set containment, then verifies it via informal prose about V-space behavior. The gap: without a formal V-space postcondition stating that the shift preserves I-address mappings, the J0 proofs are arguments by assertion.
**Required**: State formal V-space postconditions for INSERT and DELETE — at minimum, the claim that shifted entries preserve their I-address mappings. For INSERT, something like: `(A q : q ∈ dom(Σ.v(d)) ∧ q ≥ p : Σ'.v(d)(q ⊕ [n]) = Σ.v(d)(q))`. This is the non-trivial step the J0 proofs depend on. The ASN need not formalize the full V-space algebra — just the postconditions that J0 requires.

### Issue 3: {next} insertion position undefined
**ASN-0025, INSERT**: "p is a valid insertion position in dom(Σ.v(d)) ∪ {next}"
**Problem**: The symbol `{next}` is not defined. The intent is clear (the position after all existing content), but `dom(Σ.v(d)) ∪ {next}` mixes V-positions with an undefined symbolic constant. For an empty document (dom = ∅), the only valid position is `next`, whose value is unspecified. The same issue appears in COPY's precondition.
**Required**: Define `next` in terms of the V-space model — e.g., one past the maximum existing V-position, or the first position when the document is empty. Alternatively, define the set of valid insertion positions directly without the symbol.

### Issue 4: Σ.D evolution not formalized
**ASN-0025, State Model**: "Σ.D is the set of existing document identifiers."
**Problem**: The state model defines Σ.D but never states how it evolves across transitions. CREATE VERSION and CREATE DOCUMENT implicitly add to Σ.D ("A new document d' appears in Σ'.D"), but no property says Σ.D only grows. Since J0 quantifies over Σ.D, and since the permanence motivation applies equally to documents as to content (a document address is an I-space orgl by CREATE DOCUMENT's postcondition), the connection should be drawn: if orgl(d) ∈ Σ.A and P0 prevents removal from Σ.A, then d cannot leave Σ.D. The ASN has the pieces — P0, the orgl allocation in CREATE DOCUMENT and CREATE VERSION — but does not assemble them into an explicit document-set monotonicity property or a formal rule for Σ'.D in each operation.
**Required**: Either introduce a property `Σ.D ⊆ Σ'.D` (analogous to P0 for Σ.A) and derive it from P0 plus the orgl relationship, or state per-operation postconditions for Σ'.D (as is done for Σ'.A).

## OUT_OF_SCOPE

### Topic 1: Full V-space editing algebra
**Why out of scope**: The formal specification of V-space shift operations (how positions are renumbered, gap closing, subspace isolation proofs) is editing-operations territory. This ASN correctly defers to TA7a/TA7b for the shift mechanics and focuses on the I-space permanence properties that survive any conforming V-space implementation.

### Topic 2: Link endset formalization
**Why out of scope**: The ASN explicitly conditions its link survivability derivation on the premise that endsets reference I-space addresses and defers the full formalization to a link ASN. This is the right boundary.

### Topic 3: COPY self-transclusion (d' = d)
**Why out of scope**: When source and target document are the same, the V-space interaction between the source span and the insertion point is an editing-operations concern. The permanence properties (P3, P5, J0) hold regardless — I-space is unchanged and the transcluded I-addresses are in Σ.A.

VERDICT: REVISE
