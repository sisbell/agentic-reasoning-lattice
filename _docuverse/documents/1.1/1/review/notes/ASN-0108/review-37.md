# Review of ASN-0108

I checked the mathematics before turning to the prose. The window/successor definitions are sound; the wp analysis in W2 is correct (I re-derived `wp(resume_offset, R) = (j'=j) ∨ (j≥m' ∧ j'≥m')` and confirmed the three-condition nesting and the `a_0`-insertion failure walk); the W4 partition induction, the three W5 walks (cut-point skip, harmless tail-reorder, clause-1 cancellation), the W6/W6a frame bridge through F-LAMBDA, the W8 cursor-survival walk, the W9 local-fact derivation and its whole-pass/terminal-state distinction, the W9a count formula (verified against m=4, 5, 0 and N=3/m=2), and the W9b charge-injectivity argument all hold. The boundary cases the standards demand — empty matching set (m=0), first window already short (N>m), cursor at the last link, orphaned cursor — are each walked explicitly. The foundation citations (D-NONMONO, LP12, LP13, F-LAMBDA, F-V/F-FULL, T9, K.λ frame) are used correctly. This is rigorous work.

The REVISE below is therefore not about correctness. The note carries the `review-mode.anti-bloat` classifier, and the key-trichotomy argument (address key / matched-content key / position foil) has accreted a layer of cross-claim meta-narrative — duplicated statements, deferrals to the same location, and forward references threading a side-story through claims that should each stand on their own property. Per the mandate these are findings.

## REVISE

### Issue 1: The "allocation is orthogonal" argument is stated in W5, then restated-and-deferred in W8, then pointed at again from the Claims table

**ASN-0108, W5**: "Allocation axioms enter only orthogonally — that the cursor c stays an allocated, uniquely-identifying address is T8 (no address is ever removed) with LP13 ... and that no distinct allocation event ever reproduces c's address is GlobalUniqueness (ASN-0034) — but none of these is what freezes the key; the freezing is the state-independence of κ itself."

**ASN-0108, W8**: "κ(c) = c is the identity applied to a value already in the reader's hand (value-totality) ... Allocation enters only orthogonally here, exactly as set out under W5."

**ASN-0108, Claims table, W8 row**: "Allocation only orthogonal (see W5)."

**Problem**: The same observation — that the allocation axioms (T8/LP13/GlobalUniqueness) are *orthogonal* to why the address key behaves well — is made fully in W5, restated in W8 prose with the explicit deferral "exactly as set out under W5," and pointed at a third time from the table. This is precisely the named pattern: two passages saying the same thing, with multiple slots deferring to the same location.

**Required**: Make the orthogonality point once (W5 is the natural home, where state-stability is established) and have W8 carry only the property it actually adds — that the *identity* key keeps `κ(c)` computable on the held value with no state lookup. The W8 prose can name computability and let the W5 statement stand; drop the table parenthetical or replace it with the substantive content (computable on held value).

### Issue 2: Key-trichotomy meta-synthesis and cross-claim deferrals recur as accretion

The per-claim statements of how the three keys fare on *that claim's* property (state-stability in W5, monotonicity in W6, computability in W8) are load-bearing and should stay. What has accreted around them is a second narrative *about* the comparison — claims that one key differs from another "only" in some respect, parentheticals naming where the comparison "lives," and forward references that import a later claim's vocabulary into an earlier one.

**ASN-0108, W6**: "so W5's cut-point hazard and **W8's disappearance hazard** are vacuous for each ... and neither key's value can be erased **(W8)** ... Allocation-monotonicity is therefore the **sole** abstract respect in which the two identity keys differ."
**ASN-0108, Claims table, W6 row**: "the sole abstract respect in which it differs from the link-address key **(the comparison's home)**."
**ASN-0108, W5, "A ladder of key conditions"**: re-collects *computability* and *value-totality* — both introduced and glossed at their use sites in W2 and W8 — alongside clause 1 and clause 2.

**Problem**: W6 forward-references W8 ("W8's disappearance hazard," "(W8)") two sections before W8 appears, to assert a meta-fact ("the sole respect they differ"). The table's "(the comparison's home)" is meta-commentary about argument structure, not a system guarantee. The glossary, while it usefully introduces the evaluability-vs-comparison-movement dichotomy, re-collects definitions already given at use sites — a use-site inventory. None of this advances the claim it sits on; a reader following W6's actual content (allocation-monotone ⟹ append-at-tail; matched-content key admits the blind spot) must skip past the W8 forward-references and the "sole respect" framing to reach it.

**Required**: Keep each claim's per-property statement of the three keys. Trim the cross-claim meta-synthesis: state W6 in terms of W6's own property (allocation-monotonicity) without importing "W8's disappearance hazard"; drop "(the comparison's home)"; reduce the glossary to the one genuinely new contribution (the two-family evaluability/comparison-stability split and the computability-vs-value-totality distinction) and let clause 1/clause 2 stand where W5 defines them rather than re-listing them.

## OUT_OF_SCOPE

The topics this note correctly declines to specify — multi-document global ordering, eventual delivery under non-monotone keys, cross-window completeness over a mutating set, exhaustion-vs-cursor-invalidation disambiguation, and delivery/count correspondence — are already placed as the five Open Questions, and the declared out-of-scope operations (count-only, full-set, MAKELINK, FOLLOWLINK, BEBE) are not the subject of any claim. W10 explicitly defers the cardinality query as "a distinct operation, out of scope here." Nothing to add; the scoping is clean.

META: (none) — the note specifies an operation and its abstract guarantees parameterized by key properties, with implementation evidence used as grounding per spec convention; it is on-track and merely over-grown, which is fixable.

VERDICT: REVISE
