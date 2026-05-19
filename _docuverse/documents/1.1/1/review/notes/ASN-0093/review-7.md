# Review of ASN-0093

## REVISE

(none)

## OUT_OF_SCOPE

(none — the open questions correctly identify deferred topics: arrangement mutation, entity stratification, provenance recording, link withdrawal, concurrency, higher-arity links, document address discipline beyond T4 + zeros=2, and additional subspace identifiers.)

---

After reviewing this ASN against the Dijkstra-standard, I find the discharge matrix exhaustive and the proofs rigorous. Specifically:

**Lemma proofs verified.** ChainPrefixExtension's induction (base case via FirstEmission's concrete structural form, step via TA5(b)/(c) + TA5-SigValid + chain-element T4-validity) holds. ChainMembershipForOrigin's contiguous-prefix form is properly maintained across K.σ (via C2/L1a from IH refuting d_new origin), K.α first-emit (placing t_1), K.α subsequent-emit (T10a.7 strict monotonicity placing t_{m_d+1}), and the K.λ analogues. StoreT4Validity reduces correctly via ChainMembershipForOrigin + FirstEmission's T4-valid concrete form + TA5a per-step k=0 propagation.

**Cross-document disjointness Case B is properly case-split** into B.i (#d₁ ≤ #d₂, extract witness from d₁ ⋠ d₂'s component-conjunct failure) and B.ii (#d₂ < #d₁, symmetric), addressing the asymmetric-length subtlety where one ⋠ clause is satisfied by length alone.

**T10a chain-lemma applicability remark** substantively justifies invoking T10a.1, T10a.7, T10a.8 on non-tree-embedded chains by inspecting which dependencies require tree-embedding (only T10a.8's T10a.4 citation does) and substituting TA5a-based per-step propagation from FirstEmission's T4-valid base.

**Simultaneous-induction discipline** is correctly applied: the IH bundles all invariants + lemmas at Σ; the step at Σ → Σ' uses only IH at Σ. K.α subsequent-emit freshness derivations consume ChainMembershipForOrigin + ChainPrefixExtension + StoreT4Validity + Cross-document disjointness all at Σ, never at Σ'.

**Worked example** exercises both first-emit and subsequent-emit branches of K.α (Steps 2, 4, 6) and K.λ (Steps 3, 7, 8), verifies Cross-document disjointness Case A (Step 5) and both Case B sub-cases (Step 9), and concretely confirms the L14 derivation via E(·)₁ partitioning.

**Foundation references** are all to verified foundations (ASN-0034, 0036, 0040, 0043).

The substrate's transition vocabulary closure is implicit ("the transitions defined later in this note") but adequate; the alternative of an explicit OperationClosure axiom would be a stylistic preference, not a correctness gap.

VERDICT: CONVERGED
