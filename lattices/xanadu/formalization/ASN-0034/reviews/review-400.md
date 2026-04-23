# Regional Review — ASN-0034/T4a (cycle 2)

*2026-04-23 00:29*

### Missing Depends slot on NAT-sub and NAT-card
**Class**: REVISE
**Foundation**: NAT-sub (NatPartialSubtraction), NAT-card (NatFiniteSetCardinality)
**ASN**: Both NAT-sub's and NAT-card's *Formal Contract* sections terminate at the *Axiom* bullet with no *Depends* slot. NAT-sub's axiom body uses `+`, `1`, `≥`, `>`, `<`, `≤`, and membership/closure in ℕ — "`(A m, n ∈ ℕ : m ≥ n : m − n ∈ ℕ)`", "`(A m, n ∈ ℕ : m > n : m − n ≥ 1)`", "`m ≥ p ∧ n ≥ p ∧ m < n ⟹ m − p < n − p`". NAT-card's axiom body invokes `<` on ℕ ("strictly increasing enumeration `s₁ < s₂ < … < s_k` under `<` on ℕ"), `≤` ("`|S| ≤ n`"), and the initial-segment notation `{1, 2, …, n}` built from `1` and successor; its prose also appeals to "NAT-order's trichotomy" to establish uniqueness of `k`.
**Issue**: Every other foundation ASN in this document declares its *Depends* bullet(s) (NAT-closure → NAT-zero; NAT-zero → NAT-order; NAT-discrete → NAT-order, NAT-closure; NAT-order declares the root status "(none)"). NAT-sub and NAT-card silently import the primitives they need. The document's own register — NAT-closure's prose explicitly says "without NAT-zero supplying the constant the left-identity clause would reference an ungrounded symbol; NAT-zero is therefore declared in the Depends slot" — makes the absence conspicuous. The previous-cycle finding fixed the *definitional* gap in `≥`/`>` (now introduced in NAT-order's Definition slot), but the *declarative* gap that NAT-sub/NAT-card cite those relations without a Depends link is separate and not subsumed.
**What needs resolving**: NAT-sub and NAT-card should each gain a *Depends* slot enumerating the foundations whose symbols their axioms use (minimally NAT-order for `<`/`≤`/`≥`/`>` and trichotomy; NAT-closure for `+` and `1`; NAT-zero for `0` where relevant; at NAT-card's discretion, a note distinguishing `|·|` from T0's `#·` can stay in the axiom body or move to a dedicated slot). The fix is declarative, not substantive.

VERDICT: REVISE
