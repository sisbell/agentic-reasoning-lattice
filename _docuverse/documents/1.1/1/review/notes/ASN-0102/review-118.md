# Review of ASN-0102

I checked the load-bearing parts specifically: the `wp(COPY, S3★)` reduction, the X15 last-component tiling, the exhaustive invariant discharge in X16 (every conjunct of `ExtendedReachableStateInvariants` plus P4★/P4a/P7a/P3), the cross-origin non-merge (X7/X10), and the self-transclusion pre-state pinning. They hold up.

## REVISE

No REVISE items.

Specifics I verified rather than assumed:

- **Boundary cases are all present and exercised by distinct worked examples** — empty subspace first-insertion (`n_S = 0`, depth choice + pin), append (`p = n_S+1`, trailing boundary absent), self-transclusion with source inside the displaced region (`d_s = d`, pre-state pinning, already-referenced address so no new provenance), cross-origin fragmentation (no merge), and the coalescing case (inter-reference + leading boundary both firing, `canonical < k`). Each bites different claims.
- **`wp(COPY, S3★)` is non-trivial and correctly reduced.** The three V-position classes (unmoved/displaced/copied) are partitioned correctly; the `s_L`-routing conjunct is genuinely discharged (COPY introduces/alters no link position), and the residual obligation `a_j+i ∈ dom(Σ.C)` is met by C1 via PC1.
- **X15 tiling is sound.** `[1,p) ∪ [p,p+W) ∪ [p+W,n_S+W] = [1,n_S+W]` holds for all `1 ≤ p ≤ n_S+1`, including the degenerate `p=1` (empty unmoved) and `p=n_S+1` (empty displaced). S2 functionality is fully discharged via within-`s_C` disjointness (tiling) plus cross-subspace component-1 distinctness — not hand-waved.
- **Provenance routing (RR, J1★/J1'★) is correct.** The carried/recorded route split is exhaustive, and the "already-referenced ⟹ already in R via P4★ at Σ₀" argument closes the J1'★ obligation with no gap.
- **No I-coordinate is rewritten** (X4/X10 origin reasoning rests on M16/M16a + GlobalUniqueness, all foundation), and the displaced runs remain lockstep correspondence runs, so S8★ survives.
- **Cross-ASN references** are all to foundation ASNs (0034, 0036, 0047, 0058, 0093) — no violation.

Anti-bloat pass: the prior cycles' targets (X9 header gloss, X14 atomicity rationale) appear already condensed; the remaining `Gregory`/Q-trace citations are implementation evidence the standards endorse, and the X16 "composite-boundary reading" paragraph is load-bearing (it licenses invoking P4★/P4a/P7a at a single elementary transition). I found no residual meta-prose the precise reader must work around.

## OUT_OF_SCOPE

The four Open Questions (later re-displacement and discoverability, transitive containment when a referencing document is itself a source, time-varying resolution views, identity when the allocating document is unreachable) are correctly framed as future work, not claims — no action needed.

VERDICT: CONVERGED
