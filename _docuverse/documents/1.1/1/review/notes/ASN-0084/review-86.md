# Review of ASN-0084

This is a mature, thorough note — the operations are well-defined, the five worked examples cover the boundary edges (minimum width, empty exteriors, all three μ sub-cases, non-S pass-through), and I found no correctness gap in the pivot/swap postconditions, the permutation bijections (R-PPERM/R-SPERM), or the run-decomposition transformation (R-BLK). The findings below are the meta-prose / forward-reference accretion the `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: Verbatim-duplicated I-address licensing clause in Split and Merge
**ASN-0084, "Split" and "Merge"**: Split says "*here it is applied to the I-address a (element-level, zeros = 3 by S7b, hence deeper than a V-position), licensed because the underlying TS3 (ShiftComposition, ASN-0034) instance holds for any tumbler in T irrespective of depth.*" Merge repeats the identical clause word-for-word for `a₁`.

**Problem**: The same licensing fact — that Extended Associativity / TS3 applies to I-addresses despite their greater depth — is stated twice in full. This is the "two paragraphs say the same thing" pattern. The fact is depth-independent and belongs at the single point where shift on I-addresses is first introduced (the Correspondence-Run Decomposition preamble already notes "`+` on I-addresses denotes `shift(a_s, k)` … irrespective of depth").

**Required**: State the I-address-shift licensing once in the section preamble; in Split and Merge replace both copies with a bare citation (e.g., "by Extended Associativity, applied to the I-address `a` per the preamble").

### Issue 2: "Reduction of compound shifts" restates Extended Associativity and defers its own coverage
**ASN-0084, "Reduction of compound shifts"** (after REARRANGE_K): "*By Extended Associativity, the compound destinations `c₀ + w_β + j` … equal the single-step shifts `(c₀ + w_β) + j` …. The coverage of [c₀, c₃) by these clauses is established where it is consumed, in R-SWP clause (a).*"

**Problem**: Two accretion patterns. (1) The associativity claim is a one-line re-application of the just-stated Extended Associativity, promoted to a named result that R-PIV/R-SWP then cite ("well-defined by the *Reduction of compound shifts* above") — an extra indirection layer for a trivial bracket-shift. (2) The second sentence is a pure forward-reference deferral ("established where it is consumed, in R-SWP clause (a)") that advances no reasoning at the point it appears.

**Required**: Drop the named "Reduction of compound shifts" result; inline the left-associative bracketing directly into R-PIV/R-SWP where the compound destinations are first written, citing Extended Associativity there. Delete the deferral sentence.

### Issue 3: Recurring "not a foundation export / defined locally" scope-defense prose
**ASN-0084, "State and Vocabulary"**: for `ord` — "*ord itself is defined locally here, as the foundation exports no tail-projection*"; for truncated subtraction — "*We define `m − n` … locally in this ASN — it is not a foundation export*."

**Problem**: The same defensive justification (this symbol is local because the foundation lacks it) recurs for two adjacent definitions. A definition does not need to argue for its own right to exist; stating the definition and its license suffices.

**Required**: Consolidate into one sentence noting that `ord` and the truncated subtraction are local depth-2 conveniences not present in the foundation, then give each definition plainly without re-justifying its locality.

## OUT_OF_SCOPE

### Topic 1: Weakest-precondition characterization of REARRANGE_K
The note verifies that R-PRE establishes every ASN-0036 invariant in the post-state, but does not compute the weakest precondition for the post-state invariant suite. It is correctly raised as an open question; deriving wp (and what R-PRE(iv) adds beyond D-SEQ) is a follow-on, not a defect here.

### Topic 2: Composition and k-cut generalization
Whether two rearrangements compose to a single rearrangement, and the natural permutation class for k > 4 cuts, are genuinely new territory listed in Open Questions — future ASNs, not gaps in this one.

VERDICT: REVISE
