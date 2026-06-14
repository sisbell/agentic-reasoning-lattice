# Review of ASN-0123

I read the note as a derivation of CREATENEWVERSION from the guarantees it must keep, and checked each proof, each boundary case, the foundation usage, and the anti-bloat patterns the classifier flags. Recording what I verified, since a CONVERGED verdict on a note this size should be auditable.

**Realizability (V-WF), both branches.** The owned branch's K.δ discharges operand-in-E (stream frontier: `k=1, t=d_src` empty / `k=0, t=max child` non-empty), `parent(v) ∈ E`, and `nextv` freshness via VN-B1. The cross-owner branch's single document-K.δ in `A_doc(pfx(π)) = S(pfx(π),2)` discharges the `k=2` descent (`t=pfx(π) ∈ E`, `zeros ≤ 1`, ChildSpawnFreshness) and the later `k=0` sibling (FrontierEquivalence), yielding `zeros(v)=2`, `Document(v)`. K.μ⁺ (canonical content positions ⊆ dom(C), S8a/S8-depth/D-CTG★/D-MIN★) and the `|A|` K.ρ steps check out. Couplings: J0 vacuous (`dom(C')=dom(C)`), J1★/J1'★ exactly the `R'` clause, `n=0` vacuous. The boundary-property claim (P4★∧P4a∧P7a at Σ') correctly rests on P-bdy + ValidComposite★.

**Severance theorem (V9a).** The maximality O5(ii) is proved structurally — any coverer of `v=[pfx(π),0,k]` longer than `pfx(π)` contains the length-`(#pfx(π)+1)` prefix `[pfx(π),0]` with two zeros, contradicting O1a via Z-mono — and the `¬(d_src ≼ v)` argument closes both comparability branches correctly. This is the load-bearing O5(ii) discharge; I confirm it is sound and consumed (not trimmable).

**VN-B1, SA, V8.** VN-B1's case split (Node/`k=2`/`k=1`/`k=0`) correctly shows every namespace arrival is the frontier, from K.δ constraints alone. SA's antichain proof (a proper stored extension forces `zeros(d') ≥ 3`) is correct. V8's coverer-set equality (⊇ by ≼-transitivity, ⊆ by Covering-chain + Z-mono) holds.

**Worked instances.** Both arithmetic checks are correct: owned (`d_src=1.1.0.1.0.1 → v=1.1.0.1.0.1.1`, `a₁ ⋠ a₂`, `project=\{[1,1],[1,3]\}`, `|A|=2<n=3` reflected in `|R'∖R|=2`) and cross-owner (divergence at position 4, `ω'(v)=π`, content witness survives severance). The `|A| < n` repeat case and the empty-source `n=0` degenerate case are both handled.

**Foundation usage.** No improper cross-ASN references — every cited ASN (0034/0036/0040/0042/0043/0045/0047/0053/0058/0086/0093/0098) is a foundation. PS is correctly framed as a standing cross-foundation assumption whose coverage half (`n₀ ≼ e` for all `e ∈ E`) is derived, with the rest absorbed into the assumption honestly. The cross-owner branch is "versioning by inclusion" (transcribed content, forker-owned), distinct from CREATENEWDOCUMENT — no scope overstep.

## REVISE

None. I could not find a correctness error, a missing boundary case, an unproven leap, a proof-by-similarly/checkmark, or an improper cross-ASN reference.

**Anti-bloat check (performed per the classifier).** I scanned for the flagged patterns and found the dense prose load-bearing rather than accreted. The closest candidates were each defensible: the V9-preamble summary sentence generalizes O5(i)/(ii) from `v` to the whole stream (supporting "within-stream index immaterial," a real V-WF need, not a restatement); the P-tier comment's node-tier paragraph explains the precondition's boundary (single-mint), which advances rather than pads; the V9w/atomicity "load-bearing" notes are genuine precision about P4★ being a boundary-only property. The two worked examples are required by the depth standard, not bloat. No actionable trim.

## OUT_OF_SCOPE

The note's eight Open Questions correctly defer non-versioning namespace allocation (the VD invariant), derivation-direction recovery under symmetric provenance, link-subspace carry, concurrent-fork serialization, location-fixed windowing, withdrawal/supersession, post-contraction provenance, and minimum shared-identity for correspondence. These belong in future ASNs; flagging them here would be redundant with the note's own deferrals.

VERDICT: CONVERGED
