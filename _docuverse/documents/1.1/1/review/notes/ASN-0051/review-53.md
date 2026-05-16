# Review of ASN-0051

## REVISE

### Issue 1: Citation inconsistency for L3

**Endset Projection section, NoStaleResolutionState architectural remark**: cites "L3 (TripleEndsetStructure, ASN-0043)" in the link-store signature paragraph.

**Scoping note, same section (subsequent paragraph)**: cites "L3 (NEndsetStructure, ASN-0043)" when discussing the arity-3 floor.

**Problem**: ASN-0043's L3 is named **NEndsetStructure**, not TripleEndsetStructure. TripleEndsetStructure is the name used in ASN-0047. The same ASN cites L3 in ASN-0043 with two different names within a few paragraphs of each other.

**Required**: Make the citation consistent. Either both cite "L3 (NEndsetStructure, ASN-0043)" — the ASN-0043 reference — or one cites "L3 (TripleEndsetStructure, ASN-0047)" if the more specific triple form is intended.

### Issue 2: Citation inconsistency for K.δ

**CrossDocumentDecoupling witness, Step 1**: "K.δ (DocumentAllocation, ASN-0047) allocates d₂ ∈ E_doc"

**Problem**: ASN-0047's K.δ is named **EntityCreation**, not DocumentAllocation. The document-allocation behavior (`M'(e) = ∅` for `IsDocument(e)`) is a sub-case of K.δ EntityCreation, not a separately-named transition. Similar K.δ usages elsewhere in the ASN (e.g., SV10 witness "K.δ ¬IsNode case") do not assign this name.

**Required**: Replace "K.δ (DocumentAllocation, ASN-0047)" with "K.δ (EntityCreation, ASN-0047)" with the document sub-case described in prose rather than as a citation name.

### Issue 3: SV11 multi-block attainment — the structural argument is stronger than "open"

**SV11, attainment witness section**: "*Multi-block (p ≥ 2) attainment — open.* This ASN does not exhibit an attainment witness for p ≥ 2... what is left open is the *existence* of a concrete (B, e) configuration realising the biconditional at p ≥ 2."

**Problem**: The configurational constraints can be analyzed within this ASN. For p ≥ 2 in the text subspace, D-CTG forces V-contiguity, so multiple blocks are V-adjacent with I-jumps (non-mergeable only by I-non-adjacency). For every (j, k) decomposition term to be non-empty, every span must intersect every block — but a span is a single interval in T, so a span intersecting both β₁ and β₂ must include the I-gap between them and fully span the prefix of β₂'s extent up to its intersection point. Combined with non-overlap within each block, the constraints appear structurally unsatisfiable: any span that reaches β₂ from β₁ covers β₁'s left portion through β₁'s right boundary, leaving no room for another span's term within β₁ that is both disjoint and non-adjacent. The ASN should either (a) prove m·p is unreachable at p ≥ 2 (sharpening the bound), or (b) exhibit a concrete witness, or (c) explicitly state that the bound is loose at p ≥ 2 rather than framing this purely as a missing witness.

**Required**: Add at least a structural argument showing why attainment fails at p ≥ 2 — interval constraint of spans + V-contiguity of blocks within a subspace — and either prove non-attainment as a sharpening of SV11 or explicitly mark the m·p bound as loose at p ≥ 2.

### Issue 4: SV5 locate transformation is not formally stated as an SV claim

**SV5 (ReorderingProjectionInvariance)**: states `π_{Σ'}(e, d) = π_Σ(e, d)` but only π, not locate.

**Problem**: The discussion after SV5 derives the formal relationship `locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)}` and uses it in SV13(e), but this relationship is not given an SV label, while SV2 and SV3 explicitly state both π and locate inclusions. The asymmetry is unmotivated — readers consulting the SV catalog will find locate's K.μ~ behavior absent.

**Required**: Either extend SV5's statement to include the locate transformation explicitly (`locate_{Σ'}(e, d) = {ψ(v) : v ∈ locate_Σ(e, d)}`), or add a separate sub-claim (e.g., SV5b) that downstream consumers can cite.

### Issue 5: SV6 sub-lemma proof structure — split needed

**SV6 proof, sub-lemma "no early divergence"**: contains nested arguments (Prefix exclusion, Divergence is upward, then steps (a) and (b)) running approximately one and a half pages.

**Problem**: The proof's load-bearing inferences are correct, but the structure conflates the sub-lemma's two parts (existence of position j for T1(i); direction of inequality from t ≥ s). A reader checking that step (b)'s "either t = s or first divergence ≥ k" case-split is exhaustive must trace back through the sub-lemma's hypotheses. The argument is correct but accessibility suffers.

**Required**: Split the sub-lemma into two named claims: (i) under the assumption of a first divergence at j < k, derive #t ≥ j and tⱼ > sⱼ; (ii) lift this to the conclusions (a) #t ≥ k and (b) t agrees with s on positions 1..k−1 via the t = s vs t ≠ s case-split. This is a stylistic revision; the proof's correctness is not in question.

## OUT_OF_SCOPE

### Topic 1: Broader-level spans (k ≤ p₃)
**Why out of scope**: The ASN explicitly defers broader-level span survivability (action point at or before the third field separator, enabling cross-document/account/node coverage) to ASN-0034's address-hierarchy machinery. SV6 is scoped to element-field spans (k > p₃) and the ASN identifies this scope boundary cleanly.

### Topic 2: Same-origin coverage growth at byte level
**Why out of scope**: The "Content Allocation and Coverage Stability" subsection identifies sequential overshoot and child-depth entry as mechanisms by which same-origin allocations can enter existing spans, but defers the precise allocator-discipline conditions to ASN-0034. This is honest scope management — the descriptive content here motivates SV6's cross-origin exclusion without overcommitting to allocator details.

### Topic 3: Per-step (intermediate-state) projection behavior under K.μ~
**Why out of scope**: K.μ~ as a distinguished composite has an intermediate state Σ_int with strictly reduced π. The ASN's composite-level π-invariance claim (SV5) and the explicit per-step note suffice for downstream consumers; a separate formal claim on Σ_int would not add survivability content.

### Topic 4: Tightness of m·p fragment bound across composite edits
**Why out of scope**: The SV13(g) caveat captures state-dependence of m·p; characterizing how composite edits raise or lower p over time is operational analysis that belongs in implementation-side notes rather than the survivability claim itself.

VERDICT: REVISE
