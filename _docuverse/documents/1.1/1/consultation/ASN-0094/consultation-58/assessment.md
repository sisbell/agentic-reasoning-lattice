# Channel Assignment — ASN-0094 review-58

**Date:** 2026-05-24 07:39

## Issue 1: AllocatedAddressAntichain Sub-case 3b's "vacuous on substrate-conforming layer" rationale misattributes the scaffolding
Reason: The minimal fix (option (a)) is derivable from the ASN's existing scaffolding via textual rewrite — walking through `#E(a) ≥ 2` (scaffolding) + R0a-Cor2 (`#E(a) = 2` link-side) + Step 3.1's shared zero positions + Prefix length constraint to force `#x = #a`. However, option (b) — strengthening the *Element-level content addresses* scaffolding clause to commit to `#E(a) = 2` exactly — would yield a cleaner vacuity description matching R0a-Cor2's link-side phrasing, and the choice between (a) and (b) turns on whether the substrate genuinely enforces the stronger condition.
Gregory question: Does the udanax-green content-store allocator enforce `#E(a) = 2` exactly for every `a ∈ dom(Σ.C)` (matching R0a-Cor2's link-side strengthening from `≥ 2` to `= 2`), or only the weaker `#E(a) ≥ 2` that the current scaffolding clause records?
