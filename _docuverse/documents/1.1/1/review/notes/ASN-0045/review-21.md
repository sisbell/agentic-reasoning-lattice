# Review of ASN-0045

## REVISE

### Issue 1: Pairwise distinctness of 0,1,2,3 mis-cited to T0

**ASN-0045, Well-Definedness (at-most-one):** "The four values 0, 1, 2, 3 are pairwise distinct as natural numbers (T0, ASN-0034)." — repeated in *Properties Introduced / Partition / Depends*: "T0 (... the pairwise distinctness of 0, 1, 2, 3 in ℕ for at-most-one)."

**Problem**: The distinctness of distinct numerals is not a T0 fact. T0 only posits ℕ as the carrier; its own note states explicitly that "the standard arithmetic facts about ℕ that proofs need are separated into their own axioms so each proof cites only what it actually uses." That `0 ≠ 1 ≠ 2 ≠ 3` (pairwise) follows from NAT-addcompat's `k < k + 1` (giving the strict chain `0 < 1 < 2 < 3`) together with NAT-order's irreflexivity/trichotomy — it does not follow from T0's carrier characterization. The defect is also internally inconsistent: the *at-least-one* paragraph correctly routes consecutiveness through NAT-addcompat and the boundary splits through NAT-order, yet *at-most-one* attributes the very same numeral-ordering content to T0.

**Required**: Re-cite the distinctness of 0,1,2,3 to NAT-order (trichotomy) and NAT-addcompat (successor inequality), matching the at-least-one derivation and T0's stated convention. Update the Partition *Depends* line for the at-most-one direction accordingly.

### Issue 2: Constant-existence citations inconsistent across the four predicates

**ASN-0045, Properties Introduced:** Node *Depends* cites "T0 (carrier ℕ; the constant 0 ∈ ℕ)", while Account cites "NAT-closure (the constant 1)", Document cites "NAT-closure (... the numeral 2 := 1 + 1)", Element cites "NAT-closure (... 3 := 2 + 1)".

**Problem**: The four predicates are structurally identical (each a conjunction `T4-valid(t) ∧ zeros(t) = k`), yet the existence/grounding of the numeral `k` is sourced from T0 for `k = 0` and from NAT-closure for `k = 1, 2, 3`. Under the per-step citation convention the foundation enforces, `0 ∈ ℕ` (additive identity, NAT-closure) should be sourced uniformly with the other numerals.

**Required**: Cite the grounding of `0` consistently (NAT-closure, as the additive identity), or justify why `0` alone is a pure T0-carrier fact while `1,2,3` are not.

## OUT_OF_SCOPE

### Topic 1: Behavior of the level predicates under editing operations
**Why out of scope**: ASN-0045 defines static one-place predicates over T. Whether INSERT/DELETE/COPY preserve a tumbler's level classification is an operations question for a later ASN, not a gap in this definitional layer. The absence of operation edge cases (empty document, zero-width span, etc.) is therefore correct here.

VERDICT: REVISE
