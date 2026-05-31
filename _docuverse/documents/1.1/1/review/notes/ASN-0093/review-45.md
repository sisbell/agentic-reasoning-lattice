# Review of ASN-0093

## REVISE

### Issue 1: Freshness lemmas' premises records omit load-bearing dependencies

**ASN-0093, Properties Introduced table** — `FirstEmissionFreshness` premises: "first-emit predicate; L0; SC-NEQ; ChainPrefixExtension; ChainMembershipForOrigin; Cross-document disjointness; StoreT4Validity; ChainElementT4Validity; T7; T10."
And `SubsequentEmissionFreshness` premises: "subsequent-emit predicate; ChainDiscipline; ChainMembershipForOrigin; ChainEnumerationInjectivity; Cross-document disjointness; L0; DisjointSubAllocatorChains; SC-NEQ; T7; T10."

**Problem**: Both lists are incomplete relative to the arguments they record, and this matters because the entire discharge rests on a *simultaneous induction* whose soundness depends on a precise dependency graph.

- `FirstEmissionFreshness` content-against-`dom(L)` discharges T7's `zeros = 3` precondition "by FirstEmission's structural form and L1" — but neither **FirstEmission** nor **L1** appears in the premises list.
- `SubsequentEmissionFreshness` is worse:
  - *cross-document* needs **ChainPrefixExtension** to place both `a` and `a'` as anchor extensions before T10/Cross-document disjointness can fire — not listed (the lemma lists `ChainMembershipForOrigin` but not `ChainPrefixExtension`).
  - *cross-subspace* invokes T7 on `(a, ℓ)`, which requires `zeros(a) = zeros(ℓ) = 3` (needs **ChainUniformZeroCount** + **L1**) and T4-validity of both operands for `E(·)₁` to be well-defined (needs **ChainElementT4Validity**/**StoreT4Validity**) — none of these four are listed.

**Required**: Either make the premises columns exhaustive for both lemmas (add the missing FirstEmission, L1, ChainPrefixExtension, ChainUniformZeroCount, ChainElementT4Validity/StoreT4Validity), or state in the table that the column lists only the *distinctive* premises and that T7/T10 precondition-discharge premises are inherited. As written, the dependency record disagrees with the proof bodies.

### Issue 2: Duplicate StandardTriple/arity-N note (anti-bloat)

**ASN-0093, Worked example, *Arity convention***: "This is one admissible instance of K.λ's general signature `K.λ(d, ℓ, (e₁, …, eₙ))` with `N = 3`; the substrate admits arbitrary `N ≥ 3` per L3, and any higher-arity link value satisfying the precondition would be equally well-formed."

**Problem**: This restates, in different words, the note already made at L3 ("The StandardTriple default is retained for worked examples and notational convenience but not enforced structurally — the substrate admits arbitrary arity `N ≥ 3`"), and again gestured at in the State-model `Σ.L` paragraph. Three locations carry the same "StandardTriple is a notational default, substrate admits N ≥ 3" content. The Open-Questions "Higher-arity link discipline" item is distinct (it asks a forward question), but the worked-example paragraph adds nothing past L3.

**Required**: Trim the worked-example *Arity convention* to a one-line back-reference (e.g., "StandardTriple `N = 3` instance; L3 admits arbitrary `N ≥ 3`") and drop the redundant restatement.

## OUT_OF_SCOPE

### Topic 1: Document-level allocation discipline (S7d)

K.σ enforces only `T4-valid(d) ∧ zeros(d) = 2 ∧ d ∉ dom(M)`, deliberately *not* requiring `d` to be a T10a allocation event (weaker than ASN-0036 S7d). This is sound here — Cross-document disjointness depends only on M0 plus the anchor construction and handles even the properly-prefixing `d₁ ≺ d₂` case — so the substrate proves more by assuming less. Whether a higher layer should re-impose S7d's global document-allocation discipline is future territory, not a defect in this note.

VERDICT: REVISE
