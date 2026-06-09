# Review of ASN-0119

## REVISE

### Issue 1: Reachable-state invariant discharge is incomplete

**ASN-0119, "What is preserved: I-address correspondence"**: "we discharge them explicitly so that the hardest-to-maintain conjuncts of a rearrangement are not left implicit. *Functionality* is preserved... *Referential integrity* is preserved..."

**Problem**: The ASN explicitly discharges only S2 and S3. But the post-state must satisfy the full reachable-state invariant package for the text subspace it operates on — D-CTG★, D-SEQ★, D-MIN★, S8a, S8-depth, S8-fin (ASN-0047 / ASN-0036). The review's own standard is "Every invariant conjunct addressed." The contiguity/tiling invariants (D-CTG, D-SEQ) are precisely the ones the rubric flags as "hardest to maintain, most often hand-waved," and they are the invariants a *future* operation will rely on to name cuts (the ASN even states cut-naming depends on D-CTG/D-SEQ). They are not mentioned among the preserved claims.

These are in fact trivially preserved — because P2 gives `dom(M'(d)) = dom(M(d))` and π permutes the affected text interval onto itself with the exterior frozen, the active set `V_{s_C}(d)` is *literally unchanged*, so every domain-only invariant (contiguity, sequentiality, minimum, well-formedness, finiteness) is inherited. But that one-line argument is exactly what is missing.

**Required**: Add an explicit discharge (even a single paragraph) noting that D-CTG★/D-SEQ★/D-MIN★/S8a/S8-depth/S8-fin are preserved because `V_{s_C}(d)` is set-invariant under P2. Without it, the claim to leave "no hard conjunct implicit" is not met — the easy-but-load-bearing tiling invariants are skipped.

### Issue 2: Footprint discontiguity is asserted ("generally"), never characterized; the one non-trivial wp goes uncomputed

**ASN-0119, "Links"**: "The two halves therefore generally land at non-adjacent V-positions, and the endset, when resolved against the new arrangement, becomes a *discontiguous span-set*." Table P7a: "footprints split by a cut become discontiguous span-sets."

**Problem**: The formal content of P7a (`project(a, i, d, Σ') = π(project(a, i, d, Σ))`) is proven, but the discontiguity *consequence* — the thing the consultation actually asks about (Question 5, Question 16) — is hedged with "generally" and never made precise. This is the one place in the ASN where a non-trivial weakest-precondition analysis exists, and it is absent. Every other postcondition (isolation, content permanence, discoverability) has `wp = true` and is trivially framed; the rubric explicitly rejects an ASN whose only wp's are trivially true and demands a non-trivial case be found.

The precise condition is derivable and not hard: within each region π is a *uniform ordinal shift* (in β of a pivot, every `v = c₁+j ↦ c₀+j`, displacement `−w_α` constant; in α, displacement `+w_β` constant; exterior, displacement 0). Hence a footprint that lies entirely within a single region (exterior, α, μ, or β) maps to a *contiguous* footprint, while a footprint straddling a cut maps to pieces carrying different shifts, which generally land non-adjacently. The "generally" is exactly the missing wp: `wp(REARRANGE_K, "footprint of (a,i) contiguous") ≡ project(a,i,d,Σ) ⊆ one region`.

**Required**: Replace the hedged "generally land at non-adjacent V-positions" with the derived characterization — a footprint preserves contiguity iff it is confined to a single region; straddling a cut fragments it — and present this as the non-trivial weakest-precondition result. This both discharges the rigor standard for wp depth and turns Question 5's qualitative answer into a proven one.

## OUT_OF_SCOPE

The six Open Questions (shared cut positions across transcluding documents, unserialized concurrent rearrangement, content-index/footprint-fragmentation invariants, prior-arrangement recoverability, subspace-boundary preservation under middle displacement, document-end well-formedness) are correctly deferred to future ASNs and are not defects here.

VERDICT: REVISE
