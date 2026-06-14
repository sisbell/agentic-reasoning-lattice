# Review of ASN-0134

This is an unusually rigorous note. The conflict analysis (H0–H2, G1) is clean, the boundary cases are handled (H2's first-emission boundary, A5's m=0/m=1/m≥2, W5's self-emit vs cross-home-pre-target), the worked scenarios in §7–§8 ground the abstract claims, and the I1a literal-vs-operative distinction in §4 instance (i) is a genuinely sharp observation. Two issues nonetheless require revision — one substantive correctness error with an internal contradiction, one editorial.

## REVISE

### Issue 1: Surface-discipline does not exclude the target-residence race
**ASN-0134, §4 (summary paragraph)**: "the target-residence race is excluded a priori by W5's emit-before-retract **(a fortiori by surface-discipline)**, whereas the toggle family's incumbent-nullify instance (ii) survives both"
**ASN-0134, §4 (instance (ii))**: "this instance survives **the disciplines that tame the others**: B's retraction of T obeys emit-before-retract (W5)... and the derivation is surface-disciplined"

**Problem**: Surface-discipline (every `L_R`-growing step is a `Nullify_Binary`, ASN-0128 SD) is *orthogonal* to emit-before-retract (order each retraction after its target's emission, W5); it does not exclude the target-residence race. Take the race exactly as the note sets it up — A = `Emit_K` at home `d` landing at `a = a_emit(Σ, d)`, B = `Nullify_Binary(a)` at home `d' ≠ d`:

- *Order A;B* is surface-disciplined (A grows `L_K`; B grows `L_R` via `Nullify_Binary`) → `a` nullified.
- *Order B;A* is **also surface-disciplined, vacuously**: at B's pre-state `a ∉ dom(L)` and `a ≠ a_emit(Σ, d')`, so P-tgt fails and B is rejected (zero steps, *no* `L_R`-growing step); A then grows only `L_K`. With no `L_R`-growing step, "every `L_R`-growing step is a `Nullify_Binary`" holds vacuously → `a` left **active**.

Two surface-disciplined orders, divergent outcomes. Surface-discipline does not remove the dependence — only emit-before-retract does, by forbidding order B;A. This contradicts the note's own statements:

- W5 (§5, §8): "**only** the coordination layer's emit-before-retract discipline removes the dependence";
- §4 body: "**absent that hypothesis** [emit-before-retract] the race is real, and the substrate's response to the losing order is a clean rejection";
- the claims-table G1 entry, which correctly reads "the target-residence race of a `Nullify` against its own cross-home target **(excluded by emit-before-retract)**" — with no surface-discipline.

The deeper point the contrast is reaching for is correct and worth preserving: instance (ii) is order-unstable *even under every retraction discipline*, because its target is an already-emitted incumbent (so emit-before-retract is vacuously satisfied in both orders), whereas the target-residence race's target is not-yet-emitted (so emit-before-retract bites). The error is only the attribution of the *exclusion* to surface-discipline.

**Required**: Strike "(a fortiori by surface-discipline)" and remove surface-discipline from "the disciplines that tame the others." State that emit-before-retract *alone* excludes the target-residence race (consistent with W5), that instance (i) is tamed by clause 8 and instance (ii) by neither, and that surface-discipline excludes none of the three families — the losing order of the target-residence race is itself surface-disciplined, with the substrate supplying a clean P-tgt rejection rather than discipline supplying determinacy.

### Issue 2: Open Question cross-references point to the wrong questions
**ASN-0134, §2 and §6**: batch read-atomicity is deferred to "Open Question 3"; **§4, §5, §8**: the target-residence / out-of-order-retraction race is attributed to "Open Question 8."

**Problem**: The Open Questions list (9 paragraphs) has Q3 = *the weakest primitive for clause 8*, and Q5 = *batch atomicity* ("the minimal additional contract that makes a multi-step batch appear atomic to a reader, closing the interior-prefix gap A5 leaves open even for a W4-contiguous run") — so §2/§6 should cite Q5, not Q3. Likewise Q8 = *same-home conflicts proven independent (static partition, weakening clause 2)*, while Q9 = *out-of-order retraction whose target has not yet been emitted* — so §4/§5/§8 should cite Q9, not Q8. A reader following the references lands on unrelated questions.

**Required**: Renumber the in-text references (3→5 for batch atomicity, 8→9 for the retraction race) or reorder the Open Questions list to match.

## OUT_OF_SCOPE

None. The deferred topics (batch read-atomicity, cross-server composition of per-home orders, verdict durability, sub-allocator static partitioning) are correctly placed in the Open Questions rather than attempted here, and the entity/document-allocation layer is appropriately excluded with document-address freshness carried as a stated precondition.

VERDICT: REVISE
