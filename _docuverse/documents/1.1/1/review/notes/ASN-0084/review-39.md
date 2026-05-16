# Review of ASN-0084

## REVISE

### Issue 1: R-NS(NS-inv) catalog conflates non-S-applicable invariants with subspace-S-specific ones

**ASN-0084, R-NS lemma, clause (NS-inv) catalog**: "D-CTG, D-CTG-depth, D-MIN, D-SEQ, S8a (VPositionWellFormedness), S8-fin, S8-depth — all dom-only invariants — depend only on (i) and are preserved by (a)."

**Problem**: (NS-inv) is stated as preserving "ASN-0036 invariants evaluated at a V-position v with subspace(v) ≠ S ... that depends only on dom(M restricted to non-S positions) and on M restricted to non-S positions". But D-CTG, D-CTG-depth, D-MIN, and D-SEQ are stated about V_1(d) — subspace 1 = S — not non-S positions. Their preservation comes from the global dom(M'(d)) = dom(M(d)) argument (already covered in the earlier "Invariant preservation" paragraph), not from (NS-inv)'s non-S framework.

**Required**: Either narrow the (NS-inv) catalog to invariants whose non-S evaluation is meaningful (S8a, S8-fin, S8-depth's per-subspace clause for S' ≠ S), or split the catalog into "preserved by dom-preservation" and "preserved by non-S restriction" sub-lists with the appropriate justification for each.

### Issue 2: R-WP S8(a) discharge implicitly relies on R-COMM for run contiguity but doesn't cite it

**ASN-0084, R-WP proof, S8(a) subspace-S case**: "Phase 3 applies π to V-starts only, preserving widths ... The image of a partition of V_S(d) under a bijection is again a partition of V_S(d) (disjointness from injectivity; coverage from surjectivity), so the V-extents of the reassembled runs are pairwise disjoint and cover V_S(d)."

**Problem**: For a reassembled run (π(v_j), a_j, n_j) to have V-extent {π(v_j), π(v_j) + 1, ..., π(v_j) + n_j − 1} (a contiguous range), π must commute with shift on that run's positions — i.e., π(v_j + k) = π(v_j) + k. This is R-COMM. The proof correctly cites R-COMM for S8(b) but treats contiguity for S8(a) as if it followed from bijectivity alone. Without R-COMM, π could scatter a run's positions, and "image of a partition under a bijection" would yield a partition of V_S(d) into arbitrary sets, not into contiguous runs.

**Required**: Add an explicit invocation of R-COMM in the S8(a) argument, parallel to its use in the S8(b) discharge. The argument should be: each post-Phase-1 run lies in one region (Phase 1 splits at cut boundaries), R-COMM gives contiguity of the image, and bijectivity then gives the partition property.

### Issue 3: R-WP omits S7 (StructuralAttribution) from its invariant catalog

**ASN-0084, R-WP Q definition**: "M'(d) satisfies every ASN-0036 invariant carried by an arrangement transition — S0, S1, S2, S3, S4, S5, S7a, S7b, S7c, S7d, S9, D-CTG, D-CTG-depth, D-MIN, D-SEQ, S8a (VPositionWellFormedness), S8-fin, S8-depth, and S8 (SpanDecomposition)..."

**Problem**: S7 (StructuralAttribution, ASN-0036) is an ASN-0036 invariant — postcondition (d) explicitly states "origin(a) is invariant across all states in which a ∈ dom(Σ.C)". This is a state-invariance claim carried by every state transition, including arrangement rearrangements. The catalog lists the underlying axioms S7a–S7d but not the derived lemma S7. The "Invariant preservation" paragraph earlier in the ASN has the same omission.

**Required**: Either add S7 to the catalog explicitly (its preservation follows trivially from C' = C and the fact that origin(a) depends only on a's structure), or add a note explaining that S7 is preserved as a derived consequence of S7a–S7d preservation under C' = C.

### Issue 4: Necessity sketch addresses only one conjunct of R-PRE

**ASN-0084, R-WP, Necessity sketch paragraph**: "We do not enumerate the corresponding counterexamples for R-PRE(i), (ii), (iii), or (v); each conjunct guards a distinct construction step ... and a similar pre-state can be constructed for each."

**Problem**: The lemma name is "RearrangeSufficientPrecondition" and the statement uses ⇐, so sufficiency-only is honest about the claim. However, the necessity sketch promises that "a similar pre-state can be constructed for each" remaining conjunct without exhibiting one. For R-PRE(ii) (V_S(d) ≠ ∅) and R-PRE(v) (regions non-empty), the construction is non-trivial — a pre-state may satisfy ASN-0036 invariants vacuously when V_S(d) is empty, so the failure mode for R-PRE(ii) isn't analogous to R-PRE(iv)'s missing-source-reference failure.

**Required**: Either exhibit at least one additional counterexample (e.g., for R-PRE(v) with w_α = 0 or for CS2 violated), or explicitly delete the "similar pre-state can be constructed for each" claim and characterize the sketch as a single example demonstrating that R-PRE has at least one load-bearing conjunct.

## OUT_OF_SCOPE

### Topic 1: k-cut rearrangements for k > 4
**Why out of scope**: The ASN explicitly restricts to CS1 (n ∈ {3, 4}) and lists generalization as the first Open Question. This is correctly deferred to a future ASN; the present ASN's well-definedness and permutation lemmas would need to be reformulated for arbitrary k.

### Topic 2: Composition of multiple REARRANGEs
**Why out of scope**: Listed as the second Open Question. Whether the composition of two cut-point rearrangements is itself expressible as a single cut-point rearrangement is a structural question about the closure of the operation class, distinct from establishing the postconditions of a single REARRANGE.

### Topic 3: Documents with text-subspace depth > 2
**Why out of scope**: The ASN explicitly restricts to m_1 = 2 ("documents with m_1 > 2 are outside the scope of this ASN"). Generalizing to deeper subspaces would require reformulating the singleton-tumbler identification, cut-sequence widths, and displacement arithmetic. Reasonable deferral.

### Topic 4: Cross-subspace rearrangements
**Why out of scope**: REARRANGE is defined to operate only on subspace S = 1 (text). Rearranging across subspaces, or rearranging the link subspace, is explicitly excluded ("REARRANGE acts on the text region of a document and is not defined as a cross-subspace operation"). Belongs in a separate operation ASN if needed.

### Topic 5: Run-count bounds and conditions for canonical-partition increase
**Why out of scope**: The Open Questions section identifies bounds on run-count increase under REARRANGE as an open question. The present ASN constructively shows R-BLK produces a valid (non-maximal) partition and leaves the canonical-partition recovery to exhaustive merge; characterizing the canonical-partition delta would be a separate analysis.

VERDICT: REVISE
