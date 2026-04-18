# Cone Review — ASN-0034/TA2 (cycle 7)

*2026-04-18 12:41*

### TA2 sub-case (ii) identifies the divergence location using ZPD's defining property without citing ZPD

**Foundation**: ZPD (cited by TumblerSub) supplies the zpd function and its defining property — that `zpd(a, w)` is the first position at which the zero-padded sequences of `a` and `w` disagree. TumblerSub's Depends cites ZPD explicitly for exactly this purpose: "ZPD (ZPD) — defines `zpd(a, w)` and supplies the ZPD–Divergence relationship identifying `zpd(a, w) = divergence(a, w) = k` in case (i)."

**ASN**: TA2 (WellDefinedSubtraction), Case 2 sub-case (ii):

> "The padded sequences agree at all positions `i ≤ #w`. The divergence `k` falls at the first position `i > #w` where `aᵢ ≠ 0` — such a position must exist, for if `aᵢ = 0` at every `i > #w` the padded sequences would agree everywhere, contradicting the case hypothesis. At position `k`, `aₖ ≠ 0 = wₖ` (zero-padded…)."

TA2 sub-case (i) similarly concludes "making `j` the first padded divergence: `k = j`" from the observation that padded sequences agree before `j` and disagree at `j`. TA2's Depends list: TumblerSub, T0, T1, T3, NAT-sub, NAT-zero, NAT-order — no ZPD.

**Issue**: In both sub-cases, TA2 identifies the location of `k` (= zpd(a, w), inherited from TumblerSub's componentwise Definition) by reconstructing it: in sub-case (i), `k = j` where `j` is T1 case (i)'s witness; in sub-case (ii), `k` is the minimum of `{i > #w : aᵢ ≠ 0}`. Both identifications rest on ZPD's defining property — that `zpd(a, w)` is the *first* (least) position of padded disagreement. Without ZPD, the passage from "there is a position where they disagree" to "that position is `k`" is not discharged. TumblerSub cites ZPD for the structurally identical identification (`zpd(a, w) = divergence(a, w) = k` in case (i)), so the per-step convention applies. Citing TumblerSub does not propagate ZPD's property through to TA2 — TumblerSub's Postconditions expose `actionPoint(a ⊖ w) = zpd(a, w)` but not the first-disagreement characterization of zpd itself.

**What needs resolving**: TA2 must either (a) add ZPD to its Depends with per-site accounting for the two sub-case identifications (sub-case (i) `k = j` from T1 case (i)'s first-disagreement witness, sub-case (ii) `k = min{i > #w : aᵢ ≠ 0}` from ZPD's minimality combined with the non-emptiness argument), mirroring TumblerSub's ZPD citation; or (b) restructure TA2 to avoid locating `k` independently — relying only on TumblerSub's componentwise formula (`rᵢ = 0` for `i < k`, `rₖ = aₖ - wₖ`, `rᵢ = aᵢ` for `i > k`) without asserting where `k` falls, so the ZPD-level identification is not made at the TA2 layer.
