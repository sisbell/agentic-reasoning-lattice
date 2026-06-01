# Review of ASN-0086

## REVISE

### Issue 1: R0's formal statement quantifies over all states but the proof requires state-local-conformance

**ASN-0086, R0 (TupleAddressFreshness)**: "`(A Σ : dom(Σ.M) ≠ ∅ :: (A F, G ∈ Endset, K ∈ T_admissible :: (E Σ' reached by one →-step from Σ, a : a ∉ dom(Σ.L) :: ...)))`"

**Problem**: The quantifier domain is "any Σ with `dom(Σ.M) ≠ ∅`," with no conformance restriction. But the proof's freshness discharges consume state-local invariants throughout:
- *first-emission, freshness against `dom(Σ.C)`* uses L0 (content carries `E₁ = s_C`);
- *subsequent-emission, well-formedness of `a`* uses L1c to obtain `T4-valid(ℓ_prev)`, and L-fin for the max to exist.

The proof even says it "carries over to every state-local-conforming state in the operations' domain." At a `↝*`-reachable state that does *not* preserve L0/L1c/L-fin, `ℓ_prev` need not be T4-valid, the homed-set max need not exist, and even K.λ's own freshness precondition cannot be discharged — so the existential `(E Σ' reached by one →-step)` is not established. The statement is strictly stronger than what is proved. Note that `Emit_K`'s signature *does* correctly scope Σ to "the state-local-conforming sub-space," and Emit_K function-ness *does* say "this Lemma holds over the operations' domain" — R0, the lemma both rest on, is left unscoped, an internal inconsistency.

**Required**: Add the conformance hypothesis to R0's quantifier: `(A Σ : Σ state-local-conforming ∧ dom(Σ.M) ≠ ∅ :: ...)`. The same over-broad "for any state Σ" appears in R5's statement, whose proof invokes L1, L1a, L1b, L4(c), L13, and R0 — fix it there too.

### Issue 2: R7a discharge (4)(iii) "Subsequent occurrences" is a case the precondition excludes

**ASN-0086, R7a proof, discharge (4)(iii)**: "At each subsequent occurrence of `d_k` in the re-ordered enumeration, the most recent prior iteration homed at `d_k` emitted the immediately preceding chain element..."

**Problem**: R7a decomposes a *single* `Σ ↝ Σ'` step issued by a substrate-conforming layer. The Definition — substrate-conforming state fixes the at-most-one-key-per-home discipline: "a composite `↝`-step may touch several homes but contributes at most one fresh key to any single home." Therefore `Δ = dom(Σ'.L) \ dom(Σ.L)` contains at most one address per home, and no home `d_k` repeats in the Δ-enumeration. The "subsequent occurrences of `d_k`" subcase cannot arise under R7a's own precondition — it imagines a case the carrier excludes. This is exactly the reviser-drift pattern the anti-bloat classifier asks to surface.

**Required**: Remove the subsequent-occurrence subcase, or, if R7a is meant to be robust to multi-key-per-home steps, drop the at-most-one discipline from substrate-conformance and re-justify R0a-Cor1's single-key contiguity induction (which likewise assumes "adds at most one fresh key" per step) for the multi-key case.

### Issue 3: state-local-conforming definition states its witness twice

**ASN-0086, Definition — state-local-conforming state**: the antichain-violating witness `a'' = inc(a, 1)` is constructed in full mid-paragraph ("a higher layer may, for instance, emit `a'' = inc(a, 1)`..."), and then the closing sentence restates it: "...it admits antichain-violating states (e.g. the `a'' = inc(a, 1)` target case above) that separate it from substrate-conformance."

**Problem**: Two sentences in the same definition say the same thing in different words — the second adds nothing the witness construction did not already establish. Anti-bloat per the forward-reference classifier ("two paragraphs in the same document say the same thing in different words").

**Required**: Drop the closing restatement; the witness construction already shows the separation.

## OUT_OF_SCOPE

### Topic 1: Cross-layer invariants between `L_K` and arrangements `Σ.M`
The first Open Question (visibility-dependent relational predicates) is genuinely new territory. Under the adopted ASN-0093 substrate, M2 keeps every arrangement empty, so this cannot be addressed here without changing the foundation.

### Topic 2: Higher-arity typed relations (`|Σ.L(a)| > 3`)
The note restricts to standard triples and says so explicitly. The `L_K^{(n)}` generalization belongs in a future ASN.

### Topic 3: Concurrency/atomicity model for Emit vs. Observe
The Open Questions on Observe ordering and Emit/Observe atomicity are new operational territory, not gaps in this note's stated scope.

VERDICT: REVISE
