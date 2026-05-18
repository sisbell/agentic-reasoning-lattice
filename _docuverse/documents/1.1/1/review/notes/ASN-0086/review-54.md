# Review of ASN-0086

## REVISE

### Issue 1: R7a proof — class-(i) admissibility argument is incomplete

**ASN-0086, R7a proof**: "the existence of this class-(i) step is admissible because d_k ∈ dom(Σ'.M) (by L1a applied to a_k at Σ' in the original ↝-step), and Σ' satisfies S7d (DocumentAllocationDiscipline, ASN-0036), so d_k ∈ dom(Σ'.M) entails T4-valid(d_k) ∧ zeros(d_k) = 2, discharging class-(i)'s allocation preconditions for d_k"

**Problem**: S7d says d_k is "the result of an allocation event under T10a". T10a-conformance requires the spawning chain (parent allocator's base address) to be in the appropriate allocator's domain at the spawning state. The proof extracts only T4-valid + zeros = 2 from S7d, but it then claims these "discharge class-(i)'s allocation preconditions" — which implicitly include T10a-conformance. If d_k's account/node ancestor is in dom(Σ'.M) but not dom(Σ_{prev}.M), the class-(i) step at Σ_{prev} cannot fire. The replay vocabulary (class (i) = document allocation only) does not include account/node allocation, so prerequisite cascading is not addressed.

**Required**: Either (a) state explicitly that class-(i)'s Frame conditions are exactly freshness + (T4-valid ∧ zeros = 2), with T10a-conformance treated as an opaque substrate guarantee delegated to ASN-0036; or (b) extend the replay vocabulary to include account/node allocation prerequisites and argue them inductively.

### Issue 2: R0a-Cor2 discussion is essay content

**ASN-0086, paragraph following R0a-Cor2 proof**: "R0a-Cor2 narrows L1b's `#E ≥ 2` admission to `#E = 2`. This narrowing *aligns with* Nelson's design intent for the link primitive: link addresses occupy a flat depth-2 element field — subspace identifier followed by per-document serial — and deeper relational structure is composed through link-to-link references (see R5's Consequences (a)–(c)), not allocated through recursive sub-link addresses. udanax-green's `findisatoinsertmolecule` realizes this discipline mechanically: the `LINKATOM` type identifier occupies one mantissa slot..."

**Problem**: Multi-sentence paragraph relating the formal result to design intent, citing implementation details (`findisatoinsertmolecule`, `LINKATOM`, `rightshift = 0`), and forward-referencing R5's Consequences. The technical content of R0a-Cor2 is `#E = 2`; nothing in this paragraph extends that claim or any other lemma. The "aligns with" / "matches" / "narrows" framing is the pattern named in the review prompt — defensive meta-prose around a formal result.

**Required**: Trim to one sentence noting the narrowing, or remove entirely. Design-intent motivation belongs in a design note, not in an ASN proof.

### Issue 3: Emit_K Definition's A_K membership paragraph duplicates WP Case 2

**ASN-0086, Emit_K Definition** (paragraph "A_K^{Σ'} membership of the fresh emission — conditional on retraction discipline"): discusses two regimes (Nullify-only discipline vs. crafted-span retractions) and the consequence for whether a fresh emission lands in `A_K`.

**ASN-0086, Weakest-Precondition Analysis, Case 2**: re-discusses the same two regimes and same membership question with the same "NoCraftedSpanReachesD" conclusion.

**Problem**: Two paragraphs in distinct sections covering identical content — regimes (i) and (ii), unit-depth vs. crafted-span, what falls in `L_K \ A_K`. This is the "two paragraphs saying the same thing" pattern.

**Required**: Pick one location. Either move the regime discussion into the WP Analysis (where it has its natural home as a precondition derivation), or keep it in the Emit_K Definition and reduce the WP Case 2 to a one-line reference.

### Issue 4: "Dependency chain" pattern repetition

**ASN-0086, R5 Consequences (a), (b), (c)**: each Consequence has a paragraph of the form "*Dependency chain — existence of the post-state with the [X] tuple:* R5 admits [Y]; R0 at a caller-supplied home then emits the [X] triple, witnessing a state with [X] recorded."

**ASN-0086, Nullify Definition**: a similar "Dependency chain — existence of the post-state Σ' with the retraction tuple" paragraph.

**Problem**: Four occurrences of the same pattern. After the first, the reader knows the recipe; the subsequent instances add no new structural information.

**Required**: Establish the recipe once (e.g., as a "Dependency chain for self-targeting emissions" remark following R5), then reference it from each Consequence and from Nullify rather than re-instantiating.

### Issue 5: Implementation Notes use-site inventory duplicates per-claim citations

**ASN-0086, Implementation Notes, boundary marker**: lists "*Substrate-guaranteed claims* — R0, R1, R2, R3, R4, R5, R6a, R6b, R6c, R6c-Corollary, R7a, ..." and "*Discipline-conditional claims* — R0a, R0a-Cor1, R0a-Cor2, `Emit_K`'s function-ness on `Σ_D`, and Nullify's single-tuple scope".

**Problem**: This is a use-site inventory of which claims need which hypotheses. The note then says "every such claim cites the relevant hypothesis explicitly in its statement or proof." Both descriptions exist; the inventory is redundant if the per-claim citations are reliable.

**Required**: Remove the inventory and rely on per-claim citations. If callers find the inventory useful, demote it to a brief "see [hypothesis name] at first citation" remark.

### Issue 6: R6c-Corollary parenthetical is defensive prose

**ASN-0086, R6c-Corollary proof**: "(ASN-0043's L12 and L12a remain in force across the step but are not what supplies the preservation — they forbid modification or removal of existing `Σ.L` entries but permit extension, so on their own they do not pin `Σ.L` fixed.)"

**Problem**: A parenthetical explaining what is NOT being used. The proof's positive argument cites the arrangement-modification frame; the parenthetical adds nothing to that argument but pre-empts an imagined objection that "shouldn't L12 + L12a be enough?". This is the "imagining a case the claim's carrier excludes" pattern.

**Required**: Delete the parenthetical. If a reader thinks L12 + L12a should suffice, the affirmative citation of the arrangement-modification frame will redirect them.

### Issue 7: Emit_K Definition has accumulated structural slots

**ASN-0086, Definition — Emit_K**: contains *Postcondition (address-construction discipline)*, *defining precondition*, *Function-ness on Σ_D*, *address-returning convention*, and *A_K^{Σ'} membership of the fresh emission — conditional on retraction discipline* — five labelled sub-sections inside one Definition.

**Problem**: A Definition that requires five distinct labelled sub-parts has accumulated content from multiple analyses. The function-ness clause is a lemma; the A_K-membership clause is a wp analysis; the address-returning convention is a notational convenience. These are not properly content of the Definition itself.

**Required**: Reduce the Definition to signature + precondition + frame. Move function-ness to a labelled lemma below the Definition. Move A_K-membership analysis to the WP section (consolidated per Issue 3). Inline the address-returning convention as a one-sentence remark.

### Issue 8: R0 Step 2 case-exhaustiveness not stated

**ASN-0086, R0 proof, Step 2**: "We case-split on whether `d` already has any link allocations under `Σ`. Both cases produce a concrete `a ∈ LS(d) \ dom(Σ.L)`..."

**Problem**: The split is binary on the predicate `{a' ∈ dom(Σ.L) : home(a') = d} = ∅`, so exhaustiveness is immediate, but it is not stated. Readers tracking proof structure must check that no third sub-case exists.

**Required**: Add one sentence after the split — "These two cases are exhaustive on Σ: either d has prior link allocations or it does not."

### Issue 9: Sparse forward references to ASN-0047

**ASN-0086 throughout**: never cites ASN-0047, even though ASN-0047 (a foundation per the review setup) defines state-transition operations K.α, K.δ, K.μ⁺, K.λ, K.μ⁺_L over the same state vector (Σ.C, Σ.M, Σ.L) and defines S3★, CL-OWN, and other invariants that ASN-0086's frame conditions appear to interact with.

**Problem**: ASN-0086's classes (i)/(ii)/(iii) map roughly to K.δ/K.α/K.λ. ASN-0086 uses S3 (ASN-0036) at R0 Step 4 where ASN-0047 would supply S3★. If ASN-0086 builds on ASN-0036+ASN-0043 only (the simpler model without link-subspace V-positions), this should be stated. If ASN-0086 is intended to interoperate with ASN-0047's extended state, citations are missing.

**Required**: State once near Setup which substrate baseline ASN-0086 builds on. If ASN-0036+ASN-0043 (no link-subspace V-positions), say so. If ASN-0047, cite S3★ and CL-OWN where currently S3 is cited.

## OUT_OF_SCOPE

### Topic 1: Higher-arity link relations

**Why out of scope**: ASN-0086 explicitly restricts to standard-triple links and acknowledges the open question for `L_K^{(n)}` with `n > 3`. Belongs to a future ASN.

### Topic 2: Tightening R0a to be unconditional

**Why out of scope**: Listed in Open Questions. Requires either substrate-level tightening of the emission primitive or substrate-level commitment to the sibling-frontier discipline — both are separate design questions.

### Topic 3: Account/node allocation primitives

**Why out of scope**: ASN-0086's primitive vocabulary is (document allocation, content emission, link emission). Account and node allocations are inherited from ASN-0036/ASN-0047. Expanding ASN-0086's vocabulary to cover them would expand its scope.

### Topic 4: Slice-wise reformulation without globally-`s_C`-resident content

**Why out of scope**: Listed in Open Questions. Lifting the Setup hypothesis would require slice-wise restatements of R0, R4, R5 and is a separate technical exercise.

### Topic 5: Concurrency semantics for Emit vs. Observe

**Why out of scope**: Listed in Open Questions. Concurrent observation is a system-level concern not present in the substrate transition vocabulary as defined.

VERDICT: REVISE
