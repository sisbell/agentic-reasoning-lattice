# Review of ASN-0047

## REVISE

### Issue 1: Self-reference to "ASN-0047" in section heading
**ASN-0047, *Amendments to existing transitions* section**: "**Consequence for J4 (Fork, ASN-0047).** Since J4's K.μ⁺ step is now restricted to content-subspace V-positions..."
**Problem**: The "ASN-0047" qualifier is a self-reference — the ASN refers to itself by its own number. J4 is defined within this ASN; the qualifier carries no information.
**Required**: Remove "ASN-0047" from the heading. Use "**Consequence for J4 (Fork).**" alone.

### Issue 2: Promised "(counterfactual)" labels not delivered
**ASN-0047, *Elementary transitions* section, Rejection model paragraph**: "Counterfactual analyses below ('Step 2 (counterfactual)', 'Step 3 (counterfactual)', 'Step 5 (counterfactual)', etc.) appeal to this convention to show that an attempted operation falls outside the transition set..."
**Problem**: No worked example contains a step labeled "(counterfactual)". Exclusion notes ("A second K.δ at `(t, 1)` is excluded...") appear in the ghost-base versioning example without that label; the labels promised in Rejection model never materialise. Forward-reference accretion: meta-prose promising content that does not exist.
**Required**: Either rewrite the rejection model paragraph without naming labels that aren't used, or add the labels to the worked-example steps that perform counterfactual analysis.

### Issue 3: P3★ and P5★ duplicate naming
**ASN-0047, *Extended monotonicity invariants* section**: "P5★ is logically equivalent to P3★ — the same six clauses grouped per-component rather than flat-conjoined — and the two names are interchangeable as monotonicity premises."
**Problem**: Two names for the same logical content. The Properties Introduced table carries both. Meta-prose ("the two names are interchangeable") confirms the duplication is conscious but unjustified.
**Required**: Pick one name. Remove the other and consolidate references.

### Issue 4: J0 axiom rationalization paragraph
**ASN-0047, *Coupling and isolation* section, J0**: The final sentence reads "J0 is *axiomatic* in this ASN, standing alongside SubspaceConventionAxiom, NodeUniqueAllocation, SubAllocatorAxiom, NoDeallocation (ASN-0034), and S0 (ASN-0036) as an axiom; the per-state invariant J1★ is *derived* from J0 by the wp analysis above (not axiomatic), so the distinction must be tracked."
**Problem**: Use-site inventory of all axioms + a "must be tracked" instruction. Both patterns flagged by the anti-bloat classifier: enumeration of related axioms is the "downstream consumers" pattern at the axiom site; "so the distinction must be tracked" is meta-prose instructing the reader rather than advancing the claim.
**Required**: J0's content is "allocation requires placement." State it. Drop the inventory of co-axioms and the bookkeeping instruction.

### Issue 5: Multiple deferrals to *Link-withdrawal gap*
**ASN-0047, three locations**:
- K.μ⁻ section: "**Link-withdrawal gap under D-CTG★ / D-MIN★.** Trading the link-subspace tombstoning provision for uniform contiguity has a load-bearing consequence..." (multi-paragraph)
- *Sufficiency claim*: "The known gap is Nelson's tombstone-style interior link withdrawal (see *Link-withdrawal gap under D-CTG★/D-MIN★* below)."
- Worked example Step 5: "Nelson's tombstoning design is not expressible as a K.μ⁻ transition — see *Link-withdrawal gap under D-CTG★ / D-MIN★* above."
- Open Questions: another paragraph on the same withdrawal mechanism.
**Problem**: Same gap deferred from four locations. Forward-reference accretion pattern: "multiple paragraphs in different sections defer to the same downstream location."
**Required**: State the gap once at the source (the D-CTG★/D-MIN★ amendment). Other locations should reference the gap by name without restating it.

### Issue 6: Document-ordering justifications
**ASN-0047, K.μ⁻ section**: "Stating admissibility as an explicit precondition aligns K.μ⁻'s contract with the form used by every other elementary transition in this ASN (K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L all state explicit preconditions), so the case analysis below acts as a closed verification rather than the sole source of admissibility content."
**ASN-0047, *Extended reachable-state invariants* section**: "The reachable-state invariant theorems for the four-component state are subsumed by ExtendedReachableStateInvariants and ExtendedTransitionInvariants stated below for the five-component state... The pair of extended theorems is stated and proved in the *Extended reachable-state invariants* section below; no separate four-component formulation is given here."
**Problem**: Both passages justify document organization rather than advancing claims. Pattern: "prose justifies document ordering."
**Required**: Delete the meta-paragraphs. The contracts and theorem statements that follow are self-justifying.

### Issue 7: Repeated "Frame-preserved invariants" verification footers
**ASN-0047, every worked example step**: Each step ends with a sentence of the form "Frame-preserved invariants: the [composite] frames C, L, E, R; arrangement-side invariants verified above. Other invariants inherit from Σₙ per ExtendedReachableStateInvariants."
**Problem**: Use-site inventory repeated across all worked examples. The verification template is identical step-to-step; only the framed components vary. The repetition wastes reader attention and obscures the substantive verification.
**Required**: State the verification template once. In subsequent steps, only call out *deviations* from the template ("S3★ does not reduce to S3 here because V_{s_L}(d) is non-empty") rather than re-stating that frame-preserved invariants are preserved by frame.

### Issue 8: Σ.E and Σ.R definitions enumerate downstream consumers in their introduction
**ASN-0047, *The state model* section**: After the Σ.E definition: "Given this exclusion, the level predicates of ASN-0045 partition E into exactly three strata: E_node = ..., E_account = ..., E_doc = ..."
**Problem**: The Σ.E definition is `E ⊆ T` with the exclusion `¬IsElement(e)`. The "partition into three strata" sentence enumerates how downstream consumers will slice E, not what E is. Pattern: "a definition's introduction enumerates downstream consumers."
**Required**: The level-predicate stratification is a consequence of T4c (ASN-0045) and Σ.E's exclusion clause; readers can derive it. Either move the stratification to a separate stated *Consequence*, or drop it from the definition introduction.

### Issue 9: J4 definition contains operational-level V-position correspondence
**ASN-0047, *Coupling and isolation* section, J4**: The J4 definition specifies "V-position–wise correspondence to d_src's content subspace: `(A v ∈ V_{s_C}(d_src) : M'(d_new)(v) = M(d_src)(v))` and `V_{s_C}(d_new) = V_{s_C}(d_src)`".
**Problem**: This is operational-level detail — it specifies what fork *does* at the V-position granularity. The scope notes exclude "Named operations and their specifications (... CREATENEWVERSION ...)". J4's abstract role in the proof (showing the elementary kinds are sufficient for fork) requires only that fork compounds K.δ + K.μ⁺ + K.ρ. The V-position correspondence belongs in a future operations ASN.
**Required**: Either weaken J4's definition to a sufficiency claim ("Fork compounds K.δ + K.μ⁺ + K.ρ; the post-state details are operation-specific") with discharge of the relevant invariants stated abstractly, or move the V-position correspondence to the open-questions / future-ASN frame.

### Issue 10: Cross-document disjointness chain lemma cites Case-B premises in a confusing order
**ASN-0047, *Allocator hierarchy under documents* section**: "Case B — Prefix-incomparable (`d₁ ⋠ d₂ ∧ d₂ ⋠ d₁`). The disjointness comes from T10a applied at the appropriate allocator-tree level: T10a.2 (NonNestingSiblingPrefixes) for any same-allocator sibling pair, T10a.5 (CrossAllocatorIncomparability) for any cross-lineage allocator pair, with mixed configurations dispatched via a layered T10a.2 at the closest common ancestor allocator. T10a.6 packages these as cross-allocator domain disjointness."
**Problem**: Case B's hypothesis is `d₁ ⋠ d₂ ∧ d₂ ⋠ d₁`. The proof step only needs to lift the document-level divergence to the anchor level. The T10a.{2,5,6} appeals are not consumed in the lift — they appear to justify *why* Case B can occur (distinct documents in distinct allocator subtrees produce prefix-incomparable document tumblers). But the case split (prefix-comparable vs not) is exhaustive by trichotomy and does not require T10a as a citation. The proof reads as "by T10a packaging" without making explicit which lemma discharges which proof step.
**Required**: Rewrite Case B to state explicitly what proof step each cited lemma discharges. Either: (a) the case split is by trichotomy and T10a citations belong only where they discharge a step, or (b) state the lift step independent of T10a and explain T10a's role in *why distinct documents can satisfy Case B's hypothesis* as a separate remark.

### Issue 11: Foundation invariants section uses essay-content framing
**ASN-0047, *Extended reachable-state invariants* section, *Foundation invariants previously implicit* paragraph**: A multi-paragraph essay covering S4, S7a, S7b, S7c, S7d, L1b, L-fin, D-SEQ★, NodeLineage in narrative form.
**Problem**: This section's structural slot is "preservation across elementary transitions." Several entries (S7a, S7b, S7c, S7d) get one-sentence preservation arguments; others (S4, L1b, NodeLineage) get multi-paragraph derivations including discussion of the first-link vs subsequent-link case, K.λ's two phases, etc. The mixing of one-liners and multi-paragraph derivations within one prose block makes it hard to verify each invariant's preservation. The label "previously implicit" is meta-framing.
**Required**: Either split into per-invariant subsections (one paragraph each) with uniform structure, or move the multi-paragraph derivations (L1b, S4, NodeLineage) to their own labeled lemmas with single-sentence "preserved by frame" notes here.

## OUT_OF_SCOPE

### Topic 1: Tombstone-style interior link withdrawal mechanism
**Why out of scope**: The withdrawal mechanism (status flag, tombstone marker, or explicit retraction link) is a separate operation, not specifiable within the current K.μ⁻ effect schema. The ASN correctly defers this. The mechanism's invariants belong in a future ASN on link withdrawal / tombstoning.

### Topic 2: Version contract for ghost-base versioning
**Why out of scope**: The ASN correctly defers "the richer version contract — including arrangement invariants, provenance flow, and lineage acyclicity" to a subsequent version-management ASN.

### Topic 3: Account-level depth-1 extension
**Why out of scope**: The open question explores whether K.δ at k = 1 with `IsAccount(t)` should be admitted. The ASN correctly defers this to a future extension; the current restriction is justified by Nelson's design and Gregory's implementation.

### Topic 4: Subspace identifier values (s_C = 1, s_L = 2)
**Why out of scope**: Pinned by SubspaceConventionAxiom citing Nelson's LM 4/30–4/31 and udanax-green's source files. Citing specific source files for an axiom is acceptable because the axiom encodes a design choice that needs grounding evidence; the line numbers stay in the consultation evidence trail, not in the spec body.

VERDICT: REVISE
