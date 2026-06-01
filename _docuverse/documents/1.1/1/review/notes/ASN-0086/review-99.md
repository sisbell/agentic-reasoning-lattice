# Review of ASN-0086

## REVISE

### Issue 1: Antichain/contiguity lemmas proven for `→*`-reachable states, consumed at `↝`-reachable states
**ASN-0086, R0a / R0a-Cor1 / R0a-Cor2**: "`(A Σ : Σ reachable from Σ_init :: ...)`" and the Reachability definition: "`Σ →* Σ'` ... is the reflexive-transitive closure of `→`."

**Problem**: R0a, R0a-Cor1, R0a-Cor2 are quantified over states reachable from `Σ_init` under `→*` (the dom-extending K-op closure). But R7a operates on the *categorical* relation `↝` (higher-layer transitions), and its discharge (4) repeatedly cites "R0a-Cor1 at Σ" and "R0a-Cor1 at Σ'" where `Σ'` is `↝`-reachable, not necessarily `→*`-reachable. The note deliberately distinguishes `→` from `↝`, so this is not a notational quibble. The bridge is applied *inconsistently*: discharge (4)(i) carefully re-derives the contiguity content at `Σ'` from conformance clause (b) ("a consequence of conformance, not... a separately imposed step-local invariant"), but Cases A/B and the "R0a-Cor1 at Σ" citations then invoke the lemma by bare reference, as if its `→*`-quantifier covered `Σ`/`Σ'`. The same gap recurs in Nullify's "Single-tuple scope, absolute under R0a" (applied at a layer-operation post-state whose pre-state may be `↝`-reachable) and in WP Case 1's R0a appeal.

**Required**: Make the quantifier and the bridge uniform. Either (a) restate R0a/Cor1/Cor2 to hold at every *substrate-conforming* state (so clause-(b) conformance, not `→*`-reachability, is the stated hypothesis), or (b) route every off-`→*` application through clause (b) explicitly at each site, rather than citing "R0a-Cor1 at Σ'" as though the existing quantifier reached it.

### Issue 2: WP Case 1's P2-exclusion paragraph explains rather than advances
**ASN-0086, WP Case 1**: "The wp above lists only P0 and P1 ... Its exclusion from the wp is therefore principled — P2 is not a guard of the wp's kind — rather than a silent demotion."

**Problem**: This is defensive meta-prose anticipating a reviewer asking "why isn't P2 in the wp?" — it justifies an omission instead of computing anything. The substantive content (P2 is a scope condition, not an executing precondition) is already stated once in the Definition of Nullify; restating it as a multi-sentence rebuttal in the wp slot is the flagged pattern (prose the reader must skip to follow the wp). The trailing sentence "The wp likewise does *not* include any conjunct on whether the internal emitter `b` is itself nullified" compounds it — enumerating what the wp omits rather than what it asserts.

**Required**: Reduce to at most one clause noting the wp ranges over executing preconditions; drop the "principled... rather than a silent demotion" defense and the does-not-include sentence.

### Issue 3: Reduction-to-`Emit_K` claim stated three times
**ASN-0086, intro / Definition — relational layer / reduction Corollary**: intro: "the relational layer is then *defined* to commit `Emit_K` as its sole state-affecting K.λ-emission, from which the reduction... follows (Corollary, below)"; Definition: "The layer commits to `Emit_K`... as its sole state-affecting class-(iii) emission"; Corollary: "the layer issues `Emit_K` only when..."

**Problem**: The same commitment ("`Emit_K` is the sole state-affecting emission") is asserted in the introduction (with a forward pointer to the Corollary), restated in the layer Definition, and restated again as the Corollary's premise. Two of the three are redundant; the intro's forward pointer to a Corollary that merely re-states the definition is the "defer to the same downstream location" pattern.

**Required**: State the commitment once in the Definition; let the intro reference the operation set without pre-announcing the reduction, and let the Corollary cite the Definition rather than re-paraphrasing it.

## OUT_OF_SCOPE

### Topic 1: `L_K`–`Σ.M` visibility invariants
The first Open Question (invariants relating `L_K` to arrangements when predicates depend on whether endset content is currently visible in a document) is correctly deferred — under M2 every arrangement is empty here, so this is genuinely a future ASN once arrangements become non-trivial.

### Topic 2: Higher-arity typed relations `L_K^{(n)}`
The note explicitly restricts to standard triples and flags multi-arity projection as an open question. Appropriately future territory, not a defect here.

VERDICT: REVISE
