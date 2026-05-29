# Review of ASN-0045

## REVISE

### Issue 1: Per-predicate Depends lists cite premises that do no work in the predicate's own postcondition

**ASN-0045, Properties Introduced (Node, Document, Element)**: e.g. Node — "*Depends.* T0 ..., T4 (T4-valid; **axiom zeros(t) ≤ 3**), T4c (level naming)."

**Problem**: Each predicate's standalone postcondition is the definitional biconditional `Node(t) ⟺ T4-valid(t) ∧ zeros(t) = 0`. Proving it requires only the definition of `Node`, `T4-valid` (T4), `zeros` (T4/TA5a), and T0's carrier. The bound `zeros(t) ≤ 3` is never invoked — it is exhausted entirely inside Partition's at-least-one step. Listing it as a Node/Document/Element dependency is extraneous, and the project's per-step citation convention (followed obsessively in the foundation) treats such over-citation as imprecise. Likewise, T4c does no proof work in the Node/Document/Element biconditionals — the ASN's own Well-Definedness section states "T4c's injectivity ... does no work here." If T4c is cited only to justify the *name* of the predicate, that should be stated as such, not folded in as a proof dependency.

**Required**: Strip `zeros(t) ≤ 3` from the Node/Account/Document/Element Depends lists (it belongs solely to Partition). For T4c on Node/Document/Element, either remove it or annotate explicitly that it justifies the level *label* only, not the postcondition.

### Issue 2: `T4-valid(t)` used as a named predicate the foundation never defines

**ASN-0045, Hierarchy Level Definitions**: "For any tumbler t, T4-valid(t) (T4, ASN-0034) means t parses as a well-formed address."

**Problem**: Foundation T4 is an axiom characterizing valid address tumblers; it does not introduce a one-place predicate symbol `T4-valid`. The ASN coins this notation and leans on it in every definition and in Partition's antecedent. This is a reasonable reading of T4, but it is a new symbol bound here without an explicit definitional line tying it to T4's four clauses (zeros ≤ 3, no adjacent zeros, t₁ ≠ 0, t_{#t} ≠ 0).

**Required**: Add a one-line definition `T4-valid(t) ≡ [the four T4 clauses]` so the predicate the entire ASN quantifies over is pinned down, rather than introduced parenthetically.

## OUT_OF_SCOPE

None. The ASN stays within address-classification vocabulary; it does not stray into the excluded operational topics.

VERDICT: REVISE
