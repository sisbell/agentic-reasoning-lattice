# Review of ASN-0086

This ASN is unusually polished — the arithmetic in the Worked Sketch checks out end to end, R0a's two-direction home-prefix argument is rigorous, and R0a-Cor2's zero-position-stability proof is sound. The findings below are precision and the anti-bloat patterns the active classifier asks me to surface.

## REVISE

### Issue 1: WP Case 1 is the trivial wp; it misses that single-tuple scope is arity-independent
**ASN-0086, Weakest-Precondition Analysis, Case 1**: "`wp(Nullify(Σ, d_retr, a), single-tuple scope at Σ') ≡ P0(Σ, d_retr) ∧ P1(Σ, a) ∧ P2(Σ, a)` ... the conjuncts are exactly Nullify's stated preconditions."

**Problem**: The review standard warns against wp analysis "only computed for postconditions where the answer is trivially true." This case reduces the wp to a verbatim restatement of the operation's own three preconditions — the trivial answer. The substantive, non-trivial observation is left unsurfaced: single-tuple scope `{t : a ≼ t} ∩ A_rel^{Σ'} = {a}` is a purely address-prefix property and is established by R0a's antichain on `dom(Σ'.L)` plus `a ∈ A_rel^{Σ'}`. It does **not** depend on `P2` (`|Σ.L(a)| = 3`). Nullifying an arity-4 address would establish single-tuple scope identically. `P2` is a meaningfulness guard for the *active-subset* effect, not a load-bearing conjunct for *this* postcondition. The analysis presents all three preconditions as if jointly required, which is precisely the depth the wp section is supposed to extract and does not.

**Required**: State that the wp for single-tuple scope reduces to `P0 ∧ P1` on the postcondition's own terms, and that `P2` is carried only because Nullify's contract restricts to arity-3 (a meaningfulness constraint, not a correctness obligation for single-tuple scope). Make the arity-independence explicit — that is the non-trivial content.

### Issue 2: "What R7a contributes beyond clause (b)" is meta-prose about significance, not argument
**ASN-0086, R7a, paragraph beginning "What R7a contributes beyond clause (b)"**: "R7a's distinctive work is the *constructive replay*: it exhibits the Δ-enumeration ... That `Σ.L` cannot be affected outside class (iii) is then a corollary of L12/L12a, not of clause (b)."

**Problem**: Per the active anti-bloat classifier, this is essay content explaining what the lemma contributes and why it is interesting, rather than advancing the proof. It does not establish any step; it editorializes about the relationship between clause (b) and the conclusion. A reader following the proof must skip it.

**Required**: Delete, or compress the single load-bearing fact (the conclusion is a corollary of L12/L12a) into the proof body where it is used.

### Issue 3: R7a carries two worked examples plus a forward deferral for one lemma
**ASN-0086, R7a, "Worked example 1" and "Worked example 2"**: example 2 "exercises the decomposition's interleaving structure ... non-trivially."

**Problem**: Two full worked examples illustrate the same decomposition; example 2 is structurally example 1 doubled, and its only novel content is the cross-home K.σ–K.λ–K.σ–K.λ interleaving. The classifier flags duplication of this kind. Relatedly, the body twice defers downstream — "extending the active-subset machinery to multi-arity relations ... is left to the open question on higher-arity links" and similar — accumulating forward pointers.

**Required**: Keep the interleaving (length-4) example and reduce example 1 to a one-line note that the single-emission case is the `m = 1` collapse, or vice versa. Remove redundant downstream deferrals.

### Issue 4: R6b's parenthetical imagines an alternative definition the claim already excludes
**ASN-0086, R6b, *Justification***: "(Had the Definition quantified over `A_R^Σ` instead, deciding `a ∈ nullified(Σ)` would require first deciding `b ∉ nullified(Σ)`, recursing into a fixpoint ...; that reading is not adopted.)"

**Problem**: The Definition of `nullified` already fixes the quantifier over the audit slice `L_R^Σ`. The parenthetical contemplates a design (`A_R^Σ` quantification) that the definition excludes — the classifier explicitly flags paragraphs that "imagine a case the claim's precondition already excludes." The flat single-pass character of the test is fully established by pointing at the `L_R^Σ` quantifier; the counterfactual adds no proof obligation.

**Required**: Remove the counterfactual, or reduce to a one-clause note that membership ranges over `L_R^Σ`, hence is witness-status-independent.

## OUT_OF_SCOPE

### Topic 1: Concurrency / atomicity model for Emit vs. Observe
The Open Questions raise Emit/Observe atomicity and the consistency model for observing `A_K` transitions. These are genuinely new territory (a concurrency layer over the sequential `→`), correctly deferred — `SequentialAtomicTransitions` (ASN-0093) gives the substrate a serial model, and a concurrent refinement belongs in its own ASN.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
The restriction to standard triples is stated cleanly, and multi-arity active subsets are explicitly out of scope. This is a future ASN, not a gap here.

META: not applicable — the ASN defines state (`L_K`, `A_K`, `nullified`), operations (Emit/Observe/Nullify), and invariants (R0–R7a) abstractly enough that any implementation must satisfy them; it has not drifted into implementation mechanics.

VERDICT: REVISE
