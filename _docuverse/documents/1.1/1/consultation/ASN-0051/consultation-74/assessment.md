# Channel Assignment — ASN-0051 review-74

**Date:** 2026-05-17 22:11

## Issue 1: SV11 attainment biconditional — proof of (⇒) surjectivity argument has a gap
Reason: Pure proof correction — the inequality direction from surjectivity is reversed. The fix is mechanical: surjectivity of Φ : non-empty terms → fragments gives |non-empty terms| ≥ |fragments|, not the reverse, and the chain |fragments| ≤ |non-empty terms| ≤ m·p with equality at m·p forces both bounds tight. All needed material is in the ASN's own proof structure.

## Issue 2: SV6 four-case lemma — case (IV) verification missing exhaustiveness check
Reason: Pure exhaustiveness gap in the case-routing of an already-stated structural lemma. The four cases (I)–(IV) are defined by length-matching and prefix-matching on y vs. β_{k₁}-elements; the routing of "#y < #e and not a prefix" into case (IV) follows from the case definitions and needs only one explicit sentence. No external input required.

## Issue 3: SV13(h) BilateralVitality predicate is over-specified
Reason: Formal redundancy of `F ≠ ∅` given `π(F, d) ≠ ∅` is a derivable consequence of the ASN's own π and coverage definitions (coverage(∅) = ∅ vacuously, so π(F, d) ≠ ∅ ⇒ F ≠ ∅). The choice between intentional emphasis and simplification is editorial; the ASN already records the design intent ("Nelson's reading literally — both ends are required to be non-empty, and each must project") so no design-intent consultation is needed.

## Issue 4: SV5 composite-endpoint reading needs clearer separation of two different "intermediate states"
Reason: Pure exposition reorganization — the three states (SV5-internal intermediate, post-K.μ~ M_reord, post-Stage-2 M') are all defined within the ASN, just introduced inline rather than up-front. The fix is to relocate the state-naming convention before Step 1 or add a state-mapping table. No external evidence required.

## Issue 5: Coverage paragraph's "in any order" lift commutativity is asserted without verification
Reason: Commutativity of (α) and (β) is derivable from the lift recipes already fully specified in the ASN — (α) modifies (m, sibling count, span set) extending each block's I-extent by 2 at the tail, while (β) adds a fresh nested block with I-extent identical to β_p. The verification that the new block's I-extent grows uniformly under (α) regardless of whether (β) was applied first is mechanical from the recipe statements. Alternatively, weakening to a fixed order is purely editorial.
