# Review of ASN-0087

## REVISE

### Issue 1: Forward references and duplicated object-level exposition in "The Problem"

**ASN-0087, The Problem**: "But *actual* discoverability from a given document is conditional: by the body's M-WP and LP17, the link is discoverable from a document only when some endset's coverage meets that document's arrangement range. If every endset coverage misses every arrangement range ... the link is *born orphaned*..."

**Problem**: The framing section cites body claims that do not yet exist (M-WP) and a foundation lemma about a result the body derives later (LP17/LP18), then develops the full "born orphaned" mechanism. That mechanism is object-level content already carried by the *Permanence* section, the LP17/LP18 discussion, and M-Reflexive — three downstream locations. A reader must hold an unestablished forward claim to follow the framing, and then re-reads the same content twice more. This is forward-reference accretion plus duplication.

**Required**: Reduce The Problem to the question being posed (what is allocated, recorded, made discoverable, untouched). Move the orphan-birth mechanism to its single home in *Permanence*/LP17 and drop the M-WP/LP17/LP18 forward citations from the framing.

### Issue 2: M-DiscSymmetry reconciliation prose pre-announces and defers to wp Case 2

**ASN-0087, What Is Indexed?**: "The symmetry is qualified in one respect: the home document additionally gains a *reflexive route* (M-Reflexive) by which a link covering ℓ is discoverable from its home regardless of prior arrangement. The content-reach route remains symmetric across all documents."

**Problem**: The home/reflexive qualification is stated here, again as the *Inputs* reflexive-authoring note, again in the worked example's reflexive variant, and is actually *derived* only in wp Case 2 (M-Reflexive). Four sections defer to the same downstream derivation, and the "qualified in one respect" reconciliation paragraph announces a result before its premises are available. Same content, several wordings.

**Required**: State the symmetry once, derive the reflexive-route exception once (in wp Case 2), and replace the other occurrences with a single pointer or remove them. Do not pre-announce the qualification in "What Is Indexed?".

### Issue 3: L1c discharged via a lemma that presupposes the invariant rather than the precondition that establishes it

**ASN-0087, Invariant Preservation (Per-State)**: "L1c (structural inc-chain conformance) requires an inc-chain from `origin(ℓ) = d` to `ℓ`. By ChainMembershipForOrigin and ChainDiscipline (ASN-0093), `ℓ` lies on `d`'s link sub-allocator chain..."

**Problem**: ChainMembershipForOrigin asserts that *every* entry of `dom(L)` inhabits its origin chain — i.e. it presupposes the structural conformance being discharged for the fresh `ℓ`. The direct ground for `ℓ`'s chain membership is K.λ's own precondition ("ℓ is produced by `A_L(d)`"), from which ChainDiscipline and ChainElementT4Validity then supply the chain shape and T4-validity. Citing ChainMembershipForOrigin routes the proof through the conclusion.

**Required**: Discharge L1c from K.λ's "produced by `A_L(d)`" precondition plus ChainDiscipline/ChainElementT4Validity; drop the ChainMembershipForOrigin citation.

### Issue 4: Defensive notation-disambiguation stated twice

**ASN-0087, Decomposition / M-Comp**: "The semicolon denotes sequential composition of atomic transitions, distinct from the tumbler addition operator `⊕` of ASN-0034."

**Problem**: The clarification that `;` is not `⊕` is defensive against a confusion the symbols do not invite, and it appears verbatim in both the Decomposition prose and the M-Comp claim row. Restating it in the claims table as well as the body is redundant.

**Required**: Keep the composite definition; remove the "distinct from ⊕" disambiguation, or state it at most once.

## OUT_OF_SCOPE

### Topic 1: Well-formedness of endsets reaching not-yet-allocated addresses
**Why out of scope**: The ASN correctly defers this to its Open Questions; L4 (EndsetGenerality) already permits forward-reaching spans, and tightening that discipline is a future ASN, not a defect here.

### Topic 2: Protocol-layer visibility bound on the intermediate state `Σ_mid`
**Why out of scope**: Composite-level atomicity is explicitly a protocol-layer guarantee above the substrate; specifying it belongs to a later transport/protocol ASN.

VERDICT: REVISE
