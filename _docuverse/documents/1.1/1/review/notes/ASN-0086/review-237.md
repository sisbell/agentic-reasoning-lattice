# Review of ASN-0086

## REVISE

### Issue 1: "into but not onto" overstates — addr is onto when the store holds only triples
**ASN-0086, Definition — TupleAddress**: "The map is *into but not onto*: its image is exactly the standard-triple subset `{a ∈ dom(Σ.L) : |Σ.L(a)| = 3}` of the codomain `A_rel^Σ = dom(Σ.L)`."

**Problem**: "not onto" is asserted as a flat fact, but it holds only in states that actually contain a higher-arity link (`|Σ.L(a)| > 3`). In any state where every link is standard-triple — which includes the *entire* Worked Sketch (`a₁, b₁, a₂, b₂, a₃` are all triples) — the image equals `dom(Σ.L) = A_rel^Σ`, so `addr` *is* onto. The precise clause that follows ("image is exactly the standard-triple subset") is correct; the surjectivity claim contradicts it in the triple-only case.

**Required**: Change "into but not onto" to "into, and onto exactly when the store holds no higher-arity link" (or "not *necessarily* onto"). The map is an injection with image `{a : |Σ.L(a)| = 3}`; surjectivity is state-dependent.

### Issue 2: Nullify's *Effect* defers its own semantics forward to wp Case 1 (forward-reference meta-prose)
**ASN-0086, Definition — Nullify**: "*Effect:* when `P1 ∨ (a = a_emit(Σ, d_retr))` holds, `a ∈ nullified(Σ')` ... This conditioned effect is the weakest precondition derived once in wp Case 1 (single-tuple scope), covering both the P1 case and the self-emit case `a = a_emit(Σ, d_retr)`; it is not re-derived here."

**Problem**: A definition's *Effect* clause should state what the operation does. Here it instead announces *where the derivation lives* ("derived once in wp Case 1 ... not re-derived here") — bookkeeping about the document's own structure, not Nullify's behavior. The same paragraph also forward-points to Corollary R5.1 ("this emission is exactly the instance of Corollary R5.1 at slot 2"). This is the flagged "multiple paragraphs defer to the same downstream location" pattern: the Effect, the wp Case 1 cross-reference, and R-Scope all point at one another. The operation's effect (emit retractor `b`; if `a` lands in the to-coverage and in `A_rel^{Σ'}`, then `a ∈ nullified(Σ')`) can be stated directly without narrating where it is proved.

**Required**: State the effect as a self-contained clause; drop "derived once in wp Case 1 ... not re-derived here" and the R5.1 deferral. Let wp Case 1 cite Nullify, not Nullify pre-announce wp Case 1.

### Issue 3: relational layer / layer-reachable restate the same discipline commitment in different words
**ASN-0086, Definition — relational layer**: "Its one discipline commitment governs only `Σ.L`-growing steps: the layer emits type-`R` tuples only via `Nullify` — it never invokes `Emit_K` at a type index `K ~ R` except through the `Nullify` alias."
**ASN-0086, Definition — layer-reachable**: "every `L_R`-growing K.λ step obeys the discipline commitment — i.e. is a `Nullify`. K.σ and K.α substrate steps, and non-`R` `Emit_K` steps, may be freely interleaved; only the type-`R` growth of `Σ.L` is constrained."

**Problem**: Two adjacent definitions assert the identical content — (i) every `L_R`-growing step is a `Nullify`, and (ii) K.σ/K.α/non-`R` steps interleave freely — in paraphrase. The "freely interleaved with the substrate's document- and content-allocation steps K.σ and K.α (which the layer does not itself rename but does not exclude...)" aside in *relational layer* is a third restatement of the same interleaving point. This is the flagged "two paragraphs say the same thing in different words" pattern.

**Required**: State the discipline commitment once (in *relational layer*), and let *layer-reachable* reference it by name rather than re-paraphrase both the commitment and the free-interleaving clause.

## OUT_OF_SCOPE

### Topic 1: cardinality/structural-ratio bound on `nullified(Σ)` vs `dom(Σ.L)`
Already correctly listed as an Open Question; the monotone-growth of `nullified` with no shrinkage means an unbounded fraction of the store can be inactive, but bounding that ratio is a future-ASN concern, not a defect here.

### Topic 2: higher-arity typed relations `L_K^{(n)}`
The note deliberately restricts `L_K` to `|Σ.L(a)| = 3` and flags multi-arity projection as an Open Question. Correctly deferred.

VERDICT: REVISE
