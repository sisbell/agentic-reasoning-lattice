# Review of ASN-0113

The mathematical core is sound. W4's coverage derivation (T5 on the shared prefix plus half-open last-component pinning), W5's contiguity biconditional (forward via the actual minimum, converse via order-convexity), W10/W11's first-component confinement, W12's reachability construction over valid composites, and the W20 weakest-precondition characterizations all hold up, and the three worked instances (including the non-vacuous depth-3 case exercising prefix-confinement) check the postconditions against concrete tumblers correctly. The findings below are the meta-prose patterns the anti-bloat classifier flags.

## REVISE

### Issue 1: W11's "we do not invoke T7" parenthetical is defensive meta-prose
**ASN-0113, "Why text and links must be reported apart" (W11)**: "(We do *not* invoke T7, SubspaceDisjointness: T7 requires element-level I-addresses with `zeros = 3` ... Indeed those tumblers need not be zero-free ... e.g. `[S,1,0,1] ∈ ⟦ext(d, S)⟧` ... T7's preconditions are thus neither met nor needed.)"
**Problem**: The actual W11 proof is complete two sentences earlier — "we would need `t₁ = s_C` and `t₁ = s_L` at once (W10), impossible since `s_C ≠ s_L` (SC-NEQ) ... suffices on its own." The parenthetical explains which foundation lemma is *not* used and constructs a `[S,1,0,1]` witness to justify the non-use. This advances no claim; a reader following W11 must skip past it. This is exactly the defensive-justification pattern the anti-bloat note names.
**Required**: Delete the parenthetical, or reduce to at most a clause noting the disjointness rests on the first component alone.

### Issue 2: W5's empty-case paragraph reasons about a case the hypothesis excludes
**ASN-0113, "The extent of a single subspace" (W5)**: "The non-emptiness hypothesis is load-bearing and cannot be dropped. For empty `V_S(d)` the biconditional fails outright: its right-hand side is ill-defined ... while its left-hand side is *false* ... The empty subspace is thus *not* a degenerate instance of W5 but a case W5 explicitly excludes: it is handled separately by W0..."
**Problem**: W5 is stated under the hypothesis `V_S(d) ≠ ∅`. This full paragraph then imagines `V_S(d) = ∅` — the case the precondition already excludes — re-derives that no span denotes `∅`, and defers to W0 downstream. This is the reviser-drift pattern (a paragraph imagining the excluded case plus a downstream deferral). One sentence stating "the empty case is excluded and handled by W0" carries the same content.
**Required**: Collapse the paragraph to a single clause recording that the hypothesis excludes empty `V_S(d)`, which W0 covers.

### Issue 3: orphan design-philosophy essay in the same section
**ASN-0113, "Why text and links must be reported apart"**: "There is a second, independent reason the kinds resist a single extent ... Text positions are rearrangeable ... Link positions, by contrast, accrue in *permanent order of arrival* ... A combined extent would conflate a count under one discipline with a count under another."
**Problem**: This "second reason" carries no claim and the structural-necessity argument (W10/W11 disjoint subtrees) already establishes that a single span cannot cover both kinds. The counting-discipline passage is design philosophy adjacent to, but not formalized by, W15 (which is about count independence, a different point). It is essay content the precise reader works around.
**Required**: Either drop it, or attach it to a claim if the discipline distinction has formal consequence; as standalone motivation it should be trimmed.

## OUT_OF_SCOPE

(none — the ASN correctly confines itself to the per-subspace extent query and defers content delivery, the single overall bound, link counting/discovery, version comparison, and transclusion to the named future operations.)

VERDICT: REVISE
