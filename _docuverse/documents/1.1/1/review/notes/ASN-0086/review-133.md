# Review of ASN-0086

## REVISE

### Issue 1: wp Case 2 domain restriction is insufficient — the derivation silently requires the unit-depth retraction discipline, which substrate-conformance does not supply

**ASN-0086, Weakest-Precondition Analysis, Case 2 (*Result* and *Domain restriction*)**: "the weakest precondition is `wp(Emit_K(Σ, d, F, G), (a, F, G) ∈ A_K^{Σ'}) ≡ d ∈ dom(Σ.M) ∧ K ∈ T_admissible` (over substrate-conforming Σ)" and "the derivation's `a ∉ nullified(Σ')` step invokes R0a's antichain, which holds only at substrate-conforming states."

**Problem**: The stated justification for the domain restriction is *only* that R0a's antichain holds at substrate-conforming states. But R0a's antichain governs link **addresses** (no nesting), not retraction **to-span shape**. The derivation's actual exclusion step reads:

> "Nullify emits only unit-depth to-spans (Definition — relational layer), so every `L_R^Σ` tuple has coverage `{t : b ≼ t}` ... the fresh `a = a_emit(Σ, d)` is prefix-incomparable with every such `b` ... so `a ∉ coverage(G')`."

This works only because unit-depth coverage is the *prefix subtree* `{t : b ≼ t}`, which prefix-incomparability excludes. For a crafted (non-unit-depth) retraction span `(s, ℓ)`, coverage is a **lexicographic interval** `{t : s ≤ t < s ⊕ ℓ}`, and prefix-incomparability does **not** exclude a fresh frontier address: a wide crafted span rooted near `d`'s link chain can have `s ⊕ ℓ > a` with `s ≤ a`, putting the fresh `a` in coverage and nullifying it.

Crucially, the ASN itself states (Definition — Unit-depth retraction discipline) that "a crafted-span retraction emitted by a direct K.λ caller ... is L-invariant-conforming yet violates it" — i.e., a substrate-conforming state can carry crafted retraction spans. Therefore "substrate-conforming Σ" is strictly larger than the class the derivation needs, and over that stated domain the wp is false: `d ∈ dom(Σ.M) ∧ K ∈ T_admissible` can hold while a pre-existing crafted retraction already covers `a`, giving `(a, F, G) ∉ A_K^{Σ'}`.

The *Scope of the result* paragraph notes the dependence on the discipline informally ("relative to this note's operation set"), but the formal Result line fixes the domain as "substrate-conforming Σ," and the two are not equivalent. This is an inconsistency in the wp's stated precondition, not just an informal caveat.

**Required**: Make the unit-depth retraction discipline (or, equivalently, "Σ reachable using only the relational layer's operations") an explicit precondition conjunct of the wp, and correct the *Domain restriction* rationale to cite both R0a's antichain **and** the discipline. As written the rationale names only half of what the derivation consumes.

### Issue 2: the audit-vs-active mechanism is stated three times with cross-deferral (anti-bloat)

**ASN-0086, Definition — Nullified / R6b statement / R6b proof**:
- Definition — Nullified: "(The existential quantifies over the *audit* slice `L_R^Σ`, not the active subset `A_R^Σ`; the consequences of this choice are developed at R6b.)"
- R6b statement: "Because deciding `a ∈ nullified(Σ)` quantifies over the audit slice `L_R^Σ`, not the active subset `A_R^Σ` ..."
- R6b proof: "the existential's range over the audit slice `L_R^Σ` is the distinction stated above."

**Problem**: The same fact (the existential ranges over `L_R`, not `A_R`) is asserted in three places, with the Nullified parenthetical deferring forward to R6b and R6b then restating it. This matches two flagged patterns: "two paragraphs in the same document say the same thing in different words" and "a paragraph deferring to a downstream location" where the downstream location merely repeats. The forward pointer in the Definition adds nothing the reader can act on at that point.

**Required**: State the audit-vs-active distinction once. The cleanest home is the Definition of `nullified` (where the choice is actually made); R6b's statement should then assert its consequence without re-deriving the same observation, and the parenthetical forward-pointer should be deleted.

### Issue 3: R7a statement carries proof-case elaboration in the statement slot

**ASN-0086, R7a (paragraph following the formal statement)**: "When an `↝`-step is itself a primitive adding a single fresh key ... the step *is* a K.λ-step and the sequence has length 1; a composite that simultaneously adds fresh document and link keys decomposes into K.λ-extensions ... the single-fresh-home case ... being the length-2 sequence of one K.σ-prefix discharging L1a followed by one first-emission K.λ."

**Problem**: This is case-structure preview content sitting in the statement slot — the proof below re-derives exactly these cases (length-1 primitive, K.σ-prefixed K.λ replay). It is concrete (so not pure meta-prose), but its placement duplicates the proof's own case analysis. A reader following the formal statement must skip it; a reader following the proof meets it again.

**Required**: Move the length-1 and single-fresh-home instances into the proof (as the worked instances of the general construction), or cut them — the formal statement plus the proof already establish them.

## OUT_OF_SCOPE

### Topic 1: elevating the unit-depth retraction discipline to a substrate guarantee
Whether a dedicated retraction K-operation with a shape constraint should replace the layer convention is genuinely new substrate territory (already listed in Open Questions). Fixing Issue 1 only requires stating the discipline as a precondition; redesigning the substrate to *enforce* it belongs to a future ASN.

### Topic 2: higher-arity typed relations `L_K^{(n)}`
The note explicitly scopes itself to standard triples; the `|Σ.L(a)| > 3` projection question is correctly deferred.

VERDICT: REVISE
