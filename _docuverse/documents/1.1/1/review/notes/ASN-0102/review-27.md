# Review of ASN-0102

## REVISE

### Issue 1: Redundant summary restating the New/Old case split in X14

**ASN-0102, X14, J1'★ bullet**: After the `(a) a ∈ New` / `(b) a ∈ Old` sub-cases are fully argued, the bullet closes with: "The recorded pairs split cleanly into two kinds: `New` addresses, which both extend the range and enter `R` fresh; and `Old` addresses, which under self-transclusion (`d_s = d`) or re-copy were already present in `d`'s range — for these J1'★ holds not by range growth but by their pre-state presence in `R` (P4★), so they add no pair to `R' ∖ R`."

**Problem**: This sentence is a verbatim recapitulation of the two preceding sub-cases (a) and (b). It adds no new premise or step — it restates the partition already established immediately above. Combined with the "Setup for the J1★/J1'★ discharges — `New` vs. `Old`" paragraph that *introduces* the same split, the New/Old distinction is now stated three times in one discharge: setup, per-case, summary. In an already-dense X14, the reader must skip past the closing restatement to confirm it carries nothing the bullets did not. This is the "two paragraphs say the same thing" anti-bloat pattern.

**Required**: Delete the closing summary sentence; the (a)/(b) sub-cases and the setup paragraph already discharge J1'★ completely. If a one-line closure is wanted, replace it with the bare conclusion ("hence no pair in `R' ∖ R` lacks a backing range extension, so J1'★ holds") without re-narrating the case split.

## OUT_OF_SCOPE

(none — the four Open Questions are correctly posed as future work, not gaps in this ASN.)

Notes on what was checked and found sound: the `wp(COPY, S3★)` reduction to the copied region; X16's three-class tiling of `[1, n_S + W]` (no gap, no overlap, S8a for copied/displaced/unmoved positions, S2 discharge); X8's two-step within-reference non-coalescence (V-contiguity then maximality) and the `≤ k` canonical bound; X12's independent leading/trailing absorption conditions; X14's J0 vacuity and the P4★/Old-branch discharge of J1'★; the standalone-composite ⇒ boundary ⇒ P4★ chain; and the four worked examples (interior cross-origin, self-transclusion `Old ≠ ∅`, empty-subspace first insertion, append boundary), which between them exercise `p = 1`, `1 < p ≤ n_S`, and `p = n_S + 1`. No correctness defect found.

VERDICT: REVISE
