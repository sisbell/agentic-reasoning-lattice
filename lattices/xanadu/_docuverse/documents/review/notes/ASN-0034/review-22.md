# Review of ASN-0034

## REVISE

### Issue 1: TA3-strict has spurious dependencies on T3 and TA6
**ASN-0034, Dependency graph (TA3-strict)**: `follows_from: [T1, T3, TA6, TumblerSub]`
**Problem**: T3 and TA6 are used only in Case 0 of the TA3 (weak) proof. TA3-strict's equal-length precondition (`#a = #b`) eliminates Case 0 entirely — two tumblers of the same length cannot be in a prefix relationship unless equal, and `a < b` rules out equality. Only Cases 1–3 remain, none of which invoke T3 or TA6. Case 1 (j = d): component subtraction and T1. Case 1 (j > d): agreement before divergence and T1. Case 3: divergence mismatch and T1. TA6 (zero tumblers less than positive) appears in Case 0 sub-sub-case 1 (`a = w`). T3 appears in Case 0's "without divergence" sub-case to establish result equality.
**Required**: Remove T3 and TA6 from TA3-strict's `follows_from`. The correct list is `[T1, TumblerSub]`.

### Issue 2: Dependency graph name mismatches
**ASN-0034, Dependency graph (multiple properties)**
**Problem**: Five YAML `name` fields do not match the canonical names given in the ASN body text (the parenthetical after each label):

| Label | YAML name | Body name |
|-------|-----------|-----------|
| T0(b) | "Tumblers of arbitrary length exist in T" | "Unbounded length" |
| Divergence | "Divergence point of two unequal tumblers" | "Divergence" |
| D0 | "Displacement well-definedness" | "DisplacementWellDefined" |
| D1 | "Displacement round-trip" | "DisplacementRoundTrip" |
| D2 | "Displacement uniqueness" | "DisplacementUnique" |

**Required**: Align the YAML `name` fields with the body text names.

### Issue 3: TA7a verification overclaims S-membership for ⊖ when #w > #o
**ASN-0034, TA7a verification, Case k ≥ 2 for ⊖**: "The result is `o` itself — a no-op. ... The result is trivially in S."
**Problem**: The claim holds only when `#w ≤ #o`. The element-local displacement definition constrains the action point (`1 ≤ k ≤ m`) but not the displacement length. When `#w > m = #o`, TumblerSub produces a result of length `max(m, #w) = #w > m` with trailing zeros at positions `m+1` through `#w`. This result is not equal to `o` (different length, by T3) and is not in S (zero components violate positivity). The same issue affects Case k = 1, d = 1: the claim "rᵢ = oᵢ > 0 for i > 1. All components positive; the result is in S" fails when `#w > m` because positions beyond `m` carry zero from the zero-padded minuend. The formal claim (result ∈ T) is unaffected — T-membership is trivial for any well-defined subtraction. The error is in the informal S-membership and equality characterizations.
**Required**: Qualify the S-membership claims with `#w ≤ m`, or restrict the element-local displacement definition to `#w = m`. A single sentence suffices: "When `#w > m`, the result has trailing zeros and lies in T \ S; the analysis below assumes the typical case `#w = m`."

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
