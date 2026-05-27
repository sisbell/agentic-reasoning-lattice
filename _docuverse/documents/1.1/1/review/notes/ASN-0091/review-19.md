# Review of ASN-0091

## REVISE

### Issue 1: S8★ (PerSubspaceSpanDecomposition, ASN-0047) not explicitly discharged at Σ'

**ASN-0091, "REARRANGE as Vstream-Only Operation"**: The admissibility discussion lists ASN-0047 extended invariants discharged separately by REARRANGE_K — "S3★ (generalised referential integrity), S3★-aux (subspace exhaustiveness), CL-OWN (link-subspace ownership), CL-UNIQ (link-subspace position uniqueness), and P4★ (content-subspace provenance bound)" — but S8★ is omitted.

**Problem**: S8★ is also an ASN-0047 invariant. After REARRANGE, the assignment of I-addresses to V-positions has been permuted via π, so the pre-state decomposition does not transfer verbatim — a new decomposition is needed at Σ'. R-SP (the cited mechanism for discharging ASN-0036 invariants) does not include S8★ in its postcondition Q. The Worked Example admissibility traces also skip S8★. A downstream consumer cannot tell from this ASN whether S8★ holds at Σ'.

**Required**: Add explicit discharge. The content-subspace clause follows from R-SP's discharge of ASN-0036's S8 at Σ' (M'(d)|_{V_{s_C}(d)} is a finite partial function with uniform depth satisfying S3, so ASN-0036's S8 applies). The link-subspace clause follows from RE-sub: M'(d)|_{V_{s_L}(d)} = M(d)|_{V_{s_L}(d)}, so the pre-state trivial length-1 decomposition carries over verbatim. State this in both the abstract admissibility section and in each Worked Example's admissibility verification.

### Issue 2: ChainDisjointAdjacency inline lemma proof is incomplete in the prefix case

**ASN-0091, inline lemma in "Reverse witness (coalescence)"**: "If d_X ≠ d_Y, then x ∈ A_{s_X}(d_X) and y ∈ A_{s_Y}(d_Y) disagree on at least one of positions 1..min(#d_X, #d_Y), so y ∉ A_{s_X}(d_X) (hence y is not the chain successor of x) and symmetrically."

**Problem**: The disagreement-in-1..min claim fails when one document is a proper prefix of the other. Take d_X = [1, 0, 1, 0, 1] (length 5, zeros = 2) and d_Y = [1, 0, 1, 0, 1, 1, 1] (length 7, zeros = 2). Both are T4-valid documents; d_X ≺ d_Y, so they agree on positions 1..#d_X = 1..min(#d_X, #d_Y). The argument as stated does not exclude y from A_{s_X}(d_X) in this case — the actual exclusion goes through ChainUniformLength (ASN-0093), since elements of A_{s_X}(d_X) have uniform length #d_X + 3 ≠ #d_Y + 3. The conclusion holds but the proof has a hole.

**Required**: Recast the argument structurally. Cleanest form: x + 1 = [d_X, 0, s_X, k_x + 1] under TA5(c); for y = x + 1, we'd need y to equal [d_X, 0, s_X, k_x + 1]; but y ∈ A_{s_Y}(d_Y) forces y = [d_Y, 0, s_Y, k_y], so equality demands (d_X, s_X, k_x + 1) = (d_Y, s_Y, k_y) — impossible under (d_X, s_X) ≠ (d_Y, s_Y). This is uniform across length cases.

### Issue 3: In-cut-subspace exterior pointwise fixity is exercised but not lifted to a named RE-* claim

**ASN-0091, Claims Introduced table**: RE-sub covers V-positions with subspace(v) ≠ S (the link-subspace fixity). No analogous claim covers V-positions in V_S(d) outside the affected range [c₀, c_{n-1}).

**Problem**: REARRANGE_K leaves in-S exterior V-positions pointwise fixed — both π(v) = v (R-PPERM/R-SPERM exterior branch) and Σ'.M(d)(v) = Σ.M(d)(v) (R-EXT, ASN-0084). This is exercised explicitly in Worked Example 3 ("Interior Cuts (R-EXT Exercised)"), where the prose says "R-EXT (left exterior). [1, 1] ∈ V_S(d) and [1, 1] < c₀ = [1, 2], so R-EXT fires." The property is REARRANGE_K-specific (RA-adm + S3★ + L14 only force subspace preservation, allowing within-subspace permutation under the abstract class), so it cannot be derived from any other RE-* claim. The omission is asymmetric with RE-sub, which is also REARRANGE_K-specific pointwise fixity. The Claims table is otherwise comprehensive — this is a coverage gap.

**Required**: Add a named claim (e.g., RE-ext) covering the in-S exterior: for every v ∈ V_S(d) with v < c₀ or v ≥ c_{n-1}, π(v) = v and Σ'.M(d)(v) = Σ.M(d)(v). Cite R-PPERM/R-SPERM exterior branch (for π) and R-EXT (for arrangement). Add it to the Claims Introduced table with provenance "REARRANGE_K" alongside RE-sub, and supply a corresponding RE-ext★ entry in the multi-step composition table.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
