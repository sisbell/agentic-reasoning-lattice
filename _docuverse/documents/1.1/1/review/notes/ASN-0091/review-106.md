# Review of ASN-0091

I checked the abstract Vstream-only class, the REARRANGE_K realisation argument, and the derived invariants (RE-C, RE-dom, RE-ran, RE-μ, RE-L, RE-cov, RE-disc, RE-proj, RE-frag/coal/eq, RE-trans, RE-origin, RE-R), plus the L-chain lemma and all five worked examples, against the foundations. I recomputed each worked example arrangement and run decomposition independently.

## Findings

The core derivations are sound:

- **RA-π → RE-ran/RE-μ**: the bijection substitution `v' = π(v)` and injectivity-on-finite-set arguments are correct; the two-case split (target via π, non-target via RA-frame) is complete over `dom(Σ.M)`.
- **L-chain**: the identification `x + 1 = inc(x,0)` under `sig(x) = #x` (TA5-SigValid) is valid, and chain-domain disjointness (T10a.6 via ASN-0093) genuinely forbids both adjacency directions. The coalescence/equality/collapse witnesses each invoke it with the right operand pairing.
- **Net-effect split**: the contrapositive — `M'(d) ≠ M(d)` forces `M(d)|_{dom_C}` to take ≥2 distinct values, hence K.μ~'s precondition — is correct, so the non-trivial case legitimately routes through K.μ~ and the collapse case through the (valid) empty composite.
- **RA-adm via reachability**: appending the realising composite to a trace, then invoking ExtendedReachableStateInvariants, correctly avoids re-verifying each per-state invariant (S3★ etc. are covered without restatement).
- **RE-trans conclusion (iii)**: the CL-OWN + S3★ argument that `a ∈ dom(Σ.C)` (excluding the link-subspace case before applying C2) is properly sequenced, and the `origin(a) ≠ d` hypothesis is correctly carried.

I recomputed all six arrangements (main pivot, 4-cut swap μ-delta, interior cuts, bijection non-uniqueness, net-effect collapse) and every run-cardinality claim; each matches the stated post-state and direction.

No REVISE-worthy rigor gap, missing boundary case, hand-wave, or cross-ASN reference (all citations are to foundations) was found. The exhaustiveness/routing preambles in the transclusion and discoverability sections are verbose but describe genuine proof structure and do not obstruct the argument; they do not rise to flaggable accretion.

## OUT_OF_SCOPE

### Topic 1: Source-span reconstitution after a transcluding cut
**Why out of scope**: Whether two fragments of a same-source transclusion *jointly* reconstitute the original span (beyond each carrying the right origin) is a new guarantee about fragment composition, correctly deferred to Open Question 1 rather than asserted here.

### Topic 2: Link-subspace rearrangement semantics
**Why out of scope**: REARRANGE_K fixes the cut subspace at `s_C` (CS3); reordering within the link subspace would be a distinct operation with its own invariants (Open Question 2), not a defect in this ASN.

### Topic 3: Bound on run-cardinality increase per invocation
**Why out of scope**: RE-frag establishes increase is possible; a tight upper bound (Open Question 4) is a quantitative refinement for a future note.

VERDICT: CONVERGED
