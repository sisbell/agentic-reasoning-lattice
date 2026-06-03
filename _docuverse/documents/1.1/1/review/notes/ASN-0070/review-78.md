# Review of ASN-0070

The mathematics is rigorous: F-canonical's existence/uniqueness proof (Steps 0–5) covers the vacuous subspace, the infinitude argument for non-terminal action points, the consecutivity characterisation with both directions, and the inter-component left/right closure. The six worked configurations exercise the full edge-case matrix (empty, cross-subspace straddle, interior clip, vacuous subspace, multiplicity, multi-doc, state-dependence). I found no correctness or missing-case defects. The findings below are the anti-bloat patterns the note's classifier flags.

## REVISE

### Issue 1: "Frame" slots in F-persist and F-state carry commentary, not frame conditions
**ASN-0070, F-persist / F-state**: 
F-persist — "Frame. The persistence is a property of Σ.L across transitions, observed via follow."
F-state — "Frame. The variation observed here is in M(d) across the transition Σ → Σ'."
**Problem**: `follow` is a pure query (`Σ' = Σ`, fixed in F1), so a per-lemma Frame slot has no object-level frame condition to state. Both entries are descriptive commentary occupying a structural slot — essay content in the wrong place. The eight other derived properties (F-sound, F-complete, F-empty, F-det, F-multi, F-slot, F-origin, F-contig, F-multidoc) correctly omit a Frame slot. Worse, F-state's Frame restates its own postcondition, which already says "The difference, when present, originates entirely in M_Σ(d) ≠ M_{Σ'}(d)."
**Required**: Delete both Frame slots; the transition context is already carried by each lemma's Preconditions and Postcondition.

### Issue 2: The "an empty component arises two ways" point is stated three times
**ASN-0070, Configuration 6 + F-empty**:
- Config 6, Vacuous-subspace bullet: "This is distinct from Configuration 1's Σ_V^{s_L} = ⟨⟩, which arose from a populated link subspace (β_L present) that coverage simply failed to reach."
- Config 6, F-multidoc bullet: "The two empty s_L-components arise differently: in d from a populated link subspace coverage misses, in d' from a vacuous one by convention."
- F-empty derivation parenthetical: "(An empty component can arise two ways — a vacuous subspace where m_S(d) is undefined, or a populated subspace whose coverage missed all link material — but F-canonical's uniqueness covers both alike.)"
**Problem**: The vacuous-vs-populated distinction for an empty component is restated twice within Configuration 6 alone (two bullets), then a third time in F-empty. Two paragraphs in the same configuration saying the same thing in different words is the redundancy the anti-bloat pass targets.
**Required**: State the distinction once. The Config 6 Vacuous-subspace bullet is the natural home; drop the duplicate restatement from the F-multidoc bullet, and trim the F-empty parenthetical to the load-bearing claim ("F-canonical's uniqueness covers the empty case regardless of cause").

### Issue 3: F-canonical Step 0 re-derives the vacuous emptiness already established in the convention
**ASN-0070, V-Restricted Denotation (Vacuous-subspace convention) and F-canonical Step 0**: The convention paragraph already argues "no V-position in subspace S exists in dom(M(d)); hence R(d, e)|_S = ∅ unconditionally." Step 0 re-proves the identical `R(d, e)|_S ⊆ V_S(d) = ∅` chain.
**Problem**: The unconditional-emptiness derivation appears in full twice. Step 0 needs only to discharge the proof obligation by citation, not re-walk the inclusion.
**Required**: Have Step 0 cite the Vacuous-subspace convention for `R(d, e)|_S = ∅` and proceed directly to the existence/uniqueness of `⟨⟩` as sole representative.

## OUT_OF_SCOPE

The two Open Questions (multi-home transclusion relationships across documents; cross-server BEBE consistency) are correctly deferred and not flagged.

VERDICT: REVISE
