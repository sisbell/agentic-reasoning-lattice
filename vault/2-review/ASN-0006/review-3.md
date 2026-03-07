# Review of ASN-0006

## REVISE

### Issue 1: Ordering of copied addresses not established
**ASN-0006, TC1/TC2**: TC2 states `{a : (E q : q ∈ [p, p + w) : poom'(target).q = a)} = iaddrs(source_span)` — a set equality.
**Problem**: Set equality does not constrain ordering. The specification permits COPY to deposit source addresses in any permutation at the target positions. If the source has addresses [a₁, a₂, a₃] at positions [s, s+3), TC2 allows poom'(target).(p+0) = a₃, poom'(target).(p+1) = a₁, poom'(target).(p+2) = a₂. The concrete trace assumes the natural ordering (H-E-L-L-O, not a permutation), but the formal statements do not establish it.
**Required**: Replace the set equality with a pointwise mapping that preserves source order: `(A i : 0 ≤ i < w : poom'(target).(p ⊕ i) = poom(source_doc).(source_start ⊕ i))`. TC1 can then be derived from TC2 by existential weakening.

### Issue 2: TC8 derivation from TC7 is unsound
**ASN-0006, TC8**: "TC8 is a corollary of TC7 and the position ordering. Since all link positions (0, _) precede all text positions (1, _)... TC7's first clause then gives poom'(target).q = poom(target).q for all such q."
**Problem**: TC7's first clause quantifies over `q ∈ text_subspace(target) ∧ q < p`. A link position q = (0, k) is not in text_subspace(target), so it does not satisfy the antecedent. TC7 says nothing about link positions — it restricts both clauses to text_subspace. The claimed derivation applies TC7 to positions outside its quantification domain.
**Required**: Either (a) broaden TC7's preservation clause to quantify over `dom(poom(target))` rather than `text_subspace(target)` — which would make TC8 a genuine corollary — or (b) state TC8 as an independent postcondition with its own justification.

### Issue 3: AX1 claims universality but verifies only four operations
**ASN-0006, AX1**: "Every operation modifies the POOM of at most one document... confirmed for each operation individually: INSERT... DELETE... COPY... CREATENEWVERSION."
**Problem**: The axiom claims "every operation" but the enumeration covers only four. MAKELINK is notably absent. If MAKELINK modifies the link subspace of a document's POOM (which the position model implies — `link_subspace(d) = {q ∈ dom(poom(d)) : q.s = 0}`), then the axiom depends on MAKELINK modifying at most one document's POOM. If a link's endsets span multiple documents and MAKELINK registers link ISAs in each, AX1 is false. The independence theorem and its corollary cite AX1 without restriction; if AX1 fails for any operation, the theorem's proof has a gap for that operation.
**Required**: Either (a) verify AX1 for MAKELINK and any other mutating operations (RETRIEVEENDSETS, FINDDOCSCONTAINING, etc. are presumably read-only but should be noted as such), or (b) restrict the claim to the verified operations and qualify the independence theorem accordingly.

### Issue 4: Frame conditions omit the links set
**ASN-0006, Formal summary**: "Frame: I-space is unchanged (TC6). No document's POOM other than the target is modified (TC5). The link subspace of the target document is unchanged (when copying text content, TC8)."
**Problem**: The state Σ includes `links` as a top-level component, but no frame condition constrains it. The specification as written allows COPY to create, modify, or delete link structures as a side effect while satisfying all stated postconditions. This is clearly not intended but is not excluded.
**Required**: Add `links' = links` to the frame conditions. COPY does not create, modify, or remove links.

### Issue 5: Concrete trace addresses violate Element subspace encoding
**ASN-0006, "The state we need"**: "The Element field's first component identifies its subspace (1 for text, 2 for links)."
**ASN-0006, "A concrete trace"**: Document A's I-addresses are `[1.0.1.0.1.0.1 .. 1.0.1.0.1.0.5]` — five text bytes.
**Problem**: Parsing `1.0.1.0.1.0.2` per the stated structure: Node=1, sep=0, User=1, sep=0, Document=1, sep=0, Element=2. The Element field's first (and only) component is 2, which by the encoding rule indicates link subspace. But this address is the second byte of "HELLO" — text content. Addresses `1.0.1.0.1.0.3`, `1.0.1.0.1.0.4`, `1.0.1.0.1.0.5` have the same problem (Element first components 3, 4, 5 are undefined by the rule). Only `1.0.1.0.1.0.1` (Element=1, text subspace) is consistent.
**Required**: Either (a) use addresses where Element is multi-component with subspace prefix (e.g., `1.0.1.0.1.0.1.1` through `1.0.1.0.1.0.1.5`, where Element = 1.1..1.5, first component = 1 = text), or (b) note that the trace uses simplified addresses and the subspace encoding applies to the full address form.

### Issue 6: TC11 is a restatement of the definition, not a derived property
**ASN-0006, TC11**: "If link L has a discoverable endset referencing I-address a, and document B's POOM maps some position to a, then L is discoverable through B."
**Problem**: This is the definition of `discoverable_links(B) = {L ∈ links : endsets(L) ∩ iaddrs_of(B) ≠ ∅}` restated as a conditional. It is tautologically true and does not reference COPY. The interesting theorem — that COPY of content whose I-addresses intersect a link's endsets causes that link to become discoverable through the target — combines TC1 with the definition, and is argued persuasively in the surrounding prose, but is not what TC11 formalizes.
**Required**: Restate TC11 as the derived property: after COPY, `discoverable_links(target) ⊇ {L ∈ links : endsets(L) ∩ iaddrs(source_span) ≠ ∅}`. This is the non-trivial consequence of TC1 + the definition.

### Issue 7: Source specification inconsistency
**ASN-0006, TC3**: `copied_addresses = iaddrs(source_specset)` — uses "source_specset."
**ASN-0006, precondition/TC4/TC7/TC10**: `source_span ⊆ dom(poom(source_doc))`, `source_doc` — uses singular span and document.
**Problem**: TC3 describes COPY as operating on a specset (possibly multi-document, multi-span). All other formal properties use a single source_span from a single source_doc. The formal specification covers single-document, single-span COPY; TC3 describes a more general operation. The signature of COPY is inconsistent across the ASN.
**Required**: Either (a) generalize the precondition and postconditions to use source_specset consistently, or (b) restrict TC3 to source_span and note that multi-span/multi-document COPY is a composition of single-span operations (or deferred to a future ASN).

### Issue 8: Missing TC12
**ASN-0006, Properties table**: Numbering proceeds TC11, TC13, TC14...
**Problem**: TC12 is absent. Whether removed or never assigned, the gap is confusing for cross-referencing.
**Required**: Either assign TC12 or renumber. If TC12 was removed, a note in the properties table would prevent confusion.

## OUT_OF_SCOPE

### Topic 1: Multi-document COPY semantics
**Why out of scope**: The ASN describes COPY with multi-document specsets in prose and TC3, but formalizing the full multi-document case — including atomicity, ordering across documents, and the interaction of multiple source POOMs — is new territory beyond fixing the current specification's inconsistency.

### Topic 2: MAKELINK specification and AX1 verification
**Why out of scope**: Verifying AX1 for MAKELINK requires formally specifying MAKELINK's effects on document POOMs and the links set. That specification is a separate ASN (or part of a link-focused ASN). The fix here is to acknowledge the gap, not to specify MAKELINK.

### Topic 3: RETRIEVE semantics and TC22 tension
**Why out of scope**: TC22 acknowledges that functionally equivalent POOMs may produce different RETRIEVE output (different span counts). Whether RETRIEVE is defined over the abstract mapping or the representation is a question about RETRIEVE's specification, not COPY's.

VERDICT: REVISE
