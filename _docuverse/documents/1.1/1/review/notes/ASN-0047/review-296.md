# Review of ASN-0047

## REVISE

### Issue 1: GlobalUniqueness invoked system-wide, but the system is a multi-rooted node forest

**ASN-0047, *Derived distinctness corollaries* and *CrossDocEntityDisjoint***: "Same-parent cross-chain pairs ... by plain GlobalUniqueness (ASN-0034) across distinct K.δ allocation events"; and elsewhere FrontierEquivalence's reverse direction: "By GlobalUniqueness (ASN-0034 ...), the address `inc(t, 0)` can be produced by exactly one allocator's tracked chain."

**Problem**: ASN-0034's GlobalUniqueness is proved by "Strong induction on allocator tree depth ... Base (d = 0): **sole root allocator**." Its precondition is a *single-rooted* T10a tree. But NodeBaptism admits repeated baptism of distinct nodes (the ASN itself constructs `N₁ = [1,2] ≼ [1,2,3] = N₂` in CrossNodeAccountBase, and NodeLineage permits any `e` with `n₀ ≼ e`). Nodes are *not* `inc`-outputs of `n₀` — they enter E only via NodeBaptism — so the `inc`-allocator structure is a *forest* with one root per baptised node, not a single tree. GlobalUniqueness as stated does not apply system-wide. The ASN reconciles *cross-node* distinctness through T10/CrossNodeAccountBase, but its *within-node* distinctness obligations are discharged by "plain GlobalUniqueness" without establishing that each baptised node anchors an independent GU-conforming subtree with that node as its sole root.

**Required**: State explicitly that each baptised node `N` roots an independent T10a/GlobalUniqueness-conforming allocator subtree (with `N` as the GU base-case root), that every "plain GlobalUniqueness" invocation is scoped to one such subtree, and that all cross-node distinctness rests on T10 (as CrossDocEntityDisjoint already does). Without this reduction, the GU citations are unlicensed in any reachable multi-node state.

### Issue 2: Chained deferrals to "the uniform shape-package discharge above"

**ASN-0047, Class (a) verification matrix and following prose**: The K.μ~ cells for `S8a/S8-depth/S8-fin`, `S8★`, `D-CTG★/D-MIN★`, and `D-SEQ★` each read "see *…* prose below"; each of those prose paragraphs then defers again to "the uniform shape-package discharge above" (the *K.μ~ discharge for the arrangement-shape package* paragraph).

**Problem**: This is a two-hop deferral chain (matrix cell → per-invariant prose → uniform-discharge paragraph) in which four distinct paragraphs all funnel to one location. The intermediate per-invariant prose adds a navigation hop without adding argument — the reader must skip past it to reach the substantive paragraph. This is the forward-reference accretion the note's anti-bloat classifier flags ("multiple paragraphs in different sections defer to the same downstream location").

**Required**: Collapse the chain — either have the four matrix cells point directly at the uniform-discharge paragraph, or fold the per-invariant K.μ~ remarks into that single paragraph, so there is one deferral hop, not two.

### Issue 3: K.δ case (ii) spawn-admissibility duplicated across two sections

**ASN-0047, K.δ definition (case ii) and *K.δ case (ii) discharge and parent-allocator activation***: The inline K.δ box states the per-sub-case requirements (k=0/1/2, spawn parameter `k' ∈ {1,2}`, zero-count side conditions) and then forward-points: "Discharge of the parent-allocator and spawn-admissibility conditions: §*K.δ case (ii) discharge…*." The dedicated section then re-states the same k=0/1/2 admissibility (e.g. "spawn parameter `k' = 2 ∈ {1, 2}` is admissible; K.δ's case-level zeros bound `zeros(t) ≤ 1` discharges T10a's zero-count side condition").

**Problem**: The spawn-admissibility content (the `k' ∈ {1,2}` membership and the zero-count discharge) appears in both the inline definition and the dedicated section. This is relocated/duplicated content rather than a single authoritative statement — the pattern the anti-bloat directive names ("a paragraph looks like a prior finding's content relocated rather than removed").

**Required**: Keep the admissibility *requirements* in the K.δ box and the *parent-allocator identification* in the dedicated section, with no restatement of the `k'`-membership/zero-count discharge in both. State each fact once.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link-arrangement contraction
K.μ⁻ models only suffix removal; interior withdrawal with compaction (the implementation's `DELETEVSPAN`) is not modelled. The ASN already lists this as an Open Question — it is future territory, not an error here.

### Topic 2: Type-only / one-sided links (empty endsets)
Whether K.λ should require `e₁ ∪ e₂ ≠ ∅` is raised in the Open Questions and depends on link semantics not specified in this transition model. Belongs to a future link-semantics ASN.

VERDICT: REVISE
