# Review of ASN-0086

## REVISE

### Issue 1: Phantom foundation citations

**ASN-0086, SharedDepthOneAllocator lemma proof, steps (a)–(c)**: "T2 (ChildSpawnAdmissibility, ASN-0034) admits a child-spawn pair (d, k') iff k' ∈ {0, 1, 2}" and "the additional condition expressed by TA5(d) (ChildSpawnZeroCount, ASN-0034) on the resulting child's zero count"

**Problem**: T2 in ASN-0034 is `IntrinsicComparison` (decidability of tumbler order), not `ChildSpawnAdmissibility`. Child-spawn admissibility is part of T10a's axiom directly. The labels (T1)/(T2)/(T3) used by `AllocatedSet`'s axiom are *transition shapes within that axiom*, not standalone claims. Similarly, TA5 is `HierarchicalIncrement` with a postcondition (d) — there is no foundation claim named `ChildSpawnZeroCount`. These descriptors will lead readers to search ASN-0034 for non-existent claims.

The citation re-appears at "Allocator-state commitment — sparse-allocator interpretation": "ASN-0034's T10a, whose T2 child-spawn admissibility requires spawnPt(A) ∈ dom_s(parent(A))".

**Required**: Replace phantom names with actual foundation citations: cite T10a's axiom directly for child-spawn admissibility, AllocatedSet's (T2) transition shape where you mean the transition admissibility predicate, and `TA5 (HierarchicalIncrement), postcondition (d)` for the length/zero-position facts.

### Issue 2: "Element-field depth" used as a primitive structural concept without formal definition

**ASN-0086, SharedDepthOneAllocator lemma proof, step (b)**: "(d, 1) yields a child... that stays at element-field depth 0 relative to d (it extends d's rightmost element-field rather than opening a new one). (d, 2) yields a child... placing the spawn one element-field deeper than d, i.e., at element-field depth 1."

**Problem**: "Element-field depth relative to d" carries the load-bearing inference of the lemma yet is never formally defined. The concept is *derivable* from T4's separator semantics (count of new zero positions appended to d's prefix), but the proof treats it as obvious. Without a definition, the step "only k' = 2 opens an allocator at element-field depth 1" is a structural claim a reader cannot verify against the foundation.

**Required**: Add a one-sentence definition before the lemma: "The element-field depth of a tumbler `t` relative to its prefix `s ≼ t` is `zeros(t) − zeros(s)`." Then step (b)'s conclusions follow directly from TA5(d)'s zero-position bookkeeping.

### Issue 3: R0 Step 4's L11a verification is too terse

**ASN-0086, R0 Step 4**: "L11a (LinkUniqueness, ASN-0043): preserved trivially. Prior pairs satisfy L11a at Σ; the new event's address a ∉ dom(Σ.L) is distinct from all prior addresses by freshness."

**Problem**: L11a asserts that *distinct allocation events* produce distinct link addresses. Freshness of `a` (i.e., `a ∉ dom(Σ.L)`) does not by itself establish that the *event* producing `a` is distinct from every prior event — that follows from T10a's at-most-once child-spawn axiom on the spawning pair, combined with the new chain's unique terminal step (Case A's `(d.0.s_L, 1)` or Case B's last sibling `inc`). The proof should make this discharge explicit, since L11a's content is about events, not just addresses.

**Required**: Replace with "By T10a's at-most-once axiom on the child-spawn pair `(d.0.s_L, 1)` (Case A) or by T10a.7 on the new sibling step (Case B), the new event is distinct from every prior event under d; combined with freshness `a ∉ dom(Σ.L)`, L11a is preserved."

### Issue 4: ASN length and density obstructs verification

**ASN-0086, throughout**: The ASN is roughly twice the length needed to express its content. Specifically:

- The Setup section spans ~10 paragraphs of meta-commentary (subspace distinctness elaboration, sparse-allocator interpretation, coarsening of ASN-0034's transition relation, frame conditions enumeration, substrate emission primitive, sibling-frontier discipline, dependency-chain summary). Several of these recur in expanded form at point of use.
- R0a includes a "Failure modes" section, a "Dependency-chain summary" up front (in the Setup section but discussing R0a), and a "Remark — substrate evidence" — each making related points.
- R0 Step 4's L-invariant enumeration spans 24 bullets, several of which (L4, L5, L6, L7, L8, L9, L10) discharge by orthogonality and could be grouped.

**Problem**: Length is not a clarity problem in itself, but the recurring meta-commentary and pre-emptive disclaimers (e.g., the dependency-chain summary near the top of the note that re-traces what subsequent sections will say) make the proof structure harder to follow. A reviewer must hold many parallel framings in mind while checking each step.

**Required**: Move the Failure modes, Allocator-state commitment, Coarsening discussion, and Dependency-chain summary into appendices or design notes; keep the main body to definitions, claim statements, and proofs. Group orthogonal L-invariant bullets in R0 Step 4. Replace the up-front Dependency-chain summary with brief in-place cross-references.

### Issue 5: R6c is not concretely exercised in the worked sketch

**ASN-0086, Worked Sketch**: Steps 1–4 demonstrate Nullify, re-emission, cross-document retraction, and the Observe hist/oper split, but no step shows R6c (RestorationByReemission) holding across multiple successive `→` steps.

**Problem**: R6c's content — that `a₁ ∉ A_K^{Σ_n}` for *every* Σ_n reachable from Σ_1 — is the operationally important property that distinguishes "retracted forever" from "retracted at the moment of retraction." Verifying it requires showing the property at a state two or three transitions past Σ_1. The current sketch verifies at Σ_2 (after re-emission) but stops there.

**Required**: Extend the sketch with one more step (Σ_3 → Σ_4 emitting some unrelated `L_K` tuple, or arrangement modification on `Σ_3.M`), and verify `a_1 ∉ A_K^{Σ_4}` directly from R6a-chained applications. This demonstrates both R6c and the R6c-Corollary (lifting to ⊑̂).

### Issue 6: Discipline-conditionality of R0a should be flagged earlier and more visibly

**ASN-0086, R0a section header and proof**: R0a, R0a-Cor1, R0a-Cor2, and Nullify's single-tuple-scope guarantee are all discipline-conditional on the sibling-frontier emission discipline. This is correctly flagged with `[Setup-free, discipline-conditional]` tags, but the substantive consequence — that the ASN's most novel structural claim about `dom(Σ.L)` is not a foundation consequence and would be violated by some substrate-primitive-permissible emissions — should be more visible.

**Problem**: A reader who picks up the Properties Introduced table sees `[Setup-free]` for R0a-Cor2 (in passing reference; the table marks it discipline-conditional) and may not immediately register that downstream operations (notably Nullify) inherit the conditionality. The Properties Introduced table flags this for Nullify, but the consequence-list in Issue 14 (e) of R6 advertises "all visible state-transforming relational-layer operations reduce to Emit_K" without restating the discipline scope, even though the closure relies on it.

**Required**: In the abstract opening paragraphs, name the discipline-conditionality of R0a as a primary structural commitment of the ASN, alongside the active/audit distinction. In R6 consequence (d), restate "for the relational layer as committed to the disciplined `Emit_K` primitive" rather than leaving it implicit.

### Issue 7: Definition of `Emit_K` should make discipline binding visible in the signature

**ASN-0086, Definition of Emit_K**: "Given input state Σ, a caller-supplied home document d ∈ dom(Σ.M), and finite endsets F, G ∈ Endset, Emit_K(Σ, d, F, G) deposits a fresh tuple under d at an address constructed by *R0 Step 2's sibling-frontier construction* applied at that d."

**Problem**: The definition states the construction is the disciplined one but does so in prose, after the signature. The "Why the construction is bound into the definition" paragraph clarifies the dependence, but the signature itself does not surface the discipline binding. Compared with `Emit_K`'s siblings (Observe, Nullify), the signature is silent on the structural commitment that distinguishes this operation from the broader substrate primitive.

**Required**: Either rename the operation `Emit_K^{disciplined}` (and reserve `Emit_K^{primitive}` for the broader admission), or add a postcondition line under the Definition: "Postcondition: a is constructed by R0 Step 2 — Case A (`a = d.0.s_L.1`) when home(d) is unused, Case B (`a = inc^i(b, 0)` for the least fresh i) otherwise."

## OUT_OF_SCOPE

### Topic 1: Slice-wise reformulation without Setup

**Why out of scope**: The Open Questions section already enumerates the slice-wise reformulation question and identifies which proof steps would need to be re-derived (R0's L14a-preservation, R4's disjointness statement, R5's inherited Setup-requirement). This is a substantial future ASN, not a fix to ASN-0086.

### Topic 2: Multi-arity link active subsets

**Why out of scope**: Defining `A_K^{(n),Σ}` for higher-arity links is named as an open question. The present ASN's restriction to standard triples is consistent with ASN-0043's conventions and matches downstream operations. A multi-arity extension is a successor ASN.

### Topic 3: Concurrency model and Observe atomicity

**Why out of scope**: Open question. The ASN gives a single-state-transition model; concurrency is a downstream concern.

### Topic 4: Ordering on Observe results

**Why out of scope**: Open question. Observe returns a set; whether to impose an ordering is a higher-layer policy decision.

### Topic 5: Substrate-level elevation of the sibling-frontier discipline

**Why out of scope**: The Open Questions section proposes two routes (tighten Emit_K postcondition; tighten substrate primitive). Either would discharge the discipline-conditionality of R0a and Nullify, but is a substrate redesign question, not a revision to the present ASN.

### Topic 6: Admitting deeper-sited link addresses (relaxing #E = 2)

**Why out of scope**: Open question. Aligning with Nelson's foundational admission of depth-N sub-links would require re-deriving R0a's sibling-stream invariant over a tree of allocators and re-deriving Nullify's single-tuple scope. A different ASN.

VERDICT: REVISE
