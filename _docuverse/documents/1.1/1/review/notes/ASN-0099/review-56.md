# Review of ASN-0099

I read the full ASN and checked the comprehension definitions, the F4 design-justification witnesses, the A1/A1a frame argument, and the F9-family / F10a / F11 / F19 derivations against the foundation contracts. The operation is sound and the proofs are unusually complete. Two issues remain — one a missing foundation citation on a load-bearing cross-definition equality, one a precision overstatement.

## REVISE

### Issue 1: `discoverable_from = matches(ran(M(d)))` equality asserted without citing the bridge lemma
**ASN-0099, "The Match Predicate" and "Persistent Discoverability (I-Side)"**: "F1 generalizes ASN-0098's `discoverable_from(a, d, Σ) = matches(a, ran(Σ.M(d)), Σ)`" and again "The two notions coincide instantaneously — `discoverable_from(a, d, Σ) = matches(a, ran(Σ.M(d)), Σ)`".

**Problem**: This is an equality between two *differently-defined* predicates. ASN-0098 defines `discoverable_from(a,d,Σ) ≡ (E i : project(a,i,d,Σ) ≠ ∅)` — a **project-based** predicate. This ASN's `matches(a, ran(M(d)), Σ) = (E i : coverage(eᵢ) ∩ ran(M(d)) ≠ ∅)` is a **coverage-based** predicate. They are equal only because LP12 (DiscoverabilityCharacterisation, ASN-0098) supplies the per-slot biconditional `project(a,i,d,Σ) ≠ ∅ ⟺ coverage(eᵢ) ∩ ran(M(d)) ≠ ∅`. The equality is stated twice as if definitional, with no citation. Per the depth standard, a derived equality must name its premise. The whole F11/ASN-0098 "I-side vs V-side" distinction rests on this coincidence being correct, so the bridge should be explicit.

**Required**: Cite LP12 (ASN-0098) at both assertion sites, or add one line: "by LP12 the project-form and coverage-form per-slot predicates coincide, so `discoverable_from(a,d,Σ) = matches(a, ran(Σ.M(d)), Σ)`."

### Issue 2: "only treatment that leaves the operation total" is an unproven uniqueness claim
**ASN-0099, "Phase 1 (V→I)"**: "silent projection is the only treatment that leaves the operation total over `R ⊆ T` for a fixed allocated document."

**Problem**: This is false as a uniqueness claim. Mapping absent V-positions to a fixed sentinel address (or to an arbitrary default I-address) also yields a total operation — it is merely semantically wrong, not non-total. The genuine argument is that silent projection is the unique total treatment that *introduces no spurious I-addresses* (every output is an actual arrangement image). The current phrasing overstates "total" as the discriminating property when the real discriminator is faithfulness of the image.

**Required**: Restate the justification in terms of the actual discriminating property — e.g., "silent projection is the only treatment that is total over `R ⊆ T` *without fabricating I-addresses absent from the arrangement*" — or downgrade to a design preference rather than a uniqueness claim.

## OUT_OF_SCOPE

None. The ASN correctly defers INSERT/DELETE/COPY mechanics, version creation, and FOLLOWLINK/inverse-direction resolution to its "What We Have Not Specified" section and Open Questions rather than specifying them.

VERDICT: REVISE
