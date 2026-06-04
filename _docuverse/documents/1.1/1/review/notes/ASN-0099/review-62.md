# Review of ASN-0099

## REVISE

### Issue 1: Silent-projection uniqueness is a one-line fact buried under an essay
**ASN-0099, "A Two-Phase Factoring" (Phase 1)**: The paragraph defining `image` proves that silent projection is the unique treatment satisfying "(i) no fabrication `g ⊆ img`" and "(ii) faithfulness `img ⊆ g`," then adds "Three families of alternative...," a constant-`ran` counterexample, a concrete `{v¹,v²,v³}` instance, and a weak-vs-strong-bound discussion.

**Problem**: Conjuncts (i) and (ii) *are* the two inclusions whose conjunction is `g = img` by extensionality — the uniqueness is immediate. The constant-`∅`, sentinel-totalisation, and constant-`ran` families, plus the worked instance, restate the same point (the strengthened bound is `img(R)` not `ran`) two or three times. This is essay content padding a trivial mutual-inclusion. A reader must wade through ~250 words to extract one line.

**Required**: Collapse to the mutual-inclusion statement plus at most the single constant-`ran` counterexample that motivates the `img`-vs-`ran` strengthening. Delete the redundant restatements.

### Issue 2: F12 citation-handle meta-prose, repeated across three sites
**ASN-0099, F12 block and Claims Introduced table**: "F12 carries two complementary roles under one block... Downstream citations of 'F12' invoke the unfolding identity... downstream citations of `findlinks_V` invoke the operation itself. The Claims Introduced table lists `findlinks_V` and F12 as separate rows..." — and the table repeats "the F12 row below is the same artifact under its citation-handle label" and "cite F12 to invoke the unfolding identity; cite `findlinks_V`... — same artifact, two labels."

**Problem**: This is meta-prose about how to cite a label, not content advancing the definition. The same "two labels, one artifact" explanation appears in the F12 prose and twice more in the table. It does not advance reasoning; it manages citation bookkeeping.

**Required**: State the definition `findlinks_V(R,d,Σ) ≡ findlinks(image(R,d,Σ),Σ)` once. Drop the paragraph explaining which label to cite and the duplicate table annotations.

### Issue 3: Spans-monotonicity argument stated in full twice
**ASN-0099, "Structural consequence of Layer 2" paragraph and F4 clause (a)**: The abstract argument — spans-monotonicity is broken only by containment; reverse-containment and cardinality are themselves spans-monotone; F1 is distinguished by per-span witness structure, not monotonicity; robustness on two counts — appears nearly verbatim in the "Structural consequence" paragraph and again inside F4(a).

**Problem**: Two paragraphs in different sections say the same thing in different words. The "illustrated" L₀/L₁ example between them is concrete (permissible), but the two abstract statements are redundant. The LM 4/60 "convergent but not the anchor" caveat is likewise repeated at the end of both the "Structural consequence" paragraph and the F4 block.

**Required**: Carry the abstract argument once (in F4(a), since F4 is the named claim), reduce the "Structural consequence" paragraph to a pointer or fold it into the F4 commentary, and state the LM 4/60 caveat a single time.

### Issue 4: A1 — K.σ-unreachability and "see above" duplication
**ASN-0099, "Arrangement Independence" prose and A1 block**: The argument that ASN-0093's K.σ is not in the operative vocabulary and "is unreachable in this model" appears in the paragraph preceding A1 ("...it belongs to the un-extended substrate (C, L, M) and is unreachable in this model") and again inside A1's *Vocabulary scope* ("not by ASN-0093's substrate K.σ (which is unreachable in the (C, L, M, E, R) model — see above)").

**Problem**: The same exclusion rationale is given twice, the second deferring to the first ("— see above"). The A1 block also accretes sub-prose ("Vocabulary scope:", per-operation frame recitals) that restate A1a's published-frame discharge already stated in A1a's own block.

**Required**: State the K.σ exclusion once. Have A1 cite A1a for the per-operation frame discharge rather than re-enumerating {K.α, K.δ, K.μ⁺, ...} a second time.

### Issue 5: F10a presented as load-bearing for F10's ordering when it is not
**ASN-0099, F10 and "For the cross-document part of F10's ordering: F10a..."**: F10 claims a unique strictly T1-increasing presentation, justified by "finiteness + T1 total order." The text then introduces F10a (AnchorLiftingOfDocumentOrdering) and ChainIndexEqualsAllocationOrder "For the cross-document part of F10's ordering."

**Problem**: F10's existence/uniqueness of the sorted presentation follows *immediately* from T1 being a total order on the finite subset `dom(Σ.L)` — no anchor-lifting or chain-index lemma is needed. F10a and ChainIndexEqualsAllocationOrder actually support only the interpretive "Chronological reading" aside (within-doc T1 = K.λ order; cross-doc T1 = document order). Framing them as "the cross-document part of F10's ordering" overstates their role and presents interpretive apparatus as proof support.

**Required**: Decouple F10a / ChainIndexEqualsAllocationOrder from F10's ordering claim and attach them explicitly to the "Chronological reading" remark, which is what they establish.

## OUT_OF_SCOPE

### Topic 1: Inverse direction (FOLLOWLINK / RETRIEVEENDSETS), partition tolerance, access control, query semantics for I-addresses outside the stores
**Why out of scope**: These are correctly listed under "What We Have Not Specified" and "Open Questions" as future ASNs; the note does not claim them, so no error here.

VERDICT: REVISE
