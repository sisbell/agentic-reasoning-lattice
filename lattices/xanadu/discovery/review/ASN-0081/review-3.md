# Review of ASN-0081

## REVISE

### Issue 1: Invariant proofs have uncovered case when L = ∅ and R = ∅
**ASN-0081, D-MIN-post**: "When L = ∅: p = min(V_S(d)) = [S, 1] by D-MIN, so ord(p) = [1]. By D-SEP(b), min Q₃ has ordinal ord(p) = [1], giving min Q₃ = [S, 1]."
**Problem**: D-SEP(b) requires R ≠ ∅, but the preconditions allow full subspace deletion (p = [S, 1], c = N), where L = ∅ and R = ∅ simultaneously. The "When L = ∅" case invokes D-SEP(b) without checking R ≠ ∅, making the proof invalid for this configuration. The same gap appears in D-CTG-post, which says "When L = ∅, Q₃ alone is contiguous. When R = ∅, L alone is contiguous. In all cases, L ∪ Q₃ is contiguous" — the double-empty case falls through both branches.
**Required**: Add a third case to both proofs. For D-MIN-post: "When L = ∅ and R = ∅: V_S(d') = L ∪ Q₃ = ∅, so D-MIN holds vacuously (no non-empty subspace to constrain)." For D-CTG-post: "When L = ∅ and R = ∅: L ∪ Q₃ = ∅, which is vacuously contiguous." The L = ∅ case of D-MIN-post should be restated as "When L = ∅ and R ≠ ∅" before invoking D-SEP(b).

### Issue 2: Missing S8-depth-post and S8a-post invariant preservation
**ASN-0081, Invariant Preservation**: "We now verify that the post-state satisfies the system invariants established in ASN-0036."
**Problem**: The section verifies S2-post, S3-post, D-CTG-post, and D-MIN-post, but omits S8-depth (FixedDepthVPositions) and S8a (VPositionWellFormedness). The D-SHIFT text informally argues S8a for Q₃ positions ("the shifted V-position satisfies S8a"), but this is buried in prose, not stated as a formal invariant preservation lemma. S8-depth is not addressed at all. Both are system invariants from ASN-0036 that the section claims to verify exhaustively.
**Required**: Add two lemmas:
- **S8-depth-post**: All positions in L retain depth 2 (unchanged). All positions in Q₃ have depth 2 (vpos(S, [x]) = [S, x]). By D-CS, other subspaces are unchanged. Hence S8-depth holds.
- **S8a-post**: Positions in L satisfy S8a by the pre-state invariant and D-L. Positions in Q₃: σ(v) = [S, vₘ − c] with S ≥ 1 (subspace identifier) and vₘ − c ≥ p₂ ≥ 1 (S8a on p), so all components are positive, zeros(σ(v)) = 0, and σ(v) > 0. By D-CS, other subspaces are unchanged. Hence S8a holds.

### Issue 3: Missing R = ∅ boundary worked example
**ASN-0081, Worked Example**: Two examples provided — main case and L = ∅ boundary case.
**Problem**: No R = ∅ case (tail deletion) and no L = ∅ ∧ R = ∅ case (full subspace deletion). Both are within the preconditions and exercise distinct proof branches. The full deletion case is particularly important because it's the case where Issue 1's proof gap manifests concretely: D-SEP(b) doesn't apply, Q₃ = ∅, and the post-state subspace is empty.
**Required**: Add at least one R = ∅ example. Suggested: same five-position arrangement, contraction at p = [1,4] with w = [0,2], giving L = {[1,1],[1,2],[1,3]}, X = {[1,4],[1,5]}, R = ∅, Q₃ = ∅, post-state = L. Also add the full deletion case: p = [1,1], w = [0,5], post-state = ∅. Verify D-DOM, D-CTG-post, D-MIN-post (vacuous), S8a-post, S8-depth-post against both.

## OUT_OF_SCOPE

### Topic 1: Generalization to ordinal depth > 2
**Why out of scope**: The ASN explicitly scopes to depth 2 via the scoping axiom and notes generalization as an open question. At depth > 2, the TumblerSub-based shift formula becomes a no-op (TumblerSub's divergence hits the first ordinal component, not the last), requiring different arithmetic — likely direct last-component manipulation rather than ordinal subtraction. This is genuinely new territory requiring new machinery, not a gap in the current depth-2 treatment.

### Topic 2: Link and endset behavior under contraction
**Why out of scope**: Contraction removes V-positions but preserves all I-addresses (D-I). Links reference I-addresses, so they survive structurally. Whether links become "unreachable" from a particular document's Vstream after contraction is a question for a future DELETE operation ASN, not for span algebra.

VERDICT: REVISE
