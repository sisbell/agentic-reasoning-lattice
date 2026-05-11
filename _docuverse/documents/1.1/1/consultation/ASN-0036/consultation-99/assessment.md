# Channel Assignment — ASN-0036 review-99

**Date:** 2026-05-11 13:57

## Issue 1: S7a/S7b textual order creates an unresolved logical dependency
Reason: Purely expository — fix is to reorder S7b before S7a or restate S7a's axiom with explicit `zeros(a) ≥ 2` conditioning. All material is already present in the ASN; no design intent or implementation evidence required.

## Issue 2: D-CTG-depth precondition cites S8-depth for `m ≥ 3`
Reason: Citation/wording correction. The issue itself identifies that `m ≥ 3` is the non-triviality bound, not an S8-depth consequence — decoupling the citation is mechanical.

## Issue 3: Within-subspace incompatibility lemma elides `v ≤ t ⟹ v < t`
Reason: Proof-step gap. The bridge from `v ≤ t` (interval membership) plus `t ≠ v` (lemma hypothesis) to `v < t` is derivable from existing hypotheses and T1; making it explicit is internal.

## Issue 4: D-CTG-depth alternative construction cites strict successor as `0 < i + 1`
Reason: Derivation-chain cleanup. The fix is either to drop the parenthetical (T0(a) already suffices in the main argument) or to spell out the NAT-zero + strict successor + transitivity + NAT-cancel chain — all foundation claims already cited in ASN-0034.

## Issue 5: S8 auxiliary lemma conclusion (ii) wording understates the prefix-copy argument
Reason: Proof presentation — the prefix-copy rule from TumblerAdd (ASN-0034) already covers every position `i < #aⱼ`; the fix is to state the all-positions-copied step explicitly before specializing to the three separator zeros. Internal.
