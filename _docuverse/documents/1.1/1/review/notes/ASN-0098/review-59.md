# Review of ASN-0098

## REVISE

### Issue 1: Repeated forward-deferral to the tightness/LP19 discussion
**ASN-0098, "Operation Effects" / LP9 and the "arrangement-fixing transitions" paragraph**:
- "Whether boundary insertion can extend a link's reach therefore depends on the endset's construction discipline; the tight case, where it cannot, is established as LP19."
- LP9: "When K.μ⁺ adds entries mapping V-positions to newly K.α-allocated I-addresses, whether the projection grows depends on the endset's construction discipline."

**Problem**: Two separate paragraphs (and LP19's own introductory paragraph) defer the same point to the downstream tightness discussion. This is the multi-paragraph-deferral-to-one-location accretion pattern. Neither deferral advances the local reasoning; each just promises a later result.
**Required**: State the local fact once (K.μ⁺ growth is conditional on coverage membership — already proven in LP9's exact-difference formula) and drop the repeated "depends on construction discipline ... established as LP19" pointers. LP19 stands on its own; it does not need to be pre-announced twice.

### Issue 2: Placement-rationale prose in the LP12 introduction
**ASN-0098, after LP12**: "K.μ⁻ is the only K.μ family member that can destroy discoverability (K.μ⁺ and K.μ⁺_L can only enlarge projections by LP9; K.μ~ rebinds without altering the I-addresses reached by LP11), so it is the natural site for a weakest-precondition derivation."

**Problem**: The trailing clause "so it is the natural site for a weakest-precondition derivation" is document-structure justification, not reasoning that advances any claim. The parenthetical re-cites LP9/LP11 conclusions already established.
**Required**: Keep the substantive observation (only K.μ⁻ can shrink a projection to empty) if it is needed as a premise; remove the "natural site" placement rationale.

### Issue 3: Recap restatement in LP18's closing
**ASN-0098, LP18**: "The system architecture admits arbitrarily many cycles of orphanage and resurrection because (i) the link's stored state is permanent (L12 ...), (ii) the I-addresses it references are permanent (S0), (iii) the projection is a live computation ..., (iv) discovery is purely I-address-based ... (LP12 ...)."

**Problem**: The (i)–(iv) enumeration restates four facts each already proven elsewhere in the note; it is recap, not derivation. This is the essay-content-in-a-proof-slot pattern.
**Required**: LP18's proof already establishes resurrection from L12 + LP3★ + the projection definition. Drop the four-point recap (or compress to a single clause), since it adds no inference.

### Issue 4: Operation enumeration omits K.δ Node/Account cases
**ASN-0098, "arrangement-fixing transitions" paragraph**: "Three operations instantiate this template directly — LP6 (Content-Allocation Invariance) at K.α ..., LP7 ... at K.λ, and LP14 ... at K.ρ."

**Problem**: LP8 handles K.δ only in the `Document(e)` case. K.δ in the `Node(e)` and `Account(e)` cases has frame `M' = M` (per ASN-0047's K.δ arrangement frame) and adds no document, so it also fixes every `M(d)` and preserves `dom(Σ.M)` — i.e., it instantiates the template too. The "three operations" phrasing reads as exhaustive of the arrangement-fixing transitions and silently drops two operation cases. A Dijkstra-strict reading of "every operation case covered" finds a hole.
**Required**: Either state that K.δ in the Node/Account cases falls under the same arrangement-fixing template (projection-invariant because `M' = M`), or fold those cases into LP8 alongside the Document case. As written, no LP claim explicitly covers projection behavior under node or account creation.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery, V-order preservation, link-to-link induction, fork-without-transclusion, link-canonical contraction
**Why out of scope**: These are correctly deferred to the Open Questions section as future ASNs. The link-canonical contraction case (where LP12b's content-subspace disjointness argument inverts) is honestly flagged as open rather than hand-waved — appropriate.

VERDICT: REVISE
