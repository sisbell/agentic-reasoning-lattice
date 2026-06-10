# Review of ASN-0115

I checked the new content (R0 plus R1–R11), the *Confinement* lemma, every worked instance, and the boundary structure of the gap analysis. I traced each proof against the foundation invariants it cites. The note is rigorous; I found no defects.

## What I verified

**Confinement lemma.** The T5 application is sound: with `p = [s₁,…,s_{m−1}]`, ordinal-level width (`actionPoint(ℓ) = m`) gives `p ≼ s` and `p ≼ reach(σ)` via TumblerAdd's prefix-copy below the action point; `s ≤ t ≤ reach(σ)` with `#p = m−1 ≥ 1` discharges T5's hypotheses, yielding `p ≼ t`. I confirmed `⟦σ⟧` has no member of depth `< m_S` (the only depth-`(m−1)` candidate is the prefix `p`, excluded by `p < s`), so the restriction to the depth-`m_S` bindable slice in R6 is exhaustive over `act`. The straddling counterexample `s=[1,5], ℓ=[2,0]` checks out (`s⊕ℓ=[3,0]`, `[2,3]∈⟦σ⟧` with subspace 2).

**R6 (gap analysis).** The case split is complete and the canonicity argument is correctly load-bearing: depth-compatibility fixes only `#s = m_S`, and the canonical prefix `s=[S,1,…,1,s_{m_S}]` is *derived from* `act ≠ ∅` (via D-SEQ★ + Confinement), not assumed. The `act = ∅ ∧ V_S(d) ≠ ∅` parenthetical correctly disposes of both sub-cases (non-canonical prefix; canonical with `s_{m_S} > n_S`), preserving the load-bearing negative (no interior hole). The worked instance (`n_1=4`, span `[1,2]`→`[1,7]`, `act={[1,2],[1,3],[1,4]}`, terminal overrun `{[1,5],[1,6]}`) is arithmetically correct, including `[1,2,1] ∈ ⟦σ⟧` being dropped by depth.

**R7 (Repeatability).** The comparability hypothesis (`Σ →* Σ'`, not merely co-reachable) is genuinely necessary, and the proof says so for the right reason: divergent branches can reach the same allocator frontier and commit the same address with distinct values (K.α admits any `v ∈ Val`), so immutability alone would not suffice. The asymmetric conclusion — link items stable from address-equality with no store invoked, content items requiring S0 — is correct.

**R8 (vacuity of link transclusion).** The subspace-sharing step (S3★-aux to land each position in `{s_C,s_L}`, then the contrapositive of S3★ against SD) is valid, and the vacuity proof (CL-OWN forces `d=d'`; CL-UNIQ forces `v=v'`) correctly rules out two distinct active link positions sharing an address, confining genuine transclusion to content.

**R11 (wp).** The single-live-condition analysis is a real wp observation: S3★ discharges store membership automatically from (i), so no independent `a ∈ dom(Σ.C)` conjunct survives. The orphan-via-K.μ⁻ instance correctly uses the K.μ⁻ frame to keep `Σ'.M(d')(v') = a` while `d`'s binding is contracted.

Boundary coverage is complete: empty spec-set, `act = ∅`, frontier overrun, empty/freshly-registered document, cross-document, cross-subspace, transclusion, and orphaned-but-referenced content are each handled. Cross-references are confined to foundation ASNs. The note specifies operation semantics abstractly (resolve-then-dereference, invariants any faithful realization owes) and does not drift into implementation mechanics; the link path correctly delivers *references*, deferring structure-reading to out-of-scope operations.

## REVISE

None.

## OUT_OF_SCOPE

### The five Open Questions are correctly deferred, not errors
**Why out of scope**: Inline content provenance, permitted-failure conditions, dangling-reference delivery, channel faithfulness, and subspace-straddling spans are each new territory. The note discharges its own boundaries cleanly — e.g., the ordinal-level restriction + Confinement scope out straddling spans (OQ5), and R2's denotation/transmission boundary scopes out channel faithfulness (OQ4) — rather than under-specifying within its lane.

VERDICT: CONVERGED
