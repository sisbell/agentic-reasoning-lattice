# Review of ASN-0108

## REVISE

### Issue 1: Mis-cited foundation claims in W7
**ASN-0108, W7 (ResultMembershipNonMonotone)**: "still permanently resident in `dom(Σ.L)` (L12, L13 of ASN-0098), but no longer discoverable (LP17)."
**Problem**: ASN-0098 contains neither `L12` nor `L13`. Link-store permanence in ASN-0098 is `LP13` (UnconditionalLinkPersistence); `L12` (LinkImmutability) lives in ASN-0043/ASN-0093, not ASN-0098. The M-mut paragraph earlier cites the same fact correctly as "`LP13`," so W7's label is an internal inconsistency, not a notational choice.
**Required**: Cite the permanent-residence fact as `LP13` (ASN-0098) and, if immutability of the value is also intended, attribute `L12` to ASN-0043. Make W7 agree with the M-mut citation.

### Issue 2: W5's necessity claim ("only if") is false as stated
**ASN-0108, W5 (OrderStability)**: "Resumption is well-defined across `Σ → Σ'` only if the ordering key preserves *relative order* among the links present and matching in both states, and preserves the cursor's cut-point."
**Problem**: The "only if" over-claims. Resumption past a cursor `c` consults only `After(c, Σ') = {a : κ(c) <_K κ(a)}` — the unseen tail. Take two already-delivered links `a, b` with `κ(a), κ(b) <_K κ(c)` in both states; let their *mutual* order swap between calls while both remain below `κ(c)`. Relative order among links "present and matching in both states" is then violated, yet `After(c, Σ')` is unchanged and resumption is perfectly well-defined. So blanket relative-order preservation is *not* necessary — only the cut-point and the order of the tail above `κ(c)` are. The ASN already concedes absolute invariance is "stronger than necessary"; its stated necessary condition is likewise not tight.
**Required**: Either weaken the necessary condition to "preserves the cursor's cut-point and the `≺`-order of the links in `After(c, ·)`," or prove the blanket relative-order claim is genuinely required (it is not, per the counterexample).

### Issue 3: W2's weakest-precondition argument is asserted, not exhibited
**ASN-0108, W2 (CursorByIdentity)**: "The wp of 'no link seen twice and none skipped' over a mutable result set is satisfiable by an identity cursor and not by an offset cursor."
**Problem**: This is the load-bearing justification for the identity-cursor design, but it is delivered entirely in prose. The wp predicate is never written, and the offset-cursor failure is never demonstrated against a concrete state change. The ASN's four worked walks all verify W4/W9/W9a under a *fixed* set; none exercises the insertion/deletion scenario that W2 claims breaks an offset cursor. Per the depth standard, a derived guarantee must show its chain, and the key non-trivial case must be checked against a specific scenario.
**Required**: State the wp explicitly for the postcondition "next window = `After(c, Σ')` exactly," and add a small concrete walk (e.g., `M = {a₁,…,a₅}`, `N = 2`, cursor after window 1, then one insertion before the offset) showing the offset cursor producing an overlap or omission while the identity cursor resumes correctly.

## OUT_OF_SCOPE

### Topic 1: Multi-document global ordering and the non-monotone-key blind spot
The failure of a single allocation-monotone key across independent home-document allocators (W6) and the resulting silent-skip hazard are correctly deferred to the Open Questions rather than claimed here. No revision needed — flagging only to confirm the deferral is appropriate, not a gap in this ASN.

VERDICT: REVISE
