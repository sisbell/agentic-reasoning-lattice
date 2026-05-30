# Review of ASN-0058

The mathematics is sound — I checked M-int, M5, M7-cov, M11/M12 (including the M12a partition corollary and both inclusions of M12), M16a, C0, and C2, and the proofs hold. My findings are about accreted meta-prose and redundant claims, consistent with the `review-mode.anti-bloat` classifier on this note.

## REVISE

### Issue 1: M6(d) is defensive filler
**ASN-0058, M6 (SplitPreservation), clause (d)**: "Each piece is a self-contained mapping block whose well-formedness depends only on its own `(v, a, n)` triple — not on external state, not on the existence of the other piece."
**Problem**: A mapping block's well-formedness is, by definition, a property of its own triple — the definition references nothing else. Clause (d) asserts independence from dependencies that were never claimed ("not on external state, not on the existence of the other piece"). This is a defensive justification that adds no obligation beyond "each piece is a mapping block," which (a)–(c) already establish. A precise reader has to confirm there is no hidden content here before moving on.
**Required**: Remove (d), or fold its one operative fact (each piece is itself a mapping block, already stated in M4) into M6's opening sentence.

### Issue 2: M16a re-derives the prefix-copy fact twice
**ASN-0058, M16a (OriginInvarianceUnderShift), `k ≥ 1` case**: Paragraph 1 establishes "By TumblerAdd ..., every component at indices `i < #a` is copied unchanged from `a` to `a + k`, including the entire document prefix and its two separator zeros." Paragraph 2 then re-walks the same copy reasoning: "The wider segment at positions `[1, z₃]` ... lies entirely at indices `< #a`, and TumblerAdd copies every such component unchanged from `a` to `a + k`."
**Problem**: The single load-bearing fact — TumblerAdd copies all components below the action point `#a`, and the document prefix plus its separators sit below `#a` — is derived once, then re-derived in a second framing. The `z₃` paragraph rebuilds the position accounting (`[1, z₃−1]`, the zero at `z₃`) that paragraph 1's "document prefix and its two separator zeros" had already covered, extended only by the third separator. The proof reads as two passes over one argument.
**Required**: Consolidate to a single derivation: action point is `#a`; the document prefix and all three separator positions lie at indices `< #a` (since `#E(a) ≥ 1`); TumblerAdd copies them unchanged; S7b fixes `zeros(a+k)=3` so the prefix boundary lands identically; T3 gives equal origins.

### Issue 3: The "M0 argument" is named but re-expanded inline at use sites
**ASN-0058, M1 proof, M5(b), M12b**: The strict-monotonicity sub-argument ("`v + j < v + k` by TS4 at `j = 0` and TS5 for `j ≥ 1`") is established in M0's verification and explicitly named "the M0 argument." M5(b) cites it correctly ("by the M0 argument (TS4 at k = 0, TS5 for k ≥ 1)"), but M1's proof and M12b ("TS4 distinguishes `i = 0` from `i ≥ 1` ..., and TS5 gives strict monotonicity for `1 ≤ i < n`") re-expand the same TS4/TS5 split verbatim instead of citing the named argument.
**Problem**: Once a sub-argument is named for reuse, re-expanding it at some sites and citing it at others is inconsistent and inflates the proofs. The reader re-reads the same case split three times.
**Required**: Cite "the M0 argument" at every use site (as M5(b) does) and drop the inline TS4/TS5 re-expansions in M1 and M12b.

### Issue 4: M14 is subsumed by M14a
**ASN-0058, M14 (IndependentOccurrences) and M14a (SharedIExtentUnmergeable)**: M14 rules out merging two blocks that share I-start `a` and width `n`; M14a rules out merging any two distinct blocks whose I-extents share at least one position.
**Problem**: M14's blocks share the I-start `a` (the case `i = j = 0`: `a + 0 = a + 0`), so their I-extents overlap and M14a applies directly. M14 is a strict special case of M14a, which the recent revision promoted to general form. Carrying both leaves a claim whose content is fully contained in its successor.
**Required**: Either delete M14 and let M14a carry the transclusion narrative, or demote M14 to a one-line corollary/example of M14a rather than an independently proved property with its own verification.

## OUT_OF_SCOPE

### Topic 1: Structure of the I-space discontinuity at a non-mergeable boundary
**Why out of scope**: The first Open Question (forward gap vs. arbitrary jump) concerns I-space allocation structure across origin boundaries — new territory beyond the block algebra, appropriately deferred.

VERDICT: REVISE
