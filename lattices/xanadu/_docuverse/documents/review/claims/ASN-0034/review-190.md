# Cone Review — ASN-0034/TA5a (cycle 5)

*2026-04-17 19:05*

### TA5a's Depends list omits NAT-* axioms despite invoking ℕ-facts
**Foundation**: NAT-zero (NatZeroMinimum), NAT-discrete (NatDiscreteness), and NAT-closure (NatArithmeticClosure) — each stated as a separate foundation object in T0, with the explicit convention "Each proof cites only the ℕ facts it actually uses". T0 in the current ASN text disclaims any standalone authority for ℕ-arithmetic inferences.
**ASN**: TA5a, case-analysis preface:
> "Positivity of non-zero components is not a separate T4 clause; it is supplied by T0's carrier ℕ."

TA5a, case `k = 0`:
> "The post-increment value `t_{sig(t)} + 1` is then non-zero as well, as the successor of a non-zero natural."

TA5a, case `k ≥ 3`:
> "By TA5(d), the appended sequence has `k - 1 ≥ 2` consecutive zero components..."

TA5a's *Depends* lists only T4, T4a, T0, TA5, TA5-SigValid — no NAT-* axioms at all.
**Issue**: Three distinct ℕ-inferences are consumed in the proof without any NAT-* citation. (1) The preface attributes "positivity of non-zero components" to T0's carrier alone — exactly the mis-attribution the ASN has explicitly corrected elsewhere (T4a, T4c, TA5-SigValid, TA5), where the trio T0 + NAT-zero + NAT-discrete is cited jointly for this same "non-zero ⇒ strictly positive on ℕ" step. T0's own contract now says the NAT-* axioms are stated separately so each proof cites only what it uses; TA5a instead uses the collapsed attribution the ASN has moved away from. (2) The case `k = 0` step "successor of a non-zero natural" has no NAT-* citation, although it requires at minimum NAT-addcompat (`n < n + 1`, or equivalently `n + 1 > n ≥ 0`) and/or NAT-closure to place `t_{sig(t)} + 1` in ℕ and then guarantee it is non-zero. TA5's own Depends has been updated to cite NAT-addcompat at the structurally identical `t'_j = t_j + 1 > t_j` step; TA5a's analogous step is uncited. (3) The case `k ≥ 3` step "`k - 1 ≥ 2`" sharpens a hypothesis on ℕ (parallel to the `k ≥ 1` sharpening in TA5, which is now cited as T0 + NAT-zero + NAT-discrete in TA5's Depends). TA5a performs a similar ℕ-level sharpening with no citation. The combined effect is that TA5a's Depends list, as written, does not surface any of the NAT-* axioms it consumes — a convention gap relative to the per-step citation standard the ASN now follows in every other proof.
**What needs resolving**: TA5a's case-analysis preface and *Depends* list must surface the NAT-* citations actually used — at least NAT-zero + NAT-discrete for the "non-zero ⇒ positive" inference in the preface (replacing the T0-only attribution), an appropriate NAT-* citation for the "successor of non-zero is non-zero" step in case `k = 0`, and a citation for the `k - 1 ≥ 2` sharpening in case `k ≥ 3` — matching the per-step convention the ASN now applies uniformly elsewhere.
