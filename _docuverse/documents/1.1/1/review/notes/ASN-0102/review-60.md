# Review of ASN-0102

## REVISE

### Issue 1: P4★ discharge in X14 is dominated by defensive meta-prose

**ASN-0102, X14, the "P4★ (`Contains_C ⊆ R`), discharged at the composite boundary" paragraph**: the paragraph states three times, in different words, that P4★ is not a per-step invariant and that K.μ⁺ refutes any such invariant:

- "P4★ is a composite-boundary property, not a per-state invariant: it need not hold at the mid-composite state Σ. A K.μ⁺ step grows Contains_C without growing R … which is exactly why P4★ is asserted only at boundaries."
- "We therefore do *not* argue by a per-elementary-step invariant Contains_C ⊆ R; K.μ⁺ refutes any such invariant, and the premise (i)/(ii) at B gives only R_B ⊆ Σ.R, never Contains_C(Σ) ⊆ Σ.R."
- "… by induction on boundaries … never via a per-elementary-step invariant Contains_C ⊆ R."

**Problem**: This is defensive prose explaining why a *rejected* proof strategy fails, restated repeatedly. The actual proof — boundary induction (base `Σ₀`, step from P4★ at `B` plus composite-wide J1★) — is two sentences. The reader must skip three K.μ⁺-refutation restatements to reach it. This is exactly the forward-reference/anti-bloat accretion the review mode targets.

**Required**: State the K.μ⁺-refutation point once (or as a single subordinate clause), then give the boundary induction directly. Delete the repetitions.

### Issue 2: Duplicated "COPY records every address it places" across the J1★ and P4★ paragraphs

**ASN-0102, X14, J1★ bullet vs. P4★ paragraph**: the J1★ bullet establishes "the only s_C-range growth COPY's own step contributes is `New` … and COPY records `(a, d)` for every `a ∈ A ⊇ New`"; the P4★ paragraph re-derives the identical fact: "the sole s_C-range growth at COPY's own step is `New`, every member of which COPY writes into `Σ'.R`."

**Problem**: The same step-local frame fact is proved twice in adjacent paragraphs. Two paragraphs saying the same thing in different words.

**Required**: Establish the step-local fact (COPY's only `s_C`-range growth is `New`, all of which it records) once, and have both the J1★ and P4★ arguments cite it.

## OUT_OF_SCOPE

(none — the open-questions section correctly defers re-displacement discoverability, transitive containment records, and origin-after-unreachability to future ASNs rather than asserting claims about them.)

Note on substance: the mathematical content is sound. The tiling in X16 (`[1,p) ∪ [p,p+W) ∪ [p+W,n_S+W]`) verifies for the full range `1 ≤ p ≤ n_S+1` including append (`p = n_S+1`) and first-insertion (`n_S = 0, p = 1`); the wp reduction to the copied region, the J1'★ split at the opening boundary `B` (rather than the unsound mid-composite `Σ`), the X8 within-vs-across-reference merge case split, and the full ExtendedReachableStateInvariants conjunct discharge are each complete. The five worked examples exercise distinct boundary configurations (cross-origin, overlapping self-transclusion, empty subspace, append, coalescing) and are legitimate concrete verification, not bloat. The findings above are confined to prose accretion in X14.

VERDICT: REVISE
