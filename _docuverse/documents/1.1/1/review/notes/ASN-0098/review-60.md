# Review of ASN-0098

## REVISE

### Issue 1: Forward-reference accretion — duplicated "construction discipline / LP19" deferral across sections

**ASN-0098, "Operation Effects" intro (after LP6/LP7/LP14 block) and LP9 body**: The same meta-claim is stated three times in different sections:

- After the LP6/7/14 paragraph: "Whether boundary insertion can extend a link's reach therefore depends on the endset's construction discipline; the tight case, where it cannot, is established as LP19."
- The immediately following sentence: "Newly allocated I-addresses are invisible to projection until some subsequent K.μ⁺ adds an arrangement entry referencing them..."
- LP9 body: "When K.μ⁺ adds entries mapping V-positions to newly K.α-allocated I-addresses, whether the projection grows depends on the endset's construction discipline."

**Problem**: This is exactly the forward-deferral pattern the anti-bloat mode targets — multiple paragraphs in different sections defer to the same downstream location (LP19) and restate "whether the projection grows depends on construction discipline" in near-identical words. The reader following LP9 must skip past prose that re-announces a result two sections away rather than advancing LP9's own claim.

**Required**: State the dependence-on-construction-discipline / LP19 pointer once (at the LP19 site, or once at the operations intro), and let LP9 state only its own monotone-growth result. Remove the duplicate sentences in the operations-intro paragraph and the redundant clause inside LP9.

### Issue 2: Degenerate-configurations overclaim ignores optional slots 4…N

**ASN-0098, "The Projection Operation" (degenerate configurations)**: "A link with empty from/to endsets but a non-empty type endset (admitted by L3 of ASN-0043, which requires only the type slot to be non-empty) has empty projections at slots 1 and 2 regardless of any document's state; only the type slot's projection can be non-empty."

**Problem**: L3 admits arity `N ≥ 3` with only slots 1,2 stipulated empty and slot 3 non-empty. The premise does not constrain slots `4,…,N`. A link `(∅, ∅, Θ, e₄)` with `e₄ ≠ ∅` satisfies the described hypothesis yet has a potentially non-empty projection at slot 4. The conclusion "only the type slot's projection can be non-empty" is therefore too strong for `N > 3`.

**Required**: Either restrict the statement to the standard triple (`N = 3`), or weaken to "slots 1 and 2 have empty projections regardless of state; non-emptiness can arise only at slots 3,…,N."

## OUT_OF_SCOPE

### Topic 1: Discoverability preservation for link-canonical endsets under content-subspace-emptying contraction
**Why out of scope**: The note already flags this in the final Open Question — LP12b discharges only the *content*-canonical case, and the inverted (link-canonical) case is correctly left open rather than asserted. This is future territory, not a gap in the present claims.

META: not needed — the ASN defines abstract state (projection as a live computation over coverage ∩ arrangement), operations' effects on it, and survivability invariants, all stated implementation-independently; it remains squarely in specification territory.

VERDICT: REVISE
