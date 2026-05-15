# Review of ASN-0084

## REVISE

### Issue 1: w_μ ≥ 1 derivation lacks explicit V-position witness

**ASN-0084, "Consequences of R-PRE" → "Middle region non-empty (n = 4 only)"**: "CS2 forces c₁ < c₂, so [c₁, c₂) is non-empty as a set of ordinals; combined with R-PRE(iv) (every position in [c₀, c₃) ∩ V_S(d) is well-defined), [c₁, c₂) ∩ V_S(d) is non-empty, i.e., w_μ ≥ 1."

**Problem**: R-PRE(iv) is a universal implication ("every v satisfying the LHS lies in V_S(d)"), not an existence statement. The leap from "ordinal range [c₁, c₂) is non-empty" to "the V-position set [c₁, c₂) ∩ V_S(d) is non-empty" requires identifying a specific V-position in the intersection. The derivation elides this bridge. This matters because w_μ ≥ 1 is consumed by R-DISP, R-BLK, and the well-definedness arguments for R-SWP — a missing existence step at the foundation propagates everywhere.

**Required**: Identify the witness explicitly. c₁ itself works: subspace(c₁) = S (CS3), #c₁ = 2 (CS4), and c₁ < c₃ = c_{n-1} (CS2 gives c₁ < c₂ < c₃). Hence by R-PRE(iv), c₁ ∈ V_S(d); trivially c₁ ∈ [c₁, c₂); so [c₁, c₂) ∩ V_S(d) is non-empty and w_μ ≥ 1.

### Issue 2: R-BLK Phase 1 closing uses interval notation for a discrete set

**ASN-0084, R-BLK Phase 1**: "After all cuts are processed, no run straddles any cut position in [c₀, c_{n−1}]."

**Problem**: The notation `[c₀, c_{n−1}]` is interval notation typically denoting all positions between c₀ and c_{n−1} inclusive. The intended meaning is the discrete set of cuts {c₀, c₁, ..., c_{n−1}}. A reader could parse this as "no run straddles any V-position in this interval", which is a different (and false) claim — runs do lie inside cut-bounded regions.

**Required**: Rephrase as "no run straddles any cut position c_i for 0 ≤ i ≤ n−1" or "no c_i is strictly interior to the V-extent of any run".

### Issue 3: Forward/backward extent maxima existence asserted without bound

**ASN-0084, CanonicalRunDecomposition (a)**: "f(v) = max{k ≥ 0 : (A j : 0 ≤ j ≤ k : v + j ∈ dom(M(d)) ∧ M(d)(v + j) = M(d)(v) + j)}. This maximum exists because dom(M(d)) is finite (S8-fin)."

**Problem**: The well-ordering argument requires (i) the set is non-empty and (ii) the set is bounded above. The ASN handles non-emptiness implicitly (k = 0 always satisfies the condition via the identity convention), but the boundedness argument leans on S8-fin without identifying the bound. The natural bound is N − ord(v) where V_S(d) = {[S, 1], ..., [S, N]} by D-SEQ — beyond this k, v + k ∉ V_S(d) violates the first conjunct. The same gap applies to r(v).

**Required**: Note the bound explicitly: by D-SEQ, V_S(d) is finite with maximum ordinal N, so the set is bounded above by N − ord(v) for f(v) and by ord(v) − 1 for r(v); existence of the max then follows from NAT-wellorder applied to the bounded non-empty subset of ℕ.

## OUT_OF_SCOPE

(None — the Open Questions section already catalogues legitimate future work: k-cut rearrangements for k > 4, composition of rearrangements, run-count change bounds, and constraints between cut positions and run boundaries. The text-subspace restriction is acknowledged explicitly.)

VERDICT: REVISE
