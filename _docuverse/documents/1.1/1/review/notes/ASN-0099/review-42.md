# Review of ASN-0099

## REVISE

### Issue 1: F5 lacks explicit derivation

**ASN-0099, "Identity, Not Value" section**: F5 states `matches(a, I, Σ)` "consults dom(Σ.L), Σ.L, and coverage(·), never Σ.C(·)" and that distinct `α ≠ β` queries are computed independently.

**Problem**: The claim is asserted but no derivation is shown. The properties follow by inspection of F1's RHS, but the standards require depth — claims without proofs are flagged. F5 is the only substantive claim in the ASN that ships with no derivation chain.

**Required**: A one-line derivation referencing F1's RHS (e.g., "By inspection of F1, the existential consults `|Σ.L(a)|` and `coverage(Σ.L(a).eᵢ)` — neither of which reads `Σ.C`. For distinct α ≠ β, the two membership tests `α ∈ coverage(·)` and `β ∈ coverage(·)` consult disjoint set-membership predicates with no shared content lookup.")

### Issue 2: F4 forward-references findlinks_filtered

**ASN-0099, "The Match Predicate" section, F4**: F4's layer-(b) argument cites `findlinks_filtered` and the equation `findlinks(I, Σ) = ⋃_{i=1}^{N} findlinks_filtered({(i, I)}, Σ)` — both introduced in the "Endset Filtering" section that follows.

**Problem**: F4 makes load-bearing use of a symbol not yet defined. A reader encountering F4 cannot verify the OR-relaxation claim without looking ahead. The union equation labeled "(the union form is derived below)" makes the dependency explicit but does not resolve it.

**Required**: Either reorder so that "Endset Filtering" precedes F4, or inline a brief definition stub in F4 ("where `findlinks_filtered({(i, I)}, Σ)` is the per-slot filtered form defined below"). The current ordering forces a forward read.

### Issue 3: F4 layered structure obscures the operational point

**ASN-0099, "The Match Predicate" section, F4**: F4 introduces three Layers (1, 2, 3) and then two factored choices (a, b), giving five sub-structures the reader must hold in mind.

**Problem**: The realizability discharge (three strengthenings + two weakenings) is rigorous, but the layered taxonomy adds conceptual overhead that obscures the actual claim: any predicate differing from F1 on a realizable witness yields a different operation under F2 ∧ F3. Layer 3 (spans-monotonicity) is largely subsumed by layer (a)'s overlap-vs-aggregate distinction; restating it as a separate layer creates apparent redundancy.

**Required**: Either consolidate Layers 2 and 3 (the spans-monotonicity consequence is internal to the per-endset existential), or label the layered taxonomy explicitly as commentary distinct from the load-bearing realizability proofs. The five witnesses do the actual work and could lead.

### Issue 4: F10a Case (ii) bookkeeping is compressed

**ASN-0099, F10a Case (ii) (proper prefix on documents)**: Step 4 concludes "no additional zeros at positions #d₁+1..#d₂" from "two zeros already accounted for at positions ≤ #d₁ − 1".

**Problem**: The step depends on `d₂[#d₁] ≠ 0` (so that position #d₁ doesn't contribute a third zero), which holds because `d₂[#d₁] = d₁[#d₁] ≠ 0` by Prefix and T4. The proof doesn't make this intermediate step explicit, leaving a reader to verify the zero-count balance includes position #d₁ as non-zero.

**Required**: One sentence in step 3 or 4 noting `d₂[#d₁] = d₁[#d₁] ≠ 0` so the zero-count argument at step 4 ranges cleanly over positions ≥ #d₁ + 1.

### Issue 5: Conformance pair variants stated only as conjunctions

**ASN-0099, "Completeness" section**: F2 and F3 are stated as separate containments. F2-filt ∧ F3-filt, F2-sco ∧ F3-sco, F2-V ∧ F3-V are stated only as equations, bundled as conjunctions.

**Problem**: The asymmetry is mild but consistent statement matters — F3 might be the deferred-index obligation in a filtered/scoped implementation, and bundling obscures which half is at stake when an implementation violates one direction.

**Required**: Either state the variants individually (matching F2/F3's treatment) or note explicitly that "F2-X ∧ F3-X" means the conjunction of the two individual containments analogous to F2 and F3.

## OUT_OF_SCOPE

None. The ASN's "What We Have Not Specified" and "Open Questions" sections explicitly enumerate the deferred items (partition tolerance, caching, access control composition, inverse operation, query semantics for off-domain addresses, timing bounds), making boundary clear.

VERDICT: REVISE
