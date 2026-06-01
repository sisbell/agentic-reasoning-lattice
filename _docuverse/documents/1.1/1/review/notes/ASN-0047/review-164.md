# Review of ASN-0047

## REVISE

### Issue 1: S7d preservation argument omits the k=0 and k=1 document-creation routes
**ASN-0047, *Extended reachable-state invariants*, S7d prose**: "*S7d (Document allocation discipline).* Every `d ∈ E_doc` is T4-valid with `zeros(d) = 2`, placed in E_doc by a K.δ case (ii) k = 2 event satisfying T10a's per-`(t, k')` discipline (e ∉ E discharged by T10a GlobalUniqueness on the parent account's document sub-allocator); preserved by P1."

**Problem**: Documents enter `E_doc` by *three* K.δ routes, not one. The ASN's own worked examples exercise the other two: the fork example creates `d₂` via **k = 1** (version), and the entity-hierarchy example Step 4 creates a sibling document via **k = 0**. The S7d preservation prose attributes all `E_doc` membership to a "k = 2 event," so it does not discharge `zeros(d) = 2` and freshness for the k = 0 and k = 1 cases. (The property does hold — K.δ-ID.zeros-0/1 preserves `zeros = 2` for k ∈ {0,1} off a document operand — but that argument is absent from the S7d discharge.) This also contradicts the more general statement two paragraphs earlier ("placed in E_doc by a K.δ event ... on the parent allocator's tracked domain") and the matrix row ("via T10a per-`(t,k')` discipline"), leaving the prose the only place that pins k = 2 — incorrectly.

**Required**: State the S7d preservation over all three routes: k = 2 (descent off an account, `zeros = 1 → 2`), k = 1 (version off a document, `zeros = 2` preserved), and k = 0 (sibling off a document, `zeros = 2` preserved), each discharging `zeros(d) = 2` via the relevant K.δ-ID.zeros identity and freshness via the corresponding discharge (GlobalUniqueness at k ∈ {1,2}, FrontierEquivalence at k = 0).

### Issue 2: P7a "Derivation" slot contains only a forward pointer; the proof lives in two places
**ASN-0047, *Cross-layer invariants*, P7a**: "*Derivation.* P7a is a composite-boundary property (Class (b)); its discharge is given in the *Extended reachable-state invariants* section under the P7a Class (b) argument — ... We do not restate it here. ∎"

**Problem**: A `*Derivation.* ... ∎` block that ends in "We do not restate it here" is a structural slot occupied by navigation, not reasoning. The actual P7a argument is given in full under ExtendedReachableStateInvariants Class (b), so the Cross-layer entry duplicates the statement and defers the proof — the reader must hold two locations for one property. This is the forward-reference-accretion pattern flagged for this note (two sections deferring to the same downstream proof).

**Required**: Either give P7a its derivation once at its definition site, or state it at the definition and prove it only under Class (b) without a `*Derivation. ... ∎*` shell that asserts a proof it does not contain.

### Issue 3: K.δ "Freshness discharge" paragraph is document-structure deferral, not argument
**ASN-0047, K.δ definition, *Freshness discharge***: "... case (ii) is closed by the parent-allocator route detailed in §*K.δ case (ii) discharge and parent-allocator activation* below. That section performs the case (ii) discharge once; it is not repeated here."

**Problem**: This paragraph advances no reasoning — it tells the reader which later section performs a discharge and announces that the discharge is "not repeated here." The case-(i) half is already a one-line citation; the case-(ii) half is a pure pointer. A reader following the `e ∉ E` precondition must skip past this to reach the actual content. Meta-prose in a discharge slot.

**Required**: Reduce to a single cross-reference inline at the precondition ("case (ii): `e ∉ E` discharged in §K.δ case (ii) discharge"), and delete the self-describing "performs the discharge once; not repeated here" sentence.

### Issue 4: "No amendment" subsections exist only to assert that nothing changed
**ASN-0047, *Amendments to existing transitions***: "**K.α (no local amendment in extended state).** ASN-0093's K.α already encodes ... so no local amendment is required ..." followed by a restated frame; likewise "**K.ρ (no precondition amendment in extended state).** K.ρ's precondition ... and effect ... are unchanged ..." followed by a restated frame.

**Problem**: Two subsections in a section titled "Amendments" exist to state that there are no amendments, then re-print frames already given at the elementary definitions. This is essay content in a structural slot — the section's purpose is to record amendments, and a "we changed nothing" entry plus a frame restatement is noise the reader works around.

**Required**: Drop the no-op subsections; if the extended-state frames for K.α/K.ρ need to appear once, place them at the elementary definitions and let the Amendments section list only transitions that are actually amended (K.μ⁺, K.μ⁻, L14a).

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: The fork composite (J4) deliberately leaves the forked document's link subspace empty, and a mechanism for propagating source links into a fork would require K.μ⁺_L steps the fork does not include. The ASN already records this as an Open Question; it is new operational territory, not a defect in the present transition taxonomy.

VERDICT: REVISE
