# Review of ASN-0094

I read this carefully. The framework is exceptionally rigorous — the proofs are stratified, the cases are exhausted, the walkthroughs exercise edge cases, and the META status of Sh5 is honestly downgraded. I have two minor REVISE items, both internal to the appendix.

## REVISE

### Issue 1: NAT-card additivity proof uses subtraction before NAT-sub is derived

**ASN-0094, Appendix: Local NAT Primitives, "Closing the step" of additivity proof**: "`|S₁ ∪ S₂| = |S₁' ∪ S₂| + 1 = |S₁'| + |S₂| + 1 = (|S₁| − 1) + |S₂| + 1 = |S₁| + |S₂|` (using ℕ-associativity and ℕ-commutativity, both derived in the Appendix)."

**Problem**: The step writes `(|S₁| − 1)` (subtraction) but NAT-sub is derived *after* NAT-card in the same appendix. The parenthetical claims only ℕ-comm and ℕ-assoc are invoked, but the equality `(|S₁| − 1) + 1 = |S₁|` requires NAT-sub. The substantive arithmetic does not need subtraction — step (γ) already establishes `|S₁| = |S₁'| + 1`, so the closing can use `|S₁'|` directly.

**Required**: Rewrite the closing step as:
`|S₁ ∪ S₂| = |S₁' ∪ S₂| + 1 = (|S₁'| + |S₂|) + 1 = |S₁'| + (|S₂| + 1) = |S₁'| + (1 + |S₂|) = (|S₁'| + 1) + |S₂| = |S₁| + |S₂|`
using only ℕ-assoc, ℕ-comm, and the (γ) identity `|S₁'| + 1 = |S₁|`. No subtraction needed.

### Issue 2: Stratified proof order omits NAT-sub from LinkAddressNotPrefixOfEmit's consumed inputs

**ASN-0094, "Stratified proof order" in the Sh-conf section, item (4)**: "LinkAddressNotPrefixOfEmit lemma ... its proof consumes only ASN-0086's R0a-Cor1/FreshEmissionAddress/L1/L1a, T10a.7/T3/Prefix, the scaffolding clauses, and NAT-card"

**Problem**: The proof's Step II.0 explicitly cites NAT-sub for the suffix length `#w := #a − #b`, and Step II.1's closing line says "NAT-sub yields `zeros(w) = 0`". Both consumption sites are textually present in the proof body. The stratification statement claiming "only NAT-card" is incomplete.

**Required**: Update the stratification to "NAT-card and NAT-sub" (or "the appendix's NAT primitives"). This is consistent with what the proof actually consumes and keeps the stratification a faithful audit of consumed inputs.

## OUT_OF_SCOPE

None beyond what the document already flags in Open Questions ([scope boundary] items for multi-process concurrency, composite shapes, `(0|1, 0|1)` shapes).

VERDICT: REVISE
