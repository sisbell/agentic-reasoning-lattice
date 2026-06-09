# Review of ASN-0116

## REVISE

(none)

I checked the load-bearing arguments specifically:

- **Composite validity.** The `K.α(×n) → K.μ⁻ → K.μ⁺ → K.ρ(×n)` sequence discharges each intermediate precondition correctly: K.μ⁻ strict-contracts the content subspace (`J−1 < N`), K.μ⁺ targets are all in `dom(C)` because allocation precedes extension, prior-domain agreement holds because the prefix is left in place, and the append/empty cases correctly drop K.μ⁻ (inapplicable, not optional). Coupling checked only at the boundary, per ValidComposite★.
- **I-NEW attribution.** The per-block-position split (I3-V for index ≤ N, I3-CS for index > N) is sound, and the "no block position is a shifted-suffix image" argument (`i−n ≤ J−1 < J`) holds uniformly across occupied, append, and mixed splits.
- **Non-inheritance discipline.** Correctly refuses to inherit I3-S3 and I3-S7 (both proved under the content frame I3-C that I-ALLOC breaks), discharging referential integrity via S3 + append-only monotonicity and content-store invariants at the K.α source instead.
- **Contiguity.** Established as INSERT's own consecutive-disjoint-interval theorem, not borrowed from the D-family contraction lemmas (which are inapplicable).
- **P6 weakest precondition.** Genuinely non-trivial: a containment (`Added ⊆ D(d,Σ)`), not emptiness, with the ghost-plus-live-span pre-state correctly distinguishing the two and exercised in the worked example.
- **Boundary cases.** Empty subspace (depth-fixing), append (`J=N+1`), front-insert (`J=1`), and `n=1` all verified; worked example checks reading order, link shift+resurrection, the P6 trap, genuine LP18 resurrection, and isolation.

The provenance coupling (J0/J1★/J1'★/P7a/P7) is discharged at the composite boundary with the correct range-new identity (`A_new` only, shifted suffix range-old). Cross-ASN references are confined to foundation ASNs. No drift: the ASN specifies state, an operation, frame, and invariants abstractly.

VERDICT: CONVERGED
