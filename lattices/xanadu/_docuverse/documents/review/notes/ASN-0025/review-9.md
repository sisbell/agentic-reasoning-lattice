# Review of ASN-0025

## REVISE

### Issue 1: DocId type undefined; fresh document identity not established

**ASN-0025, State Model / CREATE VERSION / CREATE DOCUMENT**: DocId is used throughout (Σ.D, Σ.v : DocId → (VPos ⇸ IAddr)) but never formally defined.

**Problem**: CREATE VERSION and CREATE DOCUMENT produce "a new document d'" and assert Σ'.D = Σ.D ∪ {d'}, but never establish d' ∉ Σ.D. Without this, d' could collide with an existing document, making the V-space postconditions inconsistent with UF-V. The natural derivation — if DocId = IAddr and documents are identified by their orgls, then o ∉ Σ.A implies o ∉ {orgl(d'') : d'' ∈ Σ.D} implies d' ∉ Σ.D — requires stating that DocId = IAddr (or providing an alternative freshness mechanism). Neither is done.

**Required**: Define DocId explicitly. Either (a) state DocId = IAddr with d identified by orgl(d), making freshness follow from o ∉ Σ.A, or (b) introduce DocId as an abstract type with an explicit freshness precondition d' ∉ Σ.D on CREATE VERSION and CREATE DOCUMENT.

---

### Issue 2: Orgl injectivity invariant missing

**ASN-0025, State Model**: "Each document d ∈ Σ.D has a distinguished I-address orgl(d) ∈ Σ.A."

**Problem**: No invariant states that distinct documents have distinct orgls. Without `(A d₁, d₂ ∈ Σ.D : d₁ ≠ d₂ ⟹ orgl(d₁) ≠ orgl(d₂))`, the orgl function could map two documents to the same I-address. If DocId = IAddr (the natural resolution of Issue 1), injectivity is automatic. If DocId is independent, injectivity is a separate invariant that must be stated and preserved by CREATE VERSION and CREATE DOCUMENT.

**Required**: State orgl injectivity as an invariant (or derive it from DocId = IAddr). Verify preservation by CREATE VERSION and CREATE DOCUMENT.

---

### Issue 3: Content at new addresses unspecified for three operations

**ASN-0025, CREATE VERSION / CREATE LINK / CREATE DOCUMENT**: Each allocates a fresh I-address (o, l, o respectively) and adds it to Σ'.A, but no postcondition specifies what Σ'.ι maps it to.

**Problem**: INSERT correctly states `(A i : 1 ≤ i ≤ n : Σ'.ι(bᵢ) = βᵢ)`. The other three I-space-extending operations do not. Since Σ'.A = dom(Σ'.ι), every address in Σ'.A must have a value. The state transitions are formally incomplete — Σ'.ι is not fully determined. The ASN notes "the permanence arguments require only that Value is a type with decidable equality," but the state model still requires Σ'.ι to be total on Σ'.A.

**Required**: For each I-space-extending operation, add a postcondition specifying Σ'.ι at the new address. Even "Σ'.ι(o) = v for the orgl structural entry v" suffices — the permanence argument does not depend on the specific value, but the state transition must be complete.

---

### Issue 4: COPY self-copy reasoning incomplete for P5

**ASN-0025, COPY**: "Combined with UF-V, the source I-addresses remain visible in d_s as well. Both documents see the same content through the same I-addresses."

**Problem**: The COPY preconditions permit d = d_s (self-copy). UF-V covers d' ≠ d, so when d = d_s, UF-V does not protect the source document's V-space. The conclusion is correct — shifted entries retain their original I-addresses, so source content remains visible — but the UF-V argument fails for this case. The phrase "both documents" is also wrong when there is one document.

**Required**: Add a case split. When d ≠ d_s, UF-V applies. When d = d_s, source visibility is preserved because the V-space effect shifts but does not remove existing entries: for each source position qᵢ ≥ p, the shifted entry Σ'.v(d)(qᵢ ⊕ [m]) = Σ.v(d)(qᵢ) = sᵢ, so sᵢ remains visible.

---

### Issue 5: REARRANGE claims "three properties" but lists four

**ASN-0025, REARRANGE**: "Three properties hold:" followed by P4, Domain preservation, Exterior frame, and Link-subspace frame.

**Problem**: Four properties are listed. The text later correctly says "satisfy all four."

**Required**: Change "Three properties hold" to "Four properties hold."

---

### Issue 6: J1/J2 preservation unverified in four operation sections

**ASN-0025, REARRANGE / CREATE VERSION / CREATE LINK / CREATE DOCUMENT**: Each section verifies J0 preservation but does not verify J1/J2. The State Model section gives one-line justifications, but these are claims, not derivations.

**Problem**: INSERT, DELETE, and COPY include explicit set-algebraic J1/J2 proofs showing how ordinal sets partition and recombine. The other four operations skip this step in their respective sections. CREATE LINK is the most notable gap: the State Model section says "CREATE LINK appends at next_link, extending the contiguous link range by one" — but the CREATE LINK section itself does not verify J2 (that appending at ordinal m+1 extends {1,...,m} to {1,...,m+1}) or confirm J1 (text ordinals unchanged).

**Required**: Add brief J1/J2 verification to each operation section. For REARRANGE: "dom(Σ'.v(d)) = dom(Σ.v(d)), so ordinal sets are identical; J1 and J2 hold." For CREATE VERSION: "Ordinal sets of d' are identical to those of d by the position-for-position copy; J1 and J2 hold." For CREATE LINK: "Text positions unchanged, so J1 holds. Pre-state link ordinals {1,...,m}; append at m+1 gives {1,...,m+1}; J2 holds." For CREATE DOCUMENT: "dom(Σ'.v(d)) = ∅; J1 and J2 hold vacuously."

---

## OUT_OF_SCOPE

### Topic 1: Link deletion and modification

The ASN defines CREATE LINK but no DELETE LINK or UPDATE LINK. DELETE's precondition restricts to text-subspace positions, so links cannot be removed from V-space. Whether links are truly permanent within a document — and whether endsets can be modified — is a legitimate design question for the link ASN.

**Why out of scope**: Link lifecycle semantics are new territory. The permanence ASN correctly models the operations it defines; link-specific operations belong in a future ASN.

### Topic 2: Historical backtrack and content recovery

The ASN notes content may become invisible in all documents (¬visible(a, Σ)) but persist in I-space by P0. Whether the system must provide a mechanism to make such content visible again is raised in Open Questions but not resolved.

**Why out of scope**: Content recovery is a system capability question beyond the permanence invariant, which concerns existence (P0) and immutability (P1), not accessibility.

### Topic 3: Storage reclamation under P0

P0 forbids shrinking I-space. Whether a conforming implementation may garbage-collect I-space content that is invisible in all documents and unreachable by any link is an operational question the ASN correctly identifies but does not resolve.

**Why out of scope**: Storage reclamation is an implementation-level concern about what "conforming" means in practice. The abstract model's P0 is clear; implementation latitude is a separate question.

VERDICT: REVISE
