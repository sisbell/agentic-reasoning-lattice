# Review of ASN-0036

I checked each proof against its preconditions, cases, and invariant conjuncts. The mathematical core (S0–S8, D-CTG, D-CTG-depth, D-SEQ, the two insertion predicates) is rigorous: the S8 partition proof handles empty `dom(M(d))`, the within-subspace lemma covers both `j < m` and `j = m` (and the `m = 2` collapse), and the across-subspace case correctly invokes T5 + T10 on the length-1 prefixes. The D-CTG-depth and D-SEQ contradiction arguments are sound. ASN-0034 is the foundation, so all `(ASN-0034)` citations are permitted. I found no hard errors. The items below are precision/anti-bloat findings the review classifier asks be flagged at source.

## REVISE

### Issue 1: Numbering gaps break self-containedness
**ASN-0036, Properties table and §Content identity / §Structural attribution**: the property sequence runs `S5` → `S7a` with no `S6`, and the S7 family is `S7a, S7b, S7d` with no `S7c`.
**Problem**: A self-contained spec that jumps `S5, S7a` and lists `S7a, S7b, S7d` reads as referencing removed or external content — a reader cannot tell whether they missed a dependency. The standard requires each ASN stand alone; orphaned numbering undermines that.
**Required**: Either renumber contiguously, or add a one-line note that `S6`/`S7c` were retired in revision so the gap is intentional.

### Issue 2: S5 treats transition invariants as vacuously satisfiable by an isolated state
**ASN-0036, §Sharing, S5 proof**: "S0 and S1 quantify over transitions; `Σ_N` is exhibited with no incident transition, so both hold vacuously."
**Problem**: S0 and S1 are *transition* invariants (`Σ → Σ'`), not state predicates — "the state `Σ_N` satisfies S0" is a category mismatch. The vacuity reading is technically defensible but slides past the fact that, in any real system, `Σ_N` would have outgoing transitions that S0/S1 do still constrain. The existence claim is about an *achievable state* exhibiting the sharing multiplicity; S0/S1 impose nothing on a standalone state, and that is the precise statement.
**Required**: Replace the "hold vacuously" phrasing with an explicit statement that S0/S1 constrain transitions only, so the construction need only verify the genuine state predicates S2/S3 plus the multiplicity count — S0/S1 place no condition on an isolated state.

### Issue 3: Editorializing meta-prose in the S8 proof and worked example
**ASN-0036, §Singleton span partition, "Uniqueness within a subspace"**: "We show `w ∉ [v, shift(v, 1))` via a clean lemma that abstracts away from the specific pair `(v, w)`."
**ASN-0036, §Worked example**: "Two further cases — an ill-formed state and a higher depth — round out the picture."
**Problem**: "a clean lemma," "abstracts away," and "round out the picture" describe the prose rather than advance the argument — exactly the accreted meta-commentary the anti-bloat classifier targets. They are skippable by the precise reader.
**Required**: State the lemma directly ("Lemma:") and drop the self-description; replace the transition sentence with the cases themselves (the concrete examples that follow are legitimate and need no framing).

## OUT_OF_SCOPE

### Topic 1: Operation-level preservation of D-CTG / D-MIN / S2
The note repeatedly defers (correctly) to a future operations ASN the proof that INSERT/DELETE/COPY/REARRANGE preserve contiguity, and the open questions name this. This is new territory, not a defect here.

### Topic 2: Subspace-alignment invariant (`subspace(v) = v₁` matching the I-address element field)
S3 constrains only `ran(M(d)) ⊆ dom(C)`; the alignment between a V-position's subspace identifier and the subspace of the I-address it maps to is explicitly an operations-layer obligation per the open questions. Belongs in a later ASN.

VERDICT: REVISE
