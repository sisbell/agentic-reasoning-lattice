# Review of ASN-0045

## REVISE

### Issue 1: ValidAddress is undefined notation
**ASN-0045, Properties Introduced table**: "Node: ValidAddress(t) ∧ zeros(t) = 0" (and the three siblings).
**Problem**: `ValidAddress` is not defined in this ASN, in the shared vocabulary, or in any cited foundation. The foundation's predicate is *T4-valid* (T4, HierarchicalParsing). Inventing a new label for an existing predicate is exactly the foundation-reinvention case the review rubric forbids.
**Required**: Either (a) cite T4 and write `T4-valid(t) ∧ zeros(t) = k`, or (b) introduce ValidAddress as an explicit abbreviation for T4-validity with a one-line definition.

### Issue 2: Foundation T4c already defines these labels
**ASN-0045, Hierarchy Level Definitions**: "A *node* is a valid tumbler with zeros(t) = 0… A *document* is a valid tumbler with zeros(t) = 2…"
**Problem**: T4c (LevelDetermination), a foundation ASN, already defines exactly this four-label assignment on the T4-valid subdomain by the same zero-count criterion, and proves both exhaustion (`zeros(t) ∈ {0,1,2,3}`) and pairwise extensional disjointness. ASN-0045 restates the definition with no citation, no acknowledgement of the existing well-definedness postcondition, and no derivation.
**Required**: Cite T4c. Express the four labels as consequences of T4c (or as renamings of T4c's labels), not as fresh introductions. State explicitly that exhaustion and disjointness follow from T4c's postconditions.

### Issue 3: Unjustified rename from T4c's "user" to "account"
**ASN-0045, E.account**: "An *account* is a valid tumbler with zeros(t) = 1."
**Problem**: T4c's Definition reads `(zeros(t) = 1 ↔ t is a user address)`. The shared vocabulary does not list either term. ASN-0045 silently substitutes "account" without explanation. A foundation rename — if intentional — needs a one-sentence justification, and the foundation's label should be flagged as deprecated or aliased so downstream consumers know which term is canonical.
**Required**: Either retain T4c's "user" or state explicitly that "account" supersedes T4c's "user", with a justification (e.g., consistency with `tumbleraccounteq`, T10/baptism prose, or a registered project decision).

### Issue 4: Well-definedness of the labelling is asserted, not derived
**ASN-0045, Properties Introduced**: Four predicates introduced as `Node`, `Account`, `Document`, `Element`.
**Problem**: For the labels to be useful, every T4-valid tumbler must satisfy exactly one of them. That fact is T4c's *exhaustion* and *pairwise extensional disjointness*. ASN-0045 states the predicates but does not record the consequence — so a downstream consumer cannot cite ASN-0045 for "every T4-valid address is exactly one of node, account, document, element."
**Required**: Add a postcondition that for every T4-valid t, exactly one of the four predicates holds, with a one-line citation to T4c's exhaustion + injectivity postconditions.

### Issue 5: No concrete example
**ASN-0045, throughout**: The ASN gives no instance of any of the four labels.
**Problem**: The rubric requires verification against at least one concrete scenario. For a labelling ASN, this is one worked tumbler per level: e.g., `[7]` is a node, `[7,0,3]` is an account (with the rename), `[7,0,3,0,5]` is a document, `[7,0,3,0,5,0,1]` is an element. Without examples, the reader cannot confirm the zero-count counting convention being used.
**Required**: Add a small example block exhibiting one T4-valid tumbler for each of the four zero-counts and verifying the label assignment.

## OUT_OF_SCOPE

None.

META: The ASN is a thin renaming of T4c's already-proved label assignment; if intentional it should be repositioned as an alias/rename layer over T4c rather than a fresh introduction, but the territory itself is in scope.

VERDICT: REVISE
