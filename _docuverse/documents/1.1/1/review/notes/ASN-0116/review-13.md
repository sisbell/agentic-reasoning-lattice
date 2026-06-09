# Review of ASN-0116

I read the ASN as a specification of INSERT decomposed into the K-vocabulary composite `K.α(×n) → K.μ⁻ → K.μ⁺ → K.ρ(×n)`, and checked each proof obligation, every boundary, and every invariant conjunct the post-state must satisfy.

## REVISE

(none)

The ASN clears the bar on every axis the standard names:

- **Validity as a composite is established, not asserted.** Clause 1 of ValidComposite★ is discharged step-by-step against each *intermediate* state (K.α freshness against the growing store; K.μ⁻ strict-contraction precondition `J−1 < N`; K.μ⁺ targets-in-`dom(C)`, S8a, D-CTG★/D-MIN★, content-subspace restriction; K.ρ `a ∈ dom(C')`). Clause 2 (J0, J1★, J1'★) is discharged at the boundary. Once validity holds, the remaining composite-boundary properties (P4★, P4a, P7a) follow from ExtendedReachableStateInvariants — the ASN correctly leans on the theorem rather than re-deriving each, while still showing the J-couplings that are *requirements* for validity.
- **Boundaries covered.** Interior (`1 ≤ J ≤ N`), append (`J = N+1`), empty subspace (`V_S(d) = ∅`), and the genuinely tricky `n ≥ 2` *mixed split* where lower block positions (index ≤ N) are withheld by I3-V and upper ones (index > N) by I3-CS — each is handled with the correct per-position attribution, not a single case on `J`.
- **The non-inheritance discipline is sharp and correct.** I3-S3 and I3-S7 are explicitly *refused* because their proof frame I3-C (`dom(C')=dom(C)`) is broken by I-ALLOC; referential integrity and the content-store invariants (S7a/S7b/C1/C1b/C1c) for `A_new` are discharged at the K.α source instead. Contiguity of the filled run is proved directly (consecutive-disjoint interval argument) rather than borrowed from ASN-0082's `#p=2` contraction lemmas.
- **Depth obligations met.** Consequences are explored (link survival P4 with the correct bijection-not-inclusion witness structure; isolation P5; resurrection via LP18). The wp (P6) is non-trivial and the subtle point — *containment*, not emptiness, because L4/L9 permit ghost references — is exactly right; the worked example exercises it (the ℓ "trap" and the ℓ' genuine resurrection).
- **Foundation usage is clean.** All cross-ASN citations are to foundation ASNs (0034, 0036, 0043, 0047, 0082, 0093, 0098); no retired/sibling-operation ASN is referenced.

## OUT_OF_SCOPE

### Transclusion-shared insertion points, concurrent allocation, transclusion provenance, post-insertion fragmentation
**Why out of scope**: The ASN's four Open Questions name exactly these, and each lands in COPY/concurrency/versioning territory the scope list defers. They are correctly held as future work, not gaps in INSERT.

VERDICT: CONVERGED
