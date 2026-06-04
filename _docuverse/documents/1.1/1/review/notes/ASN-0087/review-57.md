# Review of ASN-0087

## REVISE

### Issue 1: Non-circularity justifications are defensive meta-prose
**ASN-0087, Invariant Preservation (D-MIN★ and D-SEQ★/D-CTG★ proofs)**: "We argue this directly — not via D-SEQ★, since ASN-0047 derives D-SEQ★ *from* D-MIN★ and the reverse appeal would be circular." and "read off the set itself, not derived from D-SEQ★ (whose ASN-0047 derivation runs *from* D-CTG★, so the reverse appeal would be circular)."
**Problem**: Both proofs supply a complete direct argument (D-MIN★ by case split; D-CTG★/D-SEQ★ by exhibiting the explicit segment set). The "would be circular" caveats justify the *proof method* rather than advancing it — exactly the "forward pointer is non-circular by Y argument" accretion pattern this note's anti-bloat classifier targets. The precise reader needs only the direct argument; the circularity note is text to skip past. The pattern recurs in two sections.
**Required**: Delete both circularity caveats. The direct arguments stand on their own.

### Issue 2: Frame statement and its derivation are restated across three sites
**ASN-0087, "What Does Not Change"**: "The frame `Σ'.C = Σ.C` is total... The frame is a direct consequence of the composite's structure: K.λ modifies only `L`, and K.μ⁺_L modifies only `M(d)`. Neither operation touches `C`."
**Problem**: This duplicates the Effect section's `Σ'.C = Σ.C` and the M-Frame / M-NoContentEffect table entries, repeating the same "K.λ touches L, K.μ⁺_L touches M(d)" justification already implicit in M-Comp's decomposition. Two paragraphs saying the same thing. The only non-duplicative content is the "referencing is read-only — the endset stores spans, not bytes" clarification.
**Required**: Collapse to the substantive clarification (endsets reference, do not embed, content); drop the re-derivation of the frame.

### Issue 3: wp "Operation enabledness" / membership-clause prose explains convention rather than advancing the argument
**ASN-0087, Weakest Precondition**: "This membership clause keeps `discoverable_from` *defined* at the post-state; it is distinct from `enabled(MAKELINK)`, which keeps the post-state from existing at all."
**Problem**: The distinction-drawing between two conjuncts is meta-commentary on why the wp has the shape it has, sitting in the reasoning path. The wp formula itself already carries the two conjuncts; the gloss on their semantic difference is dispensable.
**Required**: Trim to the wp formula and the one-line reduction. Let the conjuncts speak for themselves.

## OUT_OF_SCOPE

### Topic 1: Forward-reaching / never-allocated endset well-formedness
The Open Questions (endset constraints when spans reference unallocated addresses; deferred-consistency model; type endsets to never-allocated addresses) are correctly posed as future territory, not gaps in this ASN. The side-effect/resurrection characterization here handles the in-scope consequence (LP18 pattern) without needing to resolve them.

VERDICT: REVISE
