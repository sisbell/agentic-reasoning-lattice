# Review of ASN-0098

I've reviewed this ASN carefully — the proofs, boundary cases, derivations, and concrete examples. The work is thorough and rigorous.

**Proofs checked:**
- LP2★/LP3★/Store Monotonicity★ — inductive proofs with both base case and step case
- LP4 — explicit dependence on M1 noted; downstream lifting via intersection form
- LP9 — exact-difference formula with forward and reverse inclusions
- LP10 — exact-difference formula with forward and reverse inclusions
- LP11 — bijection equation gives both projection equality and range equality
- LP12 — per-slot biconditional lifted existentially
- LP12a — wp derived from LP10's exact-difference formula + per-slot non-emptiness biconditional
- LP12b — chain of citations explicit (ChainMembershipForOrigin → FirstEmission + ChainDiscipline → M0)
- LP-Fin — full case decomposition (sub-cases (i), (ii) for length, A and B for sub-case decomposition)
- LP-Fin Corollary — exact characterization of F ∩ interval
- LP19a/LP19 — freshness contradiction via tightness, projection-level consequence
- Achievability — each sub-case (CrossSub-C, CrossSub-L, NonNest, Desc, Anc) verified individually with explicit T1 divergence position

**Boundary cases checked:**
- Empty endset, empty arrangement, link with empty from/to endsets
- K.μ⁻ retention R = ∅ (wp = false)
- K.μ⁻ retention n'_{s_C} = 0, n'_{s_L} > 0 (discharged for content-canonical via LP12b)
- LP-Fin sub-case A range empty when #d_0 = z_2 + 1
- Non-canonical span cases (i), (ii), (iii) with explicit reasons for non-tightness
- Within-chain emission frontier at k_s = m

**Scope handling:**
- Link-canonical class for LP12a's second boundary case explicitly flagged OUT_OF_SCOPE with structural justification (LP-Fin Corollary at X = s_L places F-candidates inside dom(L)-eligible space)
- LP-Comp explicitly demoted to documentation note; LP18 and LP19 carry self-contained proofs

**Foundation references:** All citations are to ASN-0034, ASN-0036, ASN-0043, ASN-0047, ASN-0093 (foundation ASNs).

**Concrete examples:** Two — the worked trace (Σ through Σ_1 → Σ_2 and Σ_1 → Σ_3 branches, with slot 1 and slot 2 projections) and the achievability numerical example (tight `ℓ = δ(3, m)` vs non-tight `ℓ = δ(4, m)` contrast).

**Derived consequences:** Each claim's consequences are explored — the "What the Link Holder Can Rely On" section consolidates LP2/LP3/LP12/LP13/LP19 into trust-relationship terms.

VERDICT: CONVERGED
