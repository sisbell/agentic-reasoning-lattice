# Review of ASN-0132

I checked each CN-claim against its cited foundations, re-derived the CN-MONO weakest-precondition collapse, and verified the worked example's tumbler arithmetic address-by-address. The ASN holds up.

## What I verified

**CN-DEF / well-definedness.** The counted set is a subset of `dom(Σ.L)` (finite by L-fin, ASN-0093) with a per-link-decidable predicate (FL-DEC, ASN-0121); cardinality is well-defined. Defining the count *through* `sat` rather than through `|findlinks_FTT|` is what makes CN-ENUM structural rather than an obligation — correct architectural choice.

**CN-LOC.** `sat` reads only `Σ.L(a)` and the address projection `home(a)`; `nullified(Σ)` is selected from `L_R^Σ ⊆ Σ.L`. So the count is `Σ.L`-local. This load-bearing fact correctly excludes the three `Σ.M`-mediated rejected units (transclusion, appearance, version-refraction).

**CN-UNIT (d), the version case.** Verified against J4 (ASN-0047): the fork composite is K.δ + K.μ⁺(`V_{s_C}`) + K.ρ "and no other elementary steps," all of which frame `L' = L`. So forking touches no link, and refraction reduces to appearance multiplicity (c), already excluded by CN-LOC. The reduction is sound, not asserted.

**CN-MONO collapse.** Walked the full derivation. For a fresh ordinary link `ℓ`: pre-existing contributions are fixed by L12/LP13 (value) and `L_R^{Σ'} = L_R^Σ ⟹ nullified(Σ') ∩ dom(Σ.L) = nullified(Σ)` (addressability); the whole change is `ℓ`'s own contribution, giving wp `= sat(ℓ, q, Σ') ∧ ¬(∃ retraction tuple covering ℓ)` — matching FL-WP(a). The unit-depth collapse is rigorous: `ℓ ∈ coverage(G')` forces `t ≼ ℓ` with `t ∈ dom(Σ.L) ⊆ dom(Σ'.L)` and `ℓ ∈ dom(Σ'.L)`, so R0a (antichain) forces `t = ℓ`, contradicting freshness. I confirmed the antichain property survives version-nesting in the ASN-0047 model (link addresses under a document `d` and its version `inc(d,1)` diverge at the element-field separator), so the R0a citation is structurally valid here. The multi-step `≤` is correctly carried by FL-MON, not the single-step wp.

**The exhaustiveness of "only K.λ moves the count."** F-PRES (ASN-0127) covers every transition in `V_atomic ∖ {K.λ}` plus `K.μ~`, all framing `L' = L`; retraction is itself a K.λ (Emit_R). So K.λ is genuinely the sole mover — no operation skipped.

**Worked example.** Checked the arithmetic: `s ⊕ δ(8,8) = [1,0,1,0,1,0,1,13]`, coverage ordinals 5..12; `a₁`'s three disjoint from-spans each meet `coverage(F)` yet yield one `touch` (CN-UNIT a); `a₂` satisfies `sat` but is filtered by `addressable` (CN-RETRACT); `a₃` matches as an orphan (CN-ORPHAN); `a₄`'s `d₂`-rooted span diverges at the document component (`2 > 1`), `> [...,1,13]`, so disjoint; `a_R`'s empty from-endset annihilates via FL-EMP; `nullified(Σ) = {a₂}` since `a₂` prefixes only itself among equal-length distinct addresses. Count `= 2`, confirmed via CN-DEF, CN-ENUM, and the all-wildcard `= |addressable| = 4`. Both home-bounds check: `H₁ = ⟨d₁⟩` admits all (reflexive `d₁ ≼ d₁`), `H₂ = ⟨d₂⟩` yields a genuine (non-degenerate) CN-ZERO since `d₂ ⋠ d₁`, with `a₄` correctly excluded by residence (FL-RES) despite pointing into `d₂`.

The depth requirements are met: postconditions yield derived consequences (CN-UNIT → CN-TRANSCL; CN-LOC → CN-STAB), the wp analysis is non-trivial, and the concrete example exercises the three hardest rulings. The implementation notes correctly frame Gregory's dedup defect as a *deviation from* CN-UNIT (a set cannot double-count), and the cost aspiration is honestly demoted to a non-claim (CN-OBT) rather than smuggled in as a guarantee.

## REVISE

None.

## OUT_OF_SCOPE

The six Open Questions (V-spec/address-count reconciliation at the resolution boundary, cross-inquiry concurrency for count-equals-length, count caching, fragmentation-dedup system contract, count-vs-enumeration cost, federation) are each correctly deferred — they concern the resolution layer, concurrency discipline, implementation contract, or replication, all genuinely downstream of the single-state, address-phrased operation specified here. None is an error in this ASN.

VERDICT: CONVERGED
