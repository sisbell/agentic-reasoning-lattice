# Review of ASN-0086

This is a mature note; the proofs (R0, R0a, R-Scope, the wp Case 2 derivation) are rigorous and the boundary cases (empty endsets, empty homed-set first-emission, self-targeting to-spans) are exercised concretely in the Worked Sketch. My findings are confined to the residual meta-prose the `anti-bloat` classifier asks me to surface, plus one under-consumed result.

## REVISE

### Issue 1: "Definition — relational layer" restates the discipline and re-derives its own reduction
**ASN-0086, Three Operations, Definition — relational layer**: "The layer's sole discipline commitment: `Emit_K` is invoked only at type indices `K ≁ R`, every `R`-typed emission is routed through the `Nullify` alias at a P1 target ... so the layer satisfies the *unit-depth retraction discipline* ... Every `Σ.L`-affecting step the layer takes thus simply *is* an `Emit_K` call ... so the layer's state-affecting operations reduce to `{Emit_K}`."
**Problem**: The unit-depth discipline already has its own standalone Definition, the table already carries the `Relational layer` COMMITMENT entry, and `Nullify` is already defined as an `Emit_R` alias. This paragraph re-states all three and then re-derives "reduces to `{Emit_K}`" as fresh prose. It is essay content in a definitional slot — the reader must re-confirm facts stated elsewhere rather than learn anything new.
**Required**: Reduce to the operation set and the one load-bearing fact not stated elsewhere (the layer never invokes `Emit_K` at `K ~ R` except via the `Nullify` alias). Drop the re-derivation.

### Issue 2: EmptyInitialLinkStore justifies the assumption via implementation rather than stating it
**ASN-0086, Assumption — EmptyInitialLinkStore**: "This is the fresh-system boot condition: Gregory's `initmagicktricks` constructs both the content (granf) and link (spanf) enfilades empty via `createenf` whenever no persistent store exists, so no link address is allocated before the first link emission."
**Problem**: The assumption itself — all three stores empty at `Σ_init` — is fully stated in the preceding sentence. The `initmagicktricks`/`granf`/`spanf`/`createenf` sentence explains *why the assumption is reasonable* in implementation terms; it does not advance what the assumption says. This is exactly the "prose around an axiom/assumption explaining why it is needed rather than what it says" pattern.
**Required**: State the assumption and stop. If the implementation grounding is wanted, it belongs as a one-clause citation, not a mechanism walkthrough.

### Issue 3: "A_rel^Σ names the whole link store, not only the tuples" is pure restatement
**ASN-0086, Definition — Partition**: "*`A_rel^Σ` names the whole link store, not only the tuples.* `A_rel^Σ = dom(Σ.L)` collects *every* link address, whereas the standard-triple tuples ... are exactly those with `|Σ.L(a)| = 3` (see Definition — TypedRelation, below)."
**Problem**: `A_rel^Σ = dom(Σ.L)` is stated one line above; the tuple/store distinction is made precisely (and necessarily) in Definition — TypedRelation. This italicized aside restates both and adds a forward pointer to where the real content lives. It is noise the reader must skip.
**Required**: Delete. The distinction is carried where it is load-bearing (the `|Σ.L(a)| = 3` conjunct of `L_K^Σ`).

### Issue 4: L-ContiguousPrefix-Cor1 is proved but consumed by no invariant or operation
**ASN-0086, L-ContiguousPrefix-Cor1 (DepthTwoLinkAddresses)**: `#E(a) = 2` strictly for every `a ∈ dom(Σ.L)`.
**Problem**: The corollary carries a full positional-zero induction, but no downstream proof consumes it — R0a Case 2 uses (UL) for equal length, R5 uses L1b's `#E ≥ 2`, R-Scope uses the antichain. Its only appearances are "witnessing L-ContiguousPrefix-Cor1" in the Worked Sketch and a motivating mention in an Open Question ("Should L1b's `#E ≥ 2` be tightened to `#E = 2`"). A lemma that exists only to feed an open question and a witness annotation is accretion: either it does work in the argument or it is commentary.
**Required**: Either consume it (e.g., use the strict `#E = 2` where the proofs currently fall back on `≥ 2`/`(UL)`), or demote it from a proved lemma to a one-line remark attached to the relevant Open Question.

## OUT_OF_SCOPE

### Topic 1: CoverageEqualityDecidable's empty-gap / immediate-successor machinery
**Why out of scope**: Decidability of `coverage(e) = coverage(e')` is invoked only to support computability asides (`A_K` computable, Observe decidable), not to establish well-definedness of any slice or invariant — the quotient `T_admissible/~` and each `L_K^Σ` are well-defined as sets regardless. The cell-partition / `c_k.0` immediate-successor proof is implementation-grade detail. If computability is a guarantee the spec wants to make, it deserves its own note; pruning the decidability proof to its statement here would not weaken any invariant in ASN-0086.

### Topic 2: Higher-arity retraction interaction with `nullified`
**Why out of scope**: `nullified(Σ)` quantifies over `L_R^Σ`, which is arity-3 by construction, so a higher-arity (`|Σ.L(b)| > 3`) link carrying type-`R` coverage in slot 3 does not nullify. Whether higher-arity links should participate in retraction is genuinely new territory, already parked in Open Questions (multi-arity projections), not an error in this ASN.

VERDICT: REVISE
