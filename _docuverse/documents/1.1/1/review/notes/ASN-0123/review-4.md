# Review of ASN-0123

I read this as a manuscript that earns its length. The operation is *derived* from the guarantees it must keep (G1–G3) rather than designed-then-checked, the no-copy result (G2) is shown *necessary* rather than merely chosen, and the proofs that carry weight are not hand-waved. I expanded the load-bearing arguments and found them sound:

- **VN-B1** — the induction over K.δ that re-proves ASN-0040's B1 in ASN-0047's vocabulary (rather than citing it as if it transferred). I checked all four arrival cases: Node and `k=2` are impossible by zero-count/penultimate-component, `k=1` forces `c₁` with `m=0`, `k=0` forces `t = c_{j−1}` and `j = m+1` via TA5-SigValid + T4-validity. Exhaustive and correct; it correctly does *not* lean on VD.
- **SA** (stored-address antichain) — the `zeros(d') ≥ 3` contradiction off LP-Sub's `[d,0,s,k]` form is tight, and it is exactly what converts subtree coverage to address identity in G2.
- **V9(a) severance** — both Covering-chain branches close (the `d_src ≼ pfx(π')` branch by Z-mono vs O1a, the `pfx(π') ≼ d_src` branch by O5(ii)-derived `#pfx(π') > #pfx(π)` vs O2's strict-max). Airtight.
- **V8** — coverer-set equality with the equal-length case spelled out via O1b. Sound.
- **V10 / G2** — `ran(Σ'.M(v)) = A` + LP12 per-slot, with the SA step closing the subtree-to-singleton gap. The biconditional is in substance the weakest precondition for "discoverable from v," so the depth check is met.
- **V-WF** — clause-1 preconditions at intermediates and clause-2 couplings (J0 vacuous; J1★/J1'★ discharged by the `R'` clause exactly because every carried `a` is range-new in `v`). The `n=0` degenerate path collapses to a single K.δ correctly.

Edge cases the topic demands are present and **correctly scoped**: empty source (`n=0`), first fork (`k=1`), iterated forks (`k=0` frontier), and cross-owner placement; V4/V5/V7/V8 are owned-only, V9/V9w cross-owner, and V0–V3/V10–V13 hold in both branches (their proofs invoke only the shared Effect/frame, not the branch). I checked that the cross-owner transcription respects CL-OWN (content subspace carries no origin constraint), that V9w's P4★-at-Σ is sound because Σ is a composite boundary by the valid-trace framework, and that the divergence from ASN-0047's J4 (content fixed to the *named source*, not the version frontier) violates no invariant.

One spot I scrutinized and judged sound rather than flag: in V-WF's K.δ check, the unified "`parent(v) = parent(d_src) ∈ E` by K.δ-ID.parent-0/1 and P8" is exact for the `k=1` sub-case; for `k=0` the lemma gives `parent(v) = parent(c_m)`, and the equality with `parent(d_src)` rides on V4(c)'s field preservation — but the *load-bearing* conjunct, `parent(v) ∈ E`, is established directly via P8 on `c_m ∈ E` in both sub-cases, so the precondition check holds regardless of the decorative equality.

## REVISE

None.

## OUT_OF_SCOPE

The cross-owner identity's exact tumbler is deferred to document creation; the ASN abstracts it through the `allocated_by(π', v)` interface (yielding O5(i)/(ii)) and proves severance/ownership from that hypothesis alone, which is the right boundary — the operation's *guarantees* are fully determined even where the identity is not. The Open Questions correctly capture the genuine future work (concurrent-fork serialization, a derivation-direction witness surviving symmetric provenance, location-fixed windowing under arrangement isolation, withdrawal/supersession). These are appropriately not addressed here.

VERDICT: CONVERGED
