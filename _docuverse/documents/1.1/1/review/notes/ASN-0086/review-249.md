# Review of ASN-0086

I worked through the lemmas (R0, R0a, R-Scope), both wp derivations, and the five-step worked sketch against the concrete tumbler values. The mathematics is sound: R0a's cross-home zero-counting argument, the self-emit branch of R-Scope, and the wp Case 1/Case 2 equivalences all check out, and the worked sketch's addresses and `nullified` sets are computed correctly. I avoided the previously-declined findings. Two issues remain, both minor (notation consistency and anti-bloat).

## REVISE

### Issue 1: Inconsistent symbol ⊀ used where the prefix-negation ⋠ is meant
**ASN-0086, R-Scope proof**: "The only new key is `b`: `a ⊀ b` by R0a at Σ' applied to `dom(Σ'.L) = dom(Σ.L) ∪ {b}`, which is an antichain (so distinct members `a, b` are prefix-incomparable...)"
**ASN-0086, Worked Sketch Step 1**: "By T10a.2 ... `a₁` and `b₁` are ... prefix-incomparable; in particular `a₁ ⊀ b₁`."

**Problem**: In this corpus `<` is the T1 lexicographic order, `≺` is *proper prefix* (Prefix, ASN-0034), and `⋠` is the negation of `≼` (used consistently in the foundations, e.g. T10's `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`, and in this note's own Step 3: "`a₁ ⋠ a₂ via R0a; b₁ ⋠ a₂ via R0a`"). The intended claim at both `⊀` sites is "not a prefix," i.e. `⋠`. Reading `⊀` as `¬(<)` makes the Step 1 statement outright false: `a₁ = 1.0.1.0.1.0.2.1 < b₁ = 1.0.1.0.1.0.2.2` under T1, so `a₁ ⊀ b₁` is false under that reading. The author clearly means prefix-incomparability (it is glossed as such in both sentences), but the symbol is the wrong one and conflicts with the note's own `⋠` usage elsewhere — exactly where the prefix-vs-order distinction is load-bearing.

**Required**: Replace `⊀` with `⋠` at both sites (R-Scope proof and Worked Sketch Step 1) to match the corpus and this note's own Step 3 usage.

### Issue 2: `addr` codomain note states its surjectivity condition three times
**ASN-0086, Definition — TupleAddress**: "it is *onto exactly when the store holds no higher-arity link* (when `dom(Σ.L)` contains no `a` with `|Σ.L(a)| > 3`, the image equals the whole codomain), and not necessarily onto otherwise."

**Problem**: This is anti-bloat (the note carries the `review-mode.anti-bloat` classifier). One fact — `addr` is surjective iff no higher-arity link exists — is asserted three ways: the lead clause ("onto exactly when the store holds no higher-arity link"), the parenthetical restatement ("when dom(Σ.L) contains no a with |Σ.L(a)|>3, the image equals the whole codomain"), and the trailing "and not necessarily onto otherwise" (which merely re-expresses the "exactly when"). The preceding clause already gives the image as `{a ∈ dom(Σ.L) : |Σ.L(a)| = 3}`, from which surjectivity-iff-no-higher-arity is immediate.

**Required**: Collapse to a single statement, e.g. "with image `{a ∈ dom(Σ.L) : |Σ.L(a)| = 3}`, onto iff `Σ.L` holds no higher-arity link." Drop the parenthetical and the trailing clause.

## OUT_OF_SCOPE

### Topic 1: Higher-arity links cannot retract
`nullified(Σ)` quantifies over the triple-restricted `L_R^Σ`, so a link with `|Σ.L(a)| > 3` whose slot-3 coverage equals `coverage(R)` does not nullify its to-targets.
**Why out of scope**: The note states this deliberately ("only standard-triple links can retract") and Open Question 2 already routes multi-arity typed relations to future work. Not an error in this ASN.

VERDICT: REVISE
