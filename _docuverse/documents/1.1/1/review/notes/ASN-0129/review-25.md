# Review of ASN-0129

## REVISE

### Issue 1: WT's plain-composition rule is not stated as a judgment of the system WT defines

**ASN-0129, WT (WellTyping)**: "PC2 yields `C₂` from `f : C₁` and the state-indexed `g : C₁ × S → C₂`, and its binder guard yields `C₂` from `f : C ∪ {⊥}`, `Γ, y : C ⊢ g : C₂`, and `Γ ⊢ c_default : C₂`"

**Problem**: WT defines exactly two judgment forms — `Γ ⊢ e : C` with `C ∈ Codom`, and `Γ ⊢ D dom(s)` — and was added precisely "so that decidability is a claim about a defined relation." The plain-PC2 rule's second premise, "the state-indexed `g : C₁ × S → C₂`", is neither judgment: `C₁ × S → C₂` is an arrow type, `Codom` contains no arrow types, and Γ assigns only codomain sorts and `Tup`. Every other binding former is transcribed in context-extension form — PC1's `Γ, x : s ⊢ P : Bool`, the binder guard's `Γ, y : C ⊢ g : C₂`, the filter rule, PC2a's fold premise `Γ, x : s ⊢ f : ℘_fin(T)` — but plain PC2 alone is left as a raw signature. Two consequences: (a) the typing relation is undefined at this rule, so the section's headline ("the typing judgment defined and decided") is not discharged for one of the four composition primitives; (b) the decidability argument ("every premise concerns a strictly smaller phrase") has no phrase to recurse into for `g` — a signature is not a sub-phrase. Note also that the context paragraph enumerates only two sources of codomain-sorted variables (address parameters at `T`, the binder guard's narrowed binder); a corrected contextual PC2 rule introduces a third, which that paragraph must admit.

**Required**: Either (a) state plain PC2 in context-extension form — from `Γ ⊢ f : C₁` and `Γ, x : C₁ ⊢ g : C₂` conclude `Γ ⊢ g[f/x] : C₂` — and extend the context paragraph's enumeration of binder sources accordingly; or (b) observe that every concrete plain-composition instance in the note (`elems(chain(t))`, `¬is_retired(h)`, etc.) is already typed by the atom/primitive application rule ("by its stated signature at matching argument sorts") together with the binder guard, restrict PC2's WT transcription to that case, and say so. Whichever way, the rule's premises must be judgments the system can derive.

### Issue 2: The self-emit grammar fact and its design conclusion are stated in full at two sites

**ASN-0129, QD-audit**: "The self-emit disjunct gets no spelling, deliberately: the vocabulary supplies no term spelling the test `a = a_emit(Σ, d)` — a grammar fact, read off V; the fact's grounds, and its conjectured strengthening to extensional inexpressibility, are C-emit's (The ceiling). The design conclusion needs only the grammar fact: the gate states the residence clause; the self-emit check belongs to the emitting surface, which performs it (S3)."
**ASN-0129, C-emit**: "The baseline is a grammar fact, read off V: the vocabulary supplies no term *spelling* the test … What stands without the conjecture is QD-audit's design conclusion, which needs only the grammar fact: the gate states P-tgt's residence clause, and the self-emit check belongs to the emitting surface, which performs it (S3)."

**Problem**: This is the anti-bloat pattern named in the review brief twice over — two paragraphs in different sections saying the same thing in different words, and a paragraph that defers to a downstream location ("are C-emit's (The ceiling)") while simultaneously restating the content it defers. The grammar fact ("no term spelling `a = a_emit(Σ, d)`") and the design conclusion (gate states residence; surface performs self-emit) each appear verbatim-near at both sites. A reader following QD-audit is told the grounds live at C-emit, then handed the conclusion anyway; a reader at C-emit gets the same conclusion re-derived with a back-pointer to QD-audit. Neither statement is wrong; the duplication is the defect, and it is exactly the accretion mode the `review-mode.anti-bloat` classifier asks to be caught at source.

**Required**: One site owns both the grammar fact and the design conclusion — C-emit is the natural owner, since it carries the grounds (FrontierUnification, the homed-set, the chain arithmetic) and the conjectured strengthening. QD-audit's treatment of the self-emit disjunct reduces to one pointer sentence ("the self-emit disjunct gets no spelling; see C-emit"), keeping its own substantive content (the residence-clause expressibility via reflected `L_dom`) intact.

## OUT_OF_SCOPE

### Topic 1: Evaluation cost model for PL terms
PC4/PC5 establish purity and termination but no complexity bounds — how a term's evaluation cost scales with `|dom(Σ.L)|`, slice sizes, and nesting depth of folds. Protocols evaluating triggers on every step will need this (a quantifier over a filtered slice nested under a fold is quadratic-plus in store size).
**Why out of scope**: Cost is a new analytical layer over a correctly specified semantics; nothing in this note's guarantees is wrong without it. It belongs in a future note, plausibly alongside Open Question 5's mechanical dynamics checker, since both serve the same protocol-validation consumer.

### Topic 2: Certified stability for non-Boolean codomains
PD0–PD2 classify Boolean terms; set-valued monotonicity appears only internally (the grow-only domain class), and ℕ-valued and `T ∪ {⊥}`-valued terms get no classification beyond the explicit exclusion of T1-extrema. A protocol watching a value evolve (a monotonically growing result set handed to a consumer, a count used as a progress measure rather than compared against a literal) would want a certified monotone-term calculus at value codomains.
**Why out of scope**: The Boolean classification is complete for the trigger/termination consumer this note names; value-codomain dynamics is genuinely new territory, not a gap in the stated theory.

VERDICT: REVISE
