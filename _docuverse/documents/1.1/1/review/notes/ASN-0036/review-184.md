# Patch Review of ASN-0036

## REVISE

### Issue 1: S8 was not restored to the correspondence-run form — the central instruction of the patch
**ASN-0036, "Correspondence-run partition" / S8**: The document still defines **S8 (Singleton span partition)**: "the singleton intervals `{[vⱼ, shift(vⱼ, 1)) : vⱼ ∈ dom(Σ.M(d))}` — one per V-position — partition the V-positions."
**Problem**: The patch's primary directive was: *"Restore S8 to the correspondence-run form: `dom(M(d))` decomposes into finitely many runs `(vⱼ, aⱼ, nⱼ)` with `M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` for `0 ≤ k < nⱼ`. Runs partition `dom(M(d))`; maximal runs are unique. Prove it non-vacuously by constructing maximal runs."* This was not done. S8 remains the singleton form — which the patch instruction itself flagged as "vacuous (S2 + S8-fin restated)." The within-subspace incompatibility lemma proves only `t ∉ [v, shift(v, 1))` (singleton uniqueness); there is no run `(vⱼ, aⱼ, nⱼ)`, no displacement identity `M(d)(shift(vⱼ, k)) = shift(aⱼ, k)`, and no maximal-run construction or uniqueness claim anywhere in the proof.
**Required**: Replace the singleton S8 with the correspondence-run statement and prove it non-vacuously: construct maximal runs by forward/backward extension while the displacement identity holds; derive existence and uniqueness from maximal extension; derive partition from extensivity and pairwise disjointness.

### Issue 2: Section intro asserts run structure that S8 does not deliver
**ASN-0036, "Correspondence-run partition" intro**: "the mapping decomposes into finitely many *correspondence runs* — maximal contiguous blocks of V-positions whose images advance in lockstep with them under ordinal displacement. This run structure, **not a position-by-position listing**, is the strand model's central architectural claim about arrangements; we establish it here."
**Problem**: S8 establishes exactly a position-by-position (singleton) listing — the opposite of what the prose claims is established. The intro is internally contradicted by the theorem it introduces. Compounding this, the Open Question "Must every arrangement admit a unique *maximal* correspondence-run decomposition…" treats run-uniqueness as open, while the intro claims it was just established.
**Required**: Once S8 is restored (Issue 1), this prose becomes accurate and the maximal-decomposition Open Question should be removed or rewritten, since S8 would settle it.

### Issue 3: Worked example does not exercise conjunct (b) at `k ≥ 1`
**ASN-0036, "Worked example", state Σ₁**: "*Verify S8 (singleton partition)*: each of the five V-positions is its own singleton… conjunct (b) holds at each: `M(d₁)(1.k) = 1.0.1.0.1.0.1.k`."
**Problem**: The patch instructed: *"Exercise conjunct (b) at some `k ≥ 1` in the worked example."* The example only verifies singletons (run length 1, `k = 0`). The "hello" arrangement in Σ₁ is in fact a single run `(v₀ = [1,1], a₀ = …1.1, n = 5)` for which `M(d₁)(shift(v₀, k)) = shift(a₀, k)` holds at `k = 1,2,3,4` — the natural place to exercise conjunct (b) at `k ≥ 1`. This was not done.
**Required**: After restoring S8, exhibit the displacement identity `M(d)(shift(vⱼ, k)) = shift(aⱼ, k)` at a concrete `k ≥ 1` (e.g. the length-5 "hello" run, and the broken run at the transclusion/append boundary in Σ₂).

### Issue 4: Newly added claims are absent from the Properties Introduced registry
**ASN-0036, "Properties Introduced" table**
**Problem**: The patch added S7c, ShiftPreservation, the V-position ordinal vocabulary (ord, vpos, w_ord), and the lemmas OrdAddHom, OrdAddS8a, OrdShiftHom. None of these appear in the registry table. `subspace_I` (defined in S7c) is also unlisted.
**Required**: Add registry rows for S7c, ShiftPreservation, ord, vpos, w_ord, OrdAddHom, OrdAddS8a, OrdShiftHom (with correct types — DEF/LEMMA/COROLLARY — and dependency notes).

### Issue 5: Ordinal-decomposition lemmas are orphaned (no downstream consumer)
**ASN-0036, "V-position ordinal decomposition" subsection**
**Problem**: ShiftPreservation and the entire ord/vpos/w_ord/OrdAddHom/OrdAddS8a/OrdShiftHom apparatus were restored as the machinery the correspondence-run S8 proof needs (shift commutes with the decomposition, structure preserved under shift). But because S8 was never converted (Issue 1), nothing in the document consumes them — S8 cites `OrdinalShift` directly, not `OrdShiftHom`, and no run construction invokes them. As added, they are dead weight.
**Required**: The restored S8 correspondence-run proof must actually cite this machinery (OrdShiftHom for the lockstep displacement identity, ShiftPreservation for structural inheritance along a run). If the restored S8 genuinely does not need them, justify their retention or remove them.

VERDICT: REVISE
