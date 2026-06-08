# Review of ASN-0102

I read the full operation, the four invariant groups (X1–X16), the InvariantPreservation discharge (X17), and verified all five worked examples arithmetically against the effect clause. The tiling in X16, the wp reduction for S3★, the J1★/J1'★ routing via RR, and the cross-origin/coalescing merge analysis all hold. One precision defect remains.

## REVISE

### Issue 1: X14 calls copied positions "fresh," contradicting X17's own domain-delta accounting
**ASN-0102, X14 (ContainmentRecording)**: "Every member of `A` is mapped at a **fresh copied position** `v + c` (COPY effect clause, PC3), so `A ⊆ ran_{s_C}(Σ'.M(d))` at COPY's post-state."

**Problem**: In the displacing case (`p ≤ n_S`), the copied positions `v + c` for `c ∈ [0, W)` have last components `[p, p+W)`, which overlaps the pre-existing key range `[1, n_S]` on at least `{p}` (since `p ≤ n_S`). So position `v = [s_C,1,…,1,p]` is *not* a fresh key — it existed pre-state and is merely rebound. This directly contradicts X17's S8-fin computation, which correctly states `dom(Σ'.M(d)) ∖ dom(Σ.M(d)) = {[s_C,1,…,1,c] : n_S+1 ≤ c ≤ n_S+W}` — i.e., only `W` keys are genuinely new, and copied keys in `[v, n_S]` are *not* among them. Worse, "fresh" carries a loaded technical meaning in this specification (newly allocated, as in PC1 and the ASN-0093 freshness lemmas), so reusing it for "a position in the copied region" misleads a reader tracking which keys are new.

The conclusion `A ⊆ ran_{s_C}(Σ'.M(d))` does not depend on freshness — it holds because those positions are bound to `A` in `Σ'` regardless — so no downstream logic breaks; this is a wording defect, not a logical one.

**Required**: Drop "fresh." State it as "Every member of `A` is the image of a copied position `v + c` (`0 ≤ c < W`) in `Σ'.M(d)`," which is what the conclusion actually uses, and avoids the contradiction with X17 and the overloaded term.

## OUT_OF_SCOPE

(none — the four Open Questions correctly defer displacement-after-copy discoverability, transclusion-of-transcluded containment, time-varying views, and unreachable-allocator identity to future ASNs, and do not introduce claims here.)

VERDICT: REVISE
