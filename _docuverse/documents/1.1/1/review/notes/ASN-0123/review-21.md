# Review of ASN-0123

I checked the load-bearing proofs line by line — the freshness/contiguity machinery (VN-B1, nextv), the well-formedness obligation (V-WF), the severance theorem (V9), the antichain lemma (SA), the G2 necessity argument, and the ownership inheritance (V8). All hold. Below I record the verifications rather than manufacture issues.

## REVISE

None.

**Verifications performed (no defects found):**

- **VN-B1 (version-namespace contiguity).** The four-case induction is complete: `Node(e)` excluded by `zeros = 0 ≠ 2`; `k=2` excluded by the penultimate-component argument (`inc(t,2)`'s separator zero vs. `d`'s nonzero last component, T4); `k=1` forces `t = d, j = 1` (T3) giving `m=0`; `k=0` forces `t = c_{j−1}` via TA5-SigValid + the no-trailing-zero constraint, then `j = m+1` from the IH and freshness. Each case is shown, not waved. The deliberate refusal to cite ASN-0040's B2 (whose precondition is *global* B1, unavailable here) and the re-derivation of the frontier from VN-B1 + S0 is exactly right.

- **V-WF.** ValidComposite★ clause 1 (elementary preconditions at intermediate states) is discharged for K.δ (both owned sub-cases and the account-tier cross-owner sub-case), K.μ⁺ (strict extension from `∅`/canonical-shape preconditions), and each K.ρ. Clause 2 (couplings initial-to-final) — J0 vacuous (`dom(C')=dom(C)`), J1★/J1'★ pinned by the `R'` clause. The `n=0` degeneration and the terminal-boundary inheritance of P4★/P4a/P7a are handled. The delegation of per-state invariants to ExtendedReachableStateInvariants (valid composite ⟹ all conjuncts, incl. CL-OWN/CL-UNIQ/D-SEQ★) is a legitimate use of a foundation theorem, not a shortcut around proof.

- **V9 (severance).** The contradiction argument is airtight: `d_src ≼ v` ⟹ (O5(ii) at the π-allocating K.δ) `#pfx(π_o) ≤ #pfx(π)` ⟹ (Covering-chain + O1b) `pfx(π_o) ≺ pfx(π)` ⟹ comparison of `pfx(π)` with `d_src` closes both branches (Z-mono/O1a on one side, O2 maximality on the other). The account-tier restriction is correctly identified as what makes `allocated_by(π, v)` — hence O5(ii) *with respect to π* — available, rather than assumed.

- **SA.** The `[d,0,s,k]` structural form (LP-Sub) plus the zero-count argument (a proper extension's document prefix would absorb a third zero, contradicting `zeros = 2`) correctly yields the antichain, and G2's use of it to collapse subtree coverage to address identity is sound.

- **VD biconditional.** `derives_addr(v,d) ⟺ v ∈ E ∩ S(d,1)` survives the forward direction precisely because `d ≼ v` rules out cross-owner forks (severed), leaving owned forks (which land in `S(d,1)`). The unrestricted forward direction is correctly flagged as false.

- **Worked instances.** Both the carry-through instance (`|A| = 2 < n = 3`, provenance counting shared addresses not positions, refraction onto both positions holding `a₁`) and the cross-owner instance (divergence at position 4, single document K.δ, witness survival under severance) compute correctly against the stated arithmetic.

- Edge cases (`n=0`, first vs. subsequent owned fork, cross-owner fork, iterated forking V6) are each addressed. Foundation references are exclusively to the verified foundation set; ASN-0103/0068/0122 appear only in the harness scope block, not the ASN body.

## OUT_OF_SCOPE

The ASN's own scope statement and Open Questions correctly defer the genuinely new territory — non-versioning allocations into a version namespace (the soundness condition for VD), derivation-direction recovery from symmetric provenance, link-subspace re-homing across a fork, concurrent-fork serialization, location-fixed windowing, and withdrawal/supersession semantics. None of these is an error in this ASN; each is future work, and the note touches them only where a frame condition bears on a fork guarantee. I have nothing to add here.

VERDICT: CONVERGED
