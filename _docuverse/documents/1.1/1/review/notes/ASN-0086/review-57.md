# Review of ASN-0086

I've worked through R0's chain construction (Cases A/B verified against Worked Sketch values), R0a's two-stage proof, R0a-Cor1's contiguous-prefix induction, R6a–R6c's coverage-purity arguments, R7a's replay decomposition, and the WP analysis. The structure is sound. The proofs are explicit. The discipline-conditionality, Setup hypothesis, and witness-only reading of L1c are all transparently flagged rather than hidden. The Worked Sketch concretely traces both retraction (Step 1) and re-emission (Step 2) and verifies R0a-Cor1/Cor2 at Σ_2.

I found two prose-clarity issues that warrant correction before the ASN is built on. Everything else either resolves correctly under careful checking or is acknowledged in the Open Questions.

## REVISE

### Issue 1: Stage 1 "By symmetry" wording in R0a's proof
**ASN-0086, R0a Stage 1 cross-home sub-argument**: "By symmetry of the argument under the swap `(a, a') ↦ (a', a)` — every step depends only on the prefix relation and the `home` projection, both symmetric in their arguments — `a' ⊀ a` likewise."

**Problem**: `≼` is asymmetric (`a ≼ b` does not entail `b ≼ a`), so "the prefix relation symmetric in its arguments" is literally false. The argument's *structure* is symmetric under the variable swap — that is, no step uses directionality of `a ≼ a'` versus `a' ≼ a` — but the relation itself is not. A reader checking the proof against the definitions will pause at this sentence.

**Required**: Reword to make the structural symmetry of the *proof* explicit, rather than asserting symmetry of the relations themselves. E.g.: "By the same argument with `a` and `a'` swapped — every step relies only on the structural form of `≼` applied to its two variables, not on their order — `a' ⊀ a` likewise."

### Issue 2: R6b prose typo in audit-slice reading clause
**ASN-0086, R6b proof, audit-slice reading (i)**: "Decidable in time proportional to `|L_R^Σ|`, independent of `|L_R^Σ|` 's structural depth."

**Problem**: The second occurrence reads "`|L_R^Σ|`'s structural depth", but `|L_R^Σ|` is a cardinality (a number), which has no structural depth. The qualifier "structural depth" applies to `L_R^Σ` itself (or, more pointedly, to the retraction-chain graph induced by `L_R^Σ`).

**Required**: Drop the cardinality bars on the second occurrence — "independent of `L_R^Σ`'s structural depth" — or rephrase to "independent of any retraction-chain depth within `L_R^Σ`" to make the contrast with the active-subset reading (ii) sharper.

## OUT_OF_SCOPE

### Topic 1: Substrate-level elevation of the sibling-frontier discipline
**Why out of scope**: R0a (and downstream R0a-Cor1, R0a-Cor2, Emit_K function-ness, Nullify single-tuple scope) is conditional on an implementation hypothesis. Elevating the discipline to a substrate guarantee is a future substrate-level change explicitly flagged in OQ.

### Topic 2: Lifting the Setup hypothesis
**Why out of scope**: The "globally `s_C`-resident content" assumption is restrictive (R4 collapses to L14's scoped form without it; R0's L14a verification needs slice-aware reformulation). The OQ section already enumerates the specific reformulation work this would require.

### Topic 3: Tightening L1b to `#E = 2`
**Why out of scope**: R0a-Cor2 narrows L1b's `#E ≥ 2` admission to `#E = 2` discipline-conditionally. Whether to tighten the substrate-level L1b is a downstream design choice; the ASN flags it.

### Topic 4: Multi-arity link analogue
**Why out of scope**: The ASN restricts to standard-triple links. Higher-arity typed relations `L_K^{(n)}` require analogous slot-position and nullification machinery not pursued here.

### Topic 5: Concurrency and ordering semantics
**Why out of scope**: Atomicity of Emit/Observe, ordering of Observe results, and consistency models are layer-level concerns flagged in OQ.

### Topic 6: Dynamic type-catalog coordination
**Why out of scope**: Cross-layer type address coordination and dynamic catalog extension are layered conventions, not substrate guarantees.

VERDICT: REVISE
