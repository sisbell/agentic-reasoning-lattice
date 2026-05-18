# Review of ASN-0086

## REVISE

### Issue 1: Use-site inventory in Sparse-allocator hypothesis
**ASN-0086, Setup**: "*Consumers.* The hypothesis is load-bearing for R0 Step 2 Case A's argument that the sibling sweep through `A_{d.0.1}` from position 1 to position `s_L` is 'witness, not material traversal'..."
**Problem**: Exactly the flagged pattern — "the definition's introduction enumerates downstream consumers." Future readers will derive load-bearing-ness from the proofs that consume it; the inventory rots as proofs evolve.
**Required**: Delete the *Consumers* paragraph. State the hypothesis once.

### Issue 2: Discipline-conditionality flag restated 6+ times
**ASN-0086, throughout**: Setup's Sibling-frontier definition, R0a's header parenthetical, R0a-Cor1's hypothesis restatement, R0a-Cor2's hypothesis restatement, Emit_K's postcondition note, Nullify's *Discipline assumption*, plus Open Questions.
**Problem**: "multiple paragraphs in different sections defer to the same downstream location" — each restating creates compound noise. The conditionality is a single fact about the substrate.
**Required**: State once at Setup. Downstream sites cross-reference rather than restate.

### Issue 3: R0a "Failure modes — necessity of the discipline" paragraph
**ASN-0086, R0a proof**: "*Failure modes — necessity of the discipline.* A single non-disciplinary class-(iii) transition depositing at a strict prefix-extension of an existing link permanently breaks the antichain..."
**Problem**: Defensive justification of the conditional form. Once R0a is stated as discipline-conditional, the discipline's necessity is implicit; this paragraph asserts that the hypothesis is genuinely needed rather than what the lemma says.
**Required**: Delete.

### Issue 4: "Modal note" on R5
**ASN-0086, R5**: "*Modal note.* R5 is a positive admissibility lemma: it asserts that a specific substrate-level construction is exhibitable (Stage 1, via L4(c) + L13 + R0) and is not opposed by any other invariant (Stage 2's exhaustive check). The classification is therefore LEMMA, not META..."
**Problem**: Defensive justification of classification choice — "new prose around an axiom explains why the axiom is needed rather than what it says." The classification stands on the proof structure, not on a paragraph defending it.
**Required**: Delete the Modal note paragraph.

### Issue 5: R6c Consequence (d) forward-reference accretion
**ASN-0086, R6c Consequences**: "*[COROLLARY, stipulation-conditional]* *All visible state-transforming relational-layer operations reduce to `Emit_K` — anticipating R7 below.* Stated here in R6's vocabulary because the active subset already places Nullify within the relational-layer operation set."
**Problem**: Two flagged patterns at once — "anticipating R7 below" is a forward reference, and "Stated here in R6's vocabulary because..." is prose justifying document ordering.
**Required**: Either prove the consequence fully in R6's scope or defer entirely to R7. Pick one location.

### Issue 6: Convention—RetractionDirectionality defensive paragraphs
**ASN-0086, Convention—RetractionDirectionality**: "The asymmetry is *not* a substrate-level entailment of L4–L8: L4 (EndsetGenerality) and L5 (EndsetSetSemantics) treat from- and to-slots symmetrically, L6 (SlotDistinction) gives them only positional identity, and L7 (DirectionalFlexibility) explicitly defers directional interpretation to the type. The convention names how the retraction type `R` exercises L7..."
**Problem**: Defensive prose explaining why the convention is a convention rather than a derived fact. The convention itself fits in one sentence.
**Required**: State the convention (to-set carries targets) without the L4–L8 disclaimer; remove the alternatives paragraph.

### Issue 7: "Why X is a caller parameter" rationale paragraphs
**ASN-0086, Definition of Emit_K**: "*Why `d` is a caller parameter.* The home document is an explicit input rather than a substrate-chosen one because link ownership is a relational fact about which document the link belongs to (Nelson's design intent) and because the udanax-green `MAKELINK` / `docreatelink` path takes the home as an explicit `docaddr` argument."
**ASN-0086, Definition of Nullify**: "*Why `d_retr` is a caller parameter, not `home(a)`.* The substrate places no constraint on which `d ∈ dom(Σ.M)` houses a retraction tuple..."
**Problem**: Design-rationale prose in specification slots. The signature carries the parameter; explaining why is commentary, not specification.
**Required**: Remove both rationale paragraphs; the parameter shape is self-evident from the signature.

### Issue 8: Allocator-naming convention restated
**ASN-0086, Setup**: "*Allocator-naming convention.* Throughout this note, `A_x` denotes the allocator whose *first emission* is `x`."
**ASN-0086, Worked Sketch**: "*Allocator scaffolding (by SharedDepthOneAllocator, R0a-Cor2; allocator-naming convention from Setup).*"
**Problem**: Convention stated in Setup, then restated/cited in Worked Sketch. The first statement should suffice.
**Required**: Remove the "allocator-naming convention from Setup" annotation in Worked Sketch.

### Issue 9: R6b classified as LEMMA but is META about the Definition
**ASN-0086, R6b**: "*Justification.* By the Definition's quantifier range over `L_R^Σ` (the audit slice, not the active subset `A_R^Σ`), `a ∈ nullified(Σ)` is witnessed by any retraction tuple in `L_R^Σ` whose to-coverage contains `a`, regardless of that witness's own active-subset status."
**Problem**: This is not a derived theorem — it is a property of the Definition's quantifier-range choice. Changing the Definition would change R6b without any further proof obligation. Calling it a LEMMA misclassifies the content.
**Required**: Reclassify as META or fold into a remark on the Definition of `nullified`. The extended worked example showing why the distinction matters can stay; the LEMMA framing should not.

### Issue 10: R5 Stage 2's exhaustiveness asserted, not enumerated
**ASN-0086, R5 proof, Stage 2**: "L4(c) (EndsetGenerality, ASN-0043) is the only L-invariant that constrains endset target addresses; it permits link-subspace targets directly. No other invariant on the ASN-0043 / ASN-0034 / ASN-0036 stack constrains endset content (the remaining invariants are properties of `Σ.L`'s shape, the addressing structure, or `(Σ.C, Σ.M)` — all orthogonal to which addresses an endset's spans may target)."
**Problem**: Exhaustiveness by class-partition without enumeration. Dijkstra-style rigor requires showing each invariant inspected; "the remaining invariants are properties of X, Y, Z" asserts a partition without verifying every L-invariant (L0–L14a, L-fin) falls into one of the named classes.
**Required**: Enumerate the L-invariants explicitly and tag each as (i) constrains endset content [permits or forbids], or (ii) orthogonal to endset content [with one-line reason]. The current sentence asserts but does not check.

### Issue 11: R7 is largely tautological given Definition of relational layer
**ASN-0086, R7 proof**: Step 1 enumerates the relational-layer operations from the Definition. Step 2 unfolds Nullify. Then "by R7a... by the Definition's commitment to `Emit_K`, every relational-layer-initiated class-(iii) step is an `Emit_K` call."
**Problem**: R7's substantive content is R7a; the remainder is unpacking the Definition. The two-claim structure (R7a + R7) inflates a single point into two named lemmas. R7's "proof" is mechanical unfolding.
**Required**: Either fold R7 into the Definition as a derived corollary (one sentence) or rewrite R7 so its proof carries weight beyond unfolding.

### Issue 12: R0a-Cor2 and Nullified definition forward-reference Open Questions
**ASN-0086, R0a-Cor2**: "R0a-Cor2 narrows L1b's `#E ≥ 2` admission to `#E = 2`, matching the udanax-green implementation; relaxation to deeper-sited links is discussed in Open Questions."
**ASN-0086, Definition of Nullified**: "Retractions whose `coverage(G')` lies entirely outside `A_rel^Σ ∩ {a : |Σ.L(a)| = 3}` are well-formed `Emit_R` calls but operationally inert for `A_K`... The higher-arity extension is flagged in Open Questions."
**Problem**: Forward-reference accretion — "the full account is in Z." Open Questions stand on their own; pointing forward at multiple sites creates noise.
**Required**: State R0a-Cor2 and the Nullified scope without forward pointers. Readers will find Open Questions independently.

### Issue 13: Worked Sketch L-invariant verification list
**ASN-0086, Worked Sketch**: 12 bullet points verifying L0/L1/L1a/L1b/L1c/L2/L3/L4(c)/L11a/L12/L12a/L12b/L14/L14a/L-fin against the concrete `b₁`, then "L-invariant verification at the concrete a₂... structurally identical to b₁'s pattern."
**Problem**: R0's proof already verifies all L-invariants generically; the concrete verification doubles work that the schematic argument already establishes. The "structurally identical" remark for a₂ implicitly admits the redundancy.
**Required**: Reduce to the invariants whose discharge depends on the concrete tumbler structure (e.g., L0 first-element check); for the rest, cite R0's discharge.

### Issue 14: Sparse-allocator hypothesis cites Nelson and udanax-green inline
**ASN-0086, Setup**: "The hypothesis is stronger than T10a alone... It matches Nelson's ghost-element design (*Literary Machines* 4/23: '...') and is realized by udanax-green's `findisatoinsertmolecule` (granf2.c:158–181)..."
**Problem**: Implementation citations embedded in axiom statement. The axiom should state what holds; that a specific implementation realizes it is commentary about realizability.
**Required**: Move the Nelson/udanax-green citations out of the hypothesis body. State the hypothesis abstractly; place realizability evidence in a separate Implementation Notes remark.

### Issue 15: Setup section is the bloat epicenter
**ASN-0086, Setup**: The Setup section runs roughly 1500 words and contains: Setup hypothesis, Subspace-distinctness hypothesis, Sparse-allocator hypothesis (with Consumers paragraph), zero-count depth definition (with Terminology note), allocator-tree depth definition, SharedDepthOneAllocator lemma with three-step proof, allocator-naming convention, state-transition relation definition (with three frame conditions, broader-transition discussion, categorical-transition discussion), substrate emission primitive paragraph, Sibling-frontier discipline definition (with discipline-conditionality flag), Unit-depth retraction discipline definition, Extension definition, BroadExtension definition, AddressUniverse, Partition.
**Problem**: A reader must absorb ~15 named constructs before reaching R0. Several are not load-bearing until later sections (Unit-depth retraction discipline, BroadExtension). The Setup mixes structural facts with implementation hypotheses with definitional conveniences.
**Required**: Separate (a) structural foundation (state-transition relation, frame conditions, AddressUniverse, Partition) from (b) implementation hypotheses (Sparse-allocator, Sibling-frontier, Unit-depth retraction). Defer definitions like BroadExtension to the point of first use (R6c-Corollary).

## OUT_OF_SCOPE

None to add — the Open Questions list captures the future-ASN topics appropriately.

META: ASN-0086 is in implementation-relevant territory — the active/audit distinction, retraction relation, and reduction-to-Emit_K are abstract structural commitments — but the document has accumulated meta-prose around forward references, defensive classifications, and discipline-conditionality flags faster than its proof content has stabilized.

VERDICT: REVISE
