# Regional Review — ASN-0034/TA-Pos (cycle 2)

*2026-04-22 16:26*

### NAT-closure uses `0` without declaring NAT-zero as a dependency
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity)
**ASN**: NAT-closure formal contract: "`1 ∈ ℕ` (one is a natural number); `(A n ∈ ℕ :: n + 1 ∈ ℕ)` (successor closure); `(A m, n ∈ ℕ :: m + n ∈ ℕ)` (addition closure); `(A n ∈ ℕ :: 0 + n = n)` (left additive identity)." No *Depends* slot is listed.
**Issue**: The left-identity clause `0 + n = n` uses the literal `0`, but `0 ∈ ℕ` is posited by NAT-zero (NatZeroMinimum), not by NAT-closure itself. NAT-closure introduces only `1 ∈ ℕ`. Without a declared dependence on NAT-zero, the symbol `0` is ungrounded inside NAT-closure — the formal contract references a constant it does not own and does not import. By contrast, sibling claims (T0, TA-Pos) carefully list each symbol-supplying dependency; NAT-closure is the lone exception.
**What needs resolving**: Either add NAT-zero (NatZeroMinimum) to NAT-closure's Depends with a note that it supplies the `0` appearing in the left-identity clause, or restructure so the left-identity clause no longer uses `0` inside NAT-closure. (No circularity arises: NAT-zero depends on NAT-order, not on NAT-closure.)
