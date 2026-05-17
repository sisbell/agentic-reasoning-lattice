# Review of ASN-0086

## REVISE

### Issue 1: Worked Sketch's ghost addresses violate T4
**ASN-0086, Worked Sketch / Concrete instantiation**: "`k = 3.0.0.0.1` — a ghost address for the classification type K" and "`r = 4.0.0.0.1` — a ghost address for the retraction coverage class [R]"

**Problem**: Both tumblers have the structure `[X, 0, 0, 0, 1]` with three adjacent zeros (positions 2-3 and 3-4), violating T4's no-adjacent-zeros conjunct `(A i : 1 ≤ i < #t : ¬(tᵢ = 0 ∧ tᵢ₊₁ = 0))` at i=2 and i=3. While L9 (TypeGhostPermission) admits non-stored tumblers as type-endset targets, the choice is jarring and uses three zeros (matching T4's zero-count bound) while violating the structural constraints that accompany that count.

**Required**: Either (a) use T4-valid ghost addresses (e.g., `k = 3` and `r = 4` as single-component tumblers — coverage `{t : 3 ≼ t}` and `{t : 4 ≼ t}` remain disjoint and serve the example), or (b) add an inline note that type-endset ghost addresses need not satisfy T4 and that the chosen format is illustrative only.

### Issue 2: Arrangement-modification frame citation imprecise
**ASN-0086, R6c-Corollary, Step 4**: "by the arrangement-modification frame stated in the Scoping note above (inherited from ASN-0036), every arrangement-modifying transition leaves `Σ.L` identical — `Σ_arr.L = Σ.L`"

**Problem**: ASN-0036 defines `Σ = (Σ.C, Σ.M)` only; `Σ.L` is introduced in ASN-0043. The preservation `Σ_arr.L = Σ.L` for arrangement-modifying transitions follows from ASN-0043's L12/L12a applied to ASN-0036's transition class, not directly from ASN-0036.

**Required**: Citation should be "frame inherited from ASN-0036's class definitions, with the Σ.L identity following from L12/L12a applied to that transition class" or equivalent. The Scoping note in the main body has the same issue and should be corrected in parallel.

### Issue 3: Setup's "Maintenance protocol" paragraph length and placement
**ASN-0086, The Two Foundational Sets / Setup hypothesis**: The "Maintenance protocol" paragraph (~25 lines) sits between the Setup statement and the Subspace-distinctness hypothesis.

**Problem**: The paragraph's substantial discussion of ASN-0036's class-(ii) emission policy and udanax-green's V-stream routing buries the next hypothesis statement. It is reference material, not the core specification.

**Required**: Condense to 2-3 sentences in the main text and move the detailed policy / udanax-green / future-work discussion to a labeled appendix or footnote.

### Issue 4: R7 row in "Properties Introduced" table — typology
**ASN-0086, Properties Introduced table, R7 row**: Type field reads "LEMMA + DEF".

**Problem**: R7a and R7b appear above as separate rows with their own types (LEMMA, DEF). The composite R7 row's hybrid type tag is unique in the table and the "+" notation is unusual.

**Required**: Either omit R7's row (the composition is described in prose and the R7a / R7b rows carry the relevant typing) or use a single category like "COMPOSITE" with a Statement field that makes the composition explicit.

### Issue 5: "Allocator-state commitment" paragraph density
**ASN-0086, Substrate emission primitive (for `Emit_K`)**: The Allocator-state commitment paragraph asserts atomic class-(iii) discharge of T10a's child-spawn admissibility and forwards to Appendix A.1.

**Problem**: The paragraph is dense and the relationship between "sparse-allocator interpretation" (A.1) and the main-text claim is not signalled clearly enough — readers may miss that the sibling-sweep-without-deposits reading is a substantial design commitment, not just an implementation detail.

**Required**: Add one sentence flagging that this is a load-bearing commitment that R0 Step 2 Case A's sibling sweep relies on, with the design rationale in A.1.

## OUT_OF_SCOPE

### Topic 1: Concurrent emission semantics
The ASN does not formalize what happens if two parallel emissions target the same logical position. R0 / R6a / R3 give individual-transition properties; the concurrent case requires a separate consistency-model treatment.
**Why out of scope**: Concurrency is appropriately deferred — the Open Questions section flags it.

### Topic 2: Multi-arity active-subset machinery `A_K^{(n)}`
The ASN scopes `A_K^Σ` to arity-3 (standard-triple) links; higher-arity active subsets are mentioned but not developed.
**Why out of scope**: The asymmetry between syntactic admissibility (Emit_R permits any to-span) and operational effect (A_K scoped to arity-3) is handled at Nullify's P1 with the higher-arity case flagged in Open Questions.

VERDICT: REVISE
