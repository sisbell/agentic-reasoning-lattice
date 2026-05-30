# Review of ASN-0084

## REVISE

### Issue 1: OrdShiftHom sub-clause mis-cited throughout (wrong premise)

**ASN-0084, "Consequences of R-PRE" / Extended Associativity / R-NS / R-COMM / R-BLK**: e.g. "OrdShiftHom (b) — `subspace(shift(v, n)) = subspace(v)` (ASN-0036)"; "By OrdShiftHom (b) of ASN-0036, subspace(shift(v_b, k)) = subspace(v_b) = S'".

**Problem**: In the foundation (ASN-0036), OrdShiftHom **(a)** is `subspace(shift(v, n)) = subspace(v)`; **(b)** is the *S8a-preservation* clause (`shift(v, n)` satisfies S8a). Subspace value is not pinned by S8a, so clause (b) cannot license `subspace(v+k) = subspace(v)`. Every subspace-preservation step in this ASN cites the wrong sub-clause. The error recurs in at least six places: Subspace confinement, the Extended Associativity consumer list, R-NS(NS-run), R-COMM (non-S case), and the R-BLK Scope note and Phase 2.

**Required**: Replace every subspace-preservation citation "OrdShiftHom (b)" with "OrdShiftHom (a)". (The genuine (b) usage — S8a preservation — appears nowhere here; confirm it is not silently needed.)

### Issue 2: The weakest-precondition open question is stated three times

**ASN-0084, R-SP, R-CS3 "Open question," and Open Questions**: R-SP says "a full necessity characterization is left as an open question"; R-CS3 closes with "A full weakest-precondition characterization of REARRANGE_K — including the precise role of R-PRE(iv) beyond what D-SEQ already supplies (D-SEQ makes every region a well-defined cardinality and keeps source references c_i + j within V_S(d) …) — is left as an open question"; the Open Questions section repeats this near-verbatim, including the "D-SEQ … keeps source references within V_S(d)" phrasing.

**Problem**: Two paragraphs (R-CS3's trailing "Open question" and the Open Questions item) say the same thing in nearly identical words — anti-bloat duplication. The R-CS3 "Open question" sub-paragraph is content relocated into the wrong slot; R-CS3's job is the CS3-necessity counterexample, not restating a global open question.

**Required**: Delete the trailing "Open question" sub-paragraph from R-CS3 (and the parenthetical hedge in R-SP); keep the single statement in the Open Questions section.

### Issue 3: Consumer-enumeration / forward-reference meta-prose

**ASN-0084, multiple sites**:
- REARRANGE_K paragraph: "This is the operation referent invoked by `wp(REARRANGE_K, Q)` in R-SP below."
- Reduction of compound shifts: "The combined identity … is what the well-definedness arguments of R-PIV and R-SWP consume…"
- Displacement Analysis: "The per-region uniformity recorded here is exactly the same-region commutation that R-COMM (below) establishes operationally and that Phase 3 of R-BLK consumes; the displacement magnitudes add no proof obligation beyond R-COMM…"
- Subspace confinement: "This is a derived consequence … **not a separate verification obligation**."

**Problem**: Each sentence enumerates downstream consumers or defends the prose's own status rather than advancing the claim. These are exactly the forward-reference accretion patterns the classifier targets; a reader following the math must skip past them.

**Required**: Strike the consumer-pointer and "not a separate obligation" clauses; let the identities stand on their own and let downstream lemmas cite upward.

### Issue 4: Repeated "B' is not needed for S8" deferral

**ASN-0084, "Canonical decomposition" paragraph, R-SP intro, R-SP S8 clause**: The point that the maximal decomposition's existence/uniqueness comes free from foundation S8 and that B' "documents how runs transform" / is "not needed for S8" is asserted in all three places ("We do not re-establish either fact…"; "are not needed for S8 (which the foundation supplies); they document how runs transform"; "Existence and uniqueness … hold by foundation S8 … To document the run-level effect, we additionally verify…").

**Problem**: Same disclaimer restated three times across sections — duplication, and partly defensive prose explaining what the ASN deliberately does *not* do.

**Required**: State once (in R-SP's S8 clause) that S8 follows from the foundation and that R-BLK is documentary; remove the duplicate disclaimers in the Canonical-decomposition paragraph and R-SP intro.

### Issue 5: R-NS(NS-inv) adds no reasoning beyond (NS-π)

**ASN-0084, R-NS(NS-inv)**: "Every ASN-0036 invariant evaluated at a V-position v with subspace(v) ≠ S … that depends only on dom(M restricted to non-S positions) … is preserved unchanged." Proof: two structural facts (dom unchanged; M' = M pointwise on non-S) "by (NS-π)," then "R-SP performs the per-clause invariant audit."

**Problem**: The clause states a generic tautology (functions agreeing pointwise on a fixed domain preserve any property of that domain) and immediately defers the real work to R-SP. It advances no reasoning the (NS-π) result and R-SP's audit do not already carry, and exists mainly to be cited.

**Required**: Either fold the one load-bearing fact into (NS-π) and drop (NS-inv), or give it a concrete obligation it discharges that R-SP does not.

## OUT_OF_SCOPE

### Topic 1: k > 4 cut rearrangements and composition of rearrangements
**Why out of scope**: Generalizing beyond n ∈ {3,4} and characterizing whether composed rearrangements remain single rearrangements are new territory; correctly deferred to Open Questions (no action beyond Issue 2's de-duplication).

### Topic 2: Operational recovery of the maximal partition from B' and merge-order confluence
**Why out of scope**: This ASN deliberately relies on foundation S8 for the maximal decomposition; the exhaustive-Merge process and its confluence belong to a future ASN.

VERDICT: REVISE
