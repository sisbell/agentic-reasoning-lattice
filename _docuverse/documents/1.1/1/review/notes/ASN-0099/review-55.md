# Review of ASN-0099

I read the ASN as a read-only query specification (FINDLINKS), checked the proofs that carry weight, and stress-tested the boundary cases and the cross-document ordering argument in particular.

## REVISE

(none)

I verified the load-bearing claims rather than taking them on trust:

- **F10a Case (ii)** correctly handles the version case (`d_new = inc(d_src, 1) = [d_src, 1]`, both `zeros = 2`, `d_src ≺ d_new`). The four-step unfolding of `d₂_{#d₁+1} ≥ 1` is sound: T4's terminal-nonzero constraint plus prefix agreement forces the two zeros into positions `≤ #d₁−1`, leaving none for `#d₁+1`. Anchor lifting via `b_L(·) = [·.0.s_L]` then puts the separator-`0` against a `≥1` at the divergence position, and PrefixOrderingExtension closes the block ordering.
- **F9 / F9★ / F9-λ** partition V's single-step impact correctly: A1a discharges link-store inertness for all six atomic ops of `V ∖ {K.λ}` from published frames (K.μ⁺/K.μ⁻ via the amended extended-state frames), K.μ~ enters only through its K.μ⁻+K.μ⁺ decomposition, and F9-λ's disjoint-union increment is justified by freshness + L12.
- **F11 vs. ASN-0098's `discoverable_from`** — the I-side/V-side persistence split is real and correctly attributed: PerLinkInvarianceUnderValuePreservation + LP13 give I-side persistence; Query 5 exhibits the V-side contraction failure honestly. Good that V-side persistence is *not* claimed.
- **F13, F20, F14, F8, F5, F6** all check out by direct unfolding; the strengthening/weakening witnesses (F4) are realizable by single K.λ steps and each genuinely disagrees with F1 on its witness.
- Boundary cases are covered: empty query, empty link store, empty non-type endsets, `d ∉ dom(Σ.M)`, V-positions outside the arrangement (silent projection), and cross-subspace link-image (Query 4). `image` is finite by S8-fin regardless of `R`. Vocabulary scope is complete for ASN-0047's extended state, and K.σ is correctly excluded as unreachable.

All cross-ASN references are to foundation ASNs (0034, 0036, 0043, 0047, 0058, 0093, 0098); no foundation notation is reinvented (`matches` is a documented generalization of `discoverable_from`, not a duplicate; coverage is used, not restated).

## OUT_OF_SCOPE

### Topic 1: Out-of-store query addresses, partition tolerance, concurrency model, access-control composition, audit witnesses, timing bounds, FOLLOWLINK inverse
**Why out of scope**: These are correctly enumerated in the ASN's own Open Questions and "What We Have Not Specified" sections as future territory. They are not defects in this ASN.

VERDICT: CONVERGED
