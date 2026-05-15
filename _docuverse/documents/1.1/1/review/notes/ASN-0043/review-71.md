# Review of ASN-0043

## REVISE

(none)

## OUT_OF_SCOPE

(none — the ASN already flags its only known limitation, the PrefixSpanCoverage axiom awaiting relocation to a future span/tumbler-algebra ASN, in its Open Questions section)

VERDICT: CONVERGED

---

*Verification notes (for the record, not findings):*

- **L1c chain existential**: The clauses `t₀ = s`, `tₙ = a`, `kᵢ ∈ {0,1,2}` with TA5a side-condition, `k₁ = 2`, and `#tᵢ > #s` are jointly tight. The argument that no later `kⱼ = 2` is admissible (zero count saturates at 3 after step 1) and the argument that `k₁ = 1` cannot deliver `s = h(a)` (the new zero would land at position `> #s + 1`) both check out against TA5(b)/(c) and the position-of-zero argument.
- **L9 construction**: With the s_C-residence precondition now in place, `g ∉ dom(Σ.C)` is delivered by T7 against the precondition's universal subspace claim. Case A's freshness uses the empty-set hypothesis directly via `home(a) = d'`; Case B's freshness uses T10a.7 + L-fin to pick the least unallocated sibling. Conformance of Σ' is verified entry-by-entry against the state-local L- and S- invariants.
- **L11a Case (ii)**: The "back to first agreement" phrasing is informal but the underlying logic (T10a per-(t,k') uniqueness forces step-1 coincidence at shared seed; determinism of `inc` propagates; T10a.6 fixes a's allocator uniquely) is sound.
- **Worked example**: Σ → Σ₁ exercises L11b (non-injective extension); Σ₁ → Σ₂ exercises L13 (link-to-link); Σ₂ → Σ₃ exercises arity-4 L3/L6/L8; Σ₃ → Σ₄ exercises L8 discrimination via sibling ghost types whose prefix cones are disjoint at position 8. Coverage of reflexivity, transitivity (implicit), discrimination, arity boundaries, and reflexive addressing is thorough.
- **PrefixSpanCoverage**: The sketch (forward via T1 case (i) at position #x with NAT-discrete bounding `t_{#x} ≤ x_{#x} < x_{#x}+1`; backward by case analysis on `#t` vs `#x` excluding T1 case (i) and forcing T1 case (ii)) is plausible and re-derivable from ASN-0034 primitives. The ASN's transparency about its axiomatic-pending-relocation status is appropriate.
