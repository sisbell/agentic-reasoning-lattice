# Review of ASN-0077

## REVISE

### Issue 1: Forward-reference duplication between "does not promise" and "Open Questions"

**ASN-0077, "What SHOWORIGIN does not promise" / "Open Questions"**: "Whether a complementary operation over `Σ.R` is required is taken up in the Open Questions." and "Whether an operation surfacing the intermediate chain is required is taken up in the Open Questions [Q10]."

**Problem**: Two paragraphs in the exclusions section ("Not historical containment", "Not transitive provenance") defer forward to the same downstream location (Open Questions), which then restates the identical questions. The cross-subspace I-span edge case ("a deliberate choice of the I-span lift's definition: SHOWORIGIN over an I-span reports origins of content, not of links") likewise overlaps the first Open Question (unified content+link operation). The exclusion *statements* themselves are object-level and legitimate; the noise is the "taken up in the Open Questions" forward pointers plus the verbatim re-posing of the same three deferred topics in two sections. This is the "multiple paragraphs defer to the same downstream location" pattern.

**Required**: State each exclusion once. Drop the "taken up in the Open Questions" forward pointers, or fold the three deferred topics into a single location rather than splitting each across the exclusions section and the Open Questions section.

### Issue 2: WF_V conjunct (iii) is redundant

**ASN-0077, Definition (WF_V)**: "(iii) `V_{u₁}(d) ≠ ∅` — the subspace identified by `u₁` is non-empty in `d`'s arrangement."

**Problem**: Conjunct (iii) is derivable from (v) + (vi). By TA-strict (ASN-0034), `u ∈ ⟦σ⟧` with `#u = m` (conjunct (v)); the range condition (vi), `{v : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d))`, then forces `u ∈ dom(M(d))`, so `u ∈ V_{u₁}(d)` and the subspace is non-empty. The "Empty-restriction within a non-empty document" edge case proves exactly this dependency. Carrying (iii) as an independent conjunct is a non-load-bearing precondition.

**Required**: Either drop (iii) and have SDP's non-emptiness citations route through (v)+(vi), or annotate (iii) as a derived convenience conjunct rather than an independent well-formedness condition.

## OUT_OF_SCOPE

### Topic 1: Unified content+link origin operation, transclusion-chain surfacing, historical-containment operation
**Why out of scope**: These are correctly posed as Open Questions — new operations beyond SHOWORIGIN's pointwise/span lifts. They are future ASNs, not defects here (subject to Issue 1's request to state them once).

VERDICT: REVISE
