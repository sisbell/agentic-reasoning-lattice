# Review of ASN-0047

This is a thorough, heavily-revised specification. The mathematical core (the mutability hierarchy P0–P3, the two-class per-state/composite-boundary partition, the K.μ~ link-subspace fixity argument, the D-SEQ★ derivation) holds up under checking. I did not find a correctness defect in the proofs. The findings below concern meta-prose accretion — the pattern the `review-mode.anti-bloat` classifier on this note asks me to surface — plus one symmetry gap.

## REVISE

### Issue 1: Non-circularity justification embedded in the K.μ~ sufficiency construction
**ASN-0047, *Necessity and sufficiency of the precondition*, sufficiency clause (i)**: "(This is the construction-level fact from which K.μ~-FIX is later derived; we cite the construction here precisely to avoid presupposing the post-state invariants that admissibility must establish.)"
**Problem**: This is the flagged "prose justifies document ordering / non-circularity by Y argument" pattern. The reader following the `π_swap` admissibility check does not need to be told *why* domain fixity is proved from the construction rather than from K.μ~-FIX; the substantive content is simply "domain fixity holds by construction." The non-circularity rationale is reviser bookkeeping, not part of the argument.
**Required**: Delete the parenthetical. The sentence "Domain fixity holds by construction: `π_swap` is a permutation of `dom(M(d))` ... so the bijection equation gives `dom(M'(d)) = dom(M(d))` directly" already carries the full claim.

### Issue 2: Full axiom restatements duplicated between body and inventory table
**ASN-0047, *The state model* / *Link store and extended system state* vs. *Inherited from foundation* table**: `SequentialTransitionAxiom` and `SubspaceConventionAxiom` are each stated in full in the body ("The transition relation `Σ → Σ'` is single-event sequential... no intermediate state in which a transition has begun but not yet committed") and then restated verbatim-equivalently in the inherited-properties table row.
**Problem**: Two paragraphs in the same document say the same thing in different words. Both are inherited foundation axioms; one full statement plus a one-line pointer to ASN-0093 suffices. The table row currently re-expands the entire axiom text rather than indexing it.
**Required**: Keep the body statement; reduce the table rows to a one-line description + foundation source (as the other inherited rows like L0, L3 already do), or vice versa. Do not state the full axiom text twice.

### Issue 3: Multiple sites defer to the same downstream discharge section
**ASN-0047, K.δ definition (k=0, k=1, k=2 cases), S7d verification-matrix cell, TrackedEmission box, *Entity distinctness* corollary**: each defers to "§*K.δ case (ii) discharge and parent-allocator activation*" for the allocator-activation argument.
**Problem**: This is the flagged "multiple paragraphs in different sections defer to the same downstream location" pattern. The K.δ case-(ii) definition body already says the discharge is "per sub-case in §...," then the case-level "where"-clause repeats it, then the matrix cell, TrackedEmission, and Entity-distinctness each re-point. A reader cannot evaluate K.δ at its definition site and must chase the same forward pointer four times.
**Required**: Consolidate the forward references — state once at the K.δ definition that all activation discharge lives in §*K.δ case (ii) discharge*, and let the matrix/TrackedEmission/Entity-distinctness cells cite the K.δ definition rather than each independently re-pointing downstream.

### Issue 4: Content-subspace depth re-pinning is treated asymmetrically with the link subspace
**ASN-0047, K.μ⁺ precondition vs. *Link-subspace V-position depth (operational)***: the link subspace gets an explicit operational depth `m_L(d)` paragraph noting that after full clearance the next K.μ⁺_L "re-pins `m_L(d)` from scratch — at any value `≥ 2`... not necessarily the prior depth." The content subspace has no symmetric `m_C(d)` treatment; K.μ⁺ mentions `ValidFirstInsertionPosition(d, v, m)` only for the `V_{s_C}(d) = ∅` case.
**Problem**: K.μ⁻ admits full content-subspace clearance (`n'_{s_C} = 0`), after which S8-depth is again vacuous and a subsequent K.μ⁺ re-pins the content depth — exactly the link-side scenario. The content side relies on `ValidFirstInsertionPosition` without stating that the re-pinned depth need not equal the prior depth, leaving the symmetry implicit where the link side makes it explicit. A reader cannot tell whether content depth is a permanent per-document constant or a per-stretch value.
**Required**: Add the one-sentence content-side counterpart (content depth tracks the live arrangement, re-pinned at any `m ≥ 2` after full clearance), or state once that both subspace depths are governed by the same live-arrangement rule and `m_L(d)`'s discussion applies mutatis mutandis to content.

## OUT_OF_SCOPE

### Topic 1: Concurrent allocation under a shared home document
The open questions raise serialization/coordination for concurrent K.λ and link-address exhaustion. These are correctly deferred — SequentialTransitionAxiom assumes total ordering, and a concurrency model is a separate ASN.
**Why out of scope**: New territory (concurrency semantics), not an error in this sequential model.

### Topic 2: Link inheritance under forking and a link-withdrawal/tombstone mechanism
J4 explicitly leaves source-link inheritance to a future ASN, and the D-CTG★/tombstone reconciliation is flagged as an open question.
**Why out of scope**: Both require new operations/state outside this transition taxonomy; the ASN correctly identifies them as future work rather than gaps here.

VERDICT: REVISE
