# Regional Review — ASN-0034/NAT-card (cycle 8)

*2026-04-24 02:39*

### "Contrapositive" mis-applied to a De Morgan rewriting
**Class**: REVISE
**Foundation**: —
**ASN**: NAT-order body: "The familiar disjointness form `m < n ⟹ m ≠ n` is the contrapositive of the mutual-exclusion conjunct `¬(m < n ∧ m = n)`"
**Issue**: The contrapositive of `P ⟹ Q` is `¬Q ⟹ ¬P`. What is going on here is a classical rewriting `¬(A ∧ B) ⟺ (A ⟹ ¬B)`, which is implication-from-conjunction by De Morgan, not contraposition. The contrapositive of `m < n ⟹ m ≠ n` would be `m = n ⟹ ¬(m < n)`, which is a *different* implicational form from the conjunct. A precise reader reading "contrapositive" and going to check the inference rule finds it is the wrong name. The axiom's soundness is unaffected, but the justifying vocabulary is imprecise.
**What needs resolving**: Either rename the operation ("the implicational form `m < n ⟹ m ≠ n` is `¬(m < n ∧ m = n)` rewritten by `¬(A ∧ B) ⟺ (A ⟹ ¬B)`"), or drop the gloss entirely — the mutual-exclusion conjunct and the implicational form are interderivable by classical logic and downstream consumers do not need the step named.

### NAT-order derivation carries a rhetorical-negation parenthetical defending the use of `=`
**Class**: REVISE
**Foundation**: —
**ASN**: NAT-order body: "`¬(m < n ∧ m = n)` follows by substituting `m = n` into `m < n` via indiscernibility of `=` — a logical property of equality available throughout, not a property of `<` — rewriting to `m < m` …".
**Issue**: The em-dashed parenthetical is defensive meta-prose about *where* indiscernibility lives (in logical equality, not in `<`). A precise reader performing the substitution does not need the substitution rule relocated onto the equality symbol versus the relation. The construction "a logical property of equality available throughout, not a property of `<`" is the "not X, Y" rhetorical shape — a negation of a non-claim ("`<` was never claimed to supply indiscernibility") bundled with the actual claim. It adds no inferential content to the derivation: the step is "rewrite `m < n` under `m = n`, conclude `m < m`, contradict irreflexivity," and any defensive framing of *which* logic supplies rewriting is outside the scope of the proof.
**What needs resolving**: Remove the parenthetical. The substitution step stands on its own; equality of terms is a background logical rule the specification does not need to re-license at the point of use.

### NAT-order Definition-slot prose carries drafting-register meta-commentary
**Class**: REVISE
**Foundation**: —
**ASN**: NAT-order body (paragraph on the Definition slot): "These are notational definitions, not additional axioms: every downstream occurrence of `m ≥ n`, `m > n` unfolds to `n ≤ m`, `n < m` and inherits the strict-total-order properties through that unfolding."
**Issue**: This is the reviser-drift pattern "new prose around an axiom explains why the axiom is needed rather than what it says" applied to the Definition slot. The sentence tells the reader how to classify Definition-slot entries (as notational, not axiomatic) and how downstream consumers are expected to unfold them — procedural instructions for future readers, not content of the definitions themselves. The definitions already state `≤`, `≥`, `>` as `⟺` equivalences; the reader does not need to be informed that these are therefore unfoldable. The "not additional axioms" framing is also the "not X, Y" construction applied to a distinction the slot structure already encodes.
**What needs resolving**: Delete the sentence. The three `⟺` definitions in the formal contract carry their own meaning; the slot name "Definition" already distinguishes them from axiomatic clauses.

### T0 body retains use-site attribution of `1` and `≤`
**Class**: REVISE
**Foundation**: —
**ASN**: T0 body: "The numeral `1` bounding the length from below is the `1 ∈ ℕ` posited by NAT-closure; the relation `≤` is the non-strict order on ℕ defined by NAT-order, so `{j ∈ ℕ : 1 ≤ j ≤ #a}` is nonempty."
**Issue**: This is the use-site inventory pattern prior findings flagged in NAT-closure's and NAT-card's bodies, now surviving in T0's body. The attribution "`1` is the `1 ∈ ℕ` posited by NAT-closure; `≤` is defined by NAT-order" is exactly the content of T0's Depends slot ("NAT-closure … supplies `1 ∈ ℕ` for the lower bound"; "NAT-order … supplies the non-strict relation `≤`"). Restating symbol-origin in the body is the inversion of body-vs-Depends that the instructions flag — the body should say what `T` *is*, and the Depends slot should attribute the imported symbols.
**What needs resolving**: Drop the use-site attribution from T0's body. One sentence stating "`(A a ∈ T :: 1 ≤ #a)` forces each tumbler to have at least one component, so the index domain is nonempty" is enough; the grounding of `1` and `≤` lives in Depends.

### NAT-card Depends NAT-closure bullet walks the `k = 0` case-split inside the Depends slot
**Class**: REVISE
**Foundation**: —
**ASN**: NAT-card Depends, NAT-closure bullet trailing text: "Also supplies `0 < 1`, which forces `{j ∈ ℕ : 1 ≤ j ≤ 0} = ∅` at `k = 0` — making the enumerating function's domain empty, `f` the empty function, and `S = ∅` the only admissible case with `|S| = 0` — and separates the empty case `n = 0` (`{j ∈ ℕ : 1 ≤ j ≤ 0} = ∅`, so the only admissible `S` is `∅`) from the nonempty case `n ≥ 1` (`1 ∈ {j ∈ ℕ : 1 ≤ j ≤ n}`, so enumerating functions with nonempty domain — `k ≥ 1` — become admissible)."
**Issue**: Two patterns compound here. First, the bullet walks the `k = 0` anatomy (empty domain → empty function → empty image → `S = ∅`) and then does a separate `n = 0` vs `n ≥ 1` case split — content duplicating the body's `k = 0` parenthetical and prior finding content that asked for the trivial-model rationale to be compressed. Second, the Depends slot's job is to name supplier and supplied symbol/property; walking two case splits inside a Depends bullet is the "paragraph looks like a prior finding's content relocated rather than removed" pattern. `0 < 1` was added to NAT-closure to exclude the trivial model; now the consequences of that addition are being catalogued inside the Depends bullet that imports it.
**What needs resolving**: Compress the bullet to the grounded-symbols reading — e.g. "Also supplies `0 < 1`, which forces `{j ∈ ℕ : 1 ≤ j ≤ 0} = ∅` and so renders the `k = 0` and `n = 0` cases of the axiom well-formed." The two case splits should not be re-performed in Depends; the axiom and the `k = 0` body parenthetical already carry them.

### NAT-card body retains drafting-register meta-commentary on the axiom's structure
**Class**: REVISE
**Foundation**: —
**ASN**: NAT-card body: "Existence-and-uniqueness of `k` — the definite article binds both — and the upper bound `|S| ≤ n` are clauses of the axiom, not consequences. Hence `|·|` is a well-defined total function on subsets of every initial segment `{j ∈ ℕ : 1 ≤ j ≤ n}` of ℕ with codomain ℕ solely by virtue of the postulate."
**Issue**: Three strands of meta-prose in two sentences: "the definite article binds both" explains the English-language device used in the Axiom clause; "are clauses of the axiom, not consequences" classifies the clauses' register; "solely by virtue of the postulate" emphasises the posit character. None of these advance the statement of what `|·|` is. The reader of the Axiom slot already sees "the unique `k ∈ ℕ`" and can read existence-and-uniqueness out of it; the classification comment is the "not X, Y" construction applied to the axiom-vs-consequence distinction the slot structure already encodes. Prior findings asked to compress NAT-card's meta-justification; these sentences are what remains of it.
**What needs resolving**: Reduce this prose to what the body actually says about `|·|` — that it is a cardinality operator on subsets of initial segments of ℕ, distinct from `#·`. The classification of clauses as axioms and the gloss on the definite article can go.

### Inconsistent "this ASN" annotation in intra-ASN Depends bullets
**Class**: OBSERVE
**Foundation**: —
**ASN**: T0 Depends: "NAT-closure (NatArithmeticClosureAndIdentity, this ASN) — supplies `1 ∈ ℕ` …"; the sibling NAT-order bullet in the same Depends slot carries no such marker, and NAT-zero / NAT-closure / NAT-card Depends bullets citing intra-ASN siblings similarly omit it.
**Issue**: All five statements live in ASN-0034, so every Depends bullet in the content points to an intra-ASN sibling. Marking one bullet with "this ASN" while leaving the others unmarked suggests a distinction that does not exist. A consistent annotation policy — either mark all intra-ASN siblings or mark none — keeps the reader from inferring a difference from the marker.
**What needs resolving**: — (OBSERVE)

VERDICT: REVISE

## Result

Regional review not converged after 8 cycles.

*Elapsed: 4774s*
