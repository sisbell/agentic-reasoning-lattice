# Review of ASN-0082

## REVISE

### Issue 1: `#v = #r` attributed to `v ≥ r` rather than S8-depth

**ASN-0082, Lemma — OrdinalExceedsDisplacement (preconditions)**: "For any V-position v with `subspace(v) = 1` and `v ≥ r` (so that `#v = #r` and OrdinalOrderEquivalence applies, giving `ord(v) ≥ ord(r)`)"

**Problem**: The parenthetical presents `#v = #r` as a consequence of `v ≥ r`. The T1 order does not constrain length — `v ≥ r` is fully compatible with `#v ≠ #r`. The equal-length fact is what licenses OrdinalOrderEquivalence (whose precondition is `#v₁ = #v₂`), so it cannot itself rest on the very comparison it is needed to translate. The actual source is S8-depth (both are subspace-1 V-positions of a document, depth fixed at `#p = 2` by the depth axiom).

**Required**: Cite S8-depth (with the `#p = 2` depth axiom) as the source of `#v = #r`, matching the per-step citation convention the foundation enforces. Do not let the inference ride on `v ≥ r`.

### Issue 2: Reciprocal forward/back pointers and "single home" meta-prose around σ(v) well-definedness

**ASN-0082, D-SHIFT (postconditions) and S8a-post (proof)**: D-SHIFT says "both discharged by the S8a-post lemma (below; its Q₃ case proves exactly this from OrdinalExceedsDisplacement (ii), (iii) and vpos's S8a-closure postcondition)." S8a-post then says "Positions in Q₃: this is the single home for the well-definedness and S8a-satisfaction of σ(v) … that the assignment `M'(d)(σ(v)) := M(d)(v)` (D-SHIFT) requires."

**Problem**: This is forward-reference accretion: D-SHIFT defers to S8a-post with a use-site inventory of the premises that proof will use, and S8a-post answers with a "this is the single home for … that D-SHIFT requires" back-pointer. The reader bounces between the two slots to assemble a single fact (σ(v) ∈ T and σ(v) ⊨ S8a). The premise inventory in D-SHIFT and the "single home" framing in S8a-post advance no reasoning.

**Required**: State σ(v)'s well-definedness and S8a-satisfaction once, at the point it is first needed, citing OrdinalExceedsDisplacement (ii)/(iii) and vpos S8a-closure directly. Drop the "single home" framing and the downstream-requirement inventory.

### Issue 3: D-DOM synthesis paragraph restates its own clauses

**ASN-0082, paragraph following D-DOM**: "Combined with D-L and D-SHIFT, this fully characterizes M'(d) within subspace S: positions in L retain their original I-address mappings, positions in Q₃ hold shifted mappings from R, and no other subspace-S positions exist in dom(M'(d)) — D-DOM pins dom(M'(d)) ∩ subspace 1 from above to exactly L ∪ Q₃."

**Problem**: Every clause here is a re-statement of D-SHIFT, D-L, and D-DOM in different words — the closing sentence re-asserts D-DOM verbatim ("= L ∪ Q₃"). Two slots saying the same thing. (The identical pattern appears for insertion: the "domain closure clauses … pin dom(M'(d)) from above" paragraph after I3-CX repeats I3-CS/I3-CX.)

**Required**: Remove the synthesis paragraph (and its insertion-side twin) or reduce to the one new fact it carries, if any.

## OUT_OF_SCOPE

### Topic 1: Full INSERT must restore the contiguity invariants the shift sub-operation breaks

The ASN correctly notes ("Arrangement invariants not preserved") that the text-subspace shift sub-operation produces an M'(d) that violates the foundation invariants D-CTG, D-SEQ, and (when p = min) D-MIN, leaving an n-position gap. Because these are foundation *invariants* meant to hold in every committed state, the obligation to re-establish them — by the content-placement step that fills the gap — must be discharged by the full INSERT operation.

**Why out of scope**: This ASN scopes itself to the shift sub-operation only; the gap-filling step and its invariant restoration are a distinct operation, not an error in the shift characterization.

### Topic 2: Contraction restricted to depth-2 V-positions

The contraction half is restricted by the depth axiom `#p = 2` (single-component ordinals), because TA4's zero-prefix precondition is only dischargeable at ordinal depth 1. Insertion, needing no subtraction, is stated for general `m ≥ 2`.

**Why out of scope**: The depth->1 generalization (and the weaker inverse law it would require) is already named in the Open Questions; it is new territory, not a defect of the depth-2 result.

VERDICT: REVISE
