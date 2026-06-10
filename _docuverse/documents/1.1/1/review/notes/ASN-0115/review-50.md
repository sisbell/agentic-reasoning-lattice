# Review of ASN-0115

I read this as a content-delivery semantics: `deliver` is resolution-through-arrangement followed by faithful dereference, in spec-set order, with a depth-compatibility override on `act`. I checked every proof, every boundary, and the anti-bloat patterns the classifier asks for. The mathematics holds.

## REVISE

None. The substantive checks below all pass; I record them so the verdict is auditable rather than a rubber stamp.

**Proofs verified:**
- *Confinement lemma.* `p = [s₁,…,s_{m−1}]` satisfies `p ≼ s` and `p ≼ reach(σ)` (TumblerAdd copies the prefix below the action point), and `s ≤ t ≤ reach(σ)` lets T5 conclude `p ≼ t`. The `#p = m−1 ≥ 1` precondition holds since `m ≥ 2`. Sound, and the non-ordinal-level counterexample (`s=[1,5]`, `ℓ=[2,0]`, `[2,3]∈⟦σ⟧` at `s_L`) is correct.
- *Override vacuity at `#s > m_S(d)`.* I confirmed independently: a depth-`m_S(d)` active position (with `m_S(d) < #s`) cannot lie in `⟦σ⟧` — Confinement forces agreement with `s` on `1..m−1`, which a shorter position cannot satisfy except by being `p ≺ s`, excluded from `[s, reach)`. So the override is genuinely a no-op there, and bites only on the "too shallow" (`#s < m_S(d)`) over-capture case. Consistent across R3/R6/R11.
- *R7 (Repeatability).* The non-trivial step — `act` reads whole-subspace state (`V_S`, `m_S`) but the hypothesis only equates the `⟦σ⟧`-restriction — is handled correctly: a shared bound `v` pins `m_S(d) = #v` equally at both comparable states (S8-depth), so `depthcompat` agrees; the empty-restriction and non-empty-with-override sub-cases both collapse to `act = ∅` at both states. The insistence on comparability (`Σ →* Σ'`, not common ancestor) is correctly justified by the fresh-allocation divergence argument. The content/link split is right: link items carry the address and need no store invariant; content items invoke S3★ + S0.
- *R8 link-vacuity.* CL-OWN forces `d = origin(a) = d'`, then CL-UNIQ forces `v = v'` — distinct link positions cannot co-resolve. The subspace-agreement step (S3★ contrapositive + SD + S3★-aux) is airtight.
- *R11 wp.* Condition (i) `v ∈ act(ρ,Σ)` with `subspace(v)=s_C` is genuinely the weakest precondition; `a ∈ dom(Σ.C)` is its automatic consequence (S3★), not a separate conjunct. The decomposition framing is correct and non-trivial.

**Boundary cases covered:** empty spec-set (`p=0 ⟹ ⟨⟩`), empty `act`, depth-incompatible spec, terminal overrun past frontier, transclusion, multi-origin, subspace crossing, orphaned-but-referenced content, weird-subspace start, unit-width and multi-position spans. The no-interior-hole guarantee is correctly *scoped to the bindable slice* (D-SEQ★ contiguity), explicitly excluding deeper named-but-unbound tumblers — a trap the ASN does not fall into.

**Anti-bloat scan:** The note structure is essentially linear; forward references are minimal (only `depthcompat` "defined below," adjacent). The recurring "terminal overrun, not interior hole" statement appears in box/proof/example, but each is in a distinct register and the example concretizes — not redundancy to flag. The "harmless subspace" paragraph handles an admitted-but-trivial case (`S ∉ {s_C,s_L}`), but it is mildly load-bearing (it establishes `act ≠ ∅ ⟹ S ∈ {s_C,s_L}`, which the D-SEQ★ reasoning in R6 implicitly needs). The recently-added off-channel frame-limit paragraph is a legitimate "what the operation does not guarantee" statement (per the nuance, not meta-prose), Nelson-grounded, and pairs sensibly with OQ4. The implementation citations (`specset2ispanset`, `whereoncrum`, absent `consolidatespans`, etc.) each ground a specific claim as confirming evidence, with explicit "an alternative implementation would still owe the same semantics" — this is the implementation grounding the review standards request, not drift.

## OUT_OF_SCOPE

The ASN's own Open Questions correctly defer the natural extensions (inline provenance, failure-vs-partial-delivery, dangling references under relaxed S3★, channel faithfulness, straddling spans). I have nothing to add — none of these is an error in this ASN, and the note states no claims for the harness-listed out-of-scope operations (extent reporting, endset search, link-structure reading); R10 explicitly defers endset structure.

VERDICT: CONVERGED
