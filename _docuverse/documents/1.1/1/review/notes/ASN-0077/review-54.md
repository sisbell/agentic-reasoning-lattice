# Review of ASN-0077

The mathematical content is strong: O0–O14 are carefully derived, every conjunct of the lifted definitions is discharged against a named foundation fact, boundary cases (empty intersection, singleton, cross-subspace, empty document, empty-restriction) are all addressed, and the worked example verifies O5★/O6★/O7/O8/O9/O10/O11/O11′ and both wp formulas against concrete states. I found no correctness gap in the proofs.

The findings below are all `review-mode.anti-bloat` items: dependency inventories and meta-prose accreted in structural slots. Per the classifier these are findings, so the verdict is REVISE.

## REVISE

### Issue 1: Summary item (1) duplicates O0's full dependency chain
**ASN-0077, Summary, item (1)**: "(established in S7 of foundation ASN-0036 for `dom(C)` and extended to `dom(L)` by O0, grounded structurally in L1 (LinkElementLevel) of ASN-0047 and semantically in L1c (LinkAllocatorConformance) composed with the Allocator hierarchy definition and SubAllocatorBundle of ASN-0047)"
**Problem**: This is a use-site/dependency inventory in a summary slot. The same chain (S7b, L1, L1b, L1c, Allocator hierarchy, SubAllocatorBundle, P6, L1a) already appears in O0's claim, its derivation, and the Claims Introduced table — three other places. The summary's own assertion ("which is structural, total, and permanent") is the load-bearing content; the parenthetical re-enumeration is noise the reader must skip.
**Required**: Drop the parenthetical dependency dump; keep "origin is structural, total, and permanent."

### Issue 2: Claims Introduced table reproduces derivations rather than stating claims
**ASN-0077, Claims Introduced, O0 row**: "with (a) structural well-definedness via S7b (dom(C)) / L1 + L1b (dom(L)), (b) semantic correspondence via S7 (for dom(C)) and L1c + Allocator hierarchy + SubAllocatorBundle (for dom(L)), (c) totality via P6 (dom(C)) / L1a (dom(L)), and single-valuedness"
**Problem**: A claims table is an index of statements; this row reproduces the three sub-proofs' citation lists, duplicating the derivation a fourth time. The table row should name *what* O0 asserts, not *how* it is proved.
**Required**: Reduce to the statement — "origin extended to a total, single-valued, document-level projection on `dom(C) ∪ dom(L)`." The per-conjunct citations belong only in the derivation.

### Issue 3: Defensive exhaustiveness meta-prose in O11★★
**ASN-0077, O11★★ derivation, sub-case (iii)**: "together the three sub-cases exhaust every transition by the binary modifies-`M(d)`/leaves-`M(d)`-fixed partition, with no appeal to a complete transition-kind enumeration."
**Problem**: The clause "with no appeal to a complete transition-kind enumeration" is meta-commentary defending the proof technique against an anticipated objection, not a step in the argument. The binary partition already states exhaustiveness; the disclaimer adds nothing.
**Required**: Keep "the two sub-cases partition every transition by whether it modifies `M(d)`"; delete the defensive tail.

### Issue 4: Forward deferral + essay tail in the post-O0 CL-OWN paragraph
**ASN-0077, "Where origin already lives," paragraph after O0**: "...The two coincide for the home-document case (`d` arranging its own link), which O2 below relies on. The extension is faithful to Nelson's design intent that origin reporting applies uniformly to all addressed material in tumbler-space, not only to content: links are first-class citizens with home documents..."
**Problem**: "which O2 below relies on" is a forward deferral that does not advance the O0 claim at its location; the closing sentence is essay restating design intent already conveyed. The substantive distinction (CL-OWN = which document *arranges*, K.λ = which document *allocates*) is worth keeping; the deferral and the design-intent flourish are not.
**Required**: Retain the arrange-vs-allocate distinction; drop the "O2 below relies on" pointer and the Nelson-intent sentence.

## OUT_OF_SCOPE

The four Open Questions (cross-subspace I-span link origins, intermediate-chain surfacing, native-vs-transcluded distinction, historical containment from `Σ.R`) are correctly deferred rather than half-specified — no action needed. The note introduces no claims for INSERT/DELETE/COPY/REARRANGE mechanics, link semantics, version DAG, or BEBE.

VERDICT: REVISE
