# Review of ASN-0123

I checked the operation contract and every V-claim against its cited premises, tracing the foundation dependencies (T10a/GlobalUniqueness, ASN-0042's O-series, ASN-0040 baptism, ASN-0047 couplings, ASN-0098 projection). I worked the boundary cases (empty source `n = 0`, first fork into an empty namespace, subsequent forks, cross-owner fork) and re-derived the load-bearing lemmas. Findings below.

## REVISE

None.

The proofs that carry the note all hold under scrutiny:

- **VN-B1** is correctly re-proven for ASN-0047's K.δ vocabulary rather than imported from ASN-0040's B1 — the case split (Node excluded by `zeros`, `k=2` excluded by the penultimate-zero argument, `k=1` forcing `c₁`, `k=0` forcing `c_{j-1} ∈ E ∧ j = m+1`) is exhaustive and each branch is shown, not asserted. The note's refusal to cite B2 (whose stated hypothesis is *global* B1) and its re-derivation of the frontier from VN-B1 + S0 is exactly the right discipline.
- **SA** is sound: the structural-form argument (`[d,0,s,k]`, separator inheritance forcing `zeros(d') ≥ 3`) correctly rules out proper extension among stored addresses, and its use in G2 to collapse subtree coverage to a singleton is valid (anchor and range members both stored ⇒ intersection `⊆ {a}`).
- **V9 severance** is a genuine theorem, not a stipulation: the two-branch contradiction (`d_src ≼ pfx(π)` ⇒ `zeros ≥ 2` vs. O1a; `pfx(π) ≼ d_src` ⇒ longer coverer vs. O2) closes, and the cross-owner worked instance (`d_src = 1.1.0.1.0.1`, `v = 1.1.0.2.0.1`, divergence at position 4) exhibits it concretely.
- **V8** coverer-set equality, **V10** via LP12 + `ran(M'(v)) = A`, **V13** pinned both ways by J1★/J1'★, and **V9w**'s careful reliance on **P-bdy** (with the explicit argument that the source-side witness *fails* at an interior start) all check out. The P-bdy necessity argument is the non-trivial weakest-precondition analysis the topic demands.
- Boundary cases are handled: `n = 0` degenerates correctly through every claim (A = ∅, R' = R, vacuous couplings, no carry-through); the single-mint guarantee is correctly forced by restricting the cross-owner branch to account-tier forkers, with the node-tier exclusion shown to be *necessary* (intermediate account = second permanent entity) rather than stipulated.

All external references are to foundation ASNs (0034, 0036, 0040, 0042, 0043, 0045, 0047, 0058, 0093, 0098). The PS hybrid (reading ASN-0042 ownership over ASN-0047 states, including the entity-level B=E identification) is load-bearing for V9's O5 invocation, but it is explicitly flagged as a standing assumption with its coverage half re-derived (`pfx(π₀) ≼ n₀ ≼ e` by induction over K.δ, position 1 never disturbed) — disclosed, not hidden.

## OUT_OF_SCOPE

The note's own Open Questions correctly defer the genuinely-future topics (concurrent-fork serialization, derivation-direction recovery from symmetric provenance, location-fixed windowing vs. arrangement isolation, withdrawal/supersession). No claims are defined for the declared out-of-scope operations: V11 establishes *editability* (an enabling property of the fork) without specifying INSERT/DELETE; V10 establishes link *carry-through* (a property of existing links under the fork) without specifying MAKELINK; the cross-owner branch correctly defers document-creation-from-nothing as "namespace mechanics out of scope." Scope is well-managed.

VERDICT: CONVERGED
