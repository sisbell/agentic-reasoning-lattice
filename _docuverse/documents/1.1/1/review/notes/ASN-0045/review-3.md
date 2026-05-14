# Review of ASN-0045

## REVISE

### Issue 1: E is undefined
**ASN-0045, Naming Convention / Hierarchy Level Definitions**: "names those levels as predicates over E for downstream use" and labels E.node, E.account, E.document, E.element, E.partition.
**Problem**: E is never defined. The carrier of tumblers in the foundation is T (T0). Worse, T4b already uses E as a partial-function symbol for the element-field projection (`E : T ⇀ T`, `t.E₁`). Using E both as a namespace prefix here and as a projection in T4b creates a name collision in any downstream context that consumes both ASNs.
**Required**: Either drop the E. prefix (use bare predicates Node, Account, Document, Element) or define a different namespace symbol that does not collide with T4b's E. State explicitly what "predicates over E" means.

### Issue 2: Predicate notation introduced without formal binding
**ASN-0045, Hierarchy Level Definitions**: "**E.node** — A *node* is a tumbler t with T4-valid(t) ∧ zeros(t) = 0."
**Problem**: The definition slot describes "a node" as a kind of tumbler, but the well-definedness clause and E.partition use predicate notation Node(t), Account(t), etc. The transition from "x is a node" to "Node(x)" is never made. T4c uses prose labels ("t is a node address") consistently; this ASN switches between informal noun and predicate without binding the two.
**Required**: Either define each predicate explicitly — `Node(t) ≡ T4-valid(t) ∧ zeros(t) = 0` — or use T4c's prose form throughout. Pick one and stick to it.

### Issue 3: account/user aliasing leaves downstream consumers undirected
**ASN-0045, Naming Convention**: "ASN-0045 adopts *account* as the canonical name and treats T4c's *user* as an alias."
**Problem**: T4c's biconditional uses "user address". T4b's projection is U with access `t.U₁`. ASN-0045 introduces Account(t) but says nothing about U/U₁. Are `Account(t)` and "t is a user address" interchangeable propositions? Is `t.U₁` to be read as `t.Account₁`? Without an operational equivalence statement, downstream specs cannot mix the two vocabularies.
**Required**: Add an explicit equivalence: `(A t : T4-valid(t) : Account(t) ⟺ t is a user address (T4c))`. State whether the U projection retains its T4b name or also gets renamed. Without this, the rename is a future-pain accelerator.

### Issue 4: E.partition derivation is asserted, not shown
**ASN-0045, Well-Definedness**: "E.partition is a corollary of T4c; ASN-0045 records it as the postcondition the four naming predicates inherit."
**Problem**: T4c's postcondition is stated on the four prose labels (node/user/document/element address). E.partition is stated on the four predicate names (Node, Account, Document, Element). The derivation requires (a) the binding of each predicate to its T4c label (missing per Issue 2) and (b) the rename Account = "user address" (missing per Issue 3). Without those, E.partition does not follow — the chain of implication has two undeclared links.
**Required**: Show the derivation. State each binding, then cite T4c's Exhaustion and Pairwise extensional disjointness postconditions, then conclude E.partition. Three lines is enough, but the lines must exist.

### Issue 5: No formal contract structure
**ASN-0045, Properties Introduced**: The properties are listed in a table with "Status" but no *Preconditions*, *Definition*, *Postconditions*, *Depends*, or *Frame* slots.
**Problem**: Every foundation ASN this one builds on (T4, T4c, T4b) uses an explicit formal-contract block. ASN-0045 omits these slots, so dependencies on T4c (and transitively on T0, T4, T4a, NAT-card, NAT-zero, NAT-closure, NAT-order) are not declared. A downstream cross-review cannot validate the dependency cone.
**Required**: For each of E.node, E.account, E.document, E.element, E.partition, emit a formal contract block matching the foundation pattern — at minimum *Preconditions* (T4-valid(t)), *Definition*, *Postconditions*, *Depends* (T4, T4c at a minimum).

### Issue 6: Examples cover only the four positive cases
**ASN-0045, Examples**: The table shows one T4-valid tumbler per level.
**Problem**: The four positive cases are the easy ones. Boundary cases that make E.partition non-trivial are absent: a tumbler with adjacent zeros (T4-invalid, all four predicates false), a tumbler with leading zero (T4-invalid), a tumbler with `zeros(t) = 4` (would-be T4-invalid by T4(i)), a tumbler at the empty-document boundary. Without these, the reader cannot see what the partition rules out.
**Required**: Add at least three counter-examples showing T4-invalid tumblers where none of the four predicates hold, and state explicitly that E.partition's quantifier ranges only over the T4-valid subdomain.

## OUT_OF_SCOPE

### Topic 1: Operational semantics of the predicates
The ASN does not specify how Node/Account/Document/Element predicates participate in operations (e.g., precondition checks for INSERT, MAKELINK, etc.). That belongs in the operation ASNs, not here.

### Topic 2: Mapping to T4b's partial projections
The relationship between Account(t) and t.U₁'s domain, between Document(t) and t.D₁'s domain, etc., is structural. A full bridge would be its own ASN. Only the minimal alias coordination (Issue 3) belongs here.

VERDICT: REVISE
