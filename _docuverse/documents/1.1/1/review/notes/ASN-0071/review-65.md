# Review of ASN-0071

I read the full note: the vspec definition, the PC derivation (componentwise fact, totality, prefix agreement), PC-RANGE's cross-depth characterisation with its `#v = #u` / `#v > #u` / `#v < #u` case split, the `iaddrs`/`find` definitions, the worked scenario's five sub-queries, and the F-* claim table.

## Rigor

- **PC** is derived without hand-wave: the first-disagreement argument invokes T0 trichotomy at the candidate position, then well-ordering to close the universal; totality is proven separately and is not circular (it reuses the componentwise fact for `p ≤ #t < #u`, where `t_p` provably exists).
- **PC-RANGE** covers every depth relation between anchor and arrangement. Boundary components are handled with the exclusive-reach distinction (`v = u` admitted by equality; `v = r` excluded because reach is exclusive, not by an order relation) — exactly the kind of boundary that usually gets skipped, and it is shown.
- **F-DEEP** treats both the empty-source (`V_{s_C}(d_s) = ∅`) and the too-deep-anchor (`#u > m_C`) cases, and the scenario exhibits the latter concretely (`Q_F`).
- Boundary cases are all present: empty query (F-EMPTY), empty/absent arrangement positions (F-FILT), shared content at non-adjacent positions (`w₁`, `w₃` → `a₁`), cross-source dedup (`Q_G`), and the cross-depth coarse-anchor capture (`Q_E`). Zero-width and link-subspace vspecs are excluded by the `Pos(ℓ)` / `subspace(u) = s_C` preconditions rather than ignored.
- The five scenario queries each discharge a distinct claim (exclusion, proper-subset/disjoint-fragment overlap, cross-source dedup, PC-RANGE width-1, F-DEEP dual); none is redundant.
- F-CONTENT, F-SELF, F-CUR, F-FIN, F-ORIGIN are derived with explicit chains, not asserted.

## Cross-ASN / notation

All numbered references are to foundation ASNs (0047, 0053, 0058) or foundation-internal claims (S3★, S8-depth, D-SEQ★, M13, M14, T1) restated within them. No reinvented notation; `vspec`/`iaddrs_one` are genuinely new objects (coverage-tolerant, set-valued), not duplications of `ContentReference`/`resolve`.

## Anti-bloat

The `resolve`/`iaddrs_one` contrast and the vspec-relaxation enumeration survive prior trimming, but both are load-bearing: the relaxation list states precisely which foundation preconditions are dropped and why search must tolerate them, and the `resolve` recap is needed to support the "discards V-order and run structure" contrast. Subspace confinement is established once and explicitly reused (not re-derived) in *Resolution* and F-CONTENT. The *Reachability* remark is consolidated rather than repeated. No defensive sub-paragraphs, use-site inventories, or duplicated claims remain.

No REVISE items. No OUT_OF_SCOPE issues — the excluded operation topics (INSERT/DELETE/COPY/links/versions/BEBE) are correctly deferred to Open Questions, not claimed here.

VERDICT: CONVERGED
