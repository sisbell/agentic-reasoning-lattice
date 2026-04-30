# Signature Resolve — ASN-0034/TA-assoc — run 1

*2026-04-30T20:29:52Z*
*Model: sonnet*

## Output

Scanning the claim body and formal contract for symbols not in the notation primitives and not owned upstream.

All of `⊕`, `Pos`, `actionPoint`, `#·`, `·ᵢ`, `T`, `<`, `≤`, `≥`, `>`, `+`, `0`, `1`, `ℕ`, `−`, `Zero`, `Z` trace to upstream owners.

The postcondition states `actionPoint(b ⊕ c) = min(k_b, k_c)` and the proof body uses `min(k_b, k_c)` throughout as a binary operator on ℕ. `min` does not appear in any of the listed upstream symbols — it is not owned by NAT-order (which gives `<`, `≤`, `≥`, `>`), nor by any other dependency in the Depends list.

INTRODUCES:
- bullet: "- `min` — binary minimum operator on ℕ; `min(m, n)` returns the lesser of two natural numbers under NAT-order, used here to characterize `actionPoint(b ⊕ c) = min(actionPoint(b), actionPoint(c))`"

REMOVES: []
