# Review of ASN-0123

I worked the proofs rather than the prose. Summary of what I verified, then the verdict.

**Verified in detail:**

- **VN-B1 induction** — all four K.δ arrival cases (Node, k=2, k=1, k=0) checked. The k=0 case correctly forces `t = c_{j−1}`, `j = m+1` (frontier-only arrival) from `sig(t)=#t`, T4 trailing-nonzero, and the IH. The deliberate avoidance of ASN-0040's B1/B2 (transition-system-dependent) in favor of a fresh induction is the right methodology, and the frontier identity `nextv = c_{hwm+1}` is re-derived from VN-B1 + S0 without B2's global precondition. Sound.
- **SA (StoredAddressAntichain)** — the zero-counting argument is correct: a proper extension `a ≺ b` of stored addresses forces a third zero into `b`'s document prefix `d'`, contradicting `zeros(d')=2`. The position bookkeeping (`#d′ ≥ #d₀+1`, extra zero at `#d₀+1 ≤ #d′`) checks out. This is load-bearing for G2/V10 and it holds.
- **V9 severance** — the structural derivation of O5(ii) (maximality) from the depth-2 SiblingStream form `[pfx(π),0,k]` via Z-mono + O1a, *without* importing the O5 axiom, is correct, and the two-branch severance proof closes both cases (`d_src ≼ pfx(π)` → `zeros ≥ 2`; `pfx(π) ≼ d_src` → contradicts O2 maximality). The cross-owner worked instance (`d_src=1.1.0.1.0.1`, `v=1.1.0.2.0.1`, divergence at position 4) makes it concrete.
- **V9w boundary-necessity** — the P4★/P-bdy dependence is real and correctly justified: the exhibited interior failure state (pending K.ρ after a K.μ⁺) shows P-bdy cannot be weakened. This is the non-trivial wp analysis the depth standard asks for.
- **V-WF** — both ValidComposite★ clauses discharged for both branches; the single-K.δ count (and the forced exclusion of node-tier forkers to preserve single-mint) is correct; K.μ⁺/K.ρ preconditions verified against the canonical transcribed positions; reliance on ExtendedReachableStateInvariants for the full per-state package is a legitimate use of the foundation theorem since every step is in-vocabulary.
- **V8, V13, V0, V4, V10** — coverer-set equality, J1★/J1'★ pinning, GlobalUniqueness applicability, ancestry-by-truncation, and the LP12 carry-through biconditional all check. The shared-address case (`|A| < n`) is handled correctly in V13 and the worked instance (`|R'∖R| = |A| = 2`, not `n = 3`).

**Edge cases checked and handled:** empty source (`n=0`, identity-allocation-only, vacuous couplings); shared content addresses; iterated forks (V6, depth-1 never spends the separator budget, B6 unconditional); node-tier non-owner (excluded by P-tier); forking a version of a version; cross-document content arrangement (transclusion, no own-origin constraint on the content subspace).

**Foundation use:** all referenced ASNs are foundations; no non-foundation cross-references. SA generalizes ASN-0086's link-only R0a to both stores via LP-Sub — a needed extension, not a reinvention. PS is an explicit, justified hybrid bridge (registry coverage re-derived so O2's totality transfers).

## REVISE

None. I could not find a skipped case, a hand-wave concealing an error, an unaddressed invariant conjunct, a missing boundary, or a foundation misuse. The proofs are detailed where they need to be (severance, VN-B1, SA, V9w), the concrete examples verify the key postconditions, and the depth requirements (multi-step derivations shown, consequences explored in V5/V7/V12, non-trivial wp via P-bdy necessity) are met.

## OUT_OF_SCOPE

### Cross-owner document number
In the cross-owner branch `v` is specified up to *which* document number it carries in `S(pfx(π), 2)`; the ASN defers this to document-allocation (CREATENEWDOCUMENT territory) while pinning every guarantee it consumes (`Document(v)`, `pfx(π) ≼ v`, O5(ii) maximality, freshness via ChildSpawnFreshness/FrontierEquivalence). This makes VERSION's cross-owner effect a relation rather than a function, which is acceptable for a postcondition-style specification.
**Why out of scope**: the document-number frontier is the CREATENEWDOCUMENT mechanism, explicitly excluded; the versioning semantics (transcription, derivation, witness) are fully specified here, and all guarantees hold for any conforming choice. The ASN's repeated "stays out of scope" caveats already mark this boundary cleanly.

VERDICT: CONVERGED
