# Review of ASN-0118

The ASN is in strong shape: the composite decomposition is genuinely exhibited (not asserted), the provenance discharge through J0/J1★/J1'★/P4★/P2 is split into branches and each branch is argued, the tiling argument is done from ordinal arithmetic with both the empty and displacing boundary cases covered, the wp analysis is non-trivial, and the worked example checks the claims numerically including the already-referenced provenance branch. The remaining issues are completeness of the frame, one inaccurate gloss, one misattributed citation, and anti-bloat duplication.

## REVISE

### Issue 1: The operation's frame omits Σ.E entirely and bounds Σ'.R from below only
**ASN-0118, "The COPY operation", frame clauses and the CP8 discussion**: "CP8 is a *membership* postcondition…" / "*Frame — link store, other subspaces, other documents.*"
**Problem**: The operation is defined as "the transition Σ → Σ' with the following effect … and with the frame conditions that say what it leaves alone." The listed clauses frame `Σ.C` (CP1), `Σ.L` (CP7a), and the arrangements (CP3b/CP6), but no clause mentions the entity set `Σ.E` at all, and `Σ'.R` is constrained only from below (CP8 gives membership of the `(cᵢ, d)` pairs, never an upper bound). A transition that satisfies every stated clause could add entities to `E` or insert arbitrary spurious pairs into `R`. Both closures *are* derivable from the exhibited composite (no K.δ step; J1'★ limits `R' ∖ R` to range-new pairs of `d`), but the ASN holds itself to a stricter standard elsewhere — CP3c exists precisely so that S2 is "dischargeable from the postconditions alone, not only through the exhibited composite." The same standard, applied to E and R, fails.
**Required**: Add an entity frame (`Σ'.E = Σ.E`) and a provenance closure (`Σ'.R = Σ.R ∪ {(cᵢ, d) : 0 ≤ i < W}`, which subsumes CP8's membership and pins `R' ∖ R` to the range-new pairs) as operation-level clauses, parallel to CP1/CP6/CP7a.

### Issue 2: Claims-table gloss for CP2 calls the placement positions "fresh"
**ASN-0118, Claims Introduced, CP2**: "`W` fresh destination V-positions bind the resolved (pre-existing) I-addresses"
**Problem**: In the displacing case the placement positions `[p, p+W)` are not fresh position names: in the worked example, `[1,2]` is bound to `x₂` in the pre-state and to `a₁` in the post-state. Those positions are vacated by the K.μ⁻ step and re-bound by the K.μ⁺ step; only the *bindings* are new. The body text states this correctly ("bound, in order, to the `W` V-positions starting at `p`"); the table gloss contradicts it, and the table is what gets extracted downstream.
**Required**: Reword the gloss — e.g., "`W` destination V-positions, freshly bound, carry the resolved (pre-existing) I-addresses" — so freshness attaches to the binding, not the position.

### Issue 3: Lockstep within runs of the restriction is cited to ASN-0036's S8
**ASN-0118, "What a spec-set names, and what resolution recovers"**: "the maximal-run lockstep property (ASN-0036, S8) fixes each run's images in step with its bound positions: `Σ.M(d_s)(vⱼ + k) = aⱼ + k`"
**Problem**: ASN-0036's S8 is stated of `dom(Σ.M(d))` as a whole. The runs in question are runs of the *restriction* `M(d_s)|⟦σ⟧`, and the lockstep equation for those runs is supplied by ASN-0058 — MaximalRun condition 1 (`f(v + k) = a + k`) and decomposition consistency B3, extended to restrictions by C1a, which the same sentence already cites for the partition. The conclusion is correct; the authority named for the load-bearing step of CP0(a) is the wrong lemma.
**Required**: Cite ASN-0058 (C1a together with MaximalRun/B3 consistency) for the per-run lockstep on the restriction; drop or demote the S8 citation.

### Issue 4: Duplicated motivation and structural announcements (anti-bloat)
**ASN-0118, "The COPY operation" (CP8 discussion) and the displacing case; "Survival of links…"; "What stays the source's…"**: (a) "getting it right matters, because a single K.μ⁺ cannot realize the displacement" followed two paragraphs later by "Here a pure K.μ⁺ is *not* a faithful decomposition… No K.μ⁺ can vacate `v`." — the same point stated twice, the second time with the actual argument; (b) "This is the place for a non-trivial weakest precondition." — an announcement of what the next paragraph is, not part of it; (c) "We tabulate it because the question turns on it." — same class.
**Problem**: (a) is two paragraphs saying the same thing in different words; the preview adds nothing the displacing case doesn't carry. (b) and (c) are structural meta-sentences the reader must skip past to reach the content.
**Required**: Delete the preview sentence in (a), keeping the displacing-case argument; delete (b) and (c) — the wp derivation and the table speak for themselves.

## OUT_OF_SCOPE

### Topic 1: Loss of discoverability when the destination later contracts the transcluded positions
**Why out of scope**: This is the DELETE-side wp (ASN-0098 LP12a territory) applied after a COPY; the ASN correctly poses it as an open question rather than specifying it here.

### Topic 2: Transclusion into the link subspace, and the correspondence relation across appearances
**Why out of scope**: Both are flagged in Open Questions; placing links by reference and the appearance-correspondence relation are new operations/relations, not gaps in the content-COPY contract.

VERDICT: REVISE
