# Review of ASN-0125

The mathematics is sound. I checked EL0 (the wp/persistence argument), EL4 (single-target via PrefixSpanCoverage + R0a), EL6/EL7 (the two-emission frame and the `nullified(Σ') = nullified(Σ)` activity argument, both the unconditional `∩ dom(Σ.L)` half and the disciplined full-state half), EL10's position-reuse construction, EL11(a)'s contextual biconditional (the "no content address extends `old(e)`" step holds: a content `t ≽ y` would carry `s_L` at the post-third-zero position by prefix agreement, contradicting `E(t)₁ = s_C`), EL13's commutation, EL14's three cardinalities, and the entire worked example (addresses, `succ_o`/`current` transitions, and the standoff `current(ℓ₀) = ∅`). No correctness gaps in the claims themselves.

The findings are one foundation misattribution and four instances of the accreted meta-prose the `anti-bloat` classifier flags.

## REVISE

### Issue 1: T10 attributed to the wrong foundation ASN
**ASN-0125, EL3, "The menu was shorter than it looked"**: "allocation under a prefix is the prefix owner's monopoly — T10, ASN-0042 —"
**Problem**: T10 (PartitionIndependence) is ASN-0034, not ASN-0042. The clause conflates two distinct foundations: T10 (ASN-0034) gives coordination-free disjointness; the *ownership monopoly* on allocation under a prefix is ASN-0042 (O5 SubdivisionAuthority / O2 exclusivity). As written, the citation asserts a theorem that does not exist in ASN-0042.
**Required**: Cite T10 as ASN-0034 and the monopoly as ASN-0042's O5, or drop the conflation and cite only the ownership lemma that carries the "owner's monopoly" claim.

### Issue 2: use-site inventory in the layer-transfer paragraph
**ASN-0125, "The substrate we build on", Layer transfer**: "Every ASN-0086 fact we cite — totality of `a_emit`, tuple freshness R0, the flat-domain antichain R0a, the chain freshness lemmas, the disciplined simplification of wp Case 2, the monotone growth of typed slices (R3) and one-way growth of `nullified` (R6a) — depends on exactly two properties of state evolution..."
**Problem**: The fact-by-fact enumeration is a use-site inventory of downstream consumers. The load-bearing content is the transfer principle alone: ASN-0086's facts hold over the full vocabulary because (i) `L` changes only by `K.λ` fresh appends and (ii) `dom(M)` is monotone — both established independently (Vocabulary fact V; M1). The reader must skip the inventory to reach the argument.
**Required**: State the two properties and the transfer principle; delete the enumeration of which facts are cited.

### Issue 3: methodology scope paragraph
**ASN-0125, "The substrate we build on", final paragraph**: "Finally, scope. This note does not specify link creation as a user surface... Where a reader capability must be named — 'the claims targeting `y` are computable' — we cite the foundations' existing operators (`Observe_K`, the projection lemmas of ASN-0098) rather than define query machinery of our own."
**Problem**: Meta-prose about method. The choice to cite rather than define is already conveyed by the citations at the use sites (EL11b cites `Observe_K`); stating it here adds nothing the reasoning needs.
**Required**: Cut, or compress to a one-line scope note.

### Issue 4: closing slogan paragraph restates the claims with no formal content
**ASN-0125, final paragraph after EL16**: "That is what the architectural commitment reveals, stated once without formalism... Under this substrate three things became theorems that elsewhere are slogans: **change is addition**...; **relationship is assertion**...; and **currency is judgment**..."
**Problem**: This re-says EL7 (frame), EL1/EL3 (assertion not inference), and EL13/EL14 (currency as query) in slogan form — and "stated once without formalism" concedes it adds no formal content. The same thesis ("relationship is made, not inferred") already appears three times: the intro ("a statement someone must make"), EL1's "This is a refusal, not a gap" coda, and EL3's "*an address cannot be false* ... A representation incapable of being mistaken cannot represent an assertion." That is the "two paragraphs say the same thing in different words" pattern, four-fold.
**Required**: Keep the thesis at one site (EL1 or EL3, where it is doing derivational work) and delete the closing paragraph and the redundant restatements; reduce to a pointer to the governing claims if a synthesis is wanted.

### Issue 5: preview and forward-reference prose
**ASN-0125, multiple sites**:
- Intro: "We shall find that EDITLINK names no substrate mutation and no new substrate mechanism at all" and "Everything else — chain semantics, fork tolerance, the refusal to name a unique 'current' — follows from taking that seriously."
- "The mutation postcondition is unachievable": "The remainder of this note determines what the quoted conjunct can mean, proves what it cannot mean, and derives the unique carrier compatible with the substrate."
- Df-DISC: "cycles of length ≥ 2 are deliberately *not* excluded — they are reverts, and we shall need them."
- Df-DIR: "the two acts remain distinct relations, and — as EL6(iv) will make exact — asserting the first never performs the second."
**Problem**: These previews assert conclusions (EL0/EL1/EL3/EL14) before they are derived, and the Df-DISC/Df-DIR clauses defer a definition's content to a not-yet-stated downstream claim ("we shall need them", "will make exact"). They do not advance the local reasoning; the claims state themselves where they appear.
**Required**: Drop the roadmap previews. Remove the forward "we shall need them"/"will make exact" pointers — the cross-reference is recoverable from the claim label at the consuming site (EL14(c), EL6(iv)) without the definition gesturing forward.

## OUT_OF_SCOPE

### Topic 1: authority over cross-asserter retraction
The worked example has H emit `Nullify(Σ, H, c₂)` against a claim `c₂` homed at P, with no authority check — mechanically permitted because ASN-0086's `Nullify` imposes none. This is **not** a REVISE: the ASN claims no authority control and explicitly defers it ("What authority invariant must govern retraction of a supersession claim by a principal other than the claim's asserter?", Open Questions). The example correctly demonstrates only mechanical possibility, consistent with the deferral.

VERDICT: REVISE
