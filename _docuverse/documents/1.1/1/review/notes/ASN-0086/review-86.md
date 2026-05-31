# Review of ASN-0086

This note has clearly been through several anti-bloat cycles, and the core proofs (R0a, R0a-Cor2, R7a, the Worked Sketch arithmetic) check out — I verified the cross-home/same-home antichain argument, the depth-2 zero-position induction, and the concrete tumbler computations in the sketch, and they hold. The remaining defects are concentrated in meta-prose that the `review-mode.anti-bloat` classifier exists to catch, plus one imprecise deferral.

## REVISE

### Issue 1: Notational-choice justification is pure meta-prose
**ASN-0086, "Notation — subscript read modulo `~`"**: "the more pedantic notation `L_{[K]}^Σ`, … would be equivalent (and is conceptually preferable when type-equivalence is in focus) but is not adopted for typographic compactness."

**Problem**: The first two sentences establish the substantive fact (the slice depends only on `[K]`, so `L_K = L_{K'}` when `K ~ K'`). Everything after — the inventory of which constructs read modulo `~`, the apologetics for *not* using the bracketed notation, "conceptually preferable but not adopted for typographic compactness" — advances no reasoning. It explains a typesetting decision. This is exactly the "essay content in structural slots" the anti-bloat pass targets.

**Required**: Keep the fact (slice depends only on `[K]`; `~`-equivalent indices induce equal slices). Delete the notation-choice justification and the use-site inventory.

### Issue 2: The relational layer is defined twice
**ASN-0086, "Definition — relational layer"** and **Properties table, "Relational layer" COMMITMENT row**: both fully restate the operation set `{Emit_K, Observe_K, Nullify}`, the Nullify-as-alias fact, the Nullify-as-sole-`R`-producer discipline, and the reduction corollary.

**Problem**: Two paragraphs in different sections say the same thing in different words — a flagged pattern. The table row is supposed to be a one-line index entry but reproduces the entire definition including the discharge rationale ("the K.λ contract makes the sibling-frontier discipline a substrate-level guarantee, so this commitment only restricts the *value-shape*…").

**Required**: The Properties table entry should be a pointer ("Operation set + reduction corollary; see Definition — relational layer"), not a second copy of the definition body.

### Issue 3: Label-taxonomy essay in "Properties Introduced"
**ASN-0086, "Properties Introduced", *Type labels* paragraph**: "DEF-Consequence marks a direct consequence of a Definition's quantifier range… The COMMITMENT label is reserved for entries that are *not* derivable from substrate axioms — they restrict caller behavior or layer discipline rather than defining substrate structure."

**Problem**: This is a meta-prose preamble explaining the table's own column vocabulary. A reader needs the labels to be self-evident from the entries, not a paragraph theorizing about what each label connotes. The DEF-Consequence justification in particular exists only to defend the R6b classification.

**Required**: Drop the taxonomy essay. If a label is non-obvious, make the single entry self-explanatory inline.

### Issue 4: R6b's table entry explains why it is *named*, not what it says
**ASN-0086, Properties table, R6b row**: "a tautological consequence of the Definition's quantification range over `L_R^Σ` (audit slice) rather than `A_R^Σ` (active subset), **named for its substantive decision-procedure-flatness implication** on retraction-of-retraction."

**Problem**: "named for its … implication" is prose about the naming decision. The substantive content (deciding `a ∈ nullified` is a single flat pass over `L_R^Σ`, unaffected by the witness retractor's own status) is already stated in the R6b body and re-exhibited in Worked Sketch Step 3. The table row should state the rule, not litigate why it earns a label.

**Required**: State R6b as the flat single-pass membership rule; remove the "named for…" framing.

### Issue 5: "Auxiliary pre-step" deferral is imprecise
**ASN-0086, Worked Sketch, *Auxiliary pre-step***: "The K.σ-then-K.λ first-emission setup … is exactly R7a's Worked Example 1 (CreateDocAndLink); see there."

**Problem**: This is a deferral to a downstream location (a flagged pattern), and it is not exact. Worked Example 1 *creates a fresh document* `d_new ∉ dom(Σ.M)` (the K.σ step is load-bearing there). In the Worked Sketch, `d = 1.0.1.0.1` is pre-existing (`d ∈ dom(Σ_{-1}.M)` per Setup), so Step 0 is a bare K.λ first-emission with no K.σ component. The "K.σ-then-K.λ" description does not match the sketch's actual Step 0. A reader following the pointer finds a different construction.

**Required**: Either drop the deferral (Step 0 is self-contained — a K.λ first-emission at pre-existing `d`) or correct the description so it does not claim a K.σ step the sketch does not take.

### Issue 6: R7a's substantive content is thin relative to its precondition weight
**ASN-0086, R7a**: quantifies over the categorical `↝` but only for a "substrate-conforming layer," where conformance (catalog (b)) is defined to preserve precisely the chain lemmas (ChainMembershipForOrigin, ChainEnumerationInjectivity) the replay-determinism step consumes.

**Problem**: The precondition is engineered to supply exactly what the conclusion needs, which makes the headline claim ("nothing outside K.λ affects `Σ.L`") close to tautological — the real work is the K.σ-interleaving and chain-order determinism, not the categorical reach. This is acceptable as a load-bearing lemma (it underwrites the reduction corollary), but the framing oversells. The `a* = [d.0.s_L.1.1]` counterexample paragraph and the dual worked examples (length-2 and length-4) are valuable; the categorical-`↝` quantifier and the repeated "this is the load-bearing site for catalog (b)" asides are where the prose inflates.

**Required**: State R7a's scope plainly (link-store effects of any K-op-composing layer decompose into K.σ/K.λ replay) and trim the catalog-(b)-rationale repetitions to a single statement.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs. Observe
**Why out of scope**: The Open Questions already park this. The sequential-atomic-transition axiom (ASN-0093) is assumed; a concurrency model is genuinely new territory, not a defect here.

### Topic 2: Higher-arity active subsets `A_K^{(n)}`
**Why out of scope**: The note explicitly restricts to standard-triple links and flags multi-arity as open. Not an error in the present scope.

VERDICT: REVISE
