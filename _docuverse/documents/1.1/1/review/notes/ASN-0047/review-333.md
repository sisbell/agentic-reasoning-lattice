# Review of ASN-0047

I checked the operation definitions (K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ), the J4 fork composite, the coupling constraints, the D-SEQ★ derivation (both m=2 and m≥3 cases), the K.μ~ necessity/sufficiency proof, and the Class (a)/(b) verification structure against their boundaries.

The correctness work holds up. I traced the K.δ k∈{0,1,2} dispatch including the forest/baptism boundary (inc never produces a node-level address because k=1/k=0 require document/non-node operands), the K.μ~ link-fixity discharge through LRP + CL-UNIQ, the fork's multiplicity-preservation against a duplicate-I-address source, and the suffix-only K.μ⁻ shape equivalence — all sound. I found no missing boundary case, no unjustified "by similar reasoning," and no checkmark-as-proof. The cross-ASN references are all to foundation ASNs (0034/0036/0043/0045/0093); no Standard-7 violation.

The remaining issues are the forward-reference accretion the note directs me to surface.

## REVISE

### Issue 1: Redundant restatement of "the full-clearance form realises every admissible π"
**ASN-0047, *Decomposition of K.μ~***: The same claim is asserted in four distinct slots: the "Full-clearance form (canonical statement)" paragraph ("This form realises *every* admissible π without per-π precondition checks"); Step (A)'s closing line ("the full-clearance decomposition realises every admissible π"); Step (B)'s preamble ("the K.μ⁻ + K.μ⁺ (full-clearance) decomposition actually realises π"); and the trailing "Decomposition" subsection ("The verification arguments realise every admissible π by the full-clearance form stated canonically above").
**Problem**: This is the same proposition reworded across four paragraphs. A reader following the K.μ~ argument re-encounters the claim without new content each time, and must check whether each instance carries a different qualifier (it does not). Matches the flagged pattern "two paragraphs in the same document say the same thing in different words."
**Required**: State the realisation claim once (in the canonical-statement paragraph), and let Steps (A)/(B) and the Decomposition subsection reference it rather than re-assert it.

### Issue 2: Cross-section deferral cluster to *Decomposition of K.μ~*
**ASN-0047, Class (a) verification matrix and surrounding prose**: At least four separated locations defer the K.μ~ facts to the same downstream section: the matrix preamble ("its composite-boundary specifics (LRP, K.μ~-S3★, K.μ~-FIX) are composite-boundary facts, discharged in the *Decomposition of K.μ~* section"); the same paragraph's earlier sentence routing the K.μ~ column elsewhere; the CL-UNIQ entry ("K.μ~ preservation: by LRP (post-state CL-UNIQ, *Decomposition of K.μ~*)"); and the S3★ matrix cell plus its prose ("K.μ~ inherits via the K.μ⁻ + K.μ⁺ decomposition").
**Problem**: Matches the flagged pattern "multiple paragraphs in different sections defer to the same downstream location." The repeated pointers add navigational weight without advancing any argument; each one restates that K.μ~ is handled there.
**Required**: Consolidate to a single statement (e.g., in the matrix preamble) that the K.μ~ named composite carries no matrix column and that all its composite-boundary facts live in *Decomposition of K.μ~*; drop the per-cell repetitions.

## OUT_OF_SCOPE

None beyond what the ASN already enumerates in its Open Questions (interior DELETEVSPAN/renumbering, transclusion-chain provenance, concurrent same-document allocation). These are correctly deferred.

VERDICT: REVISE
