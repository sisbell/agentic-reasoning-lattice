# Review of ASN-0086

The note is mathematically sound — I checked R0, R0a, R-Scope, R6a/b/c, and both wp cases and found the derivations correct, the edge cases (first/subsequent emission, self-targeting, retraction-of-retractor, self-nullifying emission) covered, and the cross-references confined to foundation ASNs (0034/0036/0040/0043/0093). The findings below are the meta-prose and over-specification the active `review-mode.anti-bloat` classifier asks me to surface.

## REVISE

### Issue 1: "Working domain" paragraph announces downstream derivations
**ASN-0086, "Working domain — `→*`-reachable states"**: "Two structural facts follow at every `→*`-reachable state, both *derived* below from this K.λ frontier-emission discipline rather than assumed: the homed link-set at each document is a contiguous chain prefix of `A_L(d)` (L-ContiguousPrefix), and `dom(Σ.L)` is a tumbler-prefix antichain (R0a)."
**Problem**: This is a forward-reference inventory — prose whose only job is to pre-announce that L-ContiguousPrefix and R0a will be proved later. The two lemmas are stated and proved in their own sections; the announcement advances no reasoning at its point of occurrence and is exactly the accretion pattern flagged for this note ("a definition's introduction enumerates downstream consumers"/forward-derivation essay).
**Required**: Delete the sentence. The lemmas carry themselves where they are stated.

### Issue 2: Nullify precondition P0f is redundant under PC
**ASN-0086, Definition — Nullify**: "**P0f**: `d_retr`'s homed link-set … is a contiguous chain prefix of `A_L(d_retr)` … without it the subsequent-emission `inc(ℓ_prev, 0)` may be off-chain and `Emit_R` undefined …; over →*-reachable Σ, P0f holds automatically at every allocated home (L-ContiguousPrefix)."
**Problem**: PC (`Σ →*-reachable`) is already a listed precondition, and the note states P0f "holds automatically" at every allocated home under exactly that condition. So `PC ∧ P0 ⟹ P0f`. The off-chain scenario the clause guards against cannot arise in this note's working domain. Listing P0f as a separate governing precondition, plus the paragraph justifying why it's needed, is dead weight — defensive over-specification.
**Required**: Drop P0f (it is entailed) or, if retained for a hypothetical non-reachable caller, state it in one clause without the guard-scenario justification.

### Issue 3: "Corollary (reduction to Emit_K)" is a restatement of its own definition
**ASN-0086, Definition — relational layer**: "*Corollary (reduction to Emit_K).* … *Proof.* The reduction follows directly from the layer's *Definition*: its only state-affecting operations are `Emit_K` and its alias `Nullify` … So every `Σ.L`-affecting step the layer takes simply *is* an `Emit_K` call, with nothing to decompose. ∎"
**Problem**: The corollary asserts what the immediately preceding Definition already fixes by construction; the proof says so ("nothing to decompose"). A definitional restatement dressed as a lemma-with-proof is structural noise.
**Required**: Fold the one substantive sentence into the Definition and remove the corollary/proof framing.

### Issue 4: Duplicate prose in the wp domain discussion
**ASN-0086, Weakest-Precondition Analysis (Case 2)**: the "*Domain restriction*" paragraph — "Restriction (ii) is the genuine added assumption: it is a *layer* commitment, not a substrate guarantee, because K.λ fixes emission *address* but not endset *shape*…" — and the next paragraph "*The unit-depth discipline is load-bearing*" — "The discipline is a layer commitment, not a substrate guarantee: because K.λ fixes emission *address* but not endset *shape* (the address-vs-shape gap)…"
**Problem**: Two consecutive paragraphs state the same proposition (the discipline is a layer commitment, not a substrate guarantee, *because* K.λ constrains address but not shape) in different words. One of them should carry the load-bearingness construction; the other is redundant.
**Required**: Merge: keep the load-bearingness construction (crafted-span counterexample) and delete the duplicated "layer commitment / address-vs-shape" framing from the Domain-restriction paragraph, which need only name restriction (ii) and cite the discipline definition.

## OUT_OF_SCOPE

### Topic 1: Higher-arity typed relations `L_K^{(n)}`
The Open Questions correctly defer treatment of `|Σ.L(a)| > 3` links as elements of higher-arity typed relations. The restriction to standard triples is stated cleanly and the arity-independence of R-Scope and `nullified` is proved where it matters; the general n-ary construction is genuinely future territory, not a gap here.

VERDICT: REVISE
