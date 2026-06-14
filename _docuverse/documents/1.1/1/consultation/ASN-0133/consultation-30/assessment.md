# Channel Assignment — ASN-0133 review-30

**Date:** 2026-06-14 05:45

## Issue 1: The H-RF/H-W separation is stated in full five times
Reason: Pure deduplication of a logical fact the note already states in full. Consolidating the separation under H-RF, reducing H-W to its definition plus the PC6a-no-fixpoint point (already present), and dropping Q6's re-derivation are all structural edits derivable from the ASN's own content — no design intent or implementation evidence at stake.

## Issue 2: Q0's rebuild conclusion is restated throughout the proof, then re-instantiated by the worked subsection
Reason: Editorial trimming of repeated meta-conclusions within Q0's proof, retaining the existing three-way classification, the single rebuild conclusion, and the worked Σ* check — all already in the note. The PL-membership argument and its PC3/PC4/UV citations are intact; only the abstract refrains shrink, so the fix is internal.

## Issue 3: Hypothesis sections carry "why the axiom is shaped this way" prose and repeat the scope-punt
Reason: Trimming axiom-motivation prose down to one clause and removing in-section scope-punts that the *What this note doesn't cover* section already owns. H-FAIR's three discharge modes are already stated and the scheduler punt already has its dedicated bullet — purely a structural edit.

## Issue 4: Q6 reintroduces H-SFAIR as a route parallel to regime (i)
Reason: Consistency fix between two sections of the same note: the H-SFAIR section already establishes it is "the strong-scheduling form of regime (i), not a disjoint second route," so aligning Q6's invocation with that conclusion (carry the turn-fairness caveat or drop the "or regime (i)" framing) is derivable from the ASN alone.

## Issue 5: Body prose defers to another ASN's open questions
Reason: The standing fact the note needs — a pdef-trigger referencing a de-registered definition still evaluates because PR3 keys on ever-registration — is already stated and cited in the *Triggers* section. Cutting the meta-narration about ASN-0130's Open Question 3 while keeping the PR3 fact is an editorial removal, requiring neither design intent nor implementation evidence.
