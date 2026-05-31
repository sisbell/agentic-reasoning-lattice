# Review of ASN-0043

## REVISE

### Issue 1: L9's formal statement drops the conformance conjunct that its prose, its proof, and its sibling lemma L11b all carry
**ASN-0043, L9 — TypeGhostPermission (formal statement vs. prose)**: prose says "there exists for every arity `N ≥ 3` a **conforming** state `Σ'` extending `Σ`…", but the formal statement reads
`(A Σ : … : (A N ≥ 3 :: (E Σ' extending Σ, a ∈ dom(Σ'.L) :: |Σ'.L(a)| = N ∧ (E (t, len) ∈ Σ'.L(a).type :: t ∉ dom(Σ'.C) ∪ dom(Σ'.L)))))`
**Problem**: `Σ' extending Σ` is StateExtension (`Σ' ⊒ Σ`), which requires only monotonic growth + agreement on shared domains — it does *not* entail that `Σ'` satisfies the state-local invariants. As written, the existential is discharged by *any* extension that adds a link of arity `N` with a ghost-type span, including a non-conforming one. The entire point of L9 — that ghost types are *permitted in conforming states* — lives in the conjunct the formal statement omits. The proof establishes it ("By FSP, `Σ'` satisfies every state-local L- and S-invariant"), and the sibling existential L11b explicitly carries `∧ Σ' satisfies the state-local L- and S-invariants` inside its existential body. L9 should match.
**Required**: Add `∧ Σ' satisfies the state-local L- and S-invariants` to L9's existential body, matching L11b and the proof. This is a statement-completeness fix, not a proof gap.

### Issue 2: L7 worked-example "illustration" is essay content in a verification slot, restating the body
**ASN-0043, Worked Example, "*L7 (DirectionalFlexibility) — illustration.*"**: "The labels `F`, `G` in the standard triple are nominal — chosen above for prose convenience … under a counterpart or equivalence type, the same `(F, G, Θ)` carries no directional weight at all (per L7)."
**Problem**: L7 is a META property that imposes *no* constraint on any state, so there is nothing about `Σ` to verify and the trailing "✓" certifies nothing. The paragraph re-explains, in different words, the directional-flexibility point already made in the body's L7 ("What 'from' and 'to' mean depend on the specific case," with the same Nelson framing). This is the flagged "essay content in structural slots" / "two paragraphs say the same thing in different words" pattern — the precise reader must skip it to reach the next real check.
**Required**: Drop the L7 illustration from the worked example (it verifies nothing), or reduce it to a single pointer noting L7 is non-checkable against a static state.

### Issue 3: Coverage's lossy-projection note duplicates what Step 6 establishes, with a back-reference closing the loop
**ASN-0043, Definition — Coverage** ("Note that coverage is a lossy projection… `{(1, [3])}` and `{(1, [1]), (2, [2])}` cover the same addresses but are distinct endsets…") and **Worked Example, Step 6** ("This instantiates the lossy-projection case flagged in the Coverage definition").
**Problem**: The Coverage definition carries an abstract worked example of the lossy projection, and Step 6 carries the full concrete verification of the same phenomenon plus an explicit back-pointer. The definition's illustration and Step 6 establish the same fact twice, joined by a cross-reference — the forward-reference accretion the anti-bloat classifier names. The definition needs only the one-sentence "coverage is a lossy projection" claim; the parenthetical re-derivation of L5's role ("which collapses only reorderings of the same span collection, not distinct collections") is a defensive gloss on L5 inside a definition.
**Required**: Keep the bare lossy-projection sentence in the Coverage definition; remove its inline example and the L5 parenthetical, letting Step 6 carry the demonstration. Remove the back-reference or keep only one direction.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace constant (extending disjointness past the `s_C`-slice)
**Why out of scope**: L14/L1d scope content-side disjointness to the `s_C`-resident slice deliberately; promoting this to all of `dom(Σ.C)` requires a content-side invariant this ASN does not own. The first Open Question already records it. Correctly deferred.

VERDICT: REVISE
