# Review of ASN-0099

## REVISE

### Issue 1: Worked example F10 case-(ii) verification has incorrect intermediate reasoning

**ASN-0099, "Verifying F10 across a version extension (T1 case (ii))"**: "For the `ℓ'' vs ℓ'` comparison, at position `#d_a + 1`: `b_L(d_c)[#d_a + 1] = 1` while `b_L(d_b)[#d_a + 1] = (d_b)_{#d_a + 1}`, and since `d_b = inc(d_a, 0)` produces a sibling that increments only the last component of `d_a` (TA5(c)), `(d_b)_{#d_a + 1}` does not exist — `d_b`'s length equals `d_a`'s length, both being depth-`#d_a` documents under the same account. The comparison `ℓ'' vs ℓ'` is therefore decided at an earlier position."

**Problem**: The equation `b_L(d_b)[#d_a + 1] = (d_b)_{#d_a + 1}` is wrong. `b_L(d_b) = [d_b, 0, s_L]` has length `#d_b + 2 = #d_a + 2`, so position `#d_a + 1` of `b_L(d_b)` is the appended separator `0` (well-defined), not `(d_b)_{#d_a + 1}` (which indeed doesn't exist). The ASN's own body proof of F10 handles the analogous case correctly: "at position `#d₁+1`, `b_L(d₁)` has the appended `0` separator while `b_L(d₂)` has `d₂_{#d₁+1} ≥ 1`". The conclusion `ℓ'' < ℓ'` is correct, but the divergence is actually decided at position `#d_a` where `b_L(d_c)[#d_a] = d_c[#d_a] = d_a[#d_a]` while `b_L(d_b)[#d_a] = d_b[#d_a] = d_a[#d_a] + 1`, by TA5(c) + TA5-SigValid — not because position `#d_a + 1` is somehow ill-defined.

**Required**: Rewrite the intermediate reasoning to correctly identify the divergence position. The clean argument: `d_c` agrees with `d_a` on positions `1..#d_a`, while `d_b[#d_a] = d_a[#d_a] + 1`; both anchors inherit their documents' components on those positions; so at position `#d_a`, `b_L(d_c)[#d_a] < b_L(d_b)[#d_a]`, and T1 case (i) at position `#d_a` yields `b_L(d_c) < b_L(d_b)`, with non-nesting verified separately.

### Issue 2: Citation error for D-SEQ★

**ASN-0099, Worked Example setup**: "Its arrangement, by D-SEQ★ (ASN-0036), is `Σ.M(d_a) = {v_a^1 ↦ α₁, v_a^2 ↦ α₂, v_a^3 ↦ α₃}`..."

**Problem**: D-SEQ★ (PerSubspaceSequentialPositions) is defined in ASN-0047, not ASN-0036. ASN-0036 contains the unstarred D-SEQ (SequentialPositions); the starred per-subspace generalization is introduced by ASN-0047's extended state.

**Required**: Correct the citation to "(D-SEQ★, ASN-0047)".

VERDICT: REVISE
