# Review of ASN-0086

## REVISE

### Issue 1: Introduction undercounts R-properties

**ASN-0086, opening paragraph after the abstract**: "Six structural properties on the typed-relation substrate, of which five (R0–R5) are derivable from ASN-0043 and one (R6, the active subset) is the substrate's own contribution"

**Problem**: R0–R5 inclusive is six labels (R0, R1, R2, R3, R4, R5), so the numerical claim "five" is internally inconsistent with the range notation. The right-hand sum ("five" + "one") nominally yields six, which the leading "Six structural properties" accepts — but identifying which six requires reading R0–R5 as five items, against the body's labeling. R0a — introduced as a separate labeled lemma in the body (FlatLinkDomain, Setup-free, discipline-conditional) and present in the Properties Introduced table — is omitted entirely from the intro count. By contrast, the same paragraph's "seventh lemma (R7)" tally is correctly stated under main-label LEMMA counting (R0, R1, R2, R3, R4, R6, R7 = 7 LEMMAs, with R5 as META).

**Required**: Reconcile the headline count with the body's labels. Either (a) restate as "seven structural properties (R0–R6), of which six (R0–R5) are derivable from ASN-0043 and one (R6) is the substrate's own contribution," with a brief parenthetical noting R0a as a discipline-conditional supplementary lemma; or (b) restructure the range to make the arithmetic correct (e.g., position R0 separately as a foundational existence lemma and group R1–R5 as the five ASN-0043-derivable structural properties). The Setup-dependence summary later in the same paragraph ("three — R0, R4, R5 — make essential use of the Setup hypothesis") references the body's labels correctly, so the inconsistency is localized to the headline sentence.

### Issue 2: Substrate emission primitive's allocator-state semantics left implicit

**ASN-0086, "The Two Foundational Sets" section, "Substrate emission primitive (for Emit_K)" paragraph**: "The L1c chain is required to *exist as a conformance witness* on Σ; it is not required to be operationally re-traversed by the emission, and intermediate addresses along the chain are not required to be in dom(Σ.L) or dom(Σ.C)."

**Problem**: T10a's child-spawn admissibility (T2 in AllocatedSet, ASN-0034) requires `spawnPt(A) ∈ dom_s(parent(A))` at the state s of the spawn step. For R0 Step 2's Case A, step (iii)'s spawn `(d.0.s_L, 1)` requires `d.0.s_L ∈ dom_Σ(A_d)` at the substrate-primitive's invocation state. When A_d's enumeration at Σ doesn't yet reach d.0.s_L (e.g., the document has prior content allocated under d.0.1.1 only, with A_d realized only to index 0), the chain isn't admissible at Σ under a literal reading of T2.

The note's "witness chain" semantics states what is *not* required (intermediate addresses don't need to be in `dom(Σ.L)` or `dom(Σ.C)`), but doesn't state what *is* required at the allocator-state level — specifically, whether the substrate primitive's atomic class-(iii) step implicitly extends `Act(Σ)` and `n_Σ` for every allocator along the witness chain that is not already activated/realized at Σ, or whether T10a's T2 admissibility is being structurally reinterpreted as logical reachability rather than realized state. The Nelson and udanax-green citations are precedential evidence — they show the sparse-allocator reading is held by concrete substrates — but they are not derivations of how the abstract substrate primitive lifts to a valid T10a transition sequence.

**Required**: Make the commitment explicit at the substrate-model interface. Either (a) state that the substrate primitive's atomic class-(iii) step implicitly extends `Act(s)` and `n_s` for every allocator along the witness chain that is not already activated/realized at Σ, with no visible effect on `dom(Σ.C)` or `dom(Σ.M)` (the sparse-allocator interpretation, consistent with the class-(iii) Frame); or (b) state that the substrate model structurally reinterprets T10a's T2 admissibility — that "T10a-conforming chain" means a sequence whose steps are pairwise consistent under T10a's axioms, independent of any state-machine `dom_s` realization at Σ. Either commitment closes the gap; without one, downstream consumers must reconstruct the implicit lifting argument themselves at every place R0 is invoked.

VERDICT: REVISE
