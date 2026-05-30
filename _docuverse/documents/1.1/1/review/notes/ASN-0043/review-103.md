# Review of ASN-0043

## REVISE

### Issue 1: Contradictory characterization of the faceted link

**ASN-0043, "The Endset Structure" vs. "Reflexive Addressing" (L13)**:

- The Endset Structure: "A faceted link relating content across more than three roles **need not be decomposed into chains of ternary links**; it can be **expressed directly as a single link** with the required number of endsets."
- L13: "A faceted link — one that relates multiple distinct groups of spans in more than three roles — **is built from a chain of links**, each contributing its three endset slots, with link-to-link references providing the composition glue."

**Problem**: These two passages describe the *same* construct ("more than three roles") with directly opposed structures. One says a faceted link is a single higher-arity link that need not be decomposed; the other says it *is* a chain of three-endset links glued by link-to-link references. A reader cannot tell which is the model's position. This is reviser drift: the higher-arity-single-link claim was added in one section while the older cons-cell/chain reading survived in L13.
**Required**: Pick one normative account. If higher-arity single links are the model's mechanism (consistent with L3/L6/the arity-4 worked example `a₃`), revise L13's prose so the faceted link is presented as either decomposition-by-choice or as a single N-ary link — not asserted to be chain-built. Keep Nelson's quote as historical evidence, not as the model's structural commitment.

### Issue 2: "Standard triple is the floor / higher arity admitted" restated three to four times

**ASN-0043, "The Endset Structure" (twice), "Convention — StandardTriple", and L3 prose**: e.g. "The standard triple — from, to, type — is the design floor"; "higher-arity links are admitted directly"; "The standard triple is the dominant case — but it is a convention, not a structural limit"; "The design commitment: every link carries the standard triple (from, to, type) as its floor, with higher arity admitted...".
**Problem**: The same proposition — three endsets are the floor, slot 3 is type, higher arity is permitted — is asserted in four places with no added content between restatements. Under the anti-bloat classifier this is "two paragraphs say the same thing in different words." The precise reader must confirm each restatement carries nothing new.
**Required**: State the floor/convention once (the StandardTriple convention is the natural site), let L3 carry the formal invariant, and delete the prose duplicates in the surrounding exposition.

### Issue 3: L9 re-derives the empty-slot padding soundness that FSP already guarantees

**ASN-0043, L9, "Define Σ' as ..." paragraph**: "padding with empty endsets at slots `4..N` is sound: each `∅ ∈ Endset`..., empty slots `4..N` are admissible (FSP's L3 case), and the conformance verification below operates uniformly on the type endset (slot 3) and the address `a`, so adding empty endsets at slots `4..N` preserves every state-local invariant established for the arity-3 witness."
**Problem**: FSP is already parametric in the payload `ℓ = (e₁,...,e_N)` with `N ≥ 3`, each `eᵢ ∈ Endset`, `e₃ ≠ ∅`, and explicitly notes "the non-emptiness conjunct constrains slot 3 alone, so empty slots `4..N` are admissible." This paragraph manually re-argues invariant preservation under empty padding — exactly FSP's job — before FSP is invoked. The subsequent "*Application to L9*" paragraph then states the same padding facts a second time ("each `∅ ∈ Endset` and the single span is T12-well-formed... slot 3 is non-empty, so `ℓ` satisfies FSP's payload hypothesis").
**Required**: Drop the inline soundness re-derivation; construct the padded payload, cite FSP's payload hypothesis once, and apply FSP.

## OUT_OF_SCOPE

### Topic 1: Content-side global subspace residence
The pervasive `s_C`-resident hypothesis (L0a, L9, L11b, L14a) means the disjointness and dual-primitive guarantees are scoped to the `s_C` slice, not all of `dom(Σ.C)`. This is transparently flagged in Open Questions #1 and belongs to a future content-side invariant, not a defect of this ASN.

META: not applicable — the ASN defines state (`Σ.L`), invariants on it, and abstract guarantees, so it remains in specification territory.

VERDICT: REVISE
