# Review of ASN-0099

## REVISE

### Issue 1: Filtered-form content placed in the Match Predicate section, before the filtered form is defined
**ASN-0099, "The Match Predicate" (paragraph "Empty endsets at non-type slots")**: "In the filtered form (below), a filter constraint `(i, J)` is unsatisfiable at `a` when `i > |Σ.L(a)|` (the slot is absent) or `Σ.L(a).eᵢ = ∅` (the slot carries no spans)."
**Problem**: This sentence discusses `findlinks_filtered`, which is not introduced until the next section ("Endset Filtering"). It is content sitting in the wrong structural slot, forcing the reader to forward-reference a definition that does not yet exist. The unfiltered half of the same paragraph belongs here; the filtered half does not.
**Required**: Move the filtered-form sentence into the "Endset Filtering" section, where `(i, J)` and the out-of-range guard are defined. Keep only the unfiltered observation in the Match Predicate section.

### Issue 2: Forward-pointer meta-prose advertising F4
**ASN-0099, "The Match Predicate" (after F1)**: "The choice of intersection over either containment direction is individuated by F4 below (Strengthening 1 and Strengthening 2), with explicit witnesses."
**Problem**: This sentence advances no reasoning — it announces that downstream work (F4) will justify the design. F4 stands on its own and carries the witnesses; the announcement is signposting noise the reader must skip past. The actual content of the surrounding paragraph (existential-over-slots, per-span overlap, identifiable witness) is substantive; this trailing pointer is not.
**Required**: Delete the sentence. F4's individuation does the work where it lives.

### Issue 3: The unfiltered-as-union-of-single-slot-filters identity is stated without derivation
**ASN-0099, "Endset Filtering"**: "`findlinks(I, Σ) = ⋃_{i=1}^{N} findlinks_filtered({(i, I)}, Σ)` where `N = max{|Σ.L(a)| : a ∈ dom(Σ.L)}` ..."
**Problem**: This is an asserted set identity with no proof. The non-trivial step is that bounding `i` by the global maximum arity `N` rather than the per-link arity `|Σ.L(a)|` is harmless — it holds only because each single-slot filter carries its own guard `i ≤ |Σ.L(a)|`, so for any fixed `a` the union over `1..N` collapses to the existential over `1..|Σ.L(a)|`. The ASN elsewhere insists derived guarantees name premises and show the chain (standard 6); this identity is given the same illustrative weight as F13/F20a, which do show their steps.
**Required**: Either supply the one-line per-link derivation (guard collapses `1..N` to `1..|Σ.L(a)|`), or mark the line explicitly as an illustrative restatement rather than a load-bearing identity.

## OUT_OF_SCOPE

### Topic 1: Combined filtered-and-scoped operation `findlinks_filtered_scoped(C, S, Σ)`
**Why out of scope**: The ASN already lists this in "What We Have Not Specified." It is genuinely new territory (a fourth surface form), not a gap in the present definitions, and the scoping/filtering machinery here would compose into it cleanly in a later note.

VERDICT: REVISE
