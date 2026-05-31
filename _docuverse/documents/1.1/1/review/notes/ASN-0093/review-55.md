# Review of ASN-0093

I checked the invariant/lemma proofs and the simultaneous induction for soundness: the chain-membership induction (FirstEmission → ChainMembershipForOrigin → StoreT4Validity → freshness → SD) is well-founded with no within-step circularity, the cross-document disjointness lemma covers both the prefix-comparable and incomparable branches correctly, and the K.α/K.λ first/subsequent-emit cases discharge C1b/C1c/L1c without gap. The substantive logic holds. The findings below are accretion patterns flagged under the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: SubspaceConventionAxiom statement and provenance duplicated verbatim
**ASN-0093, State model ("Subspace identifiers")** and **Properties Introduced table (SubspaceConventionAxiom row)**: the State model gives "`s_C = 1 ∧ s_L = 2` … Pinned by Nelson's design (LM 4/30–4/31) and Gregory's `xanadu.h:144–146` / `granf2.c:162` / `do2.c:94`." The table row repeats "Substrate commitment: `s_C = 1 ∧ s_L = 2`; pinned by Nelson (LM 4/30–4/31) and Gregory (`xanadu.h:144–146`, `granf2.c:162`, `do2.c:94`)."
**Problem**: Both the axiom statement and the full file:line provenance appear in two locations — the "two paragraphs say the same thing in different words" pattern. The table is an index; carrying the complete citation set there duplicates the canonical statement in the State model.
**Required**: Keep the statement and provenance in the State model; reduce the table row to a name/status pointer (e.g., "Substrate commitment; see State model").

### Issue 2: M2 enumerates which foundation invariants it makes vacuous
**ASN-0093, M2 (EmptyArrangement)**: "M2 is the explicit ground on which the arrangement-side invariants of ASN-0036 (S2, S3, S8a, S8-depth, S8-fin, D-CTG, D-MIN) hold vacuously in the substrate."
**Problem**: This is a downstream-consumer inventory — it names seven foundation invariants that benefit from M2 rather than advancing M2's assertion (`M(d) = ∅`) or its proof. It is distinct from the previously-declined deferral finding (different sentence, different pattern), and it is exactly the "definition enumerates downstream consumers" pattern.
**Required**: Drop the enumeration. M2's body should end at the preservation argument (`M(d) = ∅` fixed at registration, no arrangement-mutation transition).

### Issue 3: Worked-example Step 8 re-narrates the abstract freshness lemma instead of checking concrete tumblers
**ASN-0093, Worked example, Step 8**: "freshness `ℓ_new ∉ …` is discharged as in the SD / ChainMembershipForOrigin matrix rows: within-document freshness against `dom(L)` (ChainEnumerationInjectivity + ChainMembershipForOrigin, separating `ℓ_new = s₂` from `ℓ = s₁`), cross-document freshness … (ChainPrefixExtension + Cross-document disjointness + T10 …), and cross-subspace freshness … (… SC-NEQ + T7 …)."
**Problem**: Steps 2–3 verify distinctness concretely ("Disagreement at position 7 gives `ℓ ≠ a`"); Step 8 instead replays the general three-way lemma machinery abstractly. The example's job is to instantiate, not to re-prove SubsequentEmissionFreshness — this is essay content in an example slot. The concrete check is one line: `ℓ_new = [1,0,2,0,5,0,2,2]` differs from `ℓ` at position 8, from `ℓ''` at position 6, and from each content address at position 7.
**Required**: Replace the lemma-citation narration with the concrete position-wise distinctness check, matching Steps 2–3.

## OUT_OF_SCOPE

### Topic 1: Whether nested documents (`d ≺ d'`, both `zeros = 2`) are admissible
**Why out of scope**: The worked example deliberately registers `d = [1,0,2,0,5]` and `d' = [1,0,2,0,5,3]` with `d ≺ d'`. K.σ admits this (T4-valid ∧ `zeros = 2` ∧ fresh), and cross-document disjointness handles the collision question correctly. Whether document-space should forbid nesting is an S7d/allocation-discipline concern, not a substrate error.

VERDICT: REVISE
