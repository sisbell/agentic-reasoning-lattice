# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ S3★ verification mislabels a precondition-carried invariant as "discharged by the decomposition"

**ASN-0047, *Decomposition of K.μ~* (Step A / Step B) and Class (a) matrix, S3★/K.μ~ cell**: The cell reads "S3★(Σ') discharged by the K.μ⁻+K.μ⁺ decomposition: survivors via B.1, new content positions via B.2."

**Problem**: Step (A) explicitly takes S3★(Σ') as a *hypothesis*: "Admissibility clause (i) hands us both S3★(Σ') and S3★-aux(Σ') as hypotheses on the candidate π. From these we derive subspace preservation." Step (B.2) then derives the new-content-position targeting "By Step (A)'s subspace preservation." So the decomposition's S3★ argument consumes Step A, which consumes the *assumed* S3★(Σ'). The bijection equation makes admissibility's "induced post-state M'(d)" identical to the decomposition's post-state, so S3★(Σ') is assumed to show S3★(Σ') is realizable — it is not independently derived. The matrix verb "discharged by the decomposition" overstates this to an independent proof. (The text itself hedges with "consistent with the filter-stipulated S3★(Σ')" in B.3, contradicting the matrix wording.)

**Required**: Relabel the matrix cell to state that S3★(Σ') holds **by admissibility (i)** (precondition-carried), with Steps A/B establishing only *realizability + non-vacuity* (the latter via the π_swap witness, whose S3★ is verified independently from its swap-within-dom_C structure). Either that, or supply an S3★(Σ')-independent derivation of subspace preservation in Step A.

### Issue 2: Document-level cross-document disjointness is re-proved from scratch despite being a foundation lemma, then double-discharged

**ASN-0047, *Lemma (Cross-document disjointness chain)* and *SubAllocatorBundle.Disjointness***: The body gives a full Case A / Case B proof (`T10a.{2,5} → T10`), then SubAllocatorBundle.Disjointness's cross-document clause is discharged by "CrossDocumentDisjointness (ASN-0093), equivalently the Cross-document disjointness chain lemma (below)."

**Problem**: ASN-0093 (a foundation) already supplies CrossDocumentDisjointness for the document-level anchor pairs. The body re-proves the same document-level fact in full, and then cites *both* the foundation lemma and the in-body re-proof for the identical SubAllocatorBundle clause — the "multiple paragraphs defer to the same fact" anti-pattern. The proof's own remark "the values of s₁, s₂ are immaterial" confirms the document-level same-subspace case is exactly the foundation's, not new.

**Required**: Cite ASN-0093's CrossDocumentDisjointness for the document-level case and present only the genuinely new deltas (account-level entities; cross-subspace `s₁ ≠ s₂` pairing) as a thin extension noting s-independence. Remove the double-discharge in SubAllocatorBundle.Disjointness.

### Issue 3: Forward-reference accretion / meta-prose (anti-bloat classifier)

**ASN-0047, multiple sites**: Prose that justifies placement or inventories downstream consumers rather than advancing the claim. Concrete instances:

- Opening: "That arrangement mutation never reaches the stored content — the separation this ASN generalises to the full extended state in *Destruction confinement* — is the property we extend here." (forward ref + essay framing before any definition).
- NodeBaptism box: "(For its role as the k'=2 spawnPt-premise source, see the K.δ case (ii) k = 2 dispatch table.)" — use-site inventory inside a definition.
- K.δ: "The routes by which a K.δ event reaches `E_doc` are enumerated under S7d below." — pure forward pointer duplicating S7d's content.
- S8★: paragraphs explaining why ASN-0036's S8 "cannot be applied to M(d) directly" / why S3 "fails on the unprojected M(d)" — rationale-for-the-property rather than the property.
- L1c parenthetical "(per-step inc-rule conformance, not full T10a discipline; see L1c discharge)" repeated across GlobalLineage (iii) and the inherited-foundation table.

**Problem**: A reader must skip past these to reach the load-bearing step; several restate the same deferral.

**Required**: Delete the forward pointers whose targets already carry the content; move any genuine object content (e.g. the S3-fails-on-unprojected-M(d) fact) into the single definitional slot that needs it.

### Issue 4: NodeLineage dropped from the end-of-document ExtendedReachableStateInvariants enumeration

**ASN-0047, *Local extensions and strengthenings* table, ExtendedReachableStateInvariants row**: The summary lists the per-state invariants as "...∧ P6–P8 ∧ L0 ∧ L1 ∧ L1a ∧ L1b ∧ L1c ∧ L3 ∧ L14 ∧ ...", omitting NodeLineage.

**Problem**: The authoritative statement (top of *Extended reachable-state invariants*) and the Class (a) verification list both include NodeLineage as a per-state invariant ("...∧ P8 ∧ NodeLineage ∧ L0..."), and it has a dedicated preservation paragraph. The summary-table enumeration silently drops it. Distant restatements of the invariant set should agree token-for-token.

**Required**: Restore NodeLineage to the summary-table enumeration (or replace the enumeration with a single cross-reference to the authoritative box).

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: The ASN correctly defers a mechanism for propagating a source's links into a forked document ("A mechanism for link inheritance under forking, if desired, would require K.μ⁺_L steps in the fork composite and is outside this ASN's scope"). This is new operation design, not a defect in the present transition model.

### Topic 2: Interior link withdrawal / tombstoning
**Why out of scope**: D-CTG★/D-MIN★ admit only suffix truncation of the link subspace, so withdrawing an interior link is impossible under K.μ⁻. The ASN flags this as an open question requiring a separate withdrawal mechanism. That mechanism belongs in a future ASN.

VERDICT: REVISE
