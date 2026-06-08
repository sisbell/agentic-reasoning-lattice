# Review of ASN-0112

## REVISE

### Issue 1: The reach biconditional is derived four times in four locations
**ASN-0112, V2 / V6 / V17 / Preconditions (wp)**: the fact `reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d` is established and re-explained in:
- V2: "`reach(σ_d) = reach_d ⟺ #origin_d ≤ #reach_d` (D1 closes the round-trip when `#origin_d ≤ #reach_d`; D0 makes it fail when `#origin_d > #reach_d`)";
- V6: "by the V2 case analysis, `reach(σ_d) = reach_d` exactly when `#origin_d ≤ #reach_d`";
- V17: "the endpoint condition `#origin_d ≤ #reach_d` governs only `reach(σ_d) = reach_d`";
- wp section: "`wp(RETRIEVEDOCVSPAN(d), "reach(σ_d) = reach_d") = (#origin_d ≤ #reach_d)`".

**Problem**: One biconditional, four derivations. V6, V17, and the wp restatement add no new reasoning over V2 — they are the same fact reasserted with back-references. This is the "two paragraphs say the same thing in different words" pattern, compounded.
**Required**: Establish the biconditional once (in V2's covering proof, where D0/D1 live) and cite it by claim label elsewhere instead of re-deriving it.

### Issue 2: Repeated deferral to "the substrate distinction"
**ASN-0112, substrate section + V2 + V6 + V17 + worked example**: the level-uniform vs endpoint-level-compatible distinction is set up in the substrate section ("We must keep this notion sharply distinct…the two inequalities point opposite ways and coincide only at equality") and then re-invoked by deferral at least four times: V2 ("the substrate section fixes the two apart"), V6 ("the endpoints are level-compatible and the span level-uniform"), V17 ("per the substrate distinction"), worked example ("the substrate distinction made concrete").
**Problem**: Multiple paragraphs in different sections deferring to the same upstream scaffold is the deferral-accretion pattern. The distinction is genuinely load-bearing (the worked variant proves it matters), but the reader is repeatedly pointed back to the same setup rather than the claim advancing.
**Required**: State the distinction once where it is used (V2), drop the "substrate section fixes…/per the substrate distinction" pointers, and let the worked variant stand as the single concretization.

### Issue 3: Meta-commentary about what the implementation "never exercises"
**ASN-0112, V6**: "The `m_C ≠ m_L` divergence is an abstract possibility S8-depth admits but the implementation never exercises… `m_C = m_L` in every realized state… content and link V-positions are *always* placed at the same depth — both depth 2."
**Problem**: The abstract spec correctly covers the `m_C ≠ m_L` case S8-depth admits; covering it is right. But the prose justifying *why* the case is being covered despite the implementation not realizing it (and the dedicated "endpoint-depth-divergent variant" worked example that exists only to exercise the never-realized case) is rationale about scope, not object-level reasoning. The worked variant duplicates V2's case-(ii) arithmetic already proved abstractly.
**Required**: Keep the abstract `m_C ≠ m_L` handling in V2/V6; drop the "implementation never exercises it" commentary and fold the divergent worked variant into a one-line note, since its arithmetic adds nothing beyond V2's second covering case.

### Issue 4: V8↔V18 mutual cross-referencing
**ASN-0112, V8 and V18**: V8 contains "the one editing transition that does move the origin; we derive it as V18 below" (stated twice in the section), and V18 closes with "exactly the boundary V8 excludes." 
**Problem**: A forward pointer ("we derive it as V18 below") paired with a back pointer ("the boundary V8 excludes") is bidirectional deferral that adds no content — V8's scope (content present) and V18's content-clearance case are adjacent and self-evident from their preconditions.
**Required**: State V8 with its precondition ("while content present") and let V18 carry the clearance case without the cross-pointing prose.

### Issue 5: The "empty ≠ zero-extent span" argument appears in both V0 and V11
**ASN-0112, V0 and V11**: V0 argues "`⟨⟩` cannot be a degenerate span, because no T12 span can denote `∅` (S2, ASN-0053)." V11 re-argues the same point at length: "this is *not* the 'zero-extent span'. A T12 span `(s, ℓ)` requires `Pos(ℓ)`… by TA6… excluded from valid addresses entirely."
**Problem**: The same distinction (empty result is not a zero-width span) is justified twice with overlapping foundation citations.
**Required**: Make the type-level point once in V0; in V11 state only the operational consequence (empty document ⟶ `⟨⟩`, undefined origin) without re-deriving the non-degeneracy.

## OUT_OF_SCOPE

(none — the ASN stays within whole-document span boundary reporting; per-subspace recovery is correctly relegated to an open question rather than a claim.)

VERDICT: REVISE
