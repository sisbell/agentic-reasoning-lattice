# Review of ASN-0102

## REVISE

### Issue 1: X14 reachability-rationale paragraph is meta-prose
**ASN-0102, X14 (Atomicity), second paragraph**: "Elementary status is a deliberate modeling choice, not a reachability necessity: in the displacing case Σ' is also reachable by a contract-then-extend composite (a K.μ⁻ retaining the content-subspace prefix `n'_{s_C} = p − 1`, followed by the amended K.μ⁺ ...), so COPY introduces no new reachable state."
**Problem**: This argues *why* elementary status is an acceptable modeling decision (the post-state is reachable by other means anyway) rather than stating what COPY does or what invariant it maintains. "deliberate modeling choice, not a reachability necessity" is precisely the reviser-drift framing the anti-bloat pass targets — defensive justification of a design choice. It also leans on the K.μ⁻/K.μ⁺ mechanics that are out of scope for this note. The atomicity *guarantee* (no observable intermediate state, single indivisible step) is already fully stated in the first paragraph; this one adds rationale, not reasoning the reader needs to follow any claim.
**Required**: Remove the paragraph. If the reachability-equivalence to a `K.μ⁻ + K.μ⁺` composite is genuinely load-bearing for some downstream claim, state it as a bare claim without the "modeling choice / not a necessity" wrapper; otherwise drop it.

## OUT_OF_SCOPE

(none — the four Open Questions are correctly deferred: later re-displacement, transitive containment of by-reference sources, time-varying resolution, and identity after the allocating document becomes unreachable all belong to future ASNs.)

---

Note on what was checked and held up: the S3★ weakest-precondition reduction to `(A j,i : a_j+i ∈ dom(Σ.C))`, the three-class tiling of X15 (`[1,p) ∪ [p,p+W) ∪ [p+W, n_S+W]`) across all boundary cases (`p=1`, `p=n_S+1`, `n_S=0`, `W > n_S−p+1`), the within-reference non-merge argument (source-V-adjacency + maximal-merge ⟹ not I-adjacent), and the full `ExtendedReachableStateInvariants`/P3/P4★/P4a/P7a discharge are all sound and complete. The five worked examples each exercise a genuinely distinct boundary (cross-origin fragmentation, self-transclusion pre-state pinning, empty-subspace first insert, append, coalescing merge) and are not redundant. Correctness is converged; the only outstanding item is the X14 prose.

VERDICT: REVISE
