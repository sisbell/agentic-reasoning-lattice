# Review of ASN-0071

The operation itself is correctly specified: the extensional `find`/`iaddrs` definitions are sound, PC and PC-RANGE are derived rigorously (componentwise fact → totality → prefix agreement is a genuinely careful argument, not a hand-wave), and the boundary coverage is strong — empty query, width-1 span, cross-depth coarse anchor, deep-anchor-empty, multi-source dedup, and a concrete non-containing document (`d_C`) are all exercised against worked states. I found no correctness or coverage gaps. The remaining findings are the meta-prose accretion this note is classified to catch.

## REVISE

### Issue 1: Defensive justification of the extensional definition
**ASN-0071, *The operation***: "so it is sound and complete by construction: a `d ∈ E_doc` is returned iff it satisfies the predicate, with no further proof obligation."
**Problem**: This is the residue of the collapsed F-COMP/F-SOUND claims, now restated as a defense of why no proof follows. "Sound and complete by construction" and "with no further proof obligation" justify the *absence* of work rather than advance any claim — a definition needs no such disclaimer.
**Required**: Reduce to the bare fact that the definition is extensional; drop the soundness/completeness self-justification.

### Issue 2: Triple restatement of current-containment
**ASN-0071, *Currency: state dependence***: "The predicate is evaluated at the moment of query, not over the lifetime of the docuverse. ... The operation reports current containment, full stop. ... the extensional result is therefore over the *currently-containing* set."
**Problem**: One fact (the result reflects current `M`, not historical `R`) is paraphrased three times in a single paragraph, with "full stop" as colloquial filler. The F-CUR claim and the one-sentence note that `find` does not consult `R` (P2) carry the content; the rest is restatement.
**Required**: State the current-vs-historical point once.

### Issue 3: PC-RANGE geometric gloss restates the closed form
**ASN-0071, PC-RANGE paragraph**: "it *lies within* the union of `ℓ_{#u}` sibling subtrees ... most of those geometric subtrees hold no arrangement positions, and if some `u_j ≠ 1` ... the intersection is empty even when `#u ≤ m_C`."
**Problem**: The closed-form characterisation is already stated as the formula immediately above; this paragraph re-describes the same set in subtree prose without introducing a new claim, and "most of those geometric subtrees hold no arrangement positions" is descriptive color. The width-1 specialisation is the only part with a downstream consumer (cited in the Q_E example).
**Required**: Keep the width-1 specialisation; drop the geometric re-description and the "most subtrees are empty" color.

### Issue 4: Essay phrasing in a proof slot
**ASN-0071, *The operation*, F-SELF**: "querying a document's own passage must return at least that document, the formal bridge between the read-direction (what `d_s` contains) and the search-direction (who contains it)."
**Problem**: The interpretive "formal bridge between the read-direction ... and the search-direction" is essay content sitting inside the F-SELF derivation; the proof that follows (`a ∈ ran(M(d_s)) ∩ iaddrs(Q)`) stands on its own.
**Required**: Drop the interpretive clause; the one-line statement of what F-SELF guarantees is enough.

## OUT_OF_SCOPE

### Topic 1: Relationship to historical containment `R`, rejection of unresolvable vspecs, contraction invariants
**Why out of scope**: These are correctly deferred to the Open Questions and concern future operations/guarantees, not defects in this query specification.

VERDICT: REVISE
