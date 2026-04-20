# Cone Review — ASN-0034/TA5a (cycle 3)

*2026-04-17 18:51*

### Case k = 0 in TA5a omits the citation that licenses `zeros(t') = zeros(t)`
**Foundation**: TA5-SigValid (SigOnValidAddresses) — guarantees `sig(t) = #t` for T4-valid `t`, which combined with T4's `t_{#t} ≠ 0` forces `t_{sig(t)} ≠ 0`. (Alternatively TA5-SIG's definition of `sig(t)` as the rightmost nonzero position whenever any nonzero component exists.)
**ASN**: TA5a, Case `k = 0`:
> "By TA5(c), `t'` has the same length as `t` and differs only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`. **No zero components are added or removed**, so `zeros(t') = zeros(t)`."

TA5a's Depends list cites TA5-SigValid only for case `k = 1` ("invoked at case `k = 1` to license the non-zero last component"); no citation appears for case `k = 0`.
**Issue**: The step "no zero components are added or removed" is not free from TA5(b)/TA5(c) alone. The construction modifies position `sig(t)` from `t_{sig(t)}` to `t_{sig(t)} + 1`. The new value is non-zero (NAT facts: successor of any natural is ≥ 1), but for the *zero count* to be unchanged the *old* value must also be non-zero — otherwise a zero is removed and `zeros(t') = zeros(t) − 1`. This failure mode is real on the unrestricted carrier: for `t = (0, 0, 0)`, TA5-SIG gives `sig(t) = #t = 3`, `t_{sig(t)} = 0`, so `inc(t, 0) = (0, 0, 1)` and `zeros(t') = 2 < 3 = zeros(t)`. The argument is rescued only by T4-validity (the precondition), which via T4's `t_{#t} ≠ 0` and TA5-SigValid's `sig(t) = #t` forces `t_{sig(t)} ≠ 0`. That precondition chain crosses the property boundary from TA5a into TA5-SigValid (or, alternatively, into T4 + TA5-SIG's definitional clause), and the chain is not surfaced in the Depends entry for case `k = 0` — matching exactly the per-step citation convention the ASN follows for the structurally identical "non-zero ⇒ strictly positive" inference elsewhere.
**What needs resolving**: TA5a's case `k = 0` argument and Depends list must surface the citation chain that licenses `t_{sig(t)} ≠ 0` under the precondition (T4-validity → TA5-SigValid → `sig(t) = #t` → T4's `t_{#t} ≠ 0`, or the analogue routed through TA5-SIG's "rightmost-nonzero" clause), so that "no zero components are added or removed" is sourced rather than left as an implicit appeal to the T4-validity precondition.
