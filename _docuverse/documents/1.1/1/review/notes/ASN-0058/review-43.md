# Review of ASN-0058

## REVISE

### Issue 1: M-int's Component-m reduction step lacks explicit T1 derivation

**ASN-0058, M-int proof, Component-m reduction paragraph**: "By depth and prefix agreement, y and x agree on components 1..m−1 and share depth m; the comparison x ≤ y < x + n reduces to component m: (x)_m ≤ (y)_m < (x)_m + n. Set k = (y)_m − (x)_m; then 0 ≤ k < n."

**Problem**: The "reduces to component m" step is load-bearing — establishing (x)_m ≤ (y)_m is necessary for the subtraction k = (y)_m − (x)_m to yield a natural number under NAT-sub, and (y)_m < (x)_m + n is necessary for k < n. The earlier M-int paragraphs (Subspace agreement, Prefix agreement) carry out T1 case analysis in detail with explicit case (ii) exclusion and witness identification. The Component-m reduction becomes terse precisely where the same T1 machinery applies again.

**Required**: Make the two T1 derivations explicit.
- For (x)_m ≤ (y)_m: case-split on x = y versus x < y. The x = y case gives (x)_m = (y)_m by T3. The x < y case excludes T1 case (ii) by equal depth #x = #y = m, applies T1 case (i) under prefix agreement at 1..m-1 to pin divergence at m, and yields (x)_m < (y)_m. Either branch concludes (x)_m ≤ (y)_m.
- For (y)_m < (x)_m + n: precondition y < x + n with #y = #(x + n) = m (TA0's result-length identity). T1 case (ii) is excluded by equal depth; T1 case (i) under transitively-established prefix agreement (y agrees with x at 1..m-1; (x + n)_i = x_i for i < m by TumblerAdd's prefix-copy at action point m) pins divergence at m, giving (y)_m < (x + n)_m = (x)_m + n.

### Issue 2: M12a's Equal Starts argument quietly handles the k₂ = 0 case via a "skip ahead" that needs explicit verification

**ASN-0058, M12a proof, Equal Starts paragraph**: "If already v₁ = v₂, set k₂ = 0 and skip ahead."

**Problem**: The "skip ahead" leaves it implicit that the Equal Widths argument (which assumes a₂ = a₁ + k₂) works when k₂ = 0. The Equal Widths argument's contradiction relies on v_1 + n_1 ∈ V(R_2) leading to a contradiction with R_1's condition 3 (and symmetrically); the proof presents this with the implicit assumption that v_1 = v_2 holds via k_2 = 0, but never explicitly walks through how Equal Widths discharges in that boundary case.

**Required**: Either (a) state explicitly that when k₂ = 0 (so v₁ = v₂ and a₂ = a₁), Equal Widths' n₁ < n₂ branch derives f(v₁ + n₁) = a₂ + n₁ = a₁ + n₁ via R₂'s condition 1 at offset n₁ < n₂, contradicting R₁'s condition 3; or (b) restructure to do Equal Widths first (without depending on Equal Starts) and then derive Equal Starts.

### Issue 3: Two sections share the heading "A Worked Example"

**ASN-0058**: One worked example follows M12 (8 V-positions, three I-jump scenario), another follows C2 (6 V-positions, content reference resolution).

**Problem**: Both sections are titled "A Worked Example", making cross-reference and table-of-contents navigation ambiguous.

**Required**: Distinguish them — e.g., "A Worked Example (Canonical Decomposition)" and "A Worked Example (Content Reference Resolution)".

## OUT_OF_SCOPE

None. The ASN's coverage (mapping block algebra, canonical decomposition, content reference resolution) is appropriately within its declared scope. The Open Questions section captures legitimate future work (lattice structure of equivalent decompositions, I-space discontinuity characterization, multi-source reordering constraints) without overreaching.

VERDICT: REVISE
