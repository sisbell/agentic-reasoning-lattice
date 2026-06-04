# Review of ASN-0091

This is a rigorous note and I found no correctness defect: the RA-* class is well-formed, the RE-* derivations are sound, every worked-example arithmetic checks (fragmentation/coalescence/equality witnesses, the S5 collapse-case witness `M'(d)=M(d)` with π≠id, the LP-Fin coverage computations), boundary cases (empty document, identity π, empty `V_S(d)` via R-PRE) are handled, and all cross-ASN references resolve to foundation ASNs. It is not drifting into implementation mechanics — so no META.

The note carries `review-mode.anti-bloat`, and the residual findings are accreted meta-prose, not math.

## REVISE

### Issue 1: RA-frame table cell enumerates downstream consumers
**ASN-0091, Clause Correspondences (RA-frame row)**: "`L' = L`, `E' = E`, `R' = R` are the sources of RE-L, RE-sub's frame, and RE-R"
**Problem**: A definition-mapping cell that should state what RA-frame fixes instead inventories which downstream claims consume each conjunct. This is a use-site inventory; the consumers are already named where they are derived.
**Required**: Delete the "are the sources of …" clause; the conjuncts stand on their own.

### Issue 2: RA-adm scope carve-out is axiom rationale, stated twice
**ASN-0091, abstract definition and Claims table (RA-adm row)**: "every per-state foundation invariant satisfied by Σ is satisfied by Σ' (composite-boundary properties P4★/P4a/P7a and state-independent theorems S5, T0(a/b) lie outside its scope, discharged by their own arguments)"
**Problem**: The parenthetical explains what the admissibility clause does *not* cover and why — rationale rather than statement — and the same scope carve-out appears both in the prose definition and restated in the Claims table. New prose around an axiom explaining its boundary is exactly the accretion pattern.
**Required**: State RA-adm once as what it asserts; drop the "lie outside its scope, discharged by their own arguments" gloss (the composite-boundary discharges are already located in the Worked Example).

### Issue 3: RE-eq witnessed three times with explicit re-surfacing of the degenerate case
**ASN-0091, "Run Decomposition Is Not Invariant"**: "Two further RE-eq witnesses sit at the boundary of this construction. The empty case … trivially satisfies RE-eq at cardinality 0; we display the non-degenerate equality witness here at cardinality 2 …" — and again in the non-uniqueness example: "this trace also serves as a richer RE-eq witness than the two-singleton case"
**Problem**: RE-eq is exhibited at the equality-witness paragraph, then re-asserted for the empty case (already covered by the abstract empty-case paragraph), then re-witnessed in the fourth worked example. Multiple paragraphs reasserting the same triviality.
**Required**: Keep one RE-eq witness; drop the "two further RE-eq witnesses" sentence and the empty-case re-mention (the abstract empty case already discharges cardinality 0).

### Issue 4: Repeated deferral to "the layers below"
**ASN-0091, Clause Correspondences table**: clause (i) → "the shape-package layer below, from RA-dom alone"; RA-adm row → "the per-invariant layers below"; plus "the subspace-preservation layer," "Remaining per-state invariants … below"
**Problem**: Several table cells and the surrounding prose defer to the same three discharge layers stated immediately afterward. The forward pointers add no content over the layers they point at.
**Required**: Since the discharge layers immediately follow the table, replace the per-row "below" pointers with the discharge inline or a single lead-in sentence.

### Issue 5: Table-column legends are presentation meta-prose
**ASN-0091, "Claims Introduced"**: "The *Provenance* column records each claim's premises: **abstract** = derivable from RA-dom, RA-π, RA-frame, RA-adm alone …; **REARRANGE_K** = requires ASN-0084's cut-sequence specifics …; **structural** = state-independent." (and the analogous ★-table preamble)
**Problem**: Prose explaining the table's own columns. The labels are self-evident from the entries; the legend restates them.
**Required**: Compress to a one-line header or drop; if a legend is needed, a single clause suffices, not a per-value gloss for both tables.

### Issue 6: Defensive justification of a proof approach not taken
**ASN-0091, ChainDisjointAdjacency inline lemma**: "Domain disjointness is established without appeal to any prefix-positional disagreement, so the conclusion holds uniformly across all length cases — including those where one document tumbler is a proper prefix of the other (e.g., `d_X = [1, 0, 1, 0, 1]` and `d_Y = [1, 0, 1, 0, 1, 1, 1]` …), where a disagreement-in-prefix argument would fail."
**Problem**: The concrete prefix-nesting example is fine, but the framing defends the lemma against an *alternative rejected proof* ("a disagreement-in-prefix argument would fail"). Justifying why a method not used would have failed is meta-prose.
**Required**: Keep the lemma's actual argument (disjointness via T10a.6); drop the "where a disagreement-in-prefix argument would fail" defense.

### Issue 7: Duplicated "two conjuncts mutually reinforcing" paragraph
**ASN-0091, RE-sub and RE-ext sections**: RE-sub — "The two conjuncts are mutually reinforcing under RA-π: substituting `π(v) = v` into … gives `Σ'.M(d)(v) = Σ.M(d)(v)`, so the first conjunct alone … implies the second, which R-FRAME-P/S(a) records independently." RE-ext — "As with RE-sub, the first conjunct `π(v) = v` … implies the second under RA-π, which R-EXT records independently."
**Problem**: The same structural observation is stated in both sections. The RE-ext copy adds nothing beyond "As with RE-sub."
**Required**: State the conjunct-implication once (at RE-sub) and let RE-ext inherit it without restatement.

## OUT_OF_SCOPE

(none — the note's own Open Questions already route link-subspace rearrangement semantics, fragment reconstitution, and the run-cardinality upper bound to future ASNs.)

VERDICT: REVISE
