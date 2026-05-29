# Review of ASN-0040

## REVISE

### Issue 1: B4 restates the foundation Σ signature and adds only implementation narrative
**ASN-0040, B4 (Atomic Baptism)**: "Each `baptize(p, d) ∈ Σ` is a single edge of `→`: the operation's three internal steps — read the high water mark, compute the next address, and commit the union (Bop) — collapse onto that one edge, with no transition interposing between the read and the commit."

**Problem**: The abstract content — "baptize is a single transition edge" — is already guaranteed for *every* `op ∈ Σ` by the foundation's transition model (NoDeallocation: each `op` is a partial function `𝒮 ⇀ 𝒮`, and a transition is the pair `(s, op(s))`). There is no separate "read" transition in the abstract model; `next(s.B,p,d)` is evaluated inside the single function application. So B4 carries no abstract guarantee specific to baptism. Its only added content is the read/compute/commit narrative, which is Gregory's two-phase query/write — implementation mechanics in a structural slot. Its downstream uses in B8 and B9 ("by B4, each baptism is a single transition edge") need only the inherited Σ fact. The motivating intro paragraph ("Baptism is a two-phase process... The write — not the query — is the moment of baptism...") is the same implementation narrative.

**Required**: Either drop B4 and have B8/B9 cite the foundation Σ signature directly, or reduce it to a one-line statement of the abstract fact (no transition interposes between evaluating `next` and committing the union) without enumerating implementation steps. Trim the intro two-phase paragraph correspondingly.

### Issue 2: Formulaic claim-restatement preambles and repeated induction boilerplate
**ASN-0040, proofs of S(p,d), B5, B5a, B1, B2, B10, Bop, B8, B9**: each proof opens by restating its own formal-contract postcondition — e.g. B10: "We must show that in every state reachable from a conforming seed B₀, every element of s.B satisfies T4"; B2: "We must show that for any registry B satisfying B1 and any valid parent-depth pair (p, d), the operationally defined next address equals the (hwm + 1)-th element..."; B9: "We must show that for any pair (p, d) satisfying B6 and any bound M ∈ ℕ, there exists a state s'...".

Additionally, B_fin, B1, and B10 each repeat the identical induction scaffolding verbatim — "By B0a, a transition s → s' is either s.B-frame — then B' = B and [X] holds at B' immediately by the inductive hypothesis — or baptismal, the case we now treat."

**Problem**: The preambles duplicate the postcondition already stated in the formal contract immediately above; they advance no reasoning. The three-way repetition of the s.B-frame dispatch is boilerplate the precise reader must skip to reach the substantive (baptismal) case.

**Required**: Delete the "We must show that..." restatements and begin each proof at its first reasoning step. State the s.B-frame dispatch once (the framing follows directly from B0a) and let B_fin/B1/B10 invoke it rather than reprinting it.

## OUT_OF_SCOPE

### Topic 1: Uniqueness across divergent (non-co-reachable) state branches
B8 deliberately restricts to *co-reachable* acts (a single path `s_init →* s`). Baptisms on divergent branches of the state DAG (e.g. forked versions, replicas) are not compared. Reconciling this with the foundation's unconditional GlobalUniqueness is genuine new territory.
**Why out of scope**: Version structure and replication are explicitly deferred (version/document structure; replication/BEBE). The foundation's allocator-partition uniqueness already covers the unconditional case; B8's registry-growth view is correctly scoped to a single path.

VERDICT: REVISE
