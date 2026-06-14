# Review of ASN-0131

I worked through the definition, the worked instance, and every derived claim. The mathematics is sound: the soundness/completeness pair is an honest read of RE-DEF; the union law and its one-sided intersection counterexample are correct (the non-injective construction `{[1,1]↦a, [1,2]↦a}` is reachable and refutes `⊇`); RE-CWP's weakest precondition is a genuinely non-trivial, correctly derived wp with the `R = ∅` boundary collapsing to `RE = ∅`; the worked instance verifies RE-OVL/RE-CLIP/RE-WHOLE/RE-UNIT against concrete values; and the transition case analysis is exhaustive (K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L, link-only K.μ⁻, K.α, K.δ via LP8, K.ρ, other-doc edits, ASN-0082 insert/delete, K.λ emission, retraction). RE-ADDR and the R-Scope confinement in RE-RET are checked and hold under the stated standing discipline. Foundation citations are all to foundation ASNs; no non-foundation ASN-number reference appears in the body.

The findings are prose, not correctness — but the anti-bloat classifier this note carries makes them in-scope.

## REVISE

### Issue 1: The Σ.L-evolution bridge states its conclusion twice
**ASN-0131, "The unit of the answer: anchoring without names"** — the bridge paragraph asserts the same conclusion at two strengths in three sentences:

> "every ASN-0086 lemma that constrains Σ.L alone holds verbatim at every ASN-0047-reachable state."

then, after the one-sentence extension reason, restates it expanded:

> "So the bridge's standing conclusion is this: every ASN-0086 lemma whose conclusion constrains Σ.L or nullified holds at every ASN-0047-reachable state, including the lemmas whose hypotheses name dom(Σ.M) or the derived emitter a_emit(Σ, d)."

**Problem**: The first statement (the "Σ.L alone" base case) is strictly subsumed by the third (which covers `Σ.L`-or-`nullified` conclusions with `dom(Σ.M)`/`a_emit` hypotheses — the base case is just the no-extra-hypothesis instance). The paragraph is build-up → extension → combined-restatement, and the restatement duplicates the opening. This is the "two sentences say the same thing in different words" pattern the anti-bloat mandate flags; a reader must absorb the conclusion, then re-absorb its superset. The middle sentence's *justification* (shared ASN-0093 substrate, single `a_emit` formula) is sound and load-bearing — only the doubled conclusion is redundant.

**Required**: State the bridge conclusion once at full generality, with the `dom(Σ.M)`/`a_emit` extension reason inline, and drop the narrower opening restatement.

### Issue 2: "three stores" mislabels the state
**ASN-0131, opening paragraph**: "We have, by the time we reach this note, three stores in the system state Σ = (Σ.C, Σ.L, Σ.E, Σ.M, Σ.R)"

**Problem**: The five-tuple is then described as three things — content store `Σ.C`, *arrangement family* `Σ.M`, link store `Σ.L` — but `Σ.M` is explicitly an arrangement family, not a store, and `Σ.E`, `Σ.R` are state components left uncounted. "Three stores" juxtaposed with a five-component tuple, one of the three not being a store, is a small imprecision in an otherwise exact note. Minor/cosmetic, but precision is the standard here.

**Required**: Rephrase to the three *state components RE engages* (or "two stores and the arrangement family"), so the count matches what is described and does not appear to inventory the whole state.

## OUT_OF_SCOPE

### Topic 1: Gap-closing interior delete at content depth `m_{s_C} > 2`
The ASN scopes delete-stability to text depth `#p = 2` because ASN-0082 supplies `D-SHIFT` only there ("the foundation supplies no gap-closing interior-span delete at greater content depths"). This is correct scoping, not a skipped case: the depth-general interior delete does not exist in the foundation, and the RE-EDIT argument is depth-independent and would cover it the moment the foundation provided one. No revision required — the limitation is in the displacement primitive's existence, not in this note.

### Topic 2: Link-subspace region queries (`subspace(v) = s_L`)
The content-subspace restriction `W ⊆ s_C` is a stated caller obligation, and the link-subspace case (where the image lands in `dom(Σ.L)` and retraction stability acquires the emitter-`b` term) is already correctly deferred to Open Question 7. New territory, appropriately marked.

VERDICT: REVISE
