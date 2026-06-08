# Review of ASN-0102

I checked the operation definition, the wp/S3★ reduction, the invariant-discharge in X16, and the boundary coverage in the worked examples.

## REVISE

(none)

The note is sound on the points that matter for an operation ASN:

- **wp completeness (X2/S3★).** The three-class partition (unmoved / displaced / copied) is exhaustive; the unmoved and displaced classes carry pre-state images unchanged (discharged by X1 and the link-frame), and the reduction to `(A j,i : a_j+i ∈ dom(Σ.C))` is correct. The `s_L` conjunct is genuinely vacuous (no link-subspace position introduced or altered).
- **Functionality (S2) and density (X15).** The three half-open last-component ranges `[1,p) ∪ [p,p+W) ∪ [p+W, n_S+W]` tile `[1,n_S+W]` with shared endpoints and no gap, using `1 ≤ p ≤ n_S+1`. Cross-subspace disjointness is established by component-1 distinctness (T3), not hand-waved.
- **Boundary coverage.** Empty-subspace first insertion (`n_S=0, p=1`), append (`p=n_S+1`, trailing boundary absent), self-transclusion with source in the displaced region, cross-origin fragmentation, and a coalescing copy (`canonical < k`, leading boundary fires) are each worked concretely against the relevant claims. Zero-width copy is excluded at PC1.
- **Invariant discharge (X16).** Every conjunct of `ExtendedReachableStateInvariants`, the composite-boundary properties (P4★/P4a/P7a via RR routing), and the transition theorem P3 are addressed individually; the singleton-composite reading legitimately licenses applying composite-boundary properties to an elementary transition.

Anti-bloat pass: I looked for accreted meta-prose around forward references (the `review-mode.anti-bloat` patterns). The one forward dependency (X6 → "tiling of X15") and the "Composite-boundary reading" sub-label are load-bearing justification, not noise; the Gregory-trace citations are confirmatory implementation evidence, not drift. No flaggable accumulation remains after the recent X14 trim.

## OUT_OF_SCOPE

### Topic 1: Re-displacement, downstream-source containment, time-varying views, unreachable-allocator identity
**Why out of scope**: The four Open Questions concern later operations acting on copied content and discoverability/reachability over time — new territory for future operation ASNs (and ASN-0098), not gaps in COPY's specification.

VERDICT: CONVERGED
