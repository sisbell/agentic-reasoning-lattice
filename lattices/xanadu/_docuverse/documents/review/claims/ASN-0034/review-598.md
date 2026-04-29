# Cone Review — ASN-0034/T10a (cycle 2)

*2026-04-26 04:27*

Looking at TA5a's proof and contract for new issues beyond the previous finding (which has been correctly addressed — T4a is no longer in Depends and Case k ≥ 3 now uses T4(ii) directly).

### Unused NAT-discrete dependency
**Class**: REVISE
**Foundation**: NAT-discrete (NatDiscreteness), NAT-zero (NatZeroMinimum)
**ASN**: TA5a — preamble prose "On ℕ, 'non-zero component' means 'strictly positive' via NAT-zero's `0 ≤ n` and NAT-discrete instantiated at `m = 0`." and Depends entry "NAT-discrete (NatDiscreteness) — with NAT-zero yields non-zero ⇒ strictly positive on ℕ."
**Issue**: NAT-discrete is declared in the Depends list with the role "with NAT-zero yields non-zero ⇒ strictly positive on ℕ", and the preamble sets up this interpretation. But the proof body never invokes "non-zero ⇒ strictly positive". The single place positivity of a non-zero component is needed — Case `k = 0`'s check that `t_{sig(t)} + 1 ≠ 0` — discharges via "by NAT-zero and NAT-addcompat, `t_{sig(t)} + 1 > t_{sig(t)} ≥ 0`", using NAT-zero's `0 ≤ n` and NAT-addcompat's strict successor only; NAT-discrete (which would lift `≠ 0` to `≥ 1`) is not invoked. Cases `k = 1` and `k = 2` use `t_{#t} ≠ 0` directly without converting to strict positivity. Case `k ≥ 3` uses NAT-sub clauses, NAT-addcompat, NAT-addassoc, NAT-order, but not NAT-discrete. The Depends entry thus mis-states a dependency the proof does not actually consume, and the preamble is meta-prose framing an inference rule the proof never applies — exactly the kind of use-site framing flagged as reviser drift in the review criteria.
**What needs resolving**: Either remove NAT-discrete from the Depends list and drop the preamble's interpretation paragraph (if the proof truly does not need it), or identify the specific proof step that converts non-zero to strict positivity via NAT-discrete and make that step explicit at its use site rather than in a setup paragraph.

VERDICT: REVISE
