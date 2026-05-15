# Channel Assignment — ASN-0084 review-22

**Date:** 2026-05-15 10:25

## Issue 1: D-SEQ citation invokes a foundation property outside its domain
Reason: The fix is derivable from the ASN's own content — replace D-SEQ citations with R-PRE(iv) (which guarantees ordinal coverage in the affected range) plus depth-2 sequential ordinals from the State and Vocabulary section. The review has already stated D-SEQ's actual scope in ASN-0036; no external clarification is needed to apply the substitution.

## Issue 2: Backward-extension argument in canonical decomposition uses Merge implicitly
Reason: The fix is internal — the Merge lemma is defined in the same section (Correspondence-Run Decomposition Transformation), just above part (b). The author can either name Merge explicitly when extending b₁ backward/forward or unfold S8(b) verification using b₁'s own consistency clause.

## Issue 3: Empty-exterior edge cases not verified
Reason: The fix is derivable from the ASN — R-EXT is already a universal quantification over v < c₀ or v ≥ c_{n−1}, which is vacuously true when those sets are empty. The author can either add a small worked example using existing definitions or insert an explanatory sentence in R-PIV/R-SWP. No external evidence or intent clarification required.

## Issue 4: R-DISP's 4-cut μ-case statement is not self-contained
Reason: Purely editorial — the three sub-cases are already stated inline in the PermutationDisplacement definition immediately preceding R-DISP. The author just transcribes them into the R-DISP statement.

## Issue 5: Disjointness justification is imprecise
Reason: Internal rewording — the half-open interval algebra is elementary and the role of w_β ≥ 1 (non-emptiness) versus disjointness (from interval structure) is already clear from R-PRE(v). No external channel needed.

## Issue 6: Subspace m_S = 2 restriction is implicit
Reason: The fix is derivable from existing citations — CS4 fixes cut depth at 2, and S8-depth (ASN-0036) is already invoked elsewhere in the ASN to force all V-positions in subspace S to share m_S. The author can state the consequence explicitly using citations already present.
