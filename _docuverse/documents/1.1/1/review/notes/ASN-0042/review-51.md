# Review of ASN-0042

## REVISE

### Issue 1: Foundation terminology error — "correspondence" vs "allocator"
**ASN-0042, Ownership Domains section, Notation paragraph**: "this is distinct from `dom(A)` of T10a (ASN-0034), which applies to a correspondence and yields the source domain of a relation."
**Problem**: T10a of ASN-0034 defines `dom(A)` for an *allocator*, with `dom(A) = {tₙ : n ≥ 0}` enumerating an allocator's per-stream chain. The word "correspondence" is not used anywhere in ASN-0034 — the foundation's terminology is consistently "allocator" (T10a's "Allocator tree 𝒯", "allocator A", etc.).
**Required**: Replace "correspondence" with "allocator" to match foundation terminology.

### Issue 2: "Vacuously" misused in NestingByDelegation base case
**ASN-0042, State Axioms section, NestingByDelegation derivation, base case**: "By O14's sixth clause, all initial principals in Π_{Σ_0} have pairwise non-nesting prefixes. So the first disjunct holds vacuously for every pair π₁, π₂ ∈ Π_{Σ_0} with π₁ ≠ π₂."
**Problem**: The first disjunct (non-nesting) is established *directly* by O14's sixth clause — it holds substantively, not vacuously. Vacuous truth applies when an antecedent is false; the non-nesting predicate has no false antecedent here.
**Required**: Replace "vacuously" with "directly" or "trivially".

### Issue 3: Wrong sub-account in B1 prerequisite for `delegated(π_M, π_C)` 
**ASN-0042, Worked Example section, opening paragraph**: "no corresponding seed is required under `π_M`, since the later delegation `delegated(π_M, π_C)` of `[2, 0, 1] = c_1 ∈ S([2], 2)` is itself the first baptism in its stream and has no B1 predecessor"
**Problem**: The worked example introduces `π_C` later only as a hypothetical sub-delegation `pfx(π_C) = [2, 0, 1]`. The claim that no seed is needed because the delegation is "the first baptism in its stream" assumes `Σ_0.B ∩ S([2], 2) = ∅`. But this is only an implicit assumption — the bootstrap state `Σ_0.B` is constructed by ad-hoc seeding earlier in the example, and the symmetric reasoning depends on showing `[2] ∈ Σ_0.B` from O14(vii) without any additional `[2, 0, k]` seeds. State this explicitly: "Since the bootstrap state contains no `[2, 0, k]` addresses (only `[2]` per O14(vii)), B1's contiguous-prefix requirement is vacuously satisfied when `[2, 0, 1] = c_1` is later baptized as `pfx(π_C)`."
**Required**: Make the negative assumption about `Σ_0.B`'s contents explicit when justifying the lack of a symmetric seed.

VERDICT: REVISE
