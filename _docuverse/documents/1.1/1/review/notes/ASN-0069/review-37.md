# Review of ASN-0069

## REVISE

### Issue 1: V11a — imprecise sibling-stream-index bound for subsequent forks

**ASN-0069, V11a, ancestry composition paragraph**: "value 1 when step i is a first fork of dⁱ⁻¹_new (V1's first-fork sub-case at inc(dⁱ⁻¹_new, 1)), and value m ≥ 1 (the sibling-stream index of dⁱ_new within A_v(dⁱ⁻¹_new)'s enumeration) when step i is a subsequent fork"

**Problem**: The bound "m ≥ 1" overlaps with the first-fork case. In V1's first-fork sub-case, dⁱ_new is the first emission of A_v(dⁱ⁻¹_new), and that first emission has sibling-stream index 1 with value 1 at position #dⁱ⁻¹_new + 1. The V11a case split labels first-fork with "value 1" and subsequent-fork with "value m ≥ 1" — the latter trivially includes m=1, making the two case labels non-disjoint. For *subsequent* forks (where A_v(dⁱ⁻¹_new) has prior emissions and dⁱ_new is the (k+1)-th emission for some k ≥ 1), the sibling-stream index of dⁱ_new is strictly ≥ 2 — verified concretely by the worked example, in which d_new² (the second sibling fork) has value 2 at position #d_src + 1, not value ≥ 1 in the loose sense. The subsequent-fork case has lower bound m=2, not m=1.

**Required**: Tighten to "value m ≥ 2 (the sibling-stream index of dⁱ_new within A_v(dⁱ⁻¹_new)'s enumeration) when step i is a subsequent fork" — this excludes the first-fork case from the subsequent label and makes the V11a case partition exclusive, matching the V1 first-fork / subsequent-fork dichotomy on which V11a is built.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
