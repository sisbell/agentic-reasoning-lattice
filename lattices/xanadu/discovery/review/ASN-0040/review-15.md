# Review of ASN-0040

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Formal bridge between Σ.B and T8's allocated set
The ASN draws the analogy — "B0 is the state-level reading of T8" — but never formally identifies Σ.B with the `allocated(Σ)` set that T8's invariant quantifies over. A one-line bridge property (`allocated(Σ) = Σ.B`) would close the loop between the algebraic (T8, T9, T10a) and set-theoretic (B0, B1, B7) derivations of global uniqueness. Not needed for the current proofs, but a future ASN establishing operational correctness will want it.
**Why out of scope**: This is a cross-cutting integration property, not a gap in the baptismal mechanism itself.

### Topic 2: Stream identity as a named property
The B1 proof and B6 necessity proof both establish that `S(p, 1) = S(p', 2)` when `p` ends in zero as its sole T4 defect and `p'` is `p` with that trailing zero removed. This stream collapse has structural consequences (many-to-one mapping from `(p, d)` pairs to streams) that downstream ASNs on allocation or namespace management may need to cite. Elevating it from an inline lemma to a named property would make it citable.
**Why out of scope**: The lemma is correctly proven and used within this ASN; naming it is a convenience for future work, not a correctness issue here.

---

The proofs in this ASN are unusually thorough. Every invariant preservation argument covers the target namespace, all B6-valid other namespaces (via B7), non-B6 namespaces whose streams are entirely T4-invalid (via B10), and the subtle trailing-zero sole-defect case where stream identity collapses a non-B6 namespace to an already-handled B6-valid one. The B6 necessity proof establishes all three conditions as independently necessary — condition (ii) for T4 directly, condition (iii) for zero-budget overflow, condition (i) for propagation of interior violations and for preventing namespace collapse via stream identity. The B7 exhaustion over different-length, equal-length non-nesting, and equal-length nesting cases is complete, with Case 3's fixed-position disagreement argument (zero separator vs. positive final prefix component) correctly grounded in TA5(d) and T4a(iii). No proof-by-similarly, no bare checkmarks, no missing cases.

VERDICT: CONVERGED
