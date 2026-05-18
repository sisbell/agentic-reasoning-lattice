# Review of ASN-0086

## REVISE

### Issue 1: Sparse-allocator hypothesis duplicated with apologetic cross-reference
**ASN-0086, Setup ("Substrate emission primitive (for Emit_K)" + "Implementation hypotheses"):** The substrate-emission paragraph defines L1c-as-witness-only behavior, then ends with "(This sparse-allocator condition is named *Sparse-allocator hypothesis* in the *Implementation hypotheses* subsection below; named for cross-reference in claim provenance only — its substantive content is the property just stated.)" The Implementation hypotheses subsection then re-states the same property under that name.
**Problem:** Two paragraphs say the same thing, with a parenthetical apologizing for the duplication. Exactly the "two paragraphs in the same document say the same thing in different words" pattern.
**Required:** Consolidate to one location. Either define-and-name in the substrate-emission paragraph (drop the Implementation hypotheses entry) or define-and-name only in Implementation hypotheses (drop the parenthetical cross-reference apology in the substrate-emission paragraph).

### Issue 2: Repeated "definitional, not derived" axiom-status meta-commentary
**ASN-0086, multiple locations:**
- Frame conditions: "these are part of what each class *is* at the `(Σ.C, Σ.M, Σ.L)` level of abstraction, not consequences derivable from the underlying ASNs' invariants"
- Class (iii) Frame: "value-preservation at existing keys is part of the Frame definition, not a derived consequence"
- Definition of relational layer: "The commitment is definitional, not derived"
- Convention RetractionDirectionality has an entire "Principled basis" subsection

**Problem:** The "new prose around an axiom explains why the axiom is needed rather than what it says" pattern. The reader does not need to be told repeatedly that axioms are stipulated; the axioms' content carries that signal. The Principled basis paragraph in particular spends two paragraphs justifying a layer-level naming choice (to-set carries targets) that L7 already permits without justification.
**Required:** Delete the "definitional, not derived" framings throughout. State each axiom or commitment once, in its own slot, and let the structural-slot convention carry the "this is stipulated" signal. For RetractionDirectionality, replace the Principled basis with a single sentence noting L7 permits the choice.

### Issue 3: R0a's proof-structure justification paragraph
**ASN-0086, R0a proof opening:** "Direct induction on antichain fails because the same-home step needs T10a.2, whose hypothesis requires both addresses in the *same* sibling stream — strictly stronger than antichain. Stage 1 dispatches cross-home unconditionally; Stage 2 strengthens the induction invariant to the sibling-stream form under the discipline; Stage 3 composes."
**Problem:** This paragraph justifies *why* the proof has its three-stage structure rather than presenting the structure. The staged proof is self-explanatory once the staging is visible from the headings. The "direct induction fails because..." line is reviser-drift residue — content explaining a path not taken.
**Required:** Delete the opening paragraph. Start directly with "Stage 1 — Cross-home sub-argument (no cross-home prefix-comparability)."

### Issue 4: R5's Stage 2 inflates a one-line check into a two-stage proof
**ASN-0086, R5 justification:** "(Stage 2 — no invariant opposes the construct.) No L-invariant of ASN-0043 constrains endset target content beyond L4(c)'s explicit permission to reference link-subspace addresses. The construct is therefore admissible by L4(c) + L13 + R0's invariant-preservation argument at Step 4."
**Problem:** Stage 2 is a single substantive sentence: "L4(c) is the only L-invariant on endset target content, and it explicitly permits." The two-stage framing implies a separate body of derivation in Stage 2 that does not exist. The "no invariant opposes" rhetoric is defensive meta — anticipating a hypothetical challenge rather than advancing the claim.
**Required:** Collapse Stage 1 and Stage 2 into a single justification paragraph: "By L13, the unit-depth span `(a, δ(1, #a))` is well-formed; by L4(c), endset spans may reference link-subspace addresses; R0 Step 4's invariant-preservation argument admits emissions carrying such spans without restriction on endset target content."

### Issue 5: R0a's formal statement followed by quantifier-range restatement
**ASN-0086, R0a:** Formal statement, then "The discipline-restricted quantifier range — `Σ` is `→_D*`-reachable from a Σ_0 with empty link store — is the substantive scope of the claim; the substrate primitive in isolation admits class-(iii) emissions falsifying the antichain."
**Problem:** The first half restates the formal statement's quantifier range in prose. The second half is a useful contrast (discipline vs. substrate primitive). The first half is redundant with the formal statement itself.
**Required:** Drop the first clause. The contrast is sufficient: "The substrate primitive in isolation admits class-(iii) emissions falsifying the antichain — R0a's claim is conditional on the sibling-frontier discipline restricting the reachable trajectory."

### Issue 6: "Operational scope of the A_rel^Σ filter" imagines excluded cases
**ASN-0086, Definition of nullified:** "*Operational scope of the `A_rel^Σ` filter.* The `a ∈ A_rel^Σ` filter scopes `nullified(Σ)` to relational addresses, while `coverage(G')` ranges over `T` and may also contain content addresses, ghosts, or higher-arity link addresses. Retractions whose `coverage(G')` lies entirely outside `A_rel^Σ ∩ {a : |Σ.L(a)| = 3}` are well-formed `Emit_R` calls but operationally inert for `A_K`..."
**Problem:** This paragraph imagines retractions whose coverage falls entirely outside the carrier `nullified(Σ)` is defined on — exactly the "paragraph imagines a case the claim's carrier or precondition already excludes" pattern. The filter in the Definition already excludes these cases; reasoning about their operational inertness is meta about the Definition's choice, not substantive.
**Required:** Delete the paragraph. The filter `a ∈ A_rel^Σ` in the Definition is self-explanatory and needs no apologetic justification for what it excludes.

### Issue 7: wp Case 3 framing as "trivial-by-design" motivation for R6b
**ASN-0086, Weakest-Precondition Analysis, Case 3:** "Case 3 is described as 'trivial-by-design' and motivates R6b... The trivial wp form is the operational signature of R6b's quantifier-range choice."
**Problem:** The wp computation is genuinely one-line (a₁ ∈ nullified(Σ)). The framing as "trivial-by-design", "operational signature", and "motivates R6b" is several paragraphs of meta-commentary on what the triviality means. R6b stands on its own; the wp Case 3 simply illustrates an aspect of R6b's design — it does not need to be framed as motivation.
**Required:** Trim Case 3 to its wp computation and the substantive R3+R2 derivation. Drop the "trivial-by-design", "operational signature", and "motivates" framing.

### Issue 8: R0 Step 4's L-invariant enumeration conflates permissions and invariants
**ASN-0086, R0 proof Step 4:** The enumeration "L4(c), L7, L9, L10 are permissions licensing the emission's content, not state-bound values" appears mid-list, after L-invariants have been discharged.
**Problem:** Permissions are not invariants requiring preservation; they license the construct. Treating them in the same enumeration as L-invariants requiring preservation conflates two distinct categories of L-clause.
**Required:** Separate the L-invariants requiring preservation (L0–L3, L11a, L12, L12a, L12b, L14, L14a, L-fin) from the L-permissions (L4(c), L7, L9, L10) into two clearly-distinguished groupings. Permissions are not part of the invariant-preservation verification.

### Issue 9: Multiple parenthetical proof-fragments inside the relational-layer Corollary
**ASN-0086, Definition — relational layer, Corollary:** "Each relational-layer state-affecting operation is itself a single-step class-(iii) `→`-step (by definition — the layer admits no composites that bundle document allocation with link emission, so R7a's multi-step branch with class-(i) prefix never fires here; the layer issues `Emit_K` only when its `d ∈ dom(Σ.M)` precondition is already established, and the replay sequence collapses to length 1)..."
**Problem:** Two distinct claims are packed into one parenthetical: (a) the layer admits no document-allocation composites, (b) the layer issues Emit_K only when d ∈ dom(Σ.M) is established. These are part of the Corollary's proof and should be inlined as proof steps, not buried in a parenthetical aside.
**Required:** Pull the parenthetical out as an explicit two-step proof of the Corollary. The flow is then: layer commitment → R7a applied → multi-step branch's class-(i) prefix vacuous → single-step Emit_K conclusion.

## OUT_OF_SCOPE

### Topic 1: Self-loop emission (a tuple whose own endsets reference its own address)
**Why out of scope:** R5 covers references from a new tuple to *existing* tuples (a ∈ A_rel^Σ). A self-loop — the emitted tuple's endsets containing its own fresh address — requires the caller to pre-compute the fresh address (deterministic under the discipline, via R0a-Cor1) and pass it to Emit_K, which the current operation signature does not directly support. This is a future operational extension, not a gap in the current ASN's substrate-level claims.

### Topic 2: Cardinality bound on nullified(Σ) relative to dom(Σ.L)
**Why out of scope:** Already surfaced in Open Questions. The substrate places no a priori bound on retraction count; whether higher-layer policy should impose one is a layer-design question, not a substrate question.

META: The ASN remains squarely at the substrate-model level — it specifies typed-relation state, operations on that state, and invariants of state, with implementation hypotheses (sibling-frontier discipline, unit-depth retraction discipline) clearly labeled as such. Not drifted.

VERDICT: REVISE
