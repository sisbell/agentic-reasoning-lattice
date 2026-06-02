# Review of ASN-0047

## REVISE

### Issue 1: The fork k=0/k=1 allocation discrimination is stated three times
**ASN-0047, J4 intro paragraph / Definition (Fork) / step (i)**: The same content — that fork allocation is uniform across versions (`inc(d_src, 1)` for the first version, `inc(prev_version, 0)` for subsequent), and that the operand-tracking rule sets `d_op = d_src` (k=1) vs `d_op = prev_version` (k=0) — is restated in three places:

- J4 intro: *"Fork is version creation on d_src's version chain A_v(d_src), with K.δ address allocation uniform across first and subsequent versions: the first version is d_new = inc(d_src, 1)... and each subsequent version is d_new = inc(prev_version, 0)..."*
- Definition (Fork): *"the k = 1 sub-case fires when A_v(d_src) has no prior emission... with d_op = d_src; the k = 0 sub-case fires when A_v(d_src) already has a frontier... with d_op = prev_version..."*
- step (i): *"k = 1 producing the first version d_new = inc(d_src, 1)... or k = 0 producing the next version d_new = inc(prev_version, 0)..."*

**Problem**: Two paragraphs in the same document saying the same thing in different words — the anti-bloat pattern explicitly flagged for this note. The discrimination is genuinely load-bearing exactly once. The triplication compounds the maintenance risk: a future edit to the discriminator (e.g., the `d_op ∈ dom(A_v(d_src))` checkable condition) must be propagated to three sites or they drift.

**Required**: State the allocation discipline and operand-tracking rule once (Definition (Fork) is the natural home, since it already labels the operand-tracking rule "the sole statement of the rule"), and have the J4 intro and step (i) invoke it by reference rather than re-deriving the k-split.

### Issue 2: K.μ⁻ precondition `dom(M(d)) ≠ ∅` is implied by the strict-contraction clause
**ASN-0047, K.μ⁻ precondition**: The precondition lists both `dom(M(d)) ≠ ∅` ("required for the effect clause") and, under the constructive specification, "with at least one S admitting strict contraction `n'_S < n_S`."

**Problem**: If some subspace S has `n'_S < n_S`, then `n_S ≥ 1`, so `V_S(d) ≠ ∅`, so `dom(M(d)) ≠ ∅`. The first conjunct is entailed by the strict-contraction constraint, so it is dead weight in the precondition list.

**Required**: Drop the standalone `dom(M(d)) ≠ ∅` conjunct, or fold its justification into the strict-contraction note ("a fortiori `dom(M(d)) ≠ ∅`, discharging the effect clause's satisfiability").

### Issue 3: Notation-section asserts a result it cannot yet support
**ASN-0047, Notation, *Subspace-position correspondence***: *"For v ∈ dom(M(d)) with M(d)(v) = a, subspace(v) = subspace_I(a); see S3★ + L0 + S3★-aux."*

**Problem**: This correspondence is a *derived consequence* requiring three results (S3★, L0, S3★-aux) all defined many sections downstream; the Notation section presents it as established notation alongside genuine projection definitions. A reader building the notation table cannot verify the claim at this point — it is a forward-pointer dressed as a definition. (It is correctly re-derived at S3★, which is where it belongs.)

**Required**: Either demote the entry to a pure pointer ("the correspondence `subspace(v) = subspace_I(a)` is established at S3★") without asserting it as notation, or remove it from the Notation table and keep only the S3★-site derivation.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal with renumbering
The ASN's K.μ⁻ contracts the link subspace by suffix removal only, and the document itself flags (Open Question) that the implementation's interior `DELETEVSPAN` compacts-and-renumbers surviving V-positions — an operation not modeled here.
**Why out of scope**: This is a named-operation / renumbering-aware contraction question, which the Scope section excludes (operations) and the ASN itself parks as an Open Question. Not a defect in the elementary K.μ⁻.

### Topic 2: Forked-arrangement / source-arrangement relationship
J4 bounds only `ran(M'(d_new)) ⊆ ran(M(d_op)|_{V_{s_C}(d_op)})`, leaving open whether the forked arrangement must structurally mirror the source (e.g., preserve duplicate-position multiplicity under S5 transclusion) or may collapse it.
**Why out of scope**: Explicitly the first Open Question ("must it be identical, or may it be a proper subset?"). New territory, not an error in J4's range bound.

VERDICT: REVISE
