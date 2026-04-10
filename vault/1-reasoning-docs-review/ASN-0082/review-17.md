# Review of ASN-0082

I have examined every claim, every proof step, every boundary case, and every foundation citation in this ASN. The results are as follows.

**I3 postcondition and frame conditions.** The eight clauses (I3, I3-L, I3-X, I3-D, I3-V, I3-C, I3-CS, I3-CX) are precisely stated with clear quantifier domains. The preconditions — `#p ≥ 2`, `subspace(p) = S ≥ 1`, depth-compatibility with existing V-positions, `n ≥ 1` — are sufficient for every downstream derivation.

**Consistency argument.** I traced every pairwise disjointness claim:
- Shifted vs left: TS4 gives `shift(v, n) > v ≥ p > u` for `u < p`. Correct.
- Shifted vs shifted: TS2 (injectivity). Correct.
- Shifted vs cross-subspace: subspace preservation when `m ≥ 2` — shift copies position 1 from `v`, so `shift(v, n)₁ = v₁ = S`, disjoint from positions with subspace `≠ S`. Correct.
- Left vs cross-subspace: subspace `S` vs subspace `≠ S`. Correct.
- Vacated vs all assignment regions: the exclusion condition in I3-V makes I3-V and I3 disjoint by construction; I3-V requires `v ≥ p` (disjoint from I3-L's `v < p`); I3-V requires subspace `S` (disjoint from I3-X). Correct.
- Closure consistency: I3-CS and I3-CX close dom(M'(d)) from above, admitting only positions placed by I3, I3-L, and I3-X. I3-V removes a subset of positions that I3-CS independently excludes (neither left-region nor shifted-image). No contradiction. Correct.

**Gap exclusion.** The argument that no shifted image lands in `[p, shift(p, n))` is sound: when `v = p`, `shift(p, n)` is the exclusive upper bound (not in the gap); when `v > p` with `#v = #p = m`, TS1 gives `shift(v, n) > shift(p, n)`. Positions of depth `≠ m` in the gap are also excluded by I3-CS, since shifted images have depth `m` and left-region positions are `< p`. Correct.

**I3-V trace (worked example).** The overlap at position `[1, 5]` is correctly handled: it is both an original position (`v = [1, 5] ∈ dom(M(d))`) and a shift destination (`shift([1, 3], 2) = [1, 5]`). I3-V's exclusion condition prevents vacating; I3 assigns `M'(d)([1, 5]) = M(d)([1, 3]) = b + 2`. The original content `M(d)([1, 5]) = b + 4` is preserved at `M'(d)([1, 7]) = M(d)([1, 5])`. No content is lost or duplicated. Correct.

**Structural preservation derivations.** Each is explicitly argued:
- I3-VD (S8-depth): left region has depth `m` by S8-depth on `M(d)`; shifted region has depth `m` by TumblerAdd's result-length identity; other subspaces unchanged by I3-CX. Correct.
- I3-VP (S8a): three regions checked — left (S8a on pre-state), shifted (shift copies nonzero components 1..m−1, produces `vₘ + n > 0` at position `m`), cross-subspace (S8a on pre-state). Correct.
- I3-S3 (referential integrity): every post-state value equals some `M(d)(u)` for `u ∈ dom(M(d))`; S3 on pre-state gives `M(d)(u) ∈ dom(C)`; I3-C gives `dom(C') = dom(C)`. Correct.
- I3-S2 (functionality): pairwise disjointness of assignment regions ensures no double-assignment. Correct.
- I3-fin (finiteness): I3-CS and I3-CX bound dom(M'(d)) by subsets and injective images of finite dom(M(d)). Correct.

**Non-preservation of D-CTG, D-MIN, D-SEQ.** Correctly identified and confirmed by the worked example: `{[1,1], [1,2], [1,5], [1,6], [1,7]}` has a gap at `[1,3]`–`[1,4]`, violating all three. The deferral to the INSERT ASN is well-scoped.

**I3-S (SpanShiftPreservation).** The restriction to ordinal-level spans (`actionPoint(ℓ) = m`) is necessary — I verified that for `actionPoint(ℓ) = k < m`, `reach(σ') = [s₁,...,s_{k-1}, s_k + ℓ_k, ℓ_{k+1},...,ℓ_m]` while `shift(reach(σ), n) = [s₁,...,s_{k-1}, s_k + ℓ_k, ℓ_{k+1},...,ℓ_m + n]`, so part (a) genuinely fails when `k < m`.

For ordinal-level spans, the TA-assoc chain is valid: both applications have action points `m ≤ m` satisfying the preconditions. The commutativity `δₙ ⊕ ℓ = ℓ ⊕ δₙ` holds because both displacements have action point `m` and the components combine by `ℕ` addition. Part (b) follows from TumblerSub applied to `shift(reach(σ), n) ⊖ shift(s, n)`: the two shifted tumblers agree at positions 1..m−1 (both copy from originals that agree there, since `actionPoint(ℓ) = m`) and differ at position `m` by `ℓ_m`. Correct.

**Boundary cases.** Insert at start (I3-L vacuous, all positions shift), insert past end (I3 vacuous, all positions preserved), empty document (both vacuous) — all verified. Correct.

**Foundation citations.** Every reference is to ASN-0034, ASN-0036, or ASN-0053. No cross-ASN references to non-foundation ASNs. No reinvented notation — all definitions use foundation terms.

## REVISE

(none)

## OUT_OF_SCOPE

### Deletion shift (reverse displacement)
**Why out of scope**: Deletion would shift positions backward; this requires subtraction-based shift semantics and its own postcondition analysis. A future operation ASN, not an error here.

### Correspondence-run preservation under shift
**Why out of scope**: For a correspondence run `(v, a, n_run)` with `v ≥ p`, the shifted run `(shift(v, n), a, n_run)` is valid in M'(d) — this follows from I3 and `shift(v + k, n) = shift(v, n) + k` (by TS3-like reasoning). A natural corollary for a POOM or operations ASN to derive, not missing from this one.

VERDICT: CONVERGED
