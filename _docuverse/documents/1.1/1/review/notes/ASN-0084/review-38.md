# Review of ASN-0084

I worked through the cut-sequence operations, the permutation lemmas, the run-decomposition transformation, and verified all three worked examples by direct computation. The ASN is rigorously constructed with detailed proofs, but a few items warrant revision.

## REVISE

### Issue 1: Necessity sketch uses a counterexample that violates ASN-0036 invariants

**ASN-0084, R-WP "Necessity sketch (R-PRE(iv) coverage)"**: The constructed pre-state has `V_S(d) = {[1, 1], [1, 2], [1, 4], [1, 5]}` with `[1, 3]` absent, which the ASN itself acknowledges: "[1, 3] is *absent* from V_S(d) — D-CTG and D-SEQ of ASN-0036 forbid such a gap in practice".

**Problem**: The counterexample violates D-CTG/D-SEQ, so it cannot arise in any well-formed pre-state. The sketch demonstrates a vacuous failure mode — one that ASN-0036 already rules out independently of R-PRE(iv). A reader cannot tell from this sketch what R-PRE(iv) is *actually* guarding against in well-formed states.

**Required**: Replace with a natural counterexample where the pre-state satisfies all ASN-0036 invariants. For example: `V_S(d) = {[1, 1], ..., [1, 5]}` (well-formed) with cut sequence `C = ([1, 2], [1, 4], [1, 100])`. Here R-PRE(iv) fails because positions `[1, 6], ..., [1, 99]` in the affected range are not in V_S(d). Then R-P1 (j ≥ 1) references undefined positions like `M(d)([1, 6])`. This exhibits R-PRE(iv) as a constraint on the cut sequence relative to V_S(d) — specifically bounding `c_{n−1} ≤ [S, N+1]` — rather than as a redundant restatement of D-CTG.

### Issue 2: Non-S subspace handling is fragmented across the ASN

**ASN-0084, multiple locations**: The treatment of positions with `subspace(v) ≠ S` is spread across:
- The "non-S" branch in the R-PPERM/R-SPERM piecewise definitions
- R-FRAME-P(a) and R-FRAME-S(a) ("For v ∈ dom(M(d)) with subspace(v) ≠ S: M'(d)(v) = M(d)(v)")
- The "Scope note on non-S runs" paragraph inside R-BLK
- Multiple discharge clauses in R-COMM, R-DISP, R-WP that re-derive "π is the identity off V_S(d)" or "non-S runs pass through R-BLK unchanged"

**Problem**: A reader must reassemble the global picture from scattered fragments. Each individual clause is correct, but the redundancy obscures the simple structural fact: REARRANGE_C is the identity on `dom(M(d)) \ V_S(d)`, so every invariant analysis for non-S positions reduces to the pre-state.

**Required**: Consolidate into a dedicated subsection — e.g., "Non-S subspace invariance" — that proves once that (i) π restricted to non-S is the identity, (ii) non-S correspondence runs are carried verbatim into B', (iii) every ASN-0036 invariant on non-S positions is preserved trivially. Subsequent sections then cite this consolidated result rather than re-deriving in each lemma.

### Issue 3: R-BLK Phase 1 "later cut falls in already-split run" argument leaves the no-skip case implicit

**ASN-0084, R-BLK Phase 1**: "When a later cut falls in a run already split by an earlier (strictly smaller) cut, it necessarily falls in the right-hand piece."

**Problem**: The argument shows `c_j` is *not* in the left piece, but only addresses cases where `c_j` falls inside `V(b_k)` at all. The conclusion "must therefore lie in the right piece's V-extent" assumes `c_j ∈ V(b_k)` was already established for the post-split partition. But after step `i`, `b_k` no longer exists — it has been replaced by left and right pieces. The argument should say: *if* `c_j` is interior to *some* run in the post-step-i partition, then since `c_j > c_i` and the left piece's extent ends at `ord(c_i)`, that run must be the right piece (or some other unsplit run outside the original `V(b_k)`).

**Required**: Tighten the prose to either (a) state that `c_j` may fall outside the original `V(b_k)` entirely (and is then processed against a different run by the same Phase 1 logic), or (b) clarify that the claim is conditional: *given* that `c_j ∈ V(b_k)` originally, after `c_i`'s split `c_j` is in the right piece. The current phrasing reads as if it covers all cases.

### Issue 4: "v_1 < v_1" phrasing in step (b) of the canonical decomposition

**ASN-0084, canonical decomposition step (b), case "Exactly one of k₁, k₂ is zero"**: "The equation v₁ = v₁ + k₂ would then yield v₁ < v₁, contradicting T1 irreflexivity."

**Problem**: The direct substitution `v₁ + k₂ = v₁` into TS4's conclusion `v₁ + k₂ > v₁` yields `v₁ > v₁`, not `v₁ < v₁`. While both are equivalent under the strict-order companion definitions, the phrasing as written requires the reader to reconstruct the reflection. Minor but inelegant.

**Required**: Write "yields `v₁ > v₁`" (matching the direct substitution) or note explicitly that the two strict-order forms are interconvertible via the `>`/`<` companion definitions.

### Issue 5: Width-bound dependence in R-PRE consequences not explicit at point of use

**ASN-0084, Consequences of R-PRE, "Middle region non-empty"**: The derivation that `w_μ ≥ 1` for n = 4 relies on R-PRE(iv) (placing c₁ in V_S(d)) and CS2/CS3/CS4. The conclusion is cited later as "by Consequences of R-PRE, n = 4 case" (in R-SWP, R-DISP, R-BLK).

**Problem**: The R-PRE clause list contains five conjuncts; clause (v) only states `w_α ≥ 1 ∧ w_β ≥ 1` explicitly. The bound `w_μ ≥ 1` for 4-cut sequences is a separate derived consequence. A reader checking R-SWP's precondition discharge has to know to look at the "Consequences of R-PRE" subsection rather than R-PRE itself.

**Required**: Either add `w_μ ≥ 1` (for n = 4) as an explicit clause in R-PRE alongside clause (v) for uniform discharge, or add a forward-reference from R-PRE to the consequence subsection so it's visible at the precondition checklist.

## OUT_OF_SCOPE

### Topic 1: Composition of REARRANGE_C operations
**Why out of scope**: The ASN acknowledges this in its open questions. Whether `REARRANGE_{C2} ∘ REARRANGE_{C1}` is expressible as a single REARRANGE belongs to a future ASN on the algebra of editing operations.

### Topic 2: Invertibility of REARRANGE_C
**Why out of scope**: Whether for each cut sequence C there exists C' such that `REARRANGE_{C'} ∘ REARRANGE_C` is the identity is a structural property of the permutation class that this ASN does not address. Belongs to a future ASN.

### Topic 3: Higher depths (m_1 > 2)
**Why out of scope**: The ASN explicitly restricts to depth-2 to use the singleton-tumbler-with-ℕ⁺ identification. Generalization to higher depths would require multi-component ordinal arithmetic and is a natural future ASN.

### Topic 4: Cross-subspace rearrangement (link subspace, S ≠ 1)
**Why out of scope**: The text-subspace restriction is deliberate; the link subspace has different invariants (sparse with tombstones, exempt from D-CTG) and requires its own analysis.

### Topic 5: Effect on link endsets under REARRANGE_C
**Why out of scope**: Links are not yet defined in ASN-0036. When introduced, their behavior under arrangement rearrangements (do link endsets follow content via S5-style identity preservation?) will require its own treatment.

### Topic 6: Conditions on cut points relative to canonical run boundaries
**Why out of scope**: The ASN's open question asks whether arbitrary cut positions are valid or whether cuts must align with run boundaries. This bears on optimization analysis, not on the operation's correctness.

VERDICT: REVISE
