# Review of ASN-0011

## REVISE

### Issue 1: CREATENEWVERSION has no stated frame conditions
**ASN-0011, Version Creation section**: DL16 states the source is unchanged, but no frame condition addresses non-source, non-new documents. Yet the DL-ISO proof claims: "by DL16 (source unchanged) and the frame condition that all documents other than the source and the new version are unaffected."
**Problem**: The cited frame condition does not exist. CREATENEWDOCUMENT has explicit frame conditions (DL-F1, DL-F2, DL-F3). CREATENEWVERSION has only DL16 (source unchanged). The proof of DL-ISO for CREATENEWVERSION appeals to a property that was never established.
**Required**: State explicit frame conditions for CREATENEWVERSION analogous to DL-F1/F2/F3: existing documents' arrangements unchanged, I-space unchanged (or only extended — DL15 claims no new allocation, which should be a frame condition), other accounts' counters unchanged.

### Issue 2: DL-ISO claims link preservation without any link frame condition
**ASN-0011, DL-ISO theorem**: "links_homed_in(d', Σ') = links_homed_in(d', Σ) — links preserved"
**Problem**: Neither CREATENEWDOCUMENT nor CREATENEWVERSION has a frame condition mentioning links. DL-F1 covers arrangements. DL-F2 covers I-space. Links are absent. The theorem introduces a new guarantee (link preservation) in its statement and declares it proven by frame conditions that do not address links.
**Required**: Either add link frame conditions to both operations, or remove the link conjunct from DL-ISO and note it as requiring separate treatment.

### Issue 3: Account permanence assumed but never stated
**ASN-0011, DL9 proof**: "The account set only grows (accounts are permanent)."
**Problem**: No axiom in this ASN establishes that Σ.accounts is monotonically growing. DΣ2 defines Σ.accounts but states no permanence property. The DL9 proof depends on account permanence — if an account could be removed, the prefix relation would lose its witness, and owner(d) would become undefined. The proof cites a property that was never introduced.
**Required**: Add an explicit property (e.g., DL-A0: a ∈ Σ.accounts ⟹ a ∈ Σ'.accounts for all subsequent Σ') or identify which existing axiom provides this.

### Issue 4: owner(d) uniqueness claimed without proof
**ASN-0011, DΣ2**: "The uniqueness of this account follows from the tumbler hierarchy: account addresses are separated by zero-field boundaries that prevent one account from being a prefix of another."
**Problem**: This is an assertion about tumbler structure, not a proof. The definition uses THE (definite description), which requires both existence and uniqueness. DΣ2 provides existence (every document has some account prefix). Uniqueness requires that no account is a prefix of another account — a property of the address space that is asserted but never formally established. The ASN should either prove prefix-freeness of accounts from tumbler structure or state it as an axiom.
**Required**: Either add an axiom (e.g., "for distinct a₁, a₂ ∈ Σ.accounts, neither prefix(a₁, a₂) nor prefix(a₂, a₁)") or derive it from stated tumbler properties.

### Issue 5: DL2 uses undefined identity function
**ASN-0011, DL2**: "identity(d, Σ) = identity(d, Σ')" where identity(d, Σ) denotes "whatever state was associated with d at its creation."
**Problem**: "Whatever state was associated with d at its creation" is not a definition. Which state components? The arrangement (which changes over time)? The I-space content (which grows)? The owner (which is derived from the address)? If identity means "the address itself," then DL2 collapses to DL0. If it means "the initial state," it needs to say which components, and it needs to explain how "initial state" is tracked (since the system doesn't record creation-time snapshots).
**Required**: Either define identity(d, Σ) precisely (e.g., as the address plus owner, which are immutable) or reformulate DL2 without it. The intent — "addresses are not recycled" — is clear; the formalization is not.

### Issue 6: Six Gregory/implementation references with function names and line numbers
**ASN-0011, multiple sections**: The ASN contains six paragraphs citing Gregory's implementation with C function names and source line numbers: `tumbleraccounteq`, `do1.c:234–241`, `do1.c:268–275`, `do1.c:281`/`do1.c:297`, `bert.c:325–336`/`orglincore`, `bert.c:145`/`bert.c:52–87`.
**Problem**: A specification note defines system guarantees, not implementation mechanics. Gregory findings may confirm properties but are not the proof. Function names and line numbers are implementation artifacts — an alternative implementation would not have them.
**Required**: Remove all Gregory references. Where they serve as the sole justification for a claim (e.g., DL22's "denial is triggered by the requester's own prior read access"), replace with behavioral reasoning from the abstract model.

### Issue 7: DL15 notation undefined
**ASN-0011, DL15**: "img(Σ'.poom(v)) = img(Σ.poom(source)|text)"
**Problem**: Two issues. First, `|text` is undefined — is this a domain restriction (V-positions in the text subspace)? A range restriction (I-addresses in the text subspace)? Second, img (image) captures only the SET of referenced I-addresses, not the arrangement structure. Two documents could satisfy DL15 while having completely different V-to-I mappings (same content, different ordering). If CREATENEWVERSION is supposed to produce an arrangement identical to the source's text arrangement, DL15 needs to say so. If only the set of I-addresses matters, state why arrangement structure is irrelevant.
**Required**: Define `|text` precisely. State whether the V-to-I mapping structure is preserved or only the image.

### Issue 8: No concrete example
**ASN-0011, entire document**: The ASN defines 25+ properties, two operations, and a theorem, but never verifies them against a specific scenario.
**Problem**: A worked example (e.g., "Account `1.0.2` creates document `1.0.2.0.1`, then inserts 'AB', then another user versions it — check DL3, DL5, DL13, DL14, DL15, DL16 against the resulting state") would expose whether the formal properties capture the intended behavior. Without one, the properties are untested against their own model.
**Required**: Add at least one concrete scenario that exercises CREATENEWDOCUMENT followed by CREATENEWVERSION (including the cross-user case), verifying the key postconditions against explicit state.

### Issue 9: DL8 introduces undefined concept
**ASN-0011, DL8**: "a link may also reference the document's address as a structural designator"
**Problem**: "Structural designator" is never defined. The ASN states that links reference I-space addresses in their endsets. An empty document has no I-space content. For a link to target an empty document, the link's endsets must reference something — but what? If the document's tumbler address can serve as a link endset entry, this conflates the document address space (tumblers in Σ.docs) with I-space addresses (tumblers in dom(Σ.ispace)). If there is a separate mechanism for document-level links, it needs to be defined.
**Required**: Either explain how link endsets reference a contentless document (which addresses are in the endset?) or qualify DL8 to state that empty documents can be identified (addressed, opened) but not linked to until they have content.

### Issue 10: DL5 claims ownership without proving allocation produces correct prefix
**ASN-0011, DL5**: "owner(d) = a ... because a is a prefix of d"
**Problem**: The claim that the allocated address d has a as a prefix is asserted but not derived. DΣ5 defines Σ.next(a) as a counter, and DL6 says it advances. But the ASN never states that addresses produced by the allocation mechanism are in the subtree rooted at a. The property "Σ.next(a) produces addresses with prefix(a, _)" needs to be stated — either as a definition of how allocation works or as a requirement on the counter.
**Required**: State explicitly that the allocation mechanism produces addresses under the account's prefix. E.g., "For all a ∈ Σ.accounts, the address produced by advancing Σ.next(a) satisfies prefix(a, d)."

## DEFER

### Topic 1: Crash recovery during CREATENEWDOCUMENT
**Why defer**: Acknowledged as an open question. The ASN correctly identifies the gap (address allocated but POOM not initialized). This is crash recovery territory, not a defect in the lifecycle model.

### Topic 2: Economic interaction with publication permanence (DL24)
**Why defer**: The ASN honestly states the tension ("the indefinite permanence of content in the absence of a paying party remains an open question"). This is economic-layer territory.

### Topic 3: Version graph recording for cross-user versions
**Why defer**: Acknowledged as open question. Whether derivation is recorded or only visible through shared I-addresses is a design decision that doesn't affect the properties stated here.

### Topic 4: Weakest precondition analysis
**Why defer**: The ASN introduces the state model and lifecycle properties. A wp analysis of operations against these invariants would strengthen it, but the current scope — defining the properties — is coherent without it. A future ASN could develop the wp analysis systematically.