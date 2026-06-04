# Review of ASN-0087

## REVISE

### Issue 1: "What Does Not Change" section is residual prose duplicating M-Frame
**ASN-0087, "What Does Not Change"**: "The frame `Σ'.C = Σ.C` holds (Effect; M-Frame): the referenced content is byte-identical before and after MAKELINK. The substantive point is that the link's endsets *reference* I-addresses in `dom(C)`, but referencing is read-only..."
**Problem**: M-Frame already carries the full statement, including the parenthetical "(referencing is read-only)." The prior cycle merged M-NoContentEffect into M-Frame; this standalone section is that content relocated rather than removed. It restates the claim and re-derives the read-only rationale without advancing any new reasoning — the reader must skip it to reach "Side Effects."
**Required**: Delete the section; M-Frame and the Effect frame clause `Σ'.C = Σ.C` already discharge it. If the read-only rationale is worth keeping, it lives in M-Frame, not in a dedicated section.

### Issue 2: M-DepthConv trailing sentence is a redundant restatement
**ASN-0087, Inputs (M-DepthConv)**: "Once it has done so, S8-depth (ASN-0047) pins `m_L(d) = 2` for all later link V-positions of that document... For any document `d` whose link V-positions were all placed by MAKELINK, `m_L(d) = 2`."
**Problem**: The final sentence re-asserts the consequence the preceding sentence already established (S8-depth pinning `m_L(d) = 2`). It adds no new content and pads the convention's definition.
**Required**: Drop the trailing sentence; the S8-depth pinning statement is sufficient.

### Issue 3: Two sections with near-identical names ("Permanence of the Recording" / "Permanence")
**ASN-0087, "Permanence"**: "*Permanence of the Recording* established that the link's identity and value are permanent (M-Perm). Taking that as given, what remains to characterize is the V-position binding..."
**Problem**: The two sections cover distinct facts (value immutability vs. binding mutable-only-by-removal), but the colliding titles force the reader to disambiguate by content. The opening sentence of "Permanence" exists only to re-orient the reader past that collision.
**Required**: Rename for distinctness (e.g., "Permanence of the Binding" for the second), letting the section lead with its own content instead of a back-reference.

## OUT_OF_SCOPE

### Topic 1: Type-slot-only discoverability semantics
LP12 treats all slots uniformly, so a link with `e₁ = e₂ = ∅` could be discoverable solely via its type endset's coverage. The worked example notes the type slot does not contribute *in that state* but the note never addresses whether type-slot-only discoverability is meaningful.
**Why out of scope**: Already captured by the open question on type endsets referencing never-allocated addresses; it is a semantics question for a future ASN, not an error here.

META: not applicable — the ASN defines an operation on state (the `K.λ ; K.μ⁺_L` composite) with abstract preconditions, effect, and invariant obligations, squarely within specification territory.

VERDICT: REVISE
