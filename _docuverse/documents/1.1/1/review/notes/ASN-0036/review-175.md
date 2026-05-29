# Review of ASN-0036

## REVISE

### Issue 1: Forward-reference justification prose in S5
**ASN-0036, S5 proof, "Genuine strand state" paragraph**: "Several of these (S7a, S7d, S8-depth, D-CTG, D-MIN) are introduced after S5 in document order; we forward-reference them here so the witness is verified against the model's complete always-on invariant set rather than a chosen subset. Each construction verifies all of them together with the multiplicity count, so the witnessing states are genuine strand states, not bare models of S0–S3."
**Problem**: This is reviser drift flagged by the anti-bloat classifier. The paragraph explains *why* forward references are made and justifies document ordering, rather than advancing the proof. The verification itself is legitimate; the meta-commentary about ordering and "complete always-on invariant set rather than a chosen subset" is noise the reader must skip past to reach the constructions.
**Required**: Delete the ordering-justification sentences. Define "genuine strand state" as the conjunction of the state-level invariants and proceed directly to the constructions. The list of which invariants are state-level vs. transition-level is the only load-bearing content; keep that, drop the apologetics.

### Issue 2: Duplicate full-invariant verification across the two S5 constructions
**ASN-0036, S5 proof, "Cross-document construction" and "Within-document construction"**: both blocks re-verify S2, S3, S7b, S7a, S7d, the domain-restriction axiom, S8-depth, D-MIN, D-CTG, and S8-fin in near-identical language ("S7b: a = [1,0,1,0,1,0,1,1] has zeros(a) = 3..."; "S7a: origin(a) = 1.0.1.0.1, and we stipulate a allocated under that document...").
**Problem**: Two paragraphs in the same document say the same thing in different words. The address `a` and its S7a/S7b/domain-restriction verification are character-for-character the same content; only the document/V-position multiplicity differs.
**Required**: Verify the shared content-store and address-validity facts once, then state only the differences for each construction (cross-document: same `v` across `N+1` distinct documents; within-document: `N+1` distinct `vₖ` in one document). This removes ~half the verification prose without weakening the proof.

### Issue 3: ValidInsertionPosition postcondition (d) form versus subspace claim
**ASN-0036, ValidInsertionPosition derivation**: "Every component is then `≥ 1` ... so `zeros(v) = 0` with componentwise positivity (b), and the preserved leading component fixes `v₁ = 1` as the text subspace identifier."
**Problem**: The derivation asserts `v₁ = 1` because the leading component is preserved under `shift`, but the explicit form (d) is written `v = [1, 1, ..., 1 + j]`, which only displays the depth-2 shape clearly. For `m ≥ 3` the "1 + j" sits at position `m` while positions `2..m−1` are also `1` — the bracket notation `[1, 1, ..., 1 + j]` is ambiguous about how many interior `1`s precede `1+j` and whether `1+j` is the last or an interior component. At `m = 2` it reads `[1, 1+j]`; at `m = 3` it should read `[1, 1, 1+j]`.
**Required**: State the form as `v = [1, 1, ..., 1, 1+j]` of depth `m` with the last component `1+j` and all `m−1` preceding components equal to `1`, matching the D-SEQ notation used elsewhere, so the depth-`m` reading is unambiguous.

## OUT_OF_SCOPE

### Topic 1: Mid-arrangement deletion and V-position renumbering
The worked example only deletes the trailing positions of `d₁` (1.3–1.5), so D-CTG is preserved without shifting. Nelson's "addresses are decreased by the length of the deleted text" requires renumbering after a mid-document deletion to preserve D-CTG/D-SEQ.
**Why out of scope**: This is operation-specific effect (DELETE frame conditions), explicitly deferred to the operations layer and noted in the Open Questions.

### Topic 2: Canonical choice of V-position depth `m`
ValidFirstInsertionPosition leaves `m ≥ 2` as a free parameter for the empty subspace.
**Why out of scope**: The note correctly identifies this as an allocation convention chosen by the first-placing operation, an operations-layer concern, and flags it in Open Questions.

VERDICT: REVISE
