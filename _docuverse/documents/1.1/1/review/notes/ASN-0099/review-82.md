# Review of ASN-0099

## REVISE

### Issue 1: "The Empty Query" forward-references claims defined in later sections
**ASN-0099, The Empty Query**: "When `dom(Σ.L) = ∅` ... F2, F3, F10, F11, F19 all hold vacuously." and "For `findlinks_scoped(I, ∅, Σ) = findlinks(I, Σ) ∩ ∅ = ∅ by F14."
**Problem**: This section appears before Scope (F14, F15), Result Ordering (F10), and Persistent Discoverability (F11, F19). The reader meets F10, F11, F14, and F19 here as already-established facts, but their definitions and statements come several sections later. This is the accretion pattern flagged for this review mode — a section reaching forward across the document to claims not yet in scope.
**Required**: Either relocate the empty-query discussion after the claims it depends on, or restrict it to claims already introduced (findlinks, findlinks_filtered, findlinks_scoped definitions) and let the vacuous-satisfaction remarks attach to F10/F11/F19 at their own sites.

### Issue 2: The match existential is written twice
**ASN-0099, A Two-Phase Factoring / The Match Predicate**: Phase 2 defines `findlinks(I, Σ) = {a ∈ dom(Σ.L) : (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)}`, and F1 then defines `matches(a, I, Σ) ≡ (E i : 1 ≤ i ≤ |Σ.L(a)| : coverage(Σ.L(a).eᵢ) ∩ I ≠ ∅)` — the identical predicate.
**Problem**: The same slot-existential is stated verbatim in two places, with F1 naming a predicate that `findlinks` had already inlined. Two statements of one predicate is the duplication pattern flagged for this mode, and it forces the reader to verify the two are character-for-character the same.
**Required**: Introduce `matches` first (or at the `findlinks` definition site) and write `findlinks(I, Σ) = {a ∈ dom(Σ.L) : matches(a, I, Σ)}`, so the predicate is defined once.

### Issue 3: Claim labels are non-contiguous and out of document order
**ASN-0099, Claims Introduced** and body: labels jump F6 → F8 → … → F15 → F19 → F20; F7, F16, F17, F18 are neither defined nor referenced anywhere, and F5 (Identity, Not Value) is introduced after F6 (Transclusion Transparency) in document order.
**Problem**: The gaps and the F6-before-F5 ordering are residue of claims removed/reordered across revisions. A precise reader cannot tell whether F7/F16/F17/F18 are missing dependencies or deleted claims, and the non-monotonic numbering impedes navigation.
**Required**: Confirm no dangling references to F7/F16/F17/F18 (none found), then renumber to a contiguous, document-order sequence — or add a one-line note that the gaps are deliberately retired labels.

## OUT_OF_SCOPE

### Topic 1: Combined filtered-and-scoped operation, auditability witness, K.λ-to-query latency bound
**Why out of scope**: These are correctly listed under "What We Have Not Specified" and "Open Questions." `findlinks_filtered_scoped`, the index-agreement witness, and any timing bound between K.λ commitment and query visibility each belong to a future ASN (or an implementation/replication ASN), not to a revision of this one.

META: not applicable — the ASN defines abstract state-image and link-discovery operations with completeness/determinism/monotonicity/transclusion guarantees stated independently of any implementation, which is squarely in-spec.

VERDICT: REVISE
