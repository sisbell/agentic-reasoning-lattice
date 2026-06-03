# Review of ASN-0071

The mathematics is solid. PC, PC-RANGE, F-DEEP, and the worked scenario all check out — the prefix-confinement derivation handles the first-disagreement well-ordering correctly, the depth-split biconditional covers `#v = #u` and `#v > #u` with proper boundary exclusion (exclusive reach), and the cross-depth/deep-anchor duals are computed correctly. No cross-ASN references outside the foundations, no rigor gaps. The remaining issues are residual non-advancing prose, consistent with this note's active anti-bloat classifier.

## REVISE

### Issue 1: Restating-and-deferring sentence in the well-definedness paragraph
**ASN-0071, *The operation* / "Well-definedness precondition"**: "When it holds, every `Σ.M(d_s)` named in `iaddrs(Q)(Σ)` is a defined arrangement and the resolution of the previous section applies unchanged."
**Problem**: The preceding sentence already establishes that `find` is defined exactly when `wp-defined` holds (because it invokes `iaddrs`, "whose definedness `wp-defined` already establishes"). This sentence re-unpacks what "`wp-defined` holds" means and then defers to "the previous section applies unchanged" — it advances no new claim. It is the defer-plus-restate pattern.
**Required**: Delete the sentence; the first sentence of the paragraph carries the full content of the well-definedness precondition.

### Issue 2: Editorial commentary in the cross-depth capture proof
**ASN-0071, *Resolution* / "Positions of depth `#v < #u`"**: "Both sides drop every position shallower than the anchor, so the characterisation contributes nothing — and costs nothing — for these positions."
**Problem**: The proof work is "both sides drop every position shallower than the anchor." The trailing clause "so the characterisation contributes nothing — and costs nothing" is commentary *about* the proof rather than a step *of* it — the precise reader skips it to reach the displayed set equality. Same applies to the ranking aside "The equal-depth sub-case is the principal one" earlier in the section: the load-bearing fact (S8-depth forces a single per-source depth `m_C`, so `#u` vs `m_C` decides the live case globally) survives without the "principal" framing.
**Required**: Trim the "contributes nothing — and costs nothing" clause to the bare exclusion statement; drop "is the principal one" while keeping the S8-depth fact it introduces.

## OUT_OF_SCOPE

### Topic 1: Relationship between current-state result and historical `R`
**Why out of scope**: Correctly deferred to the Open Questions; F-CUR's statement that `find` does not consult `R` is sufficient for this ASN, and the guarantee linking the two belongs to a future ASN.

### Topic 2: Reject-vs-filter policy for unresolvable vspec positions
**Why out of scope**: F-FILT fixes the silent-filter semantics for this operation; whether the system should instead reject is a separate operational-policy question, properly listed as open.

VERDICT: REVISE
