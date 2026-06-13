# Review of ASN-0123

I checked this as a proof manuscript: every operation clause traced to the invariant it must keep, every case of the inductions walked, the cross-foundation bridge audited for what it imports versus assumes, and the worked arithmetic recomputed. The note is unusually disciplined — it reduces all per-state invariant preservation to a single valid-composite obligation (V-WF) and then discharges that obligation case by case, rather than hand-waving "S0–S3 maintained similarly." Below I record what I verified and why I found nothing to revise.

**Proofs I checked in full and found sound:**

- **VN-B1 (version-namespace contiguity).** The induction over the atomic vocabulary is complete: Node(e) excluded by `zeros`, k=2 excluded by the penultimate-separator argument (`0 = d_{#d} ≠ 0`), k=1 forced to `c₁` with `m=0`, k=0 forced to operand `t = c_{j−1}` via TA5-SigValid on the T4-valid operand, yielding `j = m+1`. The note correctly refuses to cite B2 (whose stated precondition is *global* B1) and derives the frontier identity `nextv(E,d) = c_{hwm+1}` directly from VN-B1 + S0. This is exactly the kind of black-box-precondition trap usually missed; it was caught.
- **V9 severance.** `¬(d_src ≼ v)` traced through both branches — the `pfx(π_o) ≺ pfx(π)` chain (via O5(ii), Covering-chain, O1b) and the `pfx(π) ≼ d_src` contradiction with O2 maximality. Correct, and the maximality it consumes is correctly pinned to `π` (the K.δ actor) rather than imported as a bare stipulation.
- **SA (stored-address antichain).** The `zeros(d') ≥ 3` contradiction is valid given LP-Sub's `[d,0,s,k]` structural form (`#E = 2` exactly in this substrate), and the conversion of subtree coverage to address identity in G2/V10 depends on it correctly.
- **V8 coverer-set equality**, **V-WF clause 1 (both K.δ branches, K.μ⁺, K.ρ preconditions at intermediate states)**, **V-WF clause 2 (J0 vacuous, J1★/J1'★ via the R′ clause)**, and **V13's two-sided pinning** all check out, including the repeats case where `|A| < n` and provenance counts distinct addresses (range-based J1★/J1'★, not position-based).
- **The cross-owner worked instance** (newest addition): `d_src = 1.1.0.1.0.1`, `pfx(π)=1.1.0.2`, `v=1.1.0.2.0.1` — divergence at position 4, `d_src ⋠ v`; `1.1.0.2` is the longest account-tier prefix of `v` so `ω'(v)=π`; `origin(a₁)=d_src` so V9w lands identically to the owned reading. Arithmetic correct.

**Boundary cases** are handled: empty source (`n=0`, composite is the lone K.δ, all couplings vacuous); both ownership branches at both forker tiers (node-tier non-owner correctly excluded by P-tier; node-tier owner served by the owned branch); links-only source (forks to empty version, forced by CL-OWN/K.μ⁺_L, and the implementation deviation flagged). The PS bridge is stated explicitly, is adequate for every ASN-0042 fact the proofs use (the dynamics-dependent ones via PS clauses, the static ones transferring freely), and its non-enforcement is honestly flagged as deviation 4.

## REVISE

None.

## OUT_OF_SCOPE

The eight Open Questions are all genuine future territory, not gaps in this note: non-versioning allocations into a version namespace (Q1 — VD is the partial answer here, the full invariant is future), recovering derivation direction from symmetric provenance (Q2, version-comparison territory), link-subspace carry-through (Q3 — the note argues content-anchoring is the complete obligation, which V2b/V10 support), concurrent-fork serialization (Q4), location-fixed windowing (Q5), withdrawal/supersession (Q6), post-contraction provenance semantics (Q7), and minimum shared-identity for correspondence (Q8). I independently confirm each belongs to a later ASN; none is a hidden in-scope obligation the note skipped. The note also stays within its declared lane — it touches editing, links, and windowing only through frame conditions and deferred remarks, never specifying those operations.

VERDICT: CONVERGED
