# Review of ASN-0043

## REVISE

### Issue 1: The Link definition mis-attributes the all-arity slot-3-is-type designation to a convention scoped to arity 3
**ASN-0043, Definition — Link / Convention — StandardTriple**: "A *link value* is a finite sequence of N ≥ 3 endsets, with the third slot designated as the type endset by the StandardTriple convention (below)." — while StandardTriple reads "The standard link form has arity 3, with slot 1 as the *from-endset*, slot 2 as the *to-endset*, and slot 3 as the *type-endset*."
**Problem**: StandardTriple is explicitly arity-3 ("The standard link form has arity 3"). Yet the slot-3-is-type designation is used at every arity N ≥ 3: L3 requires `Σ.L(a).e₃ ≠ ∅` for all links, L8 fixes `.type ≡ .e₃` universally, and L9/worked-example Step 3 treat slot 3 as the type at arity 4 with padded slots `4..N`. The actual carrier of "slot 3 is the type endset at every arity" is L3 (and the Named accessor), not StandardTriple. As written, the definition grounds an all-arity designation in a convention that only speaks to N = 3.
**Required**: Cite L3 (or generalize the convention to "slot 3 is the type endset for every N ≥ 3, the arity-3 case being the standard triple") as the source of the slot-3 designation in the Link definition, rather than StandardTriple.

### Issue 2: Motivational section pre-quotes Nelson passages re-quoted verbatim at their establishing invariants
**ASN-0043, "Why Connections Need Identity" vs L2 and L13**:
- The home/ownership quote — "A link need not point anywhere in its home document. Its home document indicates who owns it, and not what it points to." — appears in the ownership bullet of "Why Connections Need Identity" and again, verbatim, in L2 ("Nelson makes this a first principle: ...").
- The CONS-cell quote — "...use the two-sided link structure much like the CONS cell in LISP, and may be built into arbitrary compound links." — appears in the referenceability bullet of "Why Connections Need Identity" and again, in full, in L13.
- The fragment "links connecting parts of a document need not reside in that document" recurs in both L2 and L4(b).
**Problem**: This is the exact accretion the anti-bloat classifier targets: the same Nelson passage carries motivational weight in the framing section and is then re-quoted at the invariant it grounds. A reader following L2/L13 re-encounters quotes already spent in the motivation. Verbatim duplication is the strong form of "two paragraphs say the same thing."
**Required**: Quote each Nelson passage once, at the invariant it establishes (L2, L13), and have the motivational section paraphrase or forward-reference rather than pre-quote. Do not delete the ontological derivation in "Why Connections Need Identity" — only remove the duplicated quotations.

## OUT_OF_SCOPE

None. The Open Questions are correctly posed as future work, and the ASN does not claim any of the scope-excluded operational topics.

VERDICT: REVISE
