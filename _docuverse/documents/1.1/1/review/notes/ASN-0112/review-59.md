# Review of ASN-0112

I checked every derivation against the foundation contracts: the T12 legality argument (D0 at the two divergence cases), V2's two covering cases (D1 round-trip closure; the componentwise TumblerSub/TumblerAdd computation at `zpd = 1`, including the proper-prefix conclusion `reach_d < r⋆` via T1 case (ii)), V3's same-depth tightness (`sig(w) = #w` from S8a via TA5-SIG, so `shift(w,1) = inc(w,0)`), V5's two-step restriction (prefix-pinning and boundary discreteness, including the zero-component sub-cases), V6's witness, V9a's inverse construction (the final-component discriminator `e_{#e} > 0 ⟺ #o ≤ #r` holds in all three depth configurations; recovery of `reach_d` and the decrement to `max O(d)` are correct), V9b's `zpd` case split, V18's case analysis over the editing vocabulary, and all four numeric scenarios (the worked report, the link-drop, the depth-divergent variant, and the golden cases `1.1 for 0.11` and `2.1 for 0.1`). All check out. Two issues remain, one coverage gap and one anti-bloat finding.

## REVISE

### Issue 1: The `m_C < m_L` configuration — the only non-level-uniform regime — is claimed but never instantiated

**ASN-0112, "A worked report" / V-LevelUniform / V9a**: "σ_d is level-uniform … strictly non-level-uniform when `m_C < m_L`"; "**An endpoint-depth-divergent variant (one line).** When `m_C = 3 > m_L = 2`: …"

**Problem**: The worked examples cover three of the four (Tight, LevelUniform) quadrants: equal-depth cross-subspace (tight, level-uniform), single-subspace (tight, level-uniform), and `m_C > m_L` (overshooting reach, level-uniform). The fourth quadrant, `m_C < m_L`, is the unique configuration where the returned span is **not** level-uniform (`#origin_d < #extent_d`) yet the reach **is** tight — the regime in which V-ReachTight and V-LevelUniform visibly decouple. It is reachable (ValidFirstLinkPosition permits any link depth `m ≥ 2` independent of `m_C`), and it is also the only configuration exercising V9a's case-1 recovery (`r = o ⊕ e` via D1) with strictly unequal endpoint depths — the case where the cross-subspace round trip closes through zero-padded subtraction (`e.g.` `o = [1,1]`, `max O(d) = [2,1,1]`, `r = [2,1,2]`, `e = [1,1,2]`: round trip closes, `e₁ = 1` flags the bounding box, `e₃ = 2 > 0` flags tightness, `#o = 2 ≠ 3 = #e` breaks S6). Both depth-divergence claims are recorded in the claims table, but only one direction is demonstrated; the variant section works `m_C > m_L` and stops.

**Required**: Add a one-line `m_C < m_L` variant mirroring the existing one, verifying that the round trip closes (`r⋆ = reach_d`, V-ReachTight affirmative), that the span is strictly non-level-uniform (V-LevelUniform's negative branch), and that both V9a/V9b width discriminators read correctly off the result.

### Issue 2: Defensive discharge framing and intra-paragraph restatement around the occupied-depth definition (anti-bloat)

**ASN-0112, "Exact cover within a subspace; a bounding box across subspaces"**: "The definition and the proof meet exactly: in the single-subspace case the sole non-empty subspace is `s`, so the only occupied depth is `m_s`, and steps (i)–(ii) dispose of every depth-`m_s` tumbler in `⟦σ_d⟧` — V5 is discharged in full under the definition." And, in the V6 paragraph: "V6 is existential, so this single depth-`m_C` witness discharges it under the definition; whether depth-`m_L` tumblers supply further witnesses when `m_L ≠ m_C` is immaterial. … `Exact` is depth-scoped and `⊊` is not; only the occupied-depth witness separates V6 from V5."

**Problem**: This is residue of the occupied-depth-tightening cycle. Each passage contains one load-bearing clause (V5: in the single-subspace case the only occupied depth is `m_s`; V6: the claim is existential, so one witness suffices) wrapped in meta-assertions that the proof satisfies the definition ("the definition and the proof meet exactly," "discharged in full under the definition," "discharges it under the definition") — prose addressed to the reviewer, not the reader. Additionally, the V6 paragraph's closing sentence ("`Exact` is depth-scoped and `⊊` is not; only the occupied-depth witness separates V6 from V5") restates what the immediately preceding two sentences just established via the `origin_d.0` corollary discussion — the same point twice in different words within one paragraph.

**Required**: Keep the two load-bearing clauses as plain proof steps (the single-subspace instantiation of occupied-depth in V5; the one-witness sufficiency note in V6); delete the "discharged under the definition" framing in both places and the duplicate closing sentence of the V6 paragraph. The `origin_d.0` observation itself should stay — it is what justifies the depth-scoped definition.

## OUT_OF_SCOPE

### Topic 1: Cross-operation contract for the returned span
Whether `σ_d` is a legal and meaningful *input* to span-consuming operations — in particular whether feeding the cross-subspace bounding box to a content retrieval over-delivers, given V6's covered-but-unoccupied positions — is a coherence obligation between this query and the retrieval vocabulary.
**Why out of scope**: Content delivery (RETRIEVEV) is explicitly excluded; the contract belongs to the consuming operation's ASN, not to this boundary query.

### Topic 2: Exact reporting for multi-subspace documents
V6 establishes that a single span cannot exactly trace a two-subspace arrangement; the natural remedy is a per-subspace span-set report.
**Why out of scope**: That is the explicitly excluded RETRIEVEDOCVSPANSET territory; this ASN correctly stops at proving the single-span limitation rather than claiming the remedy.

VERDICT: REVISE
