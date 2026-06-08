# Review of ASN-0102

## REVISE

### Issue 1: "The cardinal question" section is meta-prose duplicating the intro and X1

**ASN-0102, "## The cardinal question"**: "COPY touches only the arrangement; it allocates no fresh I-address and adds nothing to dom(Σ.C) — placing existing content and creating new content are different acts over the same address machinery."

**Problem**: This whole section is a heading-slot holding a single sentence that restates the opening paragraph ("Placement here is by reference, not duplication: COPY allocates no content (X1), and this single fact dictates what the operation may and may not do") and pre-states X1. Three loci now assert "COPY allocates no content" before X1 establishes it — the anti-bloat pattern of two passages saying the same thing in different words, with essay framing occupying a structural slot.

**Required**: Delete the "The cardinal question" section; the claim is carried by X1 and the intro already states the motivating fact once.

### Issue 2: X16's S2 discharge claims "fully discharged" on a tiling that only covers the content subspace

**ASN-0102, X16 (PostStateDensity)**: "the copied, displaced, and unmoved classes occupying pairwise-disjoint V-positions (the tiling above), the post-state arrangement Σ'.M(d) is a well-defined partial function — S2 (functionality) is fully discharged for the post-state."

**Problem**: The "unmoved" class is defined (in the effect clause's first bullet) to include every `subspace(u) ≠ s_C` position — i.e. the link-subspace positions. The tiling argument reasons purely about last-component ranges `[1,p) ∪ [p,p+W) ∪ [p+W, n_S+W]` of `s_C`-positions; it says nothing about `s_L` positions. Disjointness of the modified `s_C` positions from the unmoved `s_L` positions follows from first-component (subspace-identifier) distinctness (T7), not from the tiling. The proof's awareness of this elsewhere (the X3/wp(S3★) discussion explicitly notes the `s_L` conjunct) makes the omission here a genuine looseness in a clause that claims S2 is "fully discharged."

**Required**: Add one clause noting that `s_L`-subspace unmoved positions are disjoint from all `s_C` positions by subspace-identifier distinctness (T7), so the tiling (which establishes disjointness within `s_C`) together with subspace separation yields full pairwise disjointness.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
