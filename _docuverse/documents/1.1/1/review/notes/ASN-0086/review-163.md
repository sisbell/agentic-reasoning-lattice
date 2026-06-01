# Review of ASN-0086

I checked the six relational properties (R0–R7a), the active/audit machinery (nullified, A_K, R6a–c), the contiguity/antichain lemmas (L-ContiguousPrefix, R0a, Cor1), the wp analysis, and the worked sketch against ASN-0093's K-operation contracts. The core reasoning is sound — the R0 branch discharge, R0a's two-case split on premise sets, R-Scope's arity-independence, and the Step 0–3 tumbler arithmetic all check out. The findings below are clarity/accretion items, consistent with the anti-bloat classifier this note carries.

## REVISE

### Issue 1: "P1 does not gate emission" is announced, then re-shown, inside the same definition
**ASN-0086, Definition — Nullify**: first paragraph closes with "Only P0 gates emission: P1 and P2 are postcondition and scope conditions respectively, and neither gates execution — **as shown in the composition below**, the underlying Emit_R executes and produces a Σ' even when `a ∉ A_rel^Σ` or `|Σ.L(a)| ≠ 3`." The very next (composition) paragraph then derives exactly that: "R0 at `d_retr` emits the retraction triple … **regardless of whether** `a ∈ A_rel^Σ` … The postcondition `a ∈ nullified(Σ')` thus holds **only on the P1 path**; off it … emission still proceeds but `a ∉ nullified(Σ')`."

**Problem**: The opening sentence forward-defers to the composition paragraph and pre-states its conclusion verbatim in substance. The reader meets the same fact ("emission is P0-gated, not P1-gated; postcondition holds only on the P1 path") twice within one definition — an announce-then-show duplication. The same point recurs a third time in *Definition — Unit-depth retraction discipline* ("since P1 gates only the postcondition, not emission (Definition — Nullify) …") and a fourth as *Definition — relational layer*'s "P1-confinement" commitment.
**Required**: State the P0-gates/P1-postcondition semantics once — in the composition derivation, where it is actually proved — and drop the pre-stating announcement. Downstream definitions may cite it without re-explaining it.

### Issue 2: wp section intro mislabels Case 1 as a weakest-precondition use
**ASN-0086, Weakest-Precondition Analysis, intro**: "Both cases use the standard wp notation `wp(S, R)`: **the weakest predicate** over the prior state Σ that guarantees the post-state Σ' satisfies R after S executes."

**Problem**: Case 1 explicitly does *not* compute a weakest predicate — it states `P0 ∧ P1 ∧ PC` is "a *sufficient* precondition," and adds "It is **not** the weakest precondition: PC is a global conformance condition … strictly stronger than the postcondition requires." Case 1 never writes a `wp(S, R) ≡ …` equation at all. So the blanket claim that "both cases use the standard wp notation … the weakest predicate" contradicts the section's own framing one sentence earlier (which correctly tags Case 1 "a sufficient precondition").
**Required**: Reword so the intro distinguishes Case 1 (a sufficient-precondition / load-bearingness analysis, not a wp) from Case 2 (the genuine weakest precondition). Don't claim both invoke the wp-as-weakest-predicate notation.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations
`L^Σ` collects only arity-3 links; the `|Σ.L(a)| > 3` case is deferred (and raised in Open Questions). Defining `L_K^{(n)}` projections is new territory, not a defect here.

### Topic 2: Concurrency/atomicity of Emit vs Observe
The consistency model under which `A_K` transitions are observed is left to a future note (Open Questions). Not required for this ASN's guarantees.

VERDICT: REVISE
