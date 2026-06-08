# Review of ASN-0102

I reviewed the COPY operation against the foundation claim statements, checking the precondition completeness, the effect clause, the tiling/density argument, the merge-boundary analysis, and the full invariant-preservation discharge in X16.

## Correctness checks performed

- **wp(COPY, S3★)** — The partition of post-state keys into unmoved / displaced / copied is exhaustive (every post-state `s_C` key `c ∈ [1, n_S+W]` lands in exactly one class via X15's tiling; all non-`s_C` keys are unmoved). The reduction to "copied addresses lie in `dom(Σ.C)`" is sound, and discharged by C1 through PC1. The `s_L` conjunct is correctly shown vacuous.
- **X15 tiling** — `[1,p) ∪ [p,p+W) ∪ [p+W,n_S+W] = [1,n_S+W]` with shared boundary endpoints and no gap, valid across `1 ≤ p ≤ n_S+1`. Boundary cases (`p=1`, `p=n_S+1`, `n_S=0`) check out. S8a is independently verified for interior copied and displaced positions, and cross-subspace disjointness via component-1 distinctness (T3) is correctly argued — so S2 is genuinely discharged, not assumed.
- **X7 fragmentation** — Within-reference non-coalescence rests correctly on maximal-run decomposition (consecutive maximal runs are source-V-adjacent, hence not I-adjacent by M12), and copy preserves I-coordinates so target adjacency mirrors source. Inter-reference merge condition (M7 + M16) is stated correctly; the `≤ k` bound with equality condition holds.
- **X11 boundaries** — Leading (`p≥2`) and trailing (`p≤n_S`) presence conditions and I-adjacency tests are correct; first-displaced-block I-start `= Σ.M(d)(v)` and last-copied I-reach `= a_k+n_k` are right, and I-adjacency subsumes origin agreement (M16a).
- **Provenance (X13/X16)** — The unconditional write plus RR routing correctly satisfies range-based J1★/J1'★: a carried address is already in `R` by P4★ at `Σ_0` (so not `R`-new, J1'★ vacuous); a range-new address is recorded (J1★). P7 grounding and `T_elem × E_doc` well-typedness (via S7b, PC2) are discharged.
- **Invariant coverage** — Every conjunct of `ExtendedReachableStateInvariants`, the composite-boundary properties P4★/P4a/P7a, and the transition theorem P3 are addressed. Self-transclusion pre-state pinning (X9(b)) is correctly handled and demonstrated.
- **Cross-ASN references** — All referenced ASNs (0034, 0036, 0047, 0058, 0093) are foundation ASNs; no violation of Standard 7.
- **Edge cases** — Append (trailing boundary absent), empty-subspace first insertion, self-transclusion with overlapping displaced region, cross-origin fragmentation, and coalescing copy are each given a distinct worked example exercising distinct claims (not redundant).

## Anti-bloat scan

I checked for the flagged forward-reference patterns: defensive justifications, exhaustiveness padding, use-site inventories, axiom-rationale prose, duplicate paragraphs, and ordering justifications. The three explanations of pre-state pinning (intro definition / X9(b) claim / worked-example demonstration) follow the legitimate define→claim→demonstrate structure rather than restating one point. The frame-trivial invariant list in X16 is load-bearing discharge work, not inventory padding. The scattered Gregory `Q`-references are brief confirmatory "what the operation does" statements, which the guidance explicitly exempts. X14 reads cleanly after its recent trim. No paragraph imagines a case the precondition already excludes; no relocated-finding residue is evident.

No REVISE items.

VERDICT: CONVERGED
