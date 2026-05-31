# Review of ASN-0043

## REVISE

### Issue 1: DocVal introduced mid-proof with a use-site inventory
**ASN-0043, L9 ("Selection of d'")**: "We record the fact used at several sites below:\n\n**DocVal (document T4-validity).** Every `d ∈ dom(Σ.M)` is T4-valid: by S7d it is the terminus of a T10a-conforming allocator chain from 𝒯's root ... and T10a.4 ... propagates T4-validity along each chain step."
**Problem**: "the fact used at several sites below" is a use-site inventory — the introduction advertises downstream consumers (L11a's "T4-valid by DocVal, above"; the worked example's S7d check) rather than advancing the local argument. A general fact about every document in `dom(Σ.M)` is buried inside the L9 witness proof, then back-referenced from L11a, which forces the reader to hunt for it outside the section that actually needs it as a standing fact.
**Required**: State the document-T4-validity fact once as a standalone named consequence of S7d + T10a.4 near L1c (or L11a, where it is structurally load-bearing), and drop the "used at several sites below" inventory. Cite it where used without the forward advertisement.

### Issue 2: Summary opens with self-referential document-structure meta-prose
**ASN-0043, "Summary of the Link Model"**: "A link is an addressed, owned, typed, bidirectional connection between arbitrary spans of content in the tumbler space. **The synthesizing observations the Properties Introduced table does not carry:** the address *is* the link's identity, and home is determined by that address alone..."
**Problem**: The clause "the synthesizing observations the Properties Introduced table does not carry" describes the document's own layout (what the table does and doesn't contain) rather than the system being specified. This is essay content about the note's structure occupying the summary slot.
**Required**: State the synthesis directly (address-is-identity; home fixed by address; type matched by coverage not dereference) without narrating which table row does or does not carry it.

### Issue 3: Worked-example deferral scaffolding accumulates
**ASN-0043, Worked Example (state Σ checks)**: e.g. L5 — "it is exercised non-vacuously at Step 5 below"; L11b — "The extension `Σ'` witnessing the existential is constructed in Step 1 below"; L12/L12a — "discharged uniformly across the six `Σ_i → Σ_{i+1}` transitions"; and the recap "Together, Steps 4 and 6 exercise L8 in both discriminating directions."
**Problem**: Several Σ-level verification entries do no work at Σ and instead announce where the real check lives, and the closing recap re-states what Steps 4/6 already demonstrated. The reader threads navigation prose between the substantive checks.
**Required**: For invariants whose only non-trivial witness is in the Extension, either move the entry to the step that exercises it (with a one-clause note that Σ satisfies it vacuously/trivially) or drop the forward announcement; remove the recap sentence, which duplicates the per-step conclusions.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace constant
The repetition of the hypothesis `(A b ∈ dom(Σ.C) :: subspace_I(b) = s_C)` across L9, L11b, L14a is forced by the absence of a content-side invariant fixing a global `s_C`. This is already the first Open Question and belongs to a content-model revision, not this ASN.

META: not applicable — the ASN defines link state, its invariants, and their interaction with ASN-0036's content/arrangement state, abstractly enough to bind any implementation; it has not drifted into implementation mechanics.

VERDICT: REVISE
