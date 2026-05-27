# Review of ASN-0069

I worked through this ASN against the foundation vocabulary (ASN-0034/0036/0047) with attention to: the V1 case-dispatch derivation, the V2 prefix-chain induction, V4b's design commitment beyond J4's range constraint, V5a's per-document frame discipline, V6a's locally-defined coverage/project machinery, V7's K.δ-alone extension of J4, V8b's witness-set non-monotonicity, V11's premise scoping across each step's gap, V11a's prefix-chain reconstruction, V12(d)'s P4★ derivation, and the ValidComposite★ verification in V0.

Specific checks that passed:

- **K.δ subsequent-fork case** (k=0, t=d_prev): The freshness argument via T10a's at-most-once + T10a.7 (EnumerationInjectivity) + SequentialTransitionAxiom + P1 + T10a.6 (DomainDisjointness) cleanly rules out all collision paths.
- **V2's nested induction** on emission count properly tracks `#d_src + 1` as the universal length for `A_v(d_src)` outputs, then handles the inductive step at `k=0` correctly via TA5-SigValid placing the modified position at `sig(d_prev) = #d_prev > #d_src`.
- **V5a's two clauses** (per-elementary and per-sequence) are both derived rigorously; the K.δ subcase correctly observes `d_new ≠ d*` from the precondition `e ∉ E` against `d* ∈ E_doc ⊆ E`.
- **V6a's three claims** (link store invariance, source projection invariance, fork projection equality) — each derivation explicitly checks set inclusion in both directions where needed.
- **V8b's transition-by-transition analysis** walks all eight elementary transition kinds and traces `Corr_g` restricted to `F` through each, correctly identifying only K.μ⁻/K.μ⁺/K.μ~ on d_src or d_new as Π_g-affecting.
- **V11's induction** with the formal premise carrying both set-equality and pointwise-equality across each step's gap; the IH supplies the membership in `V_{s_C}(d^{k-1}_new)` at post-(k−1) via `subspace(v) = s_C` directly without needing set equality back to `V_{s_C}(d_src)`.
- **V11a's transitivity of ≼** is unpacked from the Prefix definition (ASN-0034) and T0 NAT-order transitivity; the inner induction on `k − i` correctly establishes `dⁱ_new ≼ d^k_new` for every chain index.
- **V12(d)** correctly derives `ran(M'(d_new)) = ran(M(d_src)|_{V_{s_C}(d_src)})` (range equality, not just inclusion) via V4b's exact domain equality before applying P4★ at the pre-fork state.
- **ValidComposite★ verification** discharges every K.δ precondition (outer + uniform + per-sub-case) for both first-fork and subsequent-fork shapes, then verifies K.μ⁺ and the K.ρ × n cumulative effect, then verifies J0/J1★/J1'★ at the composite boundary.

Deviations from J4 (V1's subsequent-fork extension, V7's K.δ-alone extension, V4b's domain-equality strengthening) are each explicitly marked and individually justified.

The Worked Example concretely verifies V1, V2, V3, V4, V5, V6, V6a, V9, V8, V10, V11, V12 plus the V7 empty-source and link-only-source cases.

ASN-0040 is correctly flagged as unused in the Dependency Audit.

## REVISE

*(none)*

## OUT_OF_SCOPE

*(none — the Open Questions section already enumerates forward-looking topics: concurrent fork semantics, transcluded-source forks, fork-tree presentation, snapshot vs. living forks, V-stream depth invariants, immediate-post-fork deletion guarantees, etc. These are correctly deferred to future ASNs.)*

VERDICT: CONVERGED
