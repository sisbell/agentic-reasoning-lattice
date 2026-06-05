# Review of ASN-0103

## REVISE

### Issue 1: `sig(·) = #(·)` asserted from TA5(c), but that identity requires T4-validity (TA5-SigValid)

**ASN-0103, Effect One, CND.monotone, "On-chain (`v_{#A+1} = 0`)" paragraph**: "while a `k=0` sibling step modifies only position `sig(·) = #(·) ≥ #A+3 > #A+2` (TA5(c), ASN-0034). So positions `#A+1, #A+2` hold throughout the chain the values its *root* document carries."

The same move appears earlier in the `A ≼ t` sub-argument: "each `k=0` step modifies only position `sig(·) ≥ #t + 1 > #t` (TA5(c), ASN-0034)."

**Problem**: TA5(c) states only that an `inc(·,0)` step modifies position `sig(t)` and preserves length (`#t' = #t`). It does **not** establish `sig(t) = #t`. That equality is the separate property TA5-SigValid (SigOnValidAddresses), which holds *only for T4-valid addresses* (`t_{#t} ≠ 0`). The inference "`k=0` touches only a position `> #A+2`" — which is what freezes the document-tier components `#A+1, #A+2` across the version chain and thereby pins `v_{#A+2} = i` — is load-bearing for the dominance conclusion `d > v`. If an intermediate operand had `sig < #operand` (a trailing-zero address), an `inc(·,0)` step could in principle alter a position `≤ #A+2`, breaking `v_{#A+2} = i` and the entire on-chain dominance. The argument silently relies on every version-chain operand being T4-valid (so `sig = length`), but cites only TA5(c), which cannot deliver this.

**Required**: At both occurrences, justify `sig(·) = #(·)` by invoking TA5-SigValid together with the T4-validity of the version-chain operands (every baptized entity in `E` satisfies T4 — B10/B6, ASN-0040, and S7d/M0). Make explicit the chain: operand T4-valid ⟹ `t_{#t} ≠ 0` ⟹ `sig(t) = #t` (TA5-SigValid) ⟹ the `inc(·,0)` step (TA5(c)) modifies position `#operand ≥ #A+3 > #A+2`, leaving positions `1..#A+2` frozen.

## OUT_OF_SCOPE

### Topic 1: The effective-owner identity `ω_{Σ'}(d) = ω_Σ(A)`
**Why out of scope**: The ASN correctly recognizes that `ω` is defined over ASN-0042's registry `B`, which is absent from ASN-0047's state `(C,L,E,M,R)`, and explicitly defers the `ω`-valued conclusion to a registry-carrying ASN (CND.own, final Open Question). This deferral is appropriate, not a defect — the needed `E`↔`B` coupling invariant genuinely belongs to a future ASN.

### Topic 2: Crash recovery, concurrency serialization, write-readiness, document removal
**Why out of scope**: These are raised as Open Questions and concern failure semantics, concurrency, and session state — territory beyond the single-operation state contract specified here.

VERDICT: REVISE
