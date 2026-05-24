# Review of ASN-0094

## REVISE

### Issue 1: AllocatedAddressAntichain worked example violates L1b / R0a-Cor2

**ASN-0094, AllocatedAddressAntichain Lemma, "Worked example — Case 3 (cross-domain) walkthrough":** "Take `x = [1, 0, 2, 0, 1, 0, 7] ∈ T` — a tumbler of length 7 with zeros at positions 2, 4, 6 (so `zeros(x) = 3`)... Suppose `x ∈ dom(Σ.L)`...". The example computes `#E(x) = 1` (Step 3.2 concrete: "T4b places `E(x)` at positions `7..7`, so `E(x) = [x_7] = [7]` and `#E(x) = 1`").

**Problem:** The example asserts `x ∈ dom(Σ.L)` but uses `#E(x) = 1`. The Lemma's own preamble cites L1b (ASN-0043) which requires `#E(a) ≥ 2` for every `a ∈ dom(Σ.L)`, and R0a-Cor2 (ASN-0086) strengthens this to `#E(a) = 2`. The hypothesized `x` cannot exist in any reachable `dom(Σ.L)`. The symmetric Sub-case 3b example uses `x' = [1, 0, 2, 0, 1, 0, 5] ∈ dom(Σ.C)` with `#E(x') = 1`, which violates the content-side scaffolding's `#E(a) ≥ 2` requirement.

The proof itself is sound — Step 3.2's general derivation explicitly uses only `#E(·) ≥ 1` from T4's last-position-non-zero clause — but the worked example claims to depict a concrete reachable-state scenario at addresses that contradict the cited substrate-level invariants.

**Required:** Use `#x = 8` with `E(x) = [s_L, 1] = [7, 1]` (satisfying `#E(x) = 2`) and `#x' = 8` with `E(x') = [s_C, 1] = [5, 1]`. Update Step 3.2 (concrete) to read: `T4b places E(x) at positions 7..8, so E(x) = [x_7, x_8] = [7, 1] and #E(x) = 2`. The contradiction at Step 3.3a still surfaces at the same place — `E(x).1 = x_7 = 7 = s_L` vs `E(a).1 = a_7 = s_C = 5` — and the example becomes faithful to the reachable-state hypothesis.

## OUT_OF_SCOPE

None — the ASN's open questions appropriately distinguish refinement candidates from scope boundaries.

VERDICT: REVISE
