# Review of ASN-0127

The technical content checks out under detailed verification: F-IMG-MONO/CONTR/SWING's derivations are correct (I recomputed all four reorder witnesses against the bijection equation — gain, loss, injective, four-position — and each is admissible and yields the claimed image); D-CWP's bridge correctly eliminates post-state quantities and both branches of the biconditional are exercised with genuine computations; E-CONS proves both directions of the "exactly" with the creation-event/set-difference anchor properly established in both directions; the Worked illustration's slot-by-slot coverage computations are all correct, including the prefix-incomparability premise (T10a.2 for siblings, T7 plus the Prefix length-gap argument for `a_θ`). The boundary cases demanded by the standards — empty region, empty arrangement, `findlinks(∅)`, full-region `W ⊇ dom(M(d))`, `R = ∅` full clearance, empty endsets — are all present and handled. The remaining findings are structural, under the anti-bloat mode this note carries.

## REVISE

### Issue 1: F-IMG-SWING buries a load-bearing unlabeled sub-claim that another lemma cites by description
**ASN-0127, Phase 1, F-IMG-SWING**: "*Availability taxonomy.* A moved image stands to its predecessor in one of two shapes: *containment* motion … or *incomparable* motion … Injectivity decides which shapes are available."
**Problem**: D-NONMONO's K.μ~ case branches on this result and cites it twice by description — "which of F-IMG-SWING's two moved-image shapes obtains," "F-IMG-SWING's availability taxonomy and its gain, loss, and four-position witnesses," "per the taxonomy." A result consumed by name from another lemma is a claim, but here it is the fifth inline-headed subsection of a single ~600-word italic derivation block, sitting after three witness constructions and a witness-admissibility schema, none of which belong to the statement F-IMG-SWING actually asserts (the reindexing formula and the cardinality pinning). The reader following D-NONMONO must excavate the block to find what is being cited. The witnesses themselves are correct concrete examples — the finding is their placement and the taxonomy's lack of a label, not their existence.
**Required**: Promote the availability taxonomy to its own labeled claim with its own statement and derivation; relocate the four witnesses and their shared admissibility schema either under that claim or into the Worked illustration; have D-NONMONO cite the label.

### Issue 2: Use-site inventories duplicating the back-references at the consuming sites
**ASN-0127, D-CWP, final sentence of the derivation**: "The Worked illustration instantiates both truth values of the biconditional: failing instances (the `n'_{s_C} = 1` drop; the `R = ∅` full clearance) and satisfied instances with genuine drops `Δ ≠ ∅` (the stable-contraction bullet — once with `findlinks(Δ, Σ) = ∅`, once with a re-witnessing link, `findlinks(Δ, Σ) ≠ ∅`)."
**Problem**: This is a forward inventory of downstream instantiation sites appended to a derivation it does not advance. The same linkage is already recorded at each consuming site ("✓ D-NONMONO contraction clause; D-CWP failing branch"; "✓ D-CWP satisfied branch, at both Δ-shapes: link-free drop and re-witnessed drop") — the same information stated twice in different words. The same consumer-annotation pattern appears in E-CONS's proof-direction header: "Inclusion (`⊇`) — the converse, the half D-ZERO consumes" — which slot D-ZERO consumes is D-ZERO's business, not the proof header's.
**Required**: Delete the D-CWP forward inventory (the Worked illustration's back-references carry the linkage); trim the E-CONS header to "Inclusion (`⊇`) — the converse."

### Issue 3: D-NONMONO's K.μ~ case embeds a self-contained mini-result mid-bullet
**ASN-0127, D-NONMONO, K.μ~ clause**: "(Image-motion is in any case *necessary but not sufficient* for the discovery set to move: by F-MATCH's per-slot existential, a displaced in-region I-address relocates a link only when it was that link's *sole* in-region witness… *Insufficiency witness:* with `Σ.M(d_q) : v₁ ↦ a, v₂ ↦ b` injective and `W = {v₁}` … `findlinks_V(W, d_q, ·)` stays fixed at that singleton while the image moves.)"
**Problem**: A ~120-word parenthetical containing a complete model construction sits inside the case-analysis bullet, and D-NONMONO's conclusion does not use it — the bullet itself says non-monotonicity is "established directly" by the Worked illustration's swing. The necessity/insufficiency observation is good content (it explains when the multi-slot existential absorbs an image move), but its placement forces the reader to skip a nested witness to follow the case analysis. Flagging placement, not existence.
**Required**: Extract the observation and its witness as a small named claim (or place the witness in the Worked illustration adjacent to the swing bullet) and reduce the parenthetical to a one-clause citation.

## OUT_OF_SCOPE

### Topic 1: Uniform stability weakest precondition across the K-vocabulary
**Why out of scope**: D-CWP correctly delivers the contraction instance; the corresponding wp for extension, reorder, and off-document transitions (Q3) is a new result over a different transition shape, not a gap in this note's contraction claim.

### Topic 2: Conjunctive slot-indexed queries and composition with link projection
**Why out of scope**: The per-slot conjunctive matching semantics (Q2) and the composition of `image()` with ASN-0098's `project()` (Q4) are new combinators with their own algebra; this note's disjunctive F-MATCH algebra is complete on its own terms.

VERDICT: REVISE
