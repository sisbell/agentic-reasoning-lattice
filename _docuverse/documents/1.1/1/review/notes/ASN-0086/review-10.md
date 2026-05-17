# Review of ASN-0086

## REVISE

### Issue 1: R5 Setup-tag inconsistency
**ASN-0086, R5 statement and proof**: "R5 — TupleSelfTargeting. *[Setup-free.]*"

**Problem**: R5's Stage 1 paragraph explicitly invokes R0's verification machinery ("R0's construction discharges invariant-preservation for an emission carrying such a span as an endset component: R0 Step 4 verifies each L-invariant..."). R5 also depends on L14a preservation for the *fresh emitter address*, and L14a preservation requires the Setup hypothesis (via S3 forcing `ran(Σ.M) ⊆ s_C`-resident content) to exclude the new address from `ran(Σ.M)`. R5's Stage 2 dismisses L14a as "orthogonal to span targets within link endsets," but this only handles the *span content* side, not the preservation of L14a against the new emitter address. The latter inherits R0's Setup-requirement.

**Required**: Either (a) re-tag R5 as `[Setup-required]`, or (b) rewrite R5 as a pure structural admissibility claim — "the construction is permitted in the sense that L4(c) + L13 admit it and no L-invariant *forbids the span* as an endset member" — without invoking the existence of an emission carrying it. Option (b) would require dropping the "may appear in the from-set or to-set of an emitted tuple" wording in favor of "is admissible as an endset member."

### Issue 2: T10a.1 citation missing for equal-length siblings
**ASN-0086, R0a Case 1 (Case B branch)**: "by T10a.8 (UniformSiblingZeroCount, ASN-0034) all such siblings share `zeros = 3` and have equal length"

**Problem**: T10a.8 covers only zero count, not length. Equal length of siblings is established by T10a.1 (UniformSiblingLength, ASN-0034) — or, step-locally, by TA5(c)'s length preservation under `inc(·, 0)` applied repeatedly. The current citation attributes both facts to T10a.8.

**Required**: Cite T10a.1 alongside T10a.8 in this paragraph: "by T10a.1 (UniformSiblingLength) all such siblings have equal length, and by T10a.8 (UniformSiblingZeroCount) they all share `zeros = 3`."

### Issue 3: T_cat^Σ definition asymmetry with L_K^Σ
**ASN-0086, Definition — TypeCatalog**: "`T_cat^Σ = {Θ ∈ T_admissible : (E a ∈ dom(Σ.L) :: |Σ.L(a)| = 3 ∧ Σ.L(a).e₃ = Θ)}`"

**Problem**: T_cat^Σ uses *literal* endset equality (`Σ.L(a).e₃ = Θ`) at the type slot, while L_K^Σ uses *coverage-equivalence* (`coverage(Σ.L(a).e₃) = coverage(K)`). Two coverage-equivalent but literally-distinct endsets would both appear as separate elements of T_cat^Σ yet be collapsed into a single L_[K]^Σ slice. This asymmetry is unaddressed and quietly contradicts the note's own Rationale paragraph for coverage-equivalence (which aligns L_K with L8). The RetractionType paragraph then uses T_cat^Σ membership ("no representative of `[R]` lies in `T_cat^Σ`") in a way that conflates the two semantics.

**Required**: Either (a) redefine T_cat^Σ in terms of coverage classes (`T_cat^Σ = {[Θ] ∈ T_admissible/~ : L_[Θ]^Σ ≠ ∅}`) for consistency with L_K^Σ, or (b) explicitly acknowledge the asymmetry and rephrase RetractionType to use the coverage-class form ("no member of L_R^Σ exists" rather than "no representative of [R] lies in T_cat^Σ").

### Issue 4: Sub-document caveat introduces undefined concept
**ASN-0086, Nullify Crafted-span retractions paragraph**: "intersected with `A_rel^Σ` is *every link sited under `d`* (and any of `d`'s sub-documents' links, if such sub-documents exist)."

**Problem**: The parenthetical introduces "sub-documents" — a concept not defined in ASN-0034, ASN-0036, or ASN-0043, and not in scope for this ASN. ASN-0036's documents are flat (no nesting hierarchy specified). The phrase forward-references a feature that may exist in some future ASN but does not exist in the current substrate model.

**Required**: Remove the parenthetical, or rephrase as "intersected with `A_rel^Σ` is *every link sited under `d`*" — dropping the sub-document reference entirely.

### Issue 5: R6a needs explicit `a ∈ A_rel^{Σ'}` step
**ASN-0086, R6a proof**: "Suppose `a ∈ nullified(Σ)`. By Definition, there exist `b ∈ dom(Σ.L)` and `(b, F', G') ∈ L_R^Σ` with `a ∈ coverage(G')`."

**Problem**: The Definition of `nullified(Σ')` requires `a ∈ A_rel^{Σ'} = dom(Σ'.L)`. The proof exhibits the witness `(b, F', G')` and `a ∈ coverage(G')` (state-independent) but never explicitly discharges `a ∈ A_rel^{Σ'}`. This follows from L12a (`dom(Σ.L) ⊆ dom(Σ'.L)`) combined with `a ∈ A_rel^Σ = dom(Σ.L)` from the precondition, but the step is missing from the proof.

**Required**: Add an explicit line: "`a ∈ A_rel^{Σ'}` by L12a applied to `a ∈ A_rel^Σ` from the precondition."

### Issue 6: Worked sketch does not link to R5
**ASN-0086, Worked Sketch Step 1**: The retraction tuple `(b₁, ∅, {(a₁, δ(1, #a₁))}, R)` has a to-set containing the *link* address `a₁` — a direct instance of R5's permission for link-to-link reference. The sketch never connects this to R5.

**Problem**: R5 is a permission claim with no explicit concrete witness within the note. The Worked Sketch's Step 1 *is* the witness, but the connection is implicit. The review rubric flags "No concrete example" as REVISE-worthy; here the example exists but the link is missing.

**Required**: Add a one-sentence forward reference from R5 to the worked sketch: "The Worked Sketch below (Step 1) instantiates R5: the retraction tuple's to-set references the link address `a₁`." Or, equivalently, add a backward reference at Step 1: "Step 1's to-set `{(a₁, δ(1, #a₁))}` instantiates R5 — a link-to-link reference."

### Issue 7: R0a Case 1 partition wording
**ASN-0086, R0a Case 1**: The proof case-splits on `d' = d` vs `d' ≠ d`, but within Case 1 further splits on whether `a` was constructed via Case A or Case B of R0 Step 2. The partition structure is on the existing address `a'`, while the A/B split is on the *new* address `a`.

**Problem**: The reader has to disentangle two superimposed case partitions. The current text reads as if Case A/B are sub-cases of Case 1, but they're actually properties of the new emission that constrain how `a` relates to all `a'` with `home(a') = d`. The vacuous-quantifier discharge in Case A's branch is correct but obscured by the conflation.

**Required**: Restructure Case 1 to make the partition explicit: "Case 1 — `d' = d`. By the discipline, the new address `a` was constructed via R0 Step 2 Case A or Case B. If Case A: no other link `a' ∈ dom(Σ.L)` has `home(a') = d` (Case A's hypothesis), so the universal over `a'` with `d' = d` is vacuous. If Case B: ..." This makes clear that A/B is a property of the new emission, and the conclusion in each branch is about how `a` relates to all existing `a'` with home `d`.

## OUT_OF_SCOPE

### Topic 1: Sub-document substrate extensions
**Why out of scope**: ASN-0036's documents are flat. Sub-documents would require an extension to the document model (perhaps via document-level prefixes that contain other document-level prefixes), which is a separate substrate change.

### Topic 2: Multi-arity active subsets
**Why out of scope**: The note's `A_K^Σ` is defined only for standard-triple links. Higher-arity links (`|Σ.L(a)| > 3`) are admitted by L3 but excluded from `L^Σ` and `A_K^Σ`. Extending the active-subset machinery to `A_K^{(n),Σ}` is listed in Open Questions.

### Topic 3: Type catalog coordination across layers
**Why out of scope**: The note observes that retraction conventions `[R]` and classification types are deployment-time choices. Coordination across independently-developed layers is a deployment/governance question, not a substrate property.

### Topic 4: Substrate-level enforcement of the sibling-frontier discipline
**Why out of scope**: The note explicitly defers this to future work in the Remark following R0a and in the Open Questions. Elevating R0a from discipline-conditional to substrate-level would require tightening either the substrate emission primitive or the Emit_K specification — a deliberate extension.

### Topic 5: Operational ordering of Observe results
**Why out of scope**: Listed in Open Questions; the substrate currently provides set semantics, and any ordering guarantee would be an additional substrate commitment.

### Topic 6: Atomicity and consistency model for concurrent Emit/Observe
**Why out of scope**: Listed in Open Questions; this is a concurrency-control concern at a level above the abstract substrate model.

VERDICT: REVISE
