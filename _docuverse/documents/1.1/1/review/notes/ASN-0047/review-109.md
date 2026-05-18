# Review of ASN-0047

## REVISE

### Issue 1: NodeRegistryBootstrap "Scope note" is defensive prose

**ASN-0047, NodeRegistryBootstrap axiom**: The axiom statement is one sentence ("At the initial state Σ₀, n₀ is committed to the node-allocation protocol's tracked domain"), followed by a multi-paragraph "*Scope note (external commitment, not state component)*" subsection that explains why the registry isn't in Σ, references future work, and rehearses how K.δ case (ii) k=2 uses it.

**Problem**: This matches the "sub-paragraphs labeled 'Scope', 'Object-level content', 'Protocol rationale'" anti-pattern flagged in the review prompt. The scope note is meta-prose explaining *why the axiom is needed* and *how it relates to other constructs* rather than what it says. Each declarative sentence in the note ("is *not* a component", "is an *external* protocol-layer construct", "Future work that lifts the registry...") defends against a possible objection rather than advancing the axiom's content.

**Required**: Trim the scope note to one sentence at most ("the node-allocation registry is external to Σ; n₀ enters at Σ₀ rather than via prior K.δ"). Move the "Future work" pointer to Open Questions if it isn't already there. Delete the rehearsal of K.δ case (ii) k=2's use of the axiom — that belongs at the discharge site, not at the axiom site.

### Issue 2: K.μ⁻ "Per-subspace suffix pattern" precondition is redundant with derived lemma

**ASN-0047, "K.μ⁻ amendment (PerSubspaceScope)" and "K.μ⁻ admissible contraction shape" sections**: The amendment states "For each subspace S ∈ {s_C, s_L} with V_S(d) ≠ ∅, there exists 0 ≤ n'_S ≤ n_S such that V_S(d') = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n'_S}" as a precondition. The "K.μ⁻ admissible contraction shape" lemma then derives the same suffix form from D-CTG★ + D-MIN★ + D-SEQ★ at the post-state.

**Problem**: A property cannot be both a precondition (caller must establish) and a derived consequence (automatic from other postconditions). Either D-CTG★/D-MIN★/D-SEQ★ at the post-state imply the suffix pattern (in which case the precondition is redundant), or they don't (in which case the lemma is missing premises).

**Required**: Pick one. Drop the per-subspace suffix pattern as a stated precondition and present it as a derived consequence of D-CTG★ + D-MIN★ + D-SEQ★ at the post-state via the lemma. The post-state invariants are the precondition; the suffix shape is the consequence.

### Issue 3: A_v(d) case-split duplicated across sections

**ASN-0047, "Allocator hierarchy under documents" and "K.δ case (ii) discharge and parent-allocator activation"**: Both sections contain a full case (a)/(b) discussion of A_v(d)'s parent allocator (original document → A_doc(parent(d)); version → A_v(predecessor)), with the same T10a.6 mutual-exclusion argument restated in each.

**Problem**: Two paragraphs in different sections say substantively the same thing. Matches the "two paragraphs in different sections defer to the same downstream location" / "say the same thing in different words" pattern.

**Required**: State the case-split once at the Sub-allocator-names definition (where A_v(d) is introduced), and have the K.δ case (ii) k=1 discharge cite that definition rather than restate the case-split. The discharge section needs only "by the Sub-allocator-names case-split, the spawnPt obligation is discharged against the parent allocator T10a.6 identifies".

### Issue 4: Sub-case labels (i)(ii)(iii) collide with K.δ top-level case labels

**ASN-0047, "K.δ case (ii) discharge and parent-allocator activation", k = 2 paragraph**: "*(i) t is an account.* ... *(ii) t is a node, with prior K.δ event.* ... *(iii) Bootstrap special case t = n₀, no prior K.δ.*"

**Problem**: K.δ has top-level case (i) (IsNode) and case (ii) (¬IsNode), with case (ii) further split into k = 0/1/2. The k = 2 paragraph then introduces sub-sub-cases also labeled (i)/(ii)/(iii). At "K.δ case (ii) k=2 sub-case (iii)" the reader must hold three layers of overloaded numbering simultaneously.

**Required**: Use different labels for the sub-sub-cases (e.g., "sub-case A: t is an account", "sub-case B: t is a non-bootstrap node", "sub-case C: t = n₀ bootstrap"). The K.δ top-level cases retain (i)/(ii); k-sub-cases retain k = 0/1/2; the t-identity sub-sub-cases get distinct labels.

### Issue 5: Fork example Step 3 mischaracterises S8-depth

**ASN-0047, "Worked example: fork with subsequent insertion", Step 3 "Reorder d₂'s arrangement"**: "Both target V-positions satisfy S8a (all components strictly positive) and S8-depth (uniform depth 2, shared first component 1)."

**Problem**: S8-depth (ASN-0036) requires uniform depth within each subspace; it says nothing about the first component value. The "shared first component 1" is the subspace-identity fact (subspace(v) = s_C = 1), not part of S8-depth. The parenthetical conflates two distinct properties.

**Required**: Either drop "shared first component 1" from the S8-depth clause and mention subspace identity separately, or revise to "S8-depth (uniform depth 2 within subspace s_C), with subspace(v) = 1 for both positions".

### Issue 6: K.μ~ partial-suffix admissibility "iff" claim overstated under sharing

**ASN-0047, "Decomposition of K.μ~", partial-suffix expansion paragraph**: "*Partial-suffix expansion* at `n'_{s_C} = k₀ − 1` for some `k₀ ≥ 1` ... This expansion is admissible iff π fixes every content-subspace position below the cut..."

**Problem**: The argument assumes the K.μ⁺ value at any below-cut position is uniquely determined by M(d)'s value there, so π(v) ≠ v below the cut forces an overwrite contradiction. But S5 (UnrestrictedSharing, ASN-0036) permits M(d)(v) = M(d)(v') for distinct V-positions v ≠ v' (transclusion). When such coincidences exist, π could permute below-cut positions among themselves whenever the permuted positions share the same M(d) value, with no K.μ⁺ overwrite required. The "iff" backward direction (admissible → π fixes below cut) therefore fails on arrangements with coincidental sharing among below-cut positions, which is the typical case for documents with transclusions of the same source content.

**Required**: Either weaken to "if" (admissible ⟸ π fixes below cut, sufficiency only), with a separate "necessity holds for arrangements injective on `dom_C(M(d))`" clause; or restate the iff as "iff π preserves below-cut M(d)-values pointwise" — `(A v < [s_C, 1, ..., 1, k₀] : M(d)(π(v)) = M(d)(v))` — which holds vacuously when π fixes below-cut and captures the coincidence case.

VERDICT: REVISE
