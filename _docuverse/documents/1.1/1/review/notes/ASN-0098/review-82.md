# Review of ASN-0098

I checked the projection-displacement machinery (LP2–LP21, LP-Sub, LP-Fin) against the foundation contracts, traced the hardest proofs by hand, and scrutinized the prose for the anti-bloat patterns the classifier flags.

## Proof verification (spot checks that held)

- **LP-Fin** (interval finitude for canonical spans): the prefix-agreement claim, the `#d ≤ #d₀` bound, and the sub-case A/B split are each discharged with T1-case-(i)/T3 arguments at the named divergence positions. Sub-case A genuinely contributes 0 (separator-zero forces `a < s`); sub-case B contributes exactly `n` (the four-way split on `k` vs `k_s` is exhaustive over `k ≥ 1`). The total `= n` is sound, and the Corollary's "no other chain contributes" follows from the same split. Rigorous.
- **LP9/LP10** exact-difference formulas: both inclusions shown, multiplicity-within-document (S5) case implicitly covered since membership turns on `dom`-difference + coverage alone.
- **LP11**: both postconditions (`π`-image equality and `ran` invariance) proven via the bijection equation + K.μ~-FIX; reverse inclusion uses `π⁻¹`. Complete.
- **LP12a** wp: the reduction `project(a,i,d,Σ') = project(a,i,d,Σ) ∩ R` (via `dom(Σ'.M(d)) = R`) is correct, and the total-correctness `enabled ∧ …` form is the weakest. `R=∅ ⟹ false` boundary checks out.
- **LP20 corollary** cites "SD (ASN-0093); equivalently L14 (ASN-0047)" — I verified ASN-0047's L14 is the *unscoped* `dom(C)∩dom(L)=∅`, so the equivalence claim is correct (not conflated with ASN-0043's scoped L14).
- Boundary coverage is complete: empty endset, empty arrangement, empty-type slots, R=∅ contraction, freshly-registered empty document (LP8b).
- Cross-references are exclusively to foundation ASNs (0034/0036/0043/0047/0093) — no rule-7 violations.
- Worked-trace arithmetic checks: `iₖ = shift(i₁,k−1)` follows from `inc(·,0)` = +1 on the T4-valid `sig` position; `coverage(e₁) ∩ ran(M(d₁)) = {i₁..i₄}` is consistent even though `coverage` also contains the unarranged `shift(i₁,4)`.

## Anti-bloat scan

The forward-reference/restatement patterns the classifier targets do not survive into the current text. The consolidation paragraph "Projection invariance under arrangement-fixing transitions" is exemplary anti-bloat practice (one template, instances enumerated, no per-operation proof repetition). The static-vs-live distinction recurs across sections but each instance is contextually distinct (motivation / coverage-combinatoriality / persistence-contrast), and the LP13 contrast is a "what the operation does/does not guarantee" statement — explicitly allowed, not meta-prose. The worked numerical example's references to LP19a/LP19 are back-anticipations of lemmas stated immediately after, not deferrals to a distant location. No use-site inventories, axiom-rationale sub-paragraphs, or document-ordering justifications found.

## OUT_OF_SCOPE

### Topic 1: Reverse discovery, V-order reflection, link-canonical contraction
The Open Questions (reverse-discovery primitive, V-order of projected positions, contiguity under K.μ~, link-references-link induction, cross-document operation comparability, link-canonical content-emptying contraction) are correctly deferred. None is an error in this ASN; each is new territory. LP12b deliberately handles only the content-canonical class and routes the link-canonical inversion to the final Open Question — appropriate scoping, not an omission.

The note defines projection state, the operations that displace it, and the invariants those operations preserve — stated abstractly enough that any implementation must satisfy them. It has not drifted into implementation mechanics.

VERDICT: CONVERGED
