# Review of ASN-0036

## REVISE

### Issue 1: OrdShiftHom omits subspace preservation as an explicit postcondition

**ASN-0036, OrdShiftHom contract (`Postconditions`)**: Lists only "(a) `ord(shift(v, n)) = shift(ord(v), n)`" and "(b) When `v` satisfies S8a, `shift(v, n)` satisfies S8a unconditionally".

**Problem**: The corollary's body says "OrdAddHom applies." OrdAddHom delivers three postconditions: (a) ord-homomorphism, (b) `subspace(v ⊕ w) = subspace(v)`, and (c) full decomposition via vpos. OrdShiftHom transfers (a) but silently drops (b). Subspace preservation is precisely the property that makes "shifts stay within a subspace" — the architectural point of the ord/vpos/w_ord decomposition. S8a preservation alone is strictly weaker: S8a is satisfied by element-field tumblers in any subspace, not just the input's, so a consumer cannot conclude `shift(v, n)₁ = v₁` from OrdShiftHom's contract. Tellingly, the S8 within-subspace incompatibility lemma derives subspace preservation inline from TumblerAdd's prefix rule rather than citing OrdShiftHom, which would otherwise be the natural call site.

**Required**: Add a postcondition `(c) subspace(shift(v, n)) = subspace(v)` to OrdShiftHom, derived from OrdAddHom (b) at `w = δ(n, m)` (whose `w₁ = 0` since `#δ(n, m) = m ≥ 2`). Without this, the corollary is not self-contained as a black-box and the subspace-preservation narrative requires extra inline reasoning at each consumer site.

### Issue 2: OrdAddHom and OrdAddS8a case analyses have unacknowledged empty branches at k = 2 and k = m

**ASN-0036, OrdAddHom proof part (a)**: "By TumblerAdd for `ord(v) ⊕ w_ord`: — For 1 ≤ j < k-1 ... — At j = k-1 ... — For k-1 < j ≤ m-1 ..."

**Problem**: At the minimal action point `k = 2` (forced by `w₁ = 0`), the first case `1 ≤ j < k - 1` reduces to `1 ≤ j < 1` — empty. At the maximal action point `k = m`, the third case `k - 1 < j ≤ m - 1` reduces to `m - 1 < j ≤ m - 1` — also empty. The proof works at both boundaries (the j = k - 1 case carries the advance in both regimes), but the reader must independently verify boundary behavior. Boundary cases are mandatory under Dijkstra's standards: empty, first, last must be handled explicitly. The analogous issue appears in OrdAddS8a: "Components r₁ through r_k are unconditionally positive" uses a case `2 ≤ i < k` that is empty at `k = 2`, and the symmetric range `k < i ≤ m` is empty at `k = m` (making S8a satisfaction vacuous in that boundary).

**Required**: Add a sentence to OrdAddHom's case analysis acknowledging both boundary regimes: at `k = 2` the first case is empty (only j = k − 1 = 1 and tail-copy contribute); at `k = m` the third case is empty (only copy-from-start and j = k − 1 = m − 1 contribute). Apply the analogous acknowledgement to OrdAddS8a's component analysis at both boundaries.

### Issue 3: "Beyond position m" wording in the within-subspace incompatibility lemma misrepresents δ(1, m)'s structure

**ASN-0036, S8 within-subspace incompatibility lemma Setup**: "at the action point, shift(v, 1)_m = v_m + 1 (NAT addition on the last component; no carry, since δ(1, m) is zero beyond position m)."

**Problem**: `δ(1, m)` is a tumbler of length exactly m by OrdinalDisplacement (ASN-0034). There are no positions "beyond position m" in δ(1, m). The intended explanation — that tumbler component-wise addition has no carry-propagation — is correct, but the supporting justification "δ(1, m) is zero beyond position m" describes nothing that exists. A careful reader checking the boundary could be misled into thinking δ(1, m) extends past its declared length with zero padding.

**Required**: Reword to "no carry, since tumbler addition is component-wise and the addition at position m does not propagate to other positions of the result". Avoid framing that suggests δ(1, m) has positions beyond its declared length.

## OUT_OF_SCOPE

(None — the ASN explicitly defers operations-layer concerns, subspace alignment, and link-subspace contiguity to its Scope section, Open Questions list, and operations-layer ASNs.)

VERDICT: REVISE
