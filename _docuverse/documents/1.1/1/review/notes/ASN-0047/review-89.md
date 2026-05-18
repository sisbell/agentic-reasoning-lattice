# Review of ASN-0047

## REVISE

### Issue 1: P5 supersession by P3★ not made explicit in prose

**ASN-0047, *Destruction confinement* and *Extended monotonicity invariants***: P5 is stated for the 4-component state without L12; P3★ is introduced later with L12 included. The text never explicitly states "P5 is superseded by P3★ in the extended state." The table footnote on P3★ describes the synthesis but a reader following the prose sequentially encounters P5 first and then P3★ without being told the relationship — they have to infer it from the table.

**Problem**: The supersession relationship is load-bearing for the ExtendedTransitionInvariants statement, which uses P3★. A reader applying invariants in the extended state needs to know whether P5 still stands as a separate claim or is fully replaced.

**Required**: Add an explicit clause where P3★ is introduced: "P3★ supersedes P5 in the extended state by extending the monotonicity statement to L."

### Issue 2: Allocator names A_C(d), A_L(d), A_v(d) used without formal definition

**ASN-0047, *Worked example: fork with subsequent insertion* and *Worked example: ghost-base document versioning***: The K.α verification cites "d₂'s content sub-allocator A_C(d₂)"; the ghost-base example cites "T10a's GlobalUniqueness on `A_v(1.0.1.0.5)`". The *Allocator hierarchy under documents* section formally names only the *anchors* `b_C(d)` and `b_L(d)`, not the allocators themselves; `A_v(d)` for version allocation is never introduced at all.

**Problem**: The proof of foundational invariants (S4, L1c) in ExtendedReachableStateInvariants relies on these allocator names. A reader checking that "A_v(1.0.1.0.5) was never validly activated" has no formal definition of A_v to verify against.

**Required**: Add formal definitions of A_C(d), A_L(d), A_v(d) — either in the *Notation* section or in the *Allocator hierarchy* section — pinning them to the T10a allocators that emit content, link, and version addresses respectively.

### Issue 3: "SubAllocatorAxiom.Namespace's structural commitment" references an unnamed sub-property

**ASN-0047, *Foundation invariants* (L1b derivation)**: "so `ℓ` has `zeros(ℓ) = 3` and is T4-valid by SubAllocatorAxiom.Namespace's structural commitment."

**Problem**: SubAllocatorAxiom's body contains no sub-property labeled "Namespace." The phrase "namespace property" was used informally earlier in §*Worked example: fork with subsequent insertion* but never formally pinned. The dot notation suggests a sub-clause that does not exist.

**Required**: Either (a) introduce a formal sub-clause label in SubAllocatorAxiom (e.g., "SubAllocatorAxiom.Namespace: outputs of d's sub-allocators are T4-valid"), or (b) replace the dot notation with a direct citation to the relevant axiom clause ("...by SubAllocatorAxiom's structural-form clause `[d.0.s_L.1]` and T4 applied to the suffix").

### Issue 4: K.μ⁻ admissible pattern has redundant disjunction

**ASN-0047, K.μ⁻ Precondition**: "the removed positions in `V_S(d)` form either a suffix of `V_S(d)` under the D-SEQ★-shaped enumeration or all of `V_S(d)`".

**Problem**: A suffix `{[S, 1, ..., 1, k] : n'_S < k ≤ n_S}` parameterised by `0 ≤ n'_S ≤ n_S` already includes the full-clearance case at `n'_S = 0`. The "or all of V_S(d)" is a special case of "suffix," not a disjoint alternative. The K.μ⁻ exhaustiveness lemma immediately afterward correctly treats full clearance as case (a) sub-case `n'_S = 0`, confirming the unification.

**Required**: Either remove "or all of V_S(d)" (since it is subsumed), or rephrase to make explicit that full clearance is the maximal-suffix case (e.g., "a suffix of V_S(d) — possibly the empty suffix (no change) or the full set (clearance)").

### Issue 5: Allocator hierarchy section's introduction enumerates downstream consumers

**ASN-0047, *Allocator hierarchy under documents***: "We formalize this structure to underwrite the K.λ first-link case's allocation discipline and to make uniqueness precise for the multi-subspace state."

**Problem**: This is consumer enumeration in a definition's introduction — listing what downstream sections will use the construction for, rather than advancing the section's own content. The structural facts that follow (anchor definitions, sub-allocator behavior) stand on their own; the consumer list is review-mode anti-bloat residue.

**Required**: Replace with a one-sentence orientation that names the object being formalised, not its downstream uses: e.g., "We formalise the sub-allocator structure under each document — anchors, frontier discipline, and emission ordering."

## OUT_OF_SCOPE

### Topic 1: Concurrency discipline for Path 2 freshness discharge
**Why out of scope**: Concurrency and the soundness of K.δ's direct-inspection path under interleaved allocation events is correctly identified as an Open Question. The single-event semantics this ASN assumes is internally consistent.

### Topic 2: Link withdrawal mechanism reconciling Nelson's tombstoning with D-CTG★
**Why out of scope**: The *Link-withdrawal gap* section explicitly identifies this as territory for a separate mechanism, not a defect in K.μ⁻'s contract under the chosen invariants. Recorded as an Open Question.

### Topic 3: Account-level depth-1 versioning admissibility
**Why out of scope**: The current ASN restricts K.δ k=1 to documents; the question of whether to admit account-level k=1 is correctly deferred as an Open Question.

### Topic 4: Version graph and lineage acyclicity
**Why out of scope**: The ghost-base relaxation defers the richer version contract to a subsequent version-management ASN, which is the right placement.

VERDICT: REVISE
