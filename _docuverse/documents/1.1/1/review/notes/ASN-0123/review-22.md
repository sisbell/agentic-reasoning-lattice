# Review of ASN-0123

I reviewed this as a fork specification must be reviewed: by trying to break the source-untouchedness frame, the freshness/contiguity of allocation, the severance theorem, and the carry-through biconditional — then re-deriving the two worked instances against concrete addresses. The proofs hold. I record the load-bearing checks below so the verdict is auditable, not a rubber stamp.

## REVISE

(none)

The following were the candidate failure points; each survived scrutiny.

**VN-B1 (VersionNamespaceContiguity)** — the induction is genuinely complete. Only K.δ mutates `E`; the four arrivals into `S(d,1)` are exhausted (Node impossible by `zeros=2`; `k=2` impossible by the penultimate-zero argument; `k=1` forces `c₁` with `m=0`; `k=0` forces operand `c_{j−1}` and freshness pins `j=m+1`). The proof correctly refuses ASN-0040's B2 because B2's stated precondition is *global* B1, which version namespaces alone do not discharge — this is exactly the kind of citation that is usually waved through, and it was not. The frontier identity `nextv = c_{hwm+1}` then rests on VN-B1 + S0 only.

**Severance V9(a)** — traced line by line. `pfx(π_o) ≼ d_src ≼ v` → O5(ii) length bound → comparability (Covering-chain) → `pfx(π_o) ≺ pfx(π)` (O1b excludes equality) → both comparability branches against `d_src` close (Z-mono+O1a kills `d_src ≼ pfx(π)`; O2 maximality kills `pfx(π) ≼ d_src`). Airtight. The reliance on `allocated_by(π,v)` is legitimately sourced from PS(ii), not assumed.

**V8 / V9(b) ownership** — coverer-set equality is correct in both directions; the `(⊆)` direction's use of Z-mono+O1a to exclude `d_src ≼ pfx(π'')` is the right move and the only non-obvious step.

**V9w's P-bdy dependence** — the strongest part of the note. The proof identifies that the source-side witness `(a,d_src) ∈ R'` rests on P4★, which is a *composite-boundary* property (not a per-state invariant), and walks the interior-start counterexample where a pending K.μ⁺ has outrun its K.ρ. This is a real wp-style precondition analysis, not a trivial one.

**V-WF** — both ValidComposite★ clauses discharged; the single-K.δ count is correctly forced in both branches (the account-tier restriction is what prevents the cross-owner path from minting account+version), and the node-tier exclusion is justified rather than stipulated.

**Worked instances** — recomputed. `a₁ ⋠ a₂` (length-9 disagreement at the final component) makes SA collapse the unit-depth subtree to `{a₁}`, so `project(ℓ,1,v,Σ')={[1,1],[1,3]}`; `|R'∖R|=|A|=2<n=3` correctly exhibits provenance-counts-addresses; the cross-owner instance's divergence at position 4 (`1.1.0.1…` vs `1.1.0.2…`) makes severance arithmetic while carry-through lands identically — the orthogonality claim is concrete, not asserted.

Boundary cases (empty source `n=0`, first vs subsequent fork, iterated forks, shared-address sources, node-tier exclusion) are all covered. Only foundation ASNs are cited; no foundation notation is reinvented (`trunc`, `Z-mono`, `SA`, `nextv` are local tools, not duplications). No drift into implementation mechanics — the implementation evidence is cleanly quarantined as correspondence + four honestly-labeled deviations.

One non-blocking observation (not a REVISE): V10's proof cites LP2/LP3 (single-step) for the multi-step composite, where LP3★ would be the formally exact citation — but the proof leads with `L'=L`, from which `Σ'.L = Σ.L` and hence coverage equality follow directly without any LP appeal, so the conclusion is fully justified regardless.

## OUT_OF_SCOPE

Nothing to reclassify. The deferred territory — concurrent-fork serialization, recovery of derivation *direction* under symmetric cross-owner provenance, link-subspace carry, location-fixed windowing vs arrangement isolation, withdrawal/supersession under permanence — is already captured in the Open Questions and is correctly future work, not a gap in this note. The cross-owner branch borrows document-identity allocation but treats it as a primitive (consuming only `Document(v) ∧ v∉E ∧` O5-wrt-π), so it does not stray into CREATENEWDOCUMENT (ASN-0103) territory.

VERDICT: CONVERGED
