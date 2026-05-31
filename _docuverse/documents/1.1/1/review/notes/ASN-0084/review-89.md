# Review of ASN-0084

## REVISE

### Issue 1: R-BLK re-derives the non-S "carried verbatim" fact four times

**ASN-0084, R-BLK (Phase 1 "Non-S runs are carried verbatim", Phase 3 bullet, "I-start, width, and contiguity", "S8-cons … Non-S runs")**: The single fact — *π is the identity on non-S positions, so a non-S run passes through with its triple intact and inherits S8-cons under M'(d)* — is stated and re-derived in at least four places:
- Phase 1: "Since π is the identity on V(b) … Phase 3 carries b through unchanged as (v_b, a_b, n_b), which inherits S8-cons under M'(d): … M'(d)(v_b + k) = M(d)(v_b + k) = a_b + k."
- Phase 3 bullet: "Non-S runs: π(vₖ) = vₖ … the triple carries through unchanged."
- contiguity para: "For non-S runs π is the identity … and the run passes through unchanged."
- S8-cons para: "Non-S runs: shown above — π is the identity, so M'(d)(vⱼ + k) = M(d)(vⱼ + k) = aⱼ + k."

**Problem**: The S8-cons computation for non-S runs is performed verbatim in both Phase 1 and the S8-cons paragraph; the "carries through unchanged" claim recurs three more times. A reader following the S8-cons obligation must skip past the earlier identical derivation. This is the "two paragraphs say the same thing" accretion the anti-bloat classifier targets.

**Required**: Derive the non-S carry once (S8-cons inclusive) and have the later paragraphs cite it by name rather than re-derive.

### Issue 2: R-NS Remark is forward-pointing accretion

**ASN-0084, R-NS Remark**: "The cut-point-induced bijection π defined below (R-PPERM for n = 3, R-SPERM for n = 4) fixes every non-S position pointwise — π(v) = v … Combined with NS-M, this gives M'(d)(π(v)) = M'(d)(v) = M(d)(v) on the non-S domain."

**Problem**: R-NS(NS-M) is a one-line lemma (pointwise identity from the frame condition). The Remark reaches forward to π, which is not defined until R-PPERM/R-SPERM, and restates the identity M'(d)(π(v)) = M(d)(v) — content the R-PPERM and R-SPERM proofs each establish in their own non-S case. The Remark advances no reasoning that R-NS needs and duplicates downstream work; it is meta-prose anticipating a forward reference.

**Required**: Delete the Remark. The non-S case of π is proved where π is defined.

### Issue 3: Repeated provenance/citation parentheticals

**ASN-0084, State and Vocabulary preamble and throughout**: "Both `ord` and the truncated subtraction `m − n` introduced below are local depth-2 conveniences not present in the foundation." Combined with the recurring parenthetical "(extended to j = 0 by the identity convention, as recorded under Extended Associativity)" repeated at R-PRE Subspace confinement, R-BLK Non-S, and elsewhere.

**Problem**: The provenance line states only that notation is local — defensive justification that advances no reasoning. The identity-convention parenthetical is a cross-reference repeated verbatim at each use site rather than established once.

**Required**: State the identity-convention extension once at Extended Associativity; drop the per-use restatement and the standalone provenance sentence.

## OUT_OF_SCOPE

### Topic 1: Documents with text-subspace depth m₁ > 2
**Why out of scope**: The ASN explicitly restricts to m₁ = 2 so that ord(v) is a singleton identified with ℕ. Lifting the displacement arithmetic to deeper text subspaces is new territory, already flagged in the Open Questions, not an error here.

### Topic 2: k-cut rearrangements for k > 4 and composition of rearrangements
**Why out of scope**: The first and fifth Open Questions. Generalizing the cut count and characterizing closure under composition are future work, not gaps in the three/four-cut specification.

VERDICT: REVISE
