# Review of ASN-0040

## REVISE

### Issue 1: B4 (Atomic Baptism) is derivable, not a design requirement, and its prose restates the foundation
**ASN-0040, B4 / Bop STRUCTURAL**: "This indivisibility is a primitive structural assumption on Σ — each element of Σ is a single partial function `op : 𝒮 ⇀ 𝒮` whose application is one transition."
**Problem**: The foundation (NoDeallocation, Signature of Σ) already fixes this: every `op ∈ Σ` is a partial function on 𝒮 and a transition `s → s'` is exactly the pair `(s, op(s))` — i.e. one edge, no intermediate state. B0a places `baptize(p, d) ∈ Σ`. Atomicity and read-against-precondition-state semantics therefore follow immediately from B0a + the foundation; B4 is a corollary, not "a primitive structural assumption" or "design requirement." The quoted sentence re-derives the foundation's Σ signature verbatim — the anti-bloat "prose restates foundation / explains why an axiom is needed" pattern.
**Required**: Demote B4 from "design requirement" to a corollary of B0a and the foundation, and delete the restatement of Σ's single-function semantics (cite the foundation instead).

### Issue 2: T4 is renamed "FieldSeparatorConstraint"
**ASN-0040, B10 invariant and proof**: "every baptized address satisfies FieldSeparatorConstraint"; "satisfies T4 (FieldSeparatorConstraint, ASN-0034)."
**Problem**: The foundation's canonical name for T4 is **HierarchicalParsing**. "FieldSeparatorConstraint" is an invented alias for a foundation concept, which Standard 7 forbids — the ASN should use the foundation's name, not coin a new one. The rest of the ASN already calls it T4 throughout, so the alias is also internally inconsistent.
**Required**: Drop "FieldSeparatorConstraint"; refer to T4 (HierarchicalParsing) consistently.

### Issue 3: s.B is introduced three times before it is defined
**ASN-0040, "State space and transitions" and "The baptismal registry"**: "this ASN extends each state with the registry component s.B"; then "This ASN introduces one state component — the baptismal registry s.B (defined below)"; then "We introduce the central state component: s.B (BaptismalRegistry)."
**Problem**: Three separate announcements that the ASN introduces one state component s.B, two of them in the same section, before the actual definition. This is the "two paragraphs say the same thing in different words" bloat pattern — the reader must skip past the repeated framing to reach the definition.
**Required**: Announce and define s.B once.

### Issue 4: Repeated Nelson quotation and repeated ownership deferral
**ASN-0040, intro vs. "The sibling stream"**: the phrase "successive new digits to the right" appears as a paraphrase in the intro and again as a full quote in the sibling-stream section; the authorization deferral to Tumbler Ownership likewise appears in both the intro and the Open Questions.
**Problem**: Duplicated quote and duplicated downstream deferral ("multiple paragraphs defer to the same downstream location") add no reasoning the second time.
**Required**: Quote "successive new digits to the right" once (at the sibling stream, where it carries the argument) and consolidate the ownership deferral to a single site.

## OUT_OF_SCOPE

### Topic 1: Cross-branch (non-co-reachable) baptism uniqueness
B8 deliberately restricts to co-reachable acts; uniqueness across divergent transition branches (where two forks could both emit `c_{m+1}`) needs merge/replication semantics. Correctly deferred (Open Questions, replication item) — not a defect in this ASN.

### Topic 2: `allocated(s) ⊆ s.B` alignment between allocator events and baptism
The relationship between T9/T10a allocator domains and the baptismal registry is raised as an open question and belongs to a future ASN; B3's ghost-validity forward requirement handles the content side cleanly here.

VERDICT: REVISE
