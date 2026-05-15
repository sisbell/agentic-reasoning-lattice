# Review of ASN-0082

## REVISE

### Issue 1: D-SEQ-post forward citation violates stated lemma ordering
**ASN-0082, Invariant preservation section**: "The lemmas are ordered so that each cites only earlier ones: typing invariants (S8-depth-post, S8a-post) first, then the contiguity triple (D-CTG-post, D-MIN-post, D-SEQ-post), then finiteness (S8-fin-post)..."

But D-SEQ-post says: "The set is finite by S8-fin-post (proved below; D-SEQ-post does not depend on the value of n delivered by S8-fin-post, only on finiteness, so the forward citation is non-circular)."

**Problem**: This contradicts the stated ordering principle. The defensive parenthetical doesn't resolve the structural issue — either the ordering claim is wrong, or the citation should be removed. The proof itself already provides a direct cardinality argument ("The pre-state has N positions; the contraction removes c positions ... so |L ∪ Q₃| = N − c") that establishes finiteness without invoking S8-fin-post.

**Required**: Remove the forward citation to S8-fin-post and rely solely on the inline cardinality argument, OR reorder the lemmas to place S8-fin-post before D-SEQ-post (and update the introductory paragraph accordingly).

### Issue 2: I3-VD proof citation incomplete for non-S subspaces
**ASN-0082, I3-VD lemma**: "For any subspace S' ≠ S: by I3-CX, the positions in dom(M'(d)) with subspace S' are exactly the positions in dom(M(d)) with subspace S', on which S8-depth holds by hypothesis."

**Problem**: I3-CX provides only one direction of the equality (dom(M'(d)) ∩ subspace S' ⊆ dom(M(d))). The reverse direction — that every position in dom(M(d)) with subspace ≠ S is in dom(M'(d)) — comes from I3-X. The "exactly" wording requires both citations.

**Required**: Cite both I3-X and I3-CX. Replace "by I3-CX" with "by I3-X and I3-CX" (or equivalent phrasing establishing the biconditional).

### Issue 3: Statement Registry definition of ordinal-level conflates two conditions
**ASN-0082, Statement Registry**: "ordinal-level | definition | A span σ = (s, ℓ) is ordinal-level when actionPoint(ℓ) = #s = #ℓ | introduced (local)"

But the body's definition (introducing I3-S) says: "We call a span *ordinal-level* when its width acts purely at the deepest component: actionPoint(ℓ) = m."

**Problem**: The body's definition is `actionPoint(ℓ) = m`, where level-uniformity (#s = #ℓ = m) is a separate condition stated as the context. The registry packs both into a single condition, which is technically equivalent under level-uniformity but misrepresents the definition's structure.

**Required**: Update the registry entry to "A span σ is ordinal-level when actionPoint(ℓ) = #ℓ" (with level-uniformity called out separately when invoked), matching the body.

## OUT_OF_SCOPE

### Topic 1: Straddling spans (start in L, reach in R)
**Why out of scope**: I3-S restricts to spans with s ≥ p (entirely shifted), and D-S restricts to spans with s ∈ R (entirely in the right region). Spans straddling the contraction boundary or insertion point require a different decomposition argument. This is span-algebra extension territory, properly belonging in a future ASN that composes span-splitting (ASN-0053 S4/S5) with the displacement properties established here.

### Topic 2: Contraction at depth #p > 2
**Why out of scope**: The depth scoping axiom (#p = 2) is justified by the mathematical necessity argument from TA4 (zero-prefix requirement collides with S8a's componentwise positivity at deeper levels). The Open Question section already names this as a separate problem requiring different lemma machinery.

### Topic 3: Link-subspace contraction (tombstone discipline)
**Why out of scope**: The subspace scoping axiom (S = 1) is justified by the foundation's text-only contiguity invariants. Link-subspace mutation uses tombstoning rather than gap-closing shift — a different operation requiring its own ASN.

### Topic 4: Full INSERT/DELETE operations (content placement, link cleanup)
**Why out of scope**: I3 is explicitly scoped to the arrangement-shift sub-operation; D-SHIFT is explicitly scoped to the V-arrangement transformation. Full INSERT (content allocation at gap positions, with weakened content-store frame matching S0) and full DELETE (with link-endpoint cleanup) compose this ASN with future content-allocation and link-management ASNs.

VERDICT: REVISE
