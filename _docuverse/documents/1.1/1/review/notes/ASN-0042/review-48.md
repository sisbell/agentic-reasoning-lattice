# Review of ASN-0042

## REVISE

### Issue 1: O18 / DelegatorAllocatesPrefix freshness gap

**ASN-0042, DelegatorAllocatesPrefix proof, sub-case 2**: "If `pfx(π_a) ≺ pfx(π')` (strict)... Condition (ii) gives `#pfx(π_a) ≤ #pfx(π_d)`, no contradiction here — but we have not yet derived a contradiction in sub-case (2). To do so: we need that no principal in Π_Σ has previously allocated pfx(π') as a non-principal sub-position. The conservative reading of the spec... closes sub-case (2) by stipulation: principal prefixes are not pre-baptized..."

**Problem**: The proof explicitly admits sub-case (2) is closed by "stipulation" / "conservative reading" rather than formal derivation — a textbook hand-wave. O18's formal statement is `pfx(π') ∈ Σ'.B` (membership), but the proof needs `pfx(π') ∈ Σ'.B ∖ Σ.B` (freshness) for O16 (AllocationClosure) to apply to the delegation transition. Without freshness, `allocated_by_{Σ'}(π_d, pfx(π'))` fails because the address was allocated earlier, not in the transition yielding Σ'. The cascade: DelegatorAllocatesPrefix is invoked in the worked example (Σ_3 delegation to π_B); the prose around O18 emphasizes "material baptism" but the formal statement does not capture that intent. The freshness premise cannot be derived from O5, O15, O16, O18, or condition (ii) as currently stated — sub-case 2 is consistent with every existing axiom.

**Required**: Strengthen O18's formal statement to `Σ → Σ' ∧ π' ∈ Π_{Σ'} ∖ Π_Σ ⟹ pfx(π') ∈ Σ'.B ∖ Σ.B`, capturing the "material baptism" prose explicitly. Alternatively, introduce a separate axiom (e.g., "principal prefixes are reserved — no principal is admitted whose prefix was previously baptized as a non-principal sub-position") and discharge sub-case 2 against it. The current proof must not rely on undeclared stipulations.

### Issue 2: Invalid Bop depth parameters in O10 worked example

**ASN-0042, O10 Fork worked example, Pre-delegation paragraph**: "then Bop([1, 0, 2, 0, 3], 3) baptizes element a₁ = [1, 0, 2, 0, 3, 0, 1]"

**ASN-0042, O10 Fork worked example, Post-delegation paragraph**: "then Bop([1, 0, 2, 0, 5], 3) baptizes element a₂ = [1, 0, 2, 0, 5, 0, 1]"

**Problem**: Both Bop calls have `d = 3`, violating ASN-0040 B6(ii) which requires `d ∈ {1, 2}`. They also violate B6(iii): `zeros([1, 0, 2, 0, 3]) + (d − 1) = 2 + 2 = 4 > 3`. With `d = 3`, `inc([1, 0, 2, 0, 3], 3) = [1, 0, 2, 0, 3, 0, 0, 1]` (length 8 with adjacent zeros), not a₁. The correct call is `Bop([1, 0, 2, 0, 3], 2)`, where `d = 2` extends by 2 positions yielding `[1, 0, 2, 0, 3, 0, 1] = a₁` and satisfying B6. The trajectory descriptions are internally inconsistent — these are not just typos but contradict the foundation ASN being cited.

**Required**: Change `Bop([1, 0, 2, 0, 3], 3)` → `Bop([1, 0, 2, 0, 3], 2)` and `Bop([1, 0, 2, 0, 5], 3)` → `Bop([1, 0, 2, 0, 5], 2)`. Verify any other Bop invocations in the worked example against B6(ii) and B6(iii).

## OUT_OF_SCOPE

(none — the Open Questions list correctly defers ownership transfer, federation, and accessibility-after-revocation.)

VERDICT: REVISE
