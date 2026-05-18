# Channel Assignment — ASN-0086 review-43

**Date:** 2026-05-18 00:47

## Issue 1: wp Case 1 contains an extraneous conjunct
Reason: The fix is a logical analysis of what Nullify's stated postcondition entails. The reviewer has correctly identified that `NoCraftedSpanReachesFreshEmitter` concerns `A_R^{Σ'}` membership of the retractor, not the set-theoretic single-tuple-scope postcondition. Removing the conjunct or augmenting the postcondition is derivable from the existing Definitions of Nullify, nullified, and the wp computation rules.

## Issue 2: Notation `↝` in R7a is not formally defined
Reason: This is a notation hygiene fix. The note already defines `→` and `↦` with their frame conditions; R7a needs to either define `↝` as their union (or some larger relation) or restate its universal quantifier over the existing relational vocabulary. The substantive content of R7a is unchanged.

## Issue 3: The "Allocator-state commitment" should be axiomatized, not buried in a remark
Reason: This is a structural reorganization — the commitment's substance, its Nelson citation, and its udanax-green realization are already in the prose. Lifting it to a named Setup hypothesis and identifying its consumers (R0 Step 2 Case A) is internal restructuring of existing content with no new substantive claims requiring validation.

## Issue 4: Rationale subparagraphs justifying design choices that don't advance claims
Reason: Anti-bloat cleanup. The decision to consolidate or remove design-rationale subparagraphs is editorial; the signature already shows `d` as a parameter, and operation contracts don't require justification of their shape. No external channel input needed.

## Issue 5: Repeated restatements of discipline-conditionality
Reason: Structural cleanup — state the discipline once in Setup with its full effect, then reference it. The discipline's content, name, and consumption sites are all already established in the note. Reorganizing the cross-references is internal.

## Issue 6: Defensive prose anticipating misuse
Reason: Anti-bloat removal. The "Scope of Emit_K's contract" paragraph documents what Emit_K *isn't*, which is unnecessary given that the operation's signature and discipline-binding positively specify what it *is*. Editorial decision.

## Issue 7: "Operational scope of the `A_rel^Σ` filter" paragraph is verbose
Reason: Anti-bloat condensation. The two-sentence reduction the reviewer requests (filter scopes to relational addresses; crafted-span non-relational retractions are syntactically admissible but operationally inert) is fully derivable from the existing Definitions of Nullified and ActiveSubset. Higher-arity discussion belongs in its dedicated Open Question.

## Issue 8: R6c Consequence (e) regime-(ii) strengthening is mislabeled and redundant
Reason: Editorial cleanup. The regime distinction is already established at Emit_K's *A_K^{Σ'} membership* note; the Consequence (e) paragraph either restates that content (remove) or needs a clarifying rename. No external validation required.

## Issue 9: "Allocator-naming convention" is introduced inline but used inconsistently
Reason: Notation hygiene fix. `A_{d.0.s_L.1}`, `A_{a₁}`, and `A_{d.0.2.1}` are the same allocator under the worked-sketch instantiation (`s_L = 2`, `a₁ = d.0.2.1`); picking one form and noting the equivalence is a purely editorial decision derivable from the existing tumbler arithmetic.

## Issue 10: Two-paragraph "Why the construction is bound into the definition" overlaps "Scope of Emit_K's contract"
Reason: Anti-bloat merge. Both paragraphs argue that Emit_K is the disciplined subset of the substrate primitive. Merging or removing one is an editorial decision; the binding is already captured by Emit_K's signature with its address-construction postcondition.
