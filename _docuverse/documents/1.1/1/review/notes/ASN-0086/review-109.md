# Review of ASN-0086

## REVISE

### Issue 1: WP Case 1 computes the weakest precondition over a domain the operation cannot inhabit
**ASN-0086, Weakest-Precondition Analysis, Case 1**: "`wp(Nullify(...), single-tuple scope at Σ') ≡ P0 ∧ P1 ∧ P2c` ... Dropping P2c admits a non-conforming pre-state with `a, a'' ∈ dom(Σ.L)`, `a ≼ a''` ... present in the full state space."

**Problem**: The Definition of Nullify states "Nullify is published by a substrate-conforming layer, so both its pre-state Σ and post-state Σ' are substrate-conforming states." If Σ is *always* conforming when Nullify executes, then P2c (Σ substrate-conforming) is a standing invariant, not a dischargeable precondition — it is identically true over the operation's actual domain. The necessity argument for P2c then draws its counterexample from states (`a ≼ a''`, non-conforming) that the operation can never be invoked from. Either the wp is computed over the operation's true (conforming) domain — in which case P2c is vacuous and the weakest precondition for single-tuple scope is `P0 ∧ P1` — or the analysis must justify how Nullify is reachable from a non-conforming pre-state despite the layer discipline. As written the two passages contradict each other on the domain of quantification.

**Required**: Fix the domain. State explicitly whether wp is taken over the full state space or the conforming sub-domain, and reconcile with the "both pre- and post-state are substrate-conforming" claim. If conforming, drop P2c from the wp; if full state space, explain the admissibility of non-conforming inputs.

### Issue 2: The same `inc`-gap illustration is restated three times
**ASN-0086**: appears in *Definition — substrate-conforming state* (contiguous-block parenthetical), in the ConformingHomedContiguity step ("rules out a step depositing, say, `inc^{J+1}` and `inc^{J+3}` while omitting `inc^{J+2}`"), and again in R7a's second worked example ("Were the composite to deposit `inc¹` and `inc³` while skipping `inc²`...").

**Problem**: This is the flagged pattern "two paragraphs in the same document say the same thing in different words." The no-skipped-index intuition is carried once by clause (b)'s contiguous-block form; restating it at each consumer is accretion the precise reader must skip past.

**Required**: State the no-gap content once (at clause (b)) and let the sub-lemma and worked example cite it without re-illustrating.

### Issue 3: Meta-prose enumerating downstream consumers and labeling structural slots
**ASN-0086, ConformingHomedContiguity sub-lemma**: "(Because the argument rests on clause (b) alone ... the sub-lemma holds at every substrate-conforming Σ ... **consumers below cite it by name**.)"
Also **R0a-Cor1**: the "*Substantive postcondition.*" label and "Beyond the index re-translation ... R0a-Cor1 carries one derived consequence"; and the *Properties Introduced* `→` row: "defined once under 'State transition relation'."

**Problem**: "consumers below cite it by name" is the flagged pattern of a result enumerating its downstream consumers rather than advancing its own content. "Substantive postcondition" and "defined once under..." are defensive/bookkeeping labels in structural slots — they tell the reader how to read the document, not what is true.

**Required**: Delete the consumer enumeration; state the sub-lemma's scope (holds at every substrate-conforming Σ) without naming who cites it. Drop the "Substantive postcondition" framing and "defined once" note — let the postcondition and definition stand on their own.

### Issue 4: R6b is asserted in prose without a formal statement
**ASN-0086, R6b**: "Retraction-of-retraction is not a fixpoint operation ... *Justification.* ..."

**Problem**: R6a and R6c carry quantified `(A ...)` statements; R6b carries only an English sentence and a *Justification*. Its operative content — deciding `a ∈ nullified(Σ)` quantifies over `L_R^Σ` (audit), not `A_R^Σ` (active), and the nullifying effect survives `→` because the witness persists by R3 — is a checkable claim. Leaving it as prose makes it the one R-property without a contract, weakening the audit/active distinction it is meant to anchor.

**Required**: Give R6b a formal statement, e.g. `(A Σ → Σ', a, b : a ∈ nullified(Σ) witnessed by tuple at b : a ∈ nullified(Σ') even if b ∈ nullified(Σ'))`, then attach the existing Justification as its proof.

### Issue 5: R7a discharge (4)(iii) "prior iteration" is ambiguous between same-home and global predecessor
**ASN-0086, R7a, discharge (4)(iii), "Subsequent occurrences"**: "At each subsequent occurrence of `d_k` ... the prior iteration has just emitted the immediately preceding chain element of `A_L(d)`."

**Problem**: With cross-home interleaving permitted, "the prior iteration" is not the globally-previous replay step but the most recent step *homed at `d_k`*. The argument is sound only because (4)(ii) immateriality lets interleaved other-home emissions be ignored, but the phrasing reads as if the immediately preceding global step emitted the preceding chain element, which need not hold.

**Required**: Rephrase to "the most recent prior iteration homed at `d_k`," explicitly leaning on (4)(ii) so the `ℓ_prev` identification is unambiguous.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs. Observe, and cardinality bounds on `nullified(Σ)`
**Why out of scope**: These are correctly deferred to the Open Questions list. The consistency model under which `A_K` transitions are observed, and any structural ratio bounding retraction, are new territory requiring their own state/operation commitments — not gaps in this note's stated scope (single-threaded, sequential `→`).

### Topic 2: Higher-arity links as `L_K^{(n)}` relations
**Why out of scope**: The note restricts to standard-triple links and flags the higher-arity generalization as an open question. The arity-3 restriction is consistently applied (`L_K`, `A_K`, Nullify scope), so this is a future extension, not an error here.

VERDICT: REVISE
