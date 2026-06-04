# Review of ASN-0099

## REVISE

### Issue 1: Mechanical variant-claims proliferate as one-line deferrals
**ASN-0099, "Scope" / "Result Ordering" sections**: "F15 follows from ComprehensionInvariantUnderΣL applied to the filtered universal. F16 follows from F8 + intersection-preservation with the query-supplied S. F17 follows from F9 ... + F15. F18 follows from F9 + intersection-preservation." Likewise F10-filt, F10-sco, F19-filt, F19-sco, and the F2/F3 conformance pairs (-filt, -sco, -V).

**Problem**: Each of these is the same property (determinism, survivability, monotonicity, ordering, conformance) restated once per operation form, with a one-line "follows from X + Y" that defers to the same upstream results (the two meta-lemmas, F8, F9). This is exactly the accretion the anti-bloat pass targets: many labeled-claim slots carrying no new reasoning, all pointing at the same downstream location. The proliferation obscures which claims are load-bearing.

**Required**: Collapse the filtered/scoped/V variants into a single parametric statement per property — e.g., one lemma "determinism, survivability, and monotonicity transfer to the filtered and scoped forms because their membership predicates consult only Σ.L and query-data (ComprehensionInvariantUnderΣL) and are closed under intersection with the query-supplied S." Keep distinct labels only where an argument genuinely differs.

### Issue 2: F4 realizability paragraph is defensive rationale
**ASN-0099, F4 (MatchIndividuation)**: "Realizability. Each witness is realizable: the I-set is a query parameter and endsets are freely chosen at K.λ (L4 places no constraint on span addresses), so every (a, I) pair below arises by a K.λ allocation under any document."

**Problem**: The witnesses themselves are concrete and legitimate (individuating the predicate is spec-useful), but the framing — a standalone "Realizability" justification plus "The natural alternative match designs ... each yield an operation distinct from FINDLINKS" — is exhaustiveness-flavored design-rationale defending the choice rather than advancing the definition. It is the kind of meta-prose the reader must read past to reach the witnesses.

**Required**: Drop the separate realizability paragraph (fold a half-sentence into the witness construction if needed) and state the witnesses directly without the "natural alternatives are each distinct" preamble.

### Issue 3: Self-cancelling "interpretation" bullet
**ASN-0099, "What We Have Not Specified"**: "The interpretation a reader should attach to a query with I-addresses outside dom(Σ.C) ∪ dom(Σ.L). The semantics are already pinned by the comprehension ... but what such a result means to the reader is left open."

**Problem**: The bullet both asserts the semantics are pinned and that the meaning is open — it cancels itself and adds essay content to a scope list. The substantive fact (ghost-covering links may appear, LP17) is already covered.

**Required**: Reduce to a plain scope exclusion or delete; the LP17 behavior needs no interpretive gloss.

### Issue 4: Redundant opener in "Arrangement Independence"
**ASN-0099, "Arrangement Independence"**: "The I→Link phase consults Σ.L and I alone. F8 already encodes this."

**Problem**: These two sentences restate F8 (Determinism) and F5 (Identity, not value) before the section does its actual work (defining link-store-inert, A1a, F9). They advance no reasoning. The section title also names "Arrangement Independence" but the content covers all V∖{K.λ} operations, not only arrangement edits.

**Required**: Delete the opener; retitle to reflect link-store-inert preservation (the actual subject).

## OUT_OF_SCOPE

### Topic 1: Antitone behavior of findlinks_filtered in the constraint set C
**Why out of scope**: The ASN proves additivity in I (F13) and monotonicity in state (F19) but not how the filtered result behaves as C grows. This is a separate algebraic property of the filtered form, fairly stated as future work alongside the ASN's own noted gap (combined `findlinks_filtered_scoped`), not a defect here.

VERDICT: REVISE
