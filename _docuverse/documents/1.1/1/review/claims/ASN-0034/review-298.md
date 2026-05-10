# Cone Review — ASN-0034/TS5 (cycle 8)

*2026-04-18 14:55*

Reading TS3, TS4, TS5 as a system against the previous-findings resolutions already applied.

### Result-length identity attributed to TA0 in TS3's Depends but to TumblerAdd in OrdinalShift's proof body
**Foundation**: The identity `#(a ⊕ w) = #w` is load-bearing for every length-preservation step in this ASN (it supplies the left equality of OrdinalShift's chain `#shift(v, n) = #δ(n, m) = m = #v` and every analogous step in TS3's three-shift length reasoning).
**ASN**:
- OrdinalShift's proof body: "TumblerAdd's result-length identity `#(a ⊕ w) = #w` yields `#shift(v, n) = #δ(n, m)`" — attributes the identity to **TumblerAdd**.
- OrdinalShift's Depends TumblerAdd entry re-asserts the same attribution: "the result-length identity `#(a ⊕ w) = #w` at the length step".
- OrdinalShift's Depends TA0 entry simultaneously claims: "TA0 also supplies the result-length identity used to conclude `#shift(v, n) = #v`" — attributes to **TA0**.
- TS3's Depends TA0 entry attributes it squarely to TA0: "to source each `⊕`'s result-length identity `#u = #δ(n₁, m) = m` (and analogous identities for `#L` and `#R`) via TA0's second exported postcondition `#(a ⊕ w) = #w`".
- TS3's Depends TumblerAdd entry makes no mention of the length step at all; it only covers the three-region rule.
**Issue**: The same identity `#(a ⊕ w) = #w` is sourced to TumblerAdd in OrdinalShift's proof body and TumblerAdd entry, to TA0 in OrdinalShift's TA0 entry, and to TA0 alone in TS3's Depends. A foundation ASN cannot have two authoritative sources for the same exported fact under the per-step discharge discipline this ASN enforces — a reviser tightening either TA0's postcondition list or TumblerAdd's construction needs a single unambiguous owner to know which callers it affects. Today, a reviser tightening TumblerAdd would believe it invalidates OrdinalShift's length step but not TS3's; a reviser tightening TA0 would believe the reverse for OrdinalShift and that TS3 is affected.
**What needs resolving**: Pick one owner of the result-length identity `#(a ⊕ w) = #w` and update every citation site in this ASN to match. If TA0 owns it, OrdinalShift's proof body and TumblerAdd Depends entry must be corrected. If TumblerAdd owns it, TS3's TA0 Depends entry must be corrected and TS3's TumblerAdd entry must be extended to cover the length step at each of the three component-computation sites.

## Result

Cone not converged after 8 cycles.

*Elapsed: 4161s*
