# Review of ASN-0102

## REVISE

### Issue 1: Citation of a non-existent sub-clause `OrdShiftHom (c)`
**ASN-0102, X16**: "shift preserves S8a unconditionally and preserves depth (`#shift(u, W) = #u = m`, OrdShiftHom (c))"
**Problem**: OrdShiftHom (OrdinalShiftPreservation, ASN-0036) has only parts (a) (subspace preservation) and (b) (S8a preservation). It has no part (c), and it makes no claim about tumbler depth. Depth preservation `#shift(v, n) = #v` is a postcondition of **OrdinalShift (ASN-0034)**, not of OrdShiftHom.
**Required**: Cite OrdinalShift (ASN-0034) for `#shift(u, W) = #u`. Remove the "(c)" reference.

### Issue 2: OrdShiftHom over-cited for intermediate-component fixity
**ASN-0102, X16**: "The shift `· + W` on subspace `s_C` increments only the last component (it is the ordinal shift `δ(W, m)`, OrdShiftHom, leaving the subspace identifier and the intermediate `1`-components fixed)."
**Problem**: OrdShiftHom (a) establishes only that the *subspace* (first component) is preserved. The claim that *all* intermediate components `2..m−1` are left fixed and only the last component is incremented is the content of OrdinalShift (ASN-0034) (`shift(v,n)ᵢ = vᵢ` for `i < m`, `shift(v,n)ₘ = vₘ + n`), not of OrdShiftHom.
**Required**: Attribute the "increments only the last component, intermediate components fixed" claim to OrdinalShift (ASN-0034). OrdShiftHom may be cited only for subspace and S8a preservation.

### Issue 3: Faulty justification in X8 — "maximally-merged ⟹ pairwise non-I-adjacent"
**ASN-0102, X8**: "`resolve(d_s, σ)` already returns the maximally-merged decomposition (ASN-0058, C1a/M12), so its blocks are pairwise non-I-adjacent. The merge condition M7 requires *both* V- and I-adjacency, so non-I-adjacency alone forecloses it"
**Problem**: Maximally-merged (M12/MaximallyMerged, ASN-0058) forbids only pairs that are *both* V- and I-adjacent; it does not give *pairwise* non-I-adjacency. Two non-consecutive blocks of the decomposition may be I-adjacent without being V-adjacent and still sit in the maximally-merged form. The stated reason is therefore wrong, even though the conclusion (no within-reference merge) is correct.
**Required**: Either derive the conclusion directly ("maximally-merged ⟹ no two blocks satisfy M7's conjunction, hence no within-reference merge candidate"), or, if the stronger fact is wanted, prove it from V-contiguity of `dom(M(d_s)|⟦σ⟧)` (D-SEQ within the subspace): consecutive blocks are V-adjacent, so maximality forces them non-I-adjacent, while non-consecutive blocks are not V-adjacent. Do not assert "pairwise non-I-adjacent" as a consequence of maximal merging alone.

### Issue 4: Coupling-invariant names diverge from the foundation
**ASN-0102, X14**: "J0 (AllocationRequiresPlacement)" and "J1★ (ExtensionRecordsProvenanceContentSubspace)"
**Problem**: ASN-0047 names these J0 = **AllocationPlacementCoupling** and J1★ = **ExtensionRecordsProvenance**. Renaming a foundation invariant in-place invites confusion about whether a different obligation is meant.
**Required**: Use the foundation's canonical names, or state explicitly that the parenthetical is a descriptive gloss, not the foundation label.

### Issue 5: Provenance pair well-typedness only half-justified
**ASN-0102, PC2 / Definition (Provenance) / X14**: "the pair `(a_j + i, d)` that COPY's effect writes into `Σ.R` is well-typed precisely because `d ∈ E_doc`."
**Problem**: `Σ.R ⊆ T_elem × E_doc` (ASN-0047). The `E_doc` side is justified by PC2, but the `T_elem` side — `Element(a_j + i)` — is not stated. It follows from `a_j + i ∈ dom(C)` (C1) via S7b, but the derivation is left implicit at the point where well-typedness is asserted.
**Required**: State that `Element(a_j + i)` holds via C1 + S7b, so both factors of `T_elem × E_doc` are discharged.

### Issue 6 (anti-bloat): Justificatory K.μ⁺ contrast in the Definition
**ASN-0102, Definition**: "It is deliberately *not* an instance of K.μ⁺ ... What separates them is the *displacement*: K.μ⁺ requires `M'(d)(v) = M(d)(v)` on every pre-existing V-position, whereas COPY *relabels* ... so no extension transition describes it."
**Problem**: This paragraph explains *why COPY is given as its own operation* rather than advancing what COPY does. The operative content — COPY relabels content-subspace positions `≥ v` by `· + W` — is already stated in the effect clause below. The "deliberately not K.μ⁺ / so no extension transition describes it" framing is design rationale of the kind the anti-bloat classifier targets.
**Required**: Trim to the structural fact (COPY is a distinct elementary transition whose effect displaces by `· + W`) and drop the comparative justification, or move it to a one-line note.

## OUT_OF_SCOPE

### Topic 1: Discoverability of copied content after later displacement
**Why out of scope**: The first Open Question (origin vs. continued discoverability under subsequent displacement) concerns interaction with future operations and link-projection (ASN-0098 territory), not the COPY contract itself.

### Topic 2: Time-varying / divergent views of the same content
**Why out of scope**: The third Open Question (references resolving to differing views across time) is new territory about versioning/view semantics, not a gap in COPY's transition definition.

VERDICT: REVISE
