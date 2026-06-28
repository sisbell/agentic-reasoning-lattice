Reading the ASN as a system — dependency graph, proof structure, axiom-to-theorem chain — before flagging anything.

**Dependency graph.** S3 depends on {S1, AX-1, AX-2}. S1 depends on S0. S0, AX-1, AX-2 are axioms. No cycle, no hidden precondition. ✓

**S1 proof.** Single step: pick arbitrary a ∈ dom(Σ.C), apply S0 to get the conjunction a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a), extract the first conjunct, close by generalization. Sound. ✓

**S3 proof — case split coverage.** The split partitions v ∈ dom(Σ'.M(d)) into: (i) inherited — v ∈ dom(Σ.M(d)) ∧ Σ'.M(d)(v) = Σ.M(d)(v); (ii) new-or-redirected — v ∉ dom(Σ.M(d)) ∨ Σ'.M(d)(v) ≠ Σ.M(d)(v). These are mutually exclusive and jointly exhaustive over the classical reading. Case (i) applies the IH then S1; case (ii) applies AX-2 directly. The antecedent of AX-2 matches case (ii) exactly: v ∈ dom(Σ'.M(d)) ∧ (v ∉ dom(Σ.M(d)) ∨ Σ'.M(d)(v) ≠ Σ.M(d)(v)). ✓

**Axiom consistency.** S0 permits dom(Σ'.C) ⊋ dom(Σ.C) (it constrains old members, not new ones). AX-2 permits a mapping to target an address added within the same transition, since the post-state C is dom(Σ'.C). No conflict. ✓

**One structural gap found — declared metadata dependency not substantiated by any formal proof step.**

---

### Declared dependency on ASN-0034 not cited in any formal proof
**Class**: REVISE
**Foundation**: N/A (internal consistency between ASN metadata and claim content)
**ASN**: ASN metadata ("Declared depends: ASN-0034") vs. formal contracts of S0, S1, S3, AX-1, AX-2
**Issue**: The ASN metadata declares ASN-0034 as a dependency. The only mentions of GlobalUniqueness appear in S1's informal prose ("each at a fresh address guaranteed unique by GlobalUniqueness (ASN-0034)") and S1's Forward References subsection, which explicitly states GlobalUniqueness is "not used in S1's proof." No formal contract in the ASN — not S0, S1, S3, AX-1, or AX-2 — lists GlobalUniqueness in a *Depends* entry or invokes it in a proof step. A declared dependency in the metadata asserts that some claim in this ASN builds on an exported statement of ASN-0034; no such claim exists. The dependency is either spurious, or a claim that actually invokes GlobalUniqueness is missing from this ASN.
**What needs resolving**: Either remove ASN-0034 from the declared dependencies (if GlobalUniqueness is genuinely not load-bearing for any claim here), or identify which claim requires the uniqueness guarantee, formalize the dependency in that claim's *Depends* entry, and invoke it in the proof. The informal prose in S1 suggests uniqueness matters for the address-allocation argument, but that argument is not currently formalized as any claim in this ASN.

---

VERDICT: REVISE