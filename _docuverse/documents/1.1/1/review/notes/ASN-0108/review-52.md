# Review of ASN-0108

The mathematical core is sound. I checked the wp analysis in W2 (the identity/offset nesting `j=j' ∨ (j≥m' ∧ j'≥m')` is the correct weakest precondition), the W4 partition induction, the W9a count formula against all four boundary walks (m=0, exact multiple, non-divisible, N>m), the W9b charge-injectivity argument, and the three W5 walks (cut-point skip, tail-reorder harmless, clause-1 cancellation). All hold. Boundary coverage (empty matching set, N>m, exact-multiple terminator) is thorough. The findings below are the residual forward-reference / meta-prose accretion the `review-mode.anti-bloat` pass exists to surface.

## REVISE

### Issue 1: Design-alternative essay around the key choice
**ASN-0108, "The Enumeration Order" (key-discussion paragraph)**: two adjacent passages defend the *fixed* slice against the *matched* slot:

> "'Fixed' is here literal: the designated slice is settled before any pagination begins and is a function of the immutable link value, **not** of whichever endpoint the link happens to match… whereas the least I-address of a slice fixed before the query runs is invariant."

> "One could instead buy totality by keying on *whichever slot the link matched*… But that key is *not free*: the matched slot varies with the query and the state… Totality and permanence pull opposite ways, and the fixed *type-including* slice is the design point meeting both."

**Problem**: ~150 words exploring and rejecting a design alternative the note does not adopt. The committed definition (least-I-address over a fixed type-including slice) is what the reader must hold; the "one could instead… but not free… pull opposite ways" framing is essay content the reader works past to reach it. The embedded concrete fact (udanax-green's spanfilade keys on the *matched* subspace) is a legitimate implementation statement — flag the framing and length, not that fact.
**Required**: Compress to the keepable concrete statement plus one clause of reason — e.g. "udanax-green keys on the matched slot (total by matching, but query- and state-dependent); we fix the slice *a priori* so the key is a function of the immutable link value, recovering totality by requiring the type slot (`e₃ ≠ ∅`, L3)." Drop the "fixed is literal" defense and the "pull opposite ways" exploration.

### Issue 2: Definition introduction enumerating downstream consumers
**ASN-0108, "The Enumeration Order" (type-slot totality argument)**: "…a type-including slice covers at least one I-address on every link in `dom(Σ.L)`, hence on every matcher — the key is total on `Match`, **and the state-stability (W5) and computability (W8) claims below inherit that totality**."

**Problem**: The bolded clause is a use-site inventory — naming which downstream claims consume the property just established rather than advancing the argument. This is exactly the "a definition's introduction enumerates downstream consumers ('consumed by X, Y, Z')" pattern. W5 and W8 already cite the totality where they use it; the back-pointer here is redundant.
**Required**: End the sentence at "the key is total on `Match`." Let W5 and W8 cite totality at their own use-sites.

### Issue 3: Roadmap preview duplicating W5's clause structure
**ASN-0108, "Stability of the Order Across Evolution" (opening paragraph)**: "Whether the *order* of the links still to come is held fixed too turns out to be a separate, strictly stronger demand — sufficient but not necessary — **which we untangle below**."

**Problem**: This previews W5's clause-1/clause-2 split before W5 states it, with a "which we untangle below" deferral. The cut-vs-order distinction, the "strictly stronger," and the "sufficient but not necessary" are all made precisely in W5; the preview is forward-reference scaffolding. Lowest-priority of the three — roadmap framing in a prose note is borderline — but it is a clean instance of the deferral pattern this pass targets.
**Required**: Either cut the preview and let the section open on the substance, or shorten to the one load-bearing fact ("it suffices that the cursor's cut not move; preserving the tail's internal order is a separate, stronger demand") without the "untangle below" deferral.

## OUT_OF_SCOPE

None. The note correctly defers count-only sizing (W10: "a separate cardinality query… out of scope here") and routes multi-document ordering, non-allocation-monotone delivery, cross-state completeness, uncomputable-key protocol, and progress-sizing correspondence to the Open Questions rather than specifying them here. No claims encroach on FINDNUMOFLINKSFROMTOTHREE, FINDLINKS, MAKELINK, FOLLOWLINK, or BEBE.

VERDICT: REVISE
