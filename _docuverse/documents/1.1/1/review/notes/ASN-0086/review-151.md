# Review of ASN-0086

## REVISE

### Issue 1: Definition — Nullified states the `A_rel` restriction's effect twice

**ASN-0086, Definition — Nullified**: 
> "The set-builder restriction `a ∈ A_rel^Σ` confines `nullified(Σ)` to tuple addresses: ghost, content, and document addresses in `coverage(G')` are not collected."

and, three sentences later:

> "By R5, `coverage(G')` may include `A_rel^Σ` addresses — and, by L9 (TypeGhostPermission, ASN-0043), content, documents, or ghost addresses as well — but the restriction confines `nullified(Σ)` to the tuple addresses in `A_rel^Σ`."

**Problem**: These two sentences make the identical point — the `A_rel^Σ` set-builder restriction excludes ghost/content/document addresses and confines `nullified(Σ)` to tuple addresses. This is the "two paragraphs in the same document say the same thing in different words" pattern the anti-bloat classifier targets, here within a single definition.

**Required**: Delete one. The first sentence already carries the full content; the R5/L9 clause can be folded into it as a parenthetical ("…in `coverage(G')` — which by R5/L9 may include link, content, document, or ghost addresses — are not collected") rather than restated as a second sentence.

### Issue 2: Definition — Nullified pre-states R6b's audit-slice semantics

**ASN-0086, Definition — Nullified**: 
> "The existential quantifies over the *audit* slice `L_R^Σ`, not the active subset `A_R^Σ`: a retractor's tuple is consulted by `nullified` regardless of the retractor's own active-subset status."

**Problem**: This is the substantive content of R6b (and is restated again in R6b's body — "The membership test consults the audit slice `L_R^Σ`, which retains `b`'s tuple regardless of `b`'s active-subset status" — and in the R6b Remark and worked Step 3). Placing it in the definition slot forward-references a downstream lemma's interpretive consequence rather than advancing the definition's meaning — exactly the "essay content in structural slots / forward-reference accretion" pattern flagged for this note. The definition is complete and unambiguous without it (`L_R^Σ` already appears explicitly in the set-builder).

**Required**: Remove the sentence from the definition; R6b is the correct home for the audit-vs-active observation.

### Issue 3: Corollary (reduction to Emit_K) asserts layer substrate-conformance without derivation

**ASN-0086, Corollary (reduction to Emit_K)**: 
> "R7a's pre-state hypothesis is met from the outset: the relational layer is substrate-conforming, and `Σ_init` is substrate-conforming by definition…"

**Problem**: R7a requires *both* a substrate-conforming pre-state and a substrate-conforming issuing layer. The corollary invokes "the relational layer is substrate-conforming" as an established premise, but the one-step derivation is left implicit. The building block exists earlier ("Every `→*`-reachable state is substrate-conforming, since the K-op primitives … satisfy (a)–(c)"), and the layer's operations are exactly `Emit_K`/`Nullify` (both K.λ `→`-steps) plus read-only `Observe_K` — so the conclusion follows, but the chain is not stated. Per standard 6, a derived guarantee should name its premises.

**Required**: Add the explicit inference: every state-affecting relational-layer operation is a single K.λ `→`-step, which satisfies clauses (a)–(c) by its ASN-0093 contract; `Observe_K` takes no transition; therefore the layer carries substrate-conforming states to substrate-conforming states.

## OUT_OF_SCOPE

### Topic 1: Elevating the unit-depth retraction discipline to a substrate guarantee
The note correctly keeps the unit-depth retraction discipline a layer commitment (a direct K.λ caller can craft a wide-span retraction). Whether the substrate should expose a designated retraction K-operation with a shape constraint is the note's own Open Question — new territory, not a defect here.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
`L^Σ` collects only arity-3 links; the note explicitly defers the higher-arity construction. A future ASN, not an error.

VERDICT: REVISE
