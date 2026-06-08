# Review of ASN-0103

## REVISE

### Issue 1: FirstForkRoot lemma and on-chain version dominance establish more than anything consumes

**ASN-0103, Effect One ("Strict advance...") and the FirstForkRoot lemma**: "*Let `v` be an on-chain version under `A` ... the root document `d_i = [A, 0, i]` lies in `D_A`.*" and the subsequent-case argument concluding "`d > v` by T1 case (i) ... regardless of how deep `v` nests."

**Problem**: The operation's correctness needs two facts about `d` relative to versions: that `d` is not a reuse (`d ∉ E`) and that `d` is permanently distinct from every version, present and future. Both are already delivered without ordering. Freshness (`d ∉ E`) is established uniformly over all of `E` in the *Freshness* paragraph. Distinctness from versions is pure namespace disjointness: every on-chain version inhabits `S(d_i, 1)` (FirstForkRoot itself shows versions carry length `≥ #A+3`, so they are not in `S(A,2)`), and `d ∈ S(A,2)` with `S(A,2) ∩ S(d_i, 1) = ∅` by B7 (ASN-0040) — which the note already invokes for cross-namespace distinctness. The *lexicographic dominance* `d > v` is strictly stronger than the needed `d ≠ v`, and it is consumed nowhere: CND.inv discharges address distinctness via "B7 for cross-namespace, S0 for same-chain injectivity," never via version dominance. FirstForkRoot (two dense paragraphs of frozen-position bookkeeping) supports only this unconsumed ordering.

**Required**: Reduce CND.monotone to its operative content — non-reuse (`d ∉ E`, already proven) plus same-chain injectivity (S0) and cross-namespace distinctness from versions (B7). Delete FirstForkRoot and the subsequent-case lexicographic dominance argument, or demonstrate a downstream invariant that requires `d > v` rather than `d ≠ v`.

### Issue 2: Citation-scope bookkeeping in the Freshness paragraph

**ASN-0103, Effect One (Freshness)**: "The cited freshness lemmas of ASN-0093 (FirstEmission, ChainEnumerationInjectivity) are stated only for the content and link sub-allocators `A_C(d)`, `A_L(d)`; the document sub-allocator `A_doc(A)` is not in their scope. But `A_doc(A) = S(A, 2)` is a SiblingStream, so it inherits the requisite properties directly from ASN-0040."

**Problem**: This is meta-prose about which foundation lemma applies, not argument. It names lemmas that *don't* apply in order to redirect to ones that do. The reader has to work past the citation-scope discussion to reach the actual point (cite ASN-0040 S0/StreamOrdering directly).

**Required**: Replace with the direct citation: `A_doc(A) = S(A, 2)`, whose enumeration is strictly increasing by S0 (StreamOrdering, ASN-0040). Drop the discussion of ASN-0093's lemma scope.

### Issue 3: Redundant restatements of the S0 strictly-increasing argument

**ASN-0103, Effect One (Freshness / Strict advance)**: "Its enumeration is strictly increasing under T1 (S0, StreamOrdering; ASN-0040)..." and later "Distinctness from every *other* document-chain emission ... has its source in S0: ... S0 (StreamOrdering; ASN-0040) makes that enumeration strictly increasing, hence injective..."

**Problem**: The same S0 "strictly-increasing-hence-injective over `S(A,2)`" fact is invoked at least twice in adjacent prose to close the same same-chain distinctness obligation. Two passages say the same thing in different words.

**Required**: State the S0 same-chain injectivity once and reference it.

### Issue 4: CND.A-act introduction explains why the axiom is needed rather than what it says

**ASN-0103, "The Operation's Input"**: "The foundations state SubAllocatorBundle only for the *document* tier, so `Activated(A_doc(A))` is not derivable from them; we take it as owed by out-of-scope account provisioning."

**Problem**: This is rationale-for-the-axiom prose (why it isn't derivable, where the obligation sits) rather than statement of what the assumption asserts. The same justification is then repeated in the CND.A-act claim row ("Not derivable from the foundations, which state SubAllocatorBundle only for the document tier").

**Problem compounds**: the redundancy across the body text and the claim table is exactly the cross-section duplication anti-bloat flags.

**Required**: State CND.A-act as the assumption it is (account existence ⟹ activated document sub-allocator), in one place. Drop the derivability rationale or compress to a half-clause.

### Issue 5: Parenthetical restatement in the Freshness exclusion

**ASN-0103, Effect One (Freshness)**: "...against nodes (`zeros = 0`), accounts (`zeros = 1`), documents, and versions at once. (Equivalently and more coarsely, `zeros(d) = 2` already excludes every node and account; the stream membership closes the residual document and version cases.)"

**Problem**: The parenthetical re-derives the immediately preceding sentence by a coarser route — the same exclusion stated twice. The "equivalently and more coarsely" framing signals the redundancy explicitly.

**Required**: Keep one formulation.

## OUT_OF_SCOPE

(none — the ASN's scope boundaries on forking, content allocation, account provisioning, and registry coupling are handled correctly via standing assumptions and open questions, not by smuggling in out-of-scope claims.)

VERDICT: REVISE
