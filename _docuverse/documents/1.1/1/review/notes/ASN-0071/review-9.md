# Review of ASN-0071

## REVISE

### Issue 1: Finiteness bound conflates elementary and composite transition counts

**ASN-0071, Finiteness (F-FIN)**: Step (b): "Each elementary transition adds at most one entity to `E_doc`." Step (c): "the count `n` of transitions producing any reachable `Σ` is a finite natural number. Combining: `|Σ.E_doc| ≤ n < ∞`."

**Problem**: Step (b) bounds growth *per elementary transition*, but step (c) draws its count `n` from "a finite sequence of valid **composite** transitions" (ExtendedReachableStateInvariants). A single valid composite is a finite sequence of atomic transitions and may fire several K.δ steps (e.g. node → account → document creation in one composite). So `|Σ.E_doc| ≤ n` with `n` = composite count is not established by step (b) and is false in general — `|E_doc|` can exceed the number of composites. The conclusion `|E_doc| < ∞` still holds, but the stated inequality is unsupported.

**Required**: Either let `n` count *elementary* transitions (each composite is a finite sequence of elementary steps; finitely many composites ⟹ finite elementary total ⟹ `|E_doc| ≤ n_elem < ∞`), or drop the exact `≤ n` bound and argue finiteness directly from "finitely many composites, each a finite sequence, each step adds ≤ 1 entity."

### Issue 2: The resolve-relationship equation is asserted without derivation

**ASN-0071, Resolution**: "The relationship to ASN-0058's `resolve` is direct: when a vspec `(d_s, σ)` is also a well-formed ContentReference, `iaddrs_one(d_s, σ)(Σ)` equals the set-flattening of `resolve(d_s, σ)` — concretely, `{ a + k : (a, n) ∈ resolve(d_s, σ) ∧ 0 ≤ k < n }`."

**Problem**: This is an asserted equation, not a definitional unfolding — "is direct" is doing the work of a proof. `resolve` is built from the unique maximally merged decomposition of `M(d_s)|⟦σ⟧` (C1a); equating its set-flattening to `{M(d_s)(v) : v ∈ ⟦σ⟧ ∩ dom(M(d_s))}` requires noting that (i) the decomposition's domain is exactly `⟦σ⟧ ∩ dom(M(d_s))`, and (ii) the blocks' I-addresses `a_j + k = M(d_s)(v_j + k)` enumerate precisely the images (B3/Consistency), with set-flattening absorbing any duplicate I-addresses. None of this is shown.

**Required**: Add the one-step argument (decomposition covers `dom(f) = ⟦σ⟧ ∩ dom(M(d_s))`; block consistency gives `a_j+k = M(d_s)(v_j+k)`; flattening dedupes shared I-addresses), or demote the claim to an explicitly-informal remark.

## OUT_OF_SCOPE

The Open Questions (relationship to `R`, distributed/replica completeness, visibility filtering, contraction-transition invariant) are correctly deferred to future ASNs rather than claimed here. No action needed.

VERDICT: REVISE
