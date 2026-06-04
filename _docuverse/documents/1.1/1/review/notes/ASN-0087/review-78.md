# Review of ASN-0087

I checked the composite decomposition (`K.λ ; K.μ⁺_L`), all three invariant classes, the wp analysis (including the reflexive case), the side-effect characterization, and the worked example. I also ran the anti-bloat pass flagged for this note.

## Technical verification

- **Boundary cases covered.** Empty link subspace (`V_{s_L}(d) = ∅`, first-link depth pinned at `m = 2` via M-DepthConv), empty non-type endsets (`coverage(∅) = ∅`), intra-document references (worked example `e₁ → a₁` under `d`), and reflexive self-reference (the reflexive variant) are all exercised.
- **S2 discharge is complete.** The two-part exclusion (`v_ℓ ∉ V_{s_L}(d)` by D-SEQ★ strictness, `v_ℓ ∉ V_{s_C}(d)` by SC-NEQ) correctly establishes `v_ℓ ∉ dom(Σ.M(d))`, not merely the within-subspace fact.
- **D-CTG★ is proven at arbitrary depth** `m ≥ 2` via the T1 case-(i) interior-component argument, not assumed at `m = 2` — this is the kind of conjunct usually hand-waved, and it is shown.
- **M-DocFixity correctly distinguishes** `dom(M)` (document set, frame-fixed) from `dom(M(d))` (per-document arrangement, extended by K.μ⁺_L). The reverse inclusion is properly derived rather than assumed from M1.
- **wp Case 2 reflexive route** is non-trivial and the standard-authoring collapse (via M-FreshExcl at `x = ℓ`, with `ℓ ∈ F` established structurally) is sound. The backward freshness transfer through Store Monotonicity★ in the side-effects section is rigorous.
- **Worked example arithmetic checks out** — `a₁ = [1,0,1,0,1,0,1,1]` and `ℓ = [1,0,1,0,1,0,2,1]` diverge at position 7, `zeros = 3` on each, discoverability intersections computed by explicit prefix-testing.

## Cross-reference and scope

All referenced ASNs (0034, 0036, 0043, 0047, 0093, 0098) are foundation ASNs; references are permitted. No reinvented notation — StandardAuthoring, M-FreshExcl, and the M-prefixed claims are legitimate ASN-local helpers; `F`, `coverage`, `project`, `discoverable_from` are used from ASN-0098 without redefinition. The note defines state-transition semantics and invariant preservation abstractly — no implementation drift, no META.

## Anti-bloat pass

I examined the flagged patterns (repeated downstream deferrals, use-site inventories, axiom rationale prose, paraphrase duplication). The narrative passages I scrutinized — the "fills in / retroactively activating" prose in *Side Effects*, the framing in *What Is Indexed?*, the *No Permission Check* statement — each advance reasoning (the first ties the side-effect window to L4; the last is a statement of what the operation does not do, explicitly permitted). The freshness citations and the invariant-table source attributions are structured use-citations in their proper slots, not accreted meta-prose. No forward-reference bloat rising to a finding; the note appears to have been cleaned in prior cycles.

No REVISE items.

VERDICT: CONVERGED
