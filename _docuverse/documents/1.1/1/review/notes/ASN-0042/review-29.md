# Review of ASN-0042

## REVISE

### Issue 1: FirstDelegatorIsπ inductive step has a gap when π already has sub-delegates in Π_Σ

**ASN-0042, Sub-lemma (FirstDelegatorIsπ)**: "Two cases on π_d. (a) π_d = π: chain π → π'' of length k = 1. (b) π_d ≠ π and pfx(π) ≺ pfx(π_d) ...: then π_d ∈ S_π(Σ̃). The state Σ̃_d at which π_d itself was introduced lies along Σ →⁺ Σ̃ — specifically, π_d ∈ Π_{Σ̃} and π_d ∉ Π_Σ (else π_d ∈ S_π(Σ) would contradict the induction setup unless S_π(Σ) ≠ ∅; in either case, walking back to the first transition introducing a sub-delegate of π yields a state Σ̃_d reachable from Σ with |S_π(Σ̃_d^-)| < m + 1...)"

**Problem**: The proof asserts π_d ∉ Π_Σ without an airtight justification. If S_π(Σ) ≠ ∅ — i.e., π already has sub-delegates established before Σ — then π_d may well be in Π_Σ. The IH (induct on |S_π(Σ̃)| at the transition introducing π'') cannot then fire on π_d, because π_d was introduced *before* Σ, not along Σ →⁺ Σ'. The chain π → ... → π_d would need to invoke delegation links that occurred before Σ, contradicting the sub-lemma's conclusion that links lie "at some intermediate state Σ^{(j)} along Σ →⁺ Σ'". The parenthetical hand-waves this with "walking back to the first transition introducing a sub-delegate of π yields a state Σ̃_d reachable from Σ" but doesn't actually close the gap — that "first transition" may itself be before Σ.

**Required**: Either restrict the sub-lemma's hypothesis to states Σ where S_π(Σ) = ∅ (so all sub-delegate construction happens after Σ), or explicitly extend the chain conclusion to allow links established before Σ (in which case the conclusion clause "at some intermediate state Σ^{(j)} along Σ →⁺ Σ'" must be reworded to permit any state in the system history). The current proof is incomplete as written.

### Issue 2: AccountField decidability is misattributed to T6

**ASN-0042, acct(a) (AccountField) definition**: "acct(a) is the tumbler whose components are N(a) followed by [0] followed by U(a) — using the foundation's field projections defined by T4(b) (UniqueParse), and decidable by T6 (DecidableContainment)"

**Problem**: T6 (DecidableContainment) is a decision procedure for hierarchical containment between two addresses (same-node, same-account, same-document, document-prefix); it does not itself establish decidability of the acct extraction function. Decidability of acct(a) comes from T4(b)'s uniqueness clause plus the finiteness of any tumbler — N(a) and U(a) are directly computable by scanning components against the zero count. T6 happens to use similar field-extraction machinery, but it is not the relevant decidability witness.

**Required**: Remove the T6 citation or replace it with a more precise reference. T4(b) alone (UniqueParse) suffices: the field decomposition is uniquely determined per T4(b), and projection plus concatenation is straightforward.

### Issue 3: O7 Postcondition (c) overstates recursive delegation as unconditional

**ASN-0042, O7 Postcondition (c)**: "the delegation relation is satisfiable with π' as delegator for sub-prefixes of pfx(π')"

**Problem**: As stated, this suggests π' may always recursively delegate any sub-prefix. But by condition (ii) of the `delegated` relation, π' can only delegate sub-prefix p'' if it remains the most-specific covering principal of p'' in the current Π. If π' has previously delegated a sub-prefix p* with pfx(π') ≺ p* ≼ p'', then the sub-delegate (not π') becomes the most-specific covering principal of p'' and condition (ii) fails. The proof body acknowledges this implicitly ("the conditions of the delegated relation are checkable from the current state") but the formal contract's wording presents the recursion as universal.

**Required**: Reword postcondition (c) to make conditionality explicit, e.g., "π' may delegate any sub-prefix p'' with pfx(π') ≺ p'' provided no existing principal in the current Π already covers p'' with a longer prefix than π'." The current phrasing risks misreading.

### Issue 4: Several "By T4" citations conflate distinct sub-claims of the foundation

**ASN-0042, AccountPrefix proof, AccountField proof, O9 proof, and elsewhere**: Recurring phrasings like "By T4, a = N₁. ... .Nα . 0 . U₁. ... .Uβ . 0 . D₁. ... .Dγ with α ≥ 1, β ≥ 1, γ ≥ 1, every Nᵢ > 0..." and "By T4's field decomposition..."

**Problem**: T4 (HierarchicalParsing) is the validity predicate. The decomposition into named fields is T4(b) (UniqueParse). The non-emptiness of each field segment (α ≥ 1, β ≥ 1, etc.) is T4a (SyntacticEquivalence). The level-determination biconditional (zeros = 0 ↔ node-level, etc.) is T4(c). Citing "By T4" everywhere obscures which sub-claim is being invoked and makes verification harder.

**Required**: Replace bare "By T4" with the specific sub-claim — T4(b) for field decomposition, T4a for segment non-emptiness, T4(c) for level determination — at each citation site.

## OUT_OF_SCOPE

### Topic 1: Concrete authentication / session-to-principal binding mechanism
O11 (IdentityAxiomatic) explicitly defers the mechanism by which `session.account = pfx(π)` is established. A future ASN should specify the authentication protocol, cryptographic binding, and certificate or capability hierarchy.

### Topic 2: Ownership transfer mechanism
The ASN's prose acknowledges Nelson's "someone who has bought the document rights" but the system as specified has no transfer machinery. The reconciliation between inalienable provenance (O6) and a hypothetical transfer regime — including whether the address records original creator vs. current holder — is a future-ASN question.

### Topic 3: Cross-node identity federation
O9 establishes node-locality unconditionally. Whether the same human can have related principals on multiple nodes — and what coordination invariants must hold across nodes — belongs to a future federation specification.

### Topic 4: Density of ownership domains
Whether every address in dom(π) must be allocatable, or whether structural gaps may exist between baptized siblings, is properly listed in Open Questions and belongs to a future allocation-discipline ASN.

### Topic 5: Delegation event recording / audit trail
Whether the system maintains an explicit delegation log distinct from the structural evidence in the address hierarchy is left open and belongs to a future audit-and-provenance ASN.

VERDICT: REVISE
