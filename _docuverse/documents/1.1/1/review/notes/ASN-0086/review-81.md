# Review of ASN-0086

This note carries the `review-mode.anti-bloat` classifier, and the dominant problem is exactly that: large stretches of proof re-verify guarantees the foundation already supplies, and meta-prose (use-site inventories, alternative-definitions-not-adopted, design-intent essays, forward-reference chains) has accreted around the forward references. The relational construction itself (R5/R6 active-audit distinction) is sound and the worked tumbler arithmetic checks out. Findings below are about redundancy and meta-prose, not about a wrong claim.

## REVISE

### Issue 1: R0 re-verifies the entire L/S/M/C catalog that K.λ already guarantees by construction
**ASN-0086, R0 proof**: "ASN-0093's K.λ is engineered to preserve every substrate invariant by construction; we verify the ASN-0043 L-invariants by reading K.λ's contract..."
**Problem**: The proof then spends ~10 paragraphs discharging L0/L1/L1a/L1b/L1c/L3/L11a/L12/L12a/L12b/L-fin/L2/L5/L6/L8/L13/L14/L14a plus the S- and M-/C-catalogs. If K.λ preserves every substrate invariant "by construction" (a foundation guarantee), re-deriving each conjunct here is redundant. The only thing R0 adds over K.λ's general contract is the standard-triple value shape `(F,G,K)` with `N=3` — which is a single L3 check.
**Required**: Cite K.λ's preservation guarantee once; verify only what Emit_K's specialization adds beyond K.λ's value-precondition (arity-3, `e₃=K∈T_admissible`). Delete the per-invariant walk.

### Issue 2: R7a's "Per-step substrate-invariant discharge" block duplicates Issue 1 across two step types
**ASN-0086, R7a, Per-step substrate-invariant discharge (α)/(β)**: each block re-lists "S0, S1, S2, S3, S7a/S7b/S7d, S8-fin, S8a, S8-depth, D-CTG, D-MIN, D-SEQ ... M0, M1, C0, C1, C1b, C1c, C-fin ... L0, L1, ..." and the mechanism for each.
**Problem**: This is the same catalog-walk as R0, now repeated twice more (K.σ-prefix and K.λ-emission). The preservation facts are K.σ's and K.λ's own contracts; enumerating them per step is bloat, not proof. The load-bearing content of R7a is the chain-order replay (discharge (4)(i)–(iii)); that is buried under the catalog enumeration.
**Required**: Reduce (α)/(β) to "each replay step is a primitive K-op, which preserves the full catalog by its ASN-0093 contract." Keep only discharge (4) (the replay determinism argument), which is the actual content.

### Issue 3: The L14/L14a SC-NEQ argument is written out verbatim three times
**ASN-0086**: the identical "by S3 `ran(Σ.M) ⊆ dom(Σ.C)`, content has `E(·)₁=s_C`, `a` has `E(a)₁=s_L`, SC-NEQ excludes `a`" discharge appears in R0's L14/L14a paragraph, again in R5-Cor's proof, and again in R7a's (β) block.
**Problem**: Two (here three) paragraphs saying the same thing in different words. SD (StoreDisjointness, ASN-0093) already delivers L14 directly, as R0 itself notes ("SD ... also delivers this conclusion directly").
**Required**: State the SC-NEQ/L14/L14a discharge once as a named sub-lemma (or just cite SD), and reference it from the other two sites.

### Issue 4: R0a-Cor1's "Substantive postconditions" enumerate downstream consumers
**ASN-0086, R0a-Cor1, postcondition (a)**: "The maximum is consumed downstream by Emit_K's function-ness (subsequent-emission branch needs the unique `ℓ_prev`) and by R7a's chain-order replay (discharge (4)(iii) at Case B's sub-case B2 selects the chain element at chain index `J_d^Σ + 1` past the maximum)." Postcondition (b): "so downstream consumers reference `J_d^Σ + 1` as 'next chain index' uniformly without case-splitting on emptiness at the citation site."
**Problem**: Use-site inventory in a definition/lemma slot. The downstream-consumer list does not advance R0a-Cor1's content; it is bookkeeping that rots when consumers move.
**Required**: State the two postconditions (unique T1-max; `J_d^Σ=-1` empty convention) and stop. Drop the "consumed downstream by..." clauses.

### Issue 5: R6b's Justification elaborates an alternative definition the ASN explicitly does not adopt
**ASN-0086, R6b Justification**: "(ii) Active-subset reading (an alternative not adopted). Had the Definition quantified `(b, F', G') ∈ A_R^Σ` instead, deciding `a ∈ nullified(Σ)` would entail first deciding `b ∉ nullified(Σ)` ... a fixpoint computation over the retraction-of-retraction graph ... parity of the retraction-chain depth ..."
**Problem**: This is an extended development of a case the Definition's quantification range already excludes — reviser drift. R6b's actual content (membership is a single-pass existential over `L_R^Σ`) is one sentence; the counterfactual decision-procedure essay is meta-prose.
**Required**: State that `nullified` quantifies over `L_R^Σ` (audit slice), so membership is a flat single-pass test independent of any witness's own status. One contrasting sentence on the active-subset reading suffices; delete the parity/fixpoint elaboration.

### Issue 6: Design Note: NonTupleRetractionViaClassifierTuples is a "why the restriction exists" essay and a deferral target
**ASN-0086, Design Note**: "Nelson's design intent treats retraction as a uniform operation over any owned addressable entity — bytes, links, and documents alike all enter the same 'not currently addressable, awaiting historical backtrack' state under owner authority ... Nelson's uniform 'DELETED' state is realized as one substrate primitive plus one layer convention, not two substrate primitives."
**Problem**: The substantive content — `nullified(Σ) ⊆ A_rel^Σ`, non-tuple withdrawal handled by classifier tuples — is two sentences. The rest justifies *why* the restriction is the right design rather than advancing reasoning. It is also a forward-reference target: the Definition of Nullified defers to it ("see Design Note ... below").
**Required**: Fold the two operative sentences into the Definition of `nullified` (the restriction and the classifier-tuple recovery). Delete the Nelson-intent essay or move it to a one-line remark.

### Issue 7: Multiple sections defer to the same downstream location (WP Case 2)
**ASN-0086**: R6c Consequence (d) ends "...is unpacked in WP Case 2 (Weakest-Precondition Analysis, below)"; the Nullify definition and an Open Question also point at the same regime distinction; WP Case 2 in turn re-cites the unit-depth discipline and R0a.
**Problem**: Three upstream sites defer to one downstream location for the same regime distinction. This is the forward-reference accretion the classifier targets.
**Required**: State the regime distinction once at its definitional home and let the others cite it without prose ("see ... below, which makes the consequence explicit").

### Issue 8: R0's verification redundantly recites the L-permissions as "not requiring preservation" — repeated in R5-Cor and R7a
**ASN-0086**: "L-permissions (not invariants requiring preservation). L4(c), L7, L9, L10, L11b are permissions ... No preservation obligation arises ... listed here for completeness against the substrate-conforming catalog." This paragraph appears in R0, in R5-Cor's discharge, and in R7a.
**Problem**: "Listed for completeness" is the tell — content that does not advance reasoning, repeated. Permissions by definition impose no obligation; saying so three times is noise.
**Required**: Remove the permission recitals; if needed, one global sentence near the substrate-conforming-layer Definition.

## OUT_OF_SCOPE

### Topic 1: Concurrency/atomicity of Emit vs Observe, ordering of Observe results, cardinality bound on nullified(Σ)
**Why out of scope**: These are already correctly parked in Open Questions. They are genuine future ASN territory (consistency model, result ordering, retraction ratio), not gaps in the present state/operation/invariant definitions.

### Topic 2: Tightening L1b (`#E ≥ 2`) to `#E = 2` at the foundation
**Why out of scope**: R0a-Cor2 establishes `#E = 2` for this note's standard-triple links; whether L1b itself should be tightened is a change to ASN-0043 (a foundation), not a revision to ASN-0086. Correctly raised as an Open Question.

META: The active/audit distinction (R5/R6) is a genuine system guarantee, so the note has not drifted into implementation mechanics — but R0–R5 and R7a are largely re-derivations of ASN-0093/0043 guarantees, and the proof bloat is the symptom to fix, not the framing.

VERDICT: REVISE
