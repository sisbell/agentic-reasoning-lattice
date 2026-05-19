# Review of ASN-0093

## REVISE

(none — see analysis notes below)

## OUT_OF_SCOPE

(none — the ASN's scope statement matches the prompt's deferred topics, and all deferred items are explicitly marked in Open Questions)

## Analysis Notes

**Simultaneous-induction framing is sound.** I verified no circular dependency within the inductive step: L14(Σ') depends on L0(Σ') and StoreT4Validity(Σ'), neither of which transitively depends on L14. ChainMembershipForOrigin(Σ') depends on IH-at-Σ plus axiom + foundation, not on itself at Σ'.

**Cross-document disjointness Case A.** Verified: from `d₁ ≼ d₂` proper with M0's `zeros = 2` at both, `d₂[#d₁+1] ≠ 0` (else `zeros(d₂) > 2`), giving divergence at `k = #d₁ + 1` within both anchors. Case B exhausts via NAT-order trichotomy with B.i and B.ii handling equality and asymmetric lengths respectively.

**T10a.7 contrapositive argument.** Verified: `t_m ≤ t_{n_prev} ⟹ m ≤ n_prev` is the correct contrapositive of strict monotonicity. The full chain `a' = t_m ≤ t_{n_prev} = a_prev < t_{n_prev+1} = a` correctly establishes `a' < a`, hence `a' ≠ a`.

**FirstEmission's freshness derivation in the Remark.** Verified: against `dom(C)`, uses ChainPrefixExtension (base case for the new emission, IH at pre-state for existing entries) + ChainMembershipForOrigin + Cross-document disjointness + T10. Against `dom(L)`, uses StoreT4Validity + L0 + SC-NEQ + T7. No circularity.

**Worked example.** Spot-checked Steps 1–9 including the structural form of `[d.0.s_C.1]`, `b_C(d)` and `b_L(d)` chain steps via TA5(c)/TA5(d), origin projection computation, Cross-document disjointness verification at Step 5 (Case A with `d ≼ d'`) and Step 9 (Case B.i with `#d = #d_alt`, Case B.ii with `#d_alt < #d'`). All concrete computations match.

**Discharge matrix.** All 17 invariants × 3 transitions = 51 entries cover preservation correctly. The repeated "Holds at Σ': same derivation" for L14 across all three transitions over-derives at K.σ (where C/L are both in frame) but is not incorrect.

**T10a chain-lemma applicability remark.** The proof-inspection argument that T10a.1/T10a.7 require no T4-validity and T10a.8's T10a.4 citation can be replaced by TA5a per-step propagation is sound. The substrate's substitution preserves T10a.8's conclusion without invoking tree-embedding.

META: (none — the ASN remains squarely in spec territory, defining state, operations, invariants, and proving preservation by simultaneous induction)

VERDICT: CONVERGED
