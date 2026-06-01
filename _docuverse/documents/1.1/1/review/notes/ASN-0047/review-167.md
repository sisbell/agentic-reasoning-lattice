# Review of ASN-0047

## REVISE

### Issue 1: M is silently re-typed from partial (foundation) to total, forcing reinterpretation of inherited preconditions

**ASN-0047, The state model**: "M : T → (T ⇀ T) is total, satisfying M(d) = ∅ for d ∉ E_doc."

**Problem**: ASN-0036 and ASN-0093 define `Σ.M(d) : T ⇀ T` with `dom(M)` as the *set of allocated documents* — foundation operations are written against this (ASN-0093's K.σ has `dom(M') = dom(M) ∪ {d}`, K.α/K.λ have `d ∈ dom(M)`). ASN-0047 re-types M as total, so `dom(M) = T` always, and every inherited `d ∈ dom(M)` precondition must be reinterpreted as `d ∈ E_doc` and ASN-0093's K.σ effect `dom(M') = dom(M) ∪ {d}` becomes vacuous. The ASN papers over this in three places ("under ASN-0047's totality framing where M is total ... `d ∈ E_doc` is the substantive predicate"). Per Standard #7, re-inventing a foundation's state typing — rather than using it — is a flag; here it manufactures a recurring reinterpretation burden that a partial M would avoid.

**Required**: Either keep M partial (matching foundation, with `d ∈ dom(M) ⟺ d ∈ E_doc` as the document-set identity) and drop the totality convention, or justify the re-typing once and state explicitly that it overrides the foundation typing rather than reinterpreting it inline at each inherited operation.

### Issue 2: J1, J1', and P4 are introduced only to be immediately superseded by J1★, J1'★, P4★, with forward "see below" deferrals

**ASN-0047, Coupling and isolation / Content-scoped containment**: "J1 above is the dom(L) = ∅ reading of the wp computation in its operative content-subspace form (invariant P4★) — see *Scoped coupling constraints*." Similarly "P4 ... is then exactly the dom(L) = ∅ specialisation of P4★" and J1' superseded by J1'★.

**Problem**: Each link-free predecessor is defined in its own section, then declared a special case of a starred form defined later, with a forward pointer. In the only regime where P4 holds (`dom(L) = ∅`), `Contains = Contains_C`, so P4 *is* P4★ verbatim — it carries no independent content. The same holds for J1/J1★ and J1'/J1'★. This is the flagged accretion pattern (predecessor stated, deferred downstream, superseded), and both forms are then carried in the Properties-Introduced inventory tables, doubling the bookkeeping.

**Required**: State only the operative J1★/J1'★/P4★ and note in one line that they reduce to the link-free reading when `dom(L) = ∅`. Remove the superseded J1/J1'/P4 sections and their separate inventory rows, or demote them to a single sentence each.

### Issue 3: The (a')/(b') sub-allocator parent-dispatch argument is restated in full in three sections

**ASN-0047, Sub-allocator names; K.δ case (ii) discharge; worked examples**: The "which allocator minted t / T10a.6 routes to the unique parent allocator" dispatch — distinguishing first-emission (T2 spawn) from sibling (T1 increment), case (a') document-allocator vs case (b') version-allocator — appears at length in *Sub-allocator names*, is re-derived as sub-cases A1/A2/B/C in *K.δ case (ii) discharge*, and is walked through again per-step in *Worked example: entity hierarchy* and *Worked example: fork*.

**Problem**: Per the anti-bloat directive, "two paragraphs in the same document say the same thing in different words" and "multiple paragraphs defer to the same downstream location" are findings. The dispatch logic is one argument repeated with cosmetic variation; the reader must reconcile three statements of the same routing rule, and divergence between them would be undetectable.

**Required**: State the (a')/(b') dispatch once (in *Sub-allocator names*) as a named sub-lemma, and have *K.δ case (ii) discharge* and the worked examples cite it rather than re-derive it.

### Issue 4: Prose around inherited/new axioms explains why the axiom is wanted rather than what it states

**ASN-0047, multiple axiom sites**: NodeRegistryBootstrap carries "a registry external to Σ, so n₀ enters at Σ₀ rather than via a prior K.δ event"; the inherited K.α/K.λ/K.σ glosses each repeat the parenthetical "ASN-0093 writes this as `d ∈ dom(M)`, but under ASN-0047's totality framing ... `d ∈ E_doc` is the substantive predicate"; SubAllocatorAxiom's restatement appends "each providing a forward-allocation frontier whose namespace property closes the uniqueness chain for K.α ... and K.λ."

**Problem**: These are "Why the axiom is needed" sub-paragraphs in structural slots — the flagged pattern. The frontier-rationale and registry-externality remarks do not advance the axiom's content; the repeated totality parenthetical is Issue 1's friction surfacing at each inherited operation.

**Required**: Reduce each axiom restatement to its content and a single citation. Move the "closes the uniqueness chain" / "external registry" rationale to the one site that consumes it, or delete it.

### Issue 5: FrontierEquivalence reverse direction mislabels the producing allocator

**ASN-0047, FrontierEquivalence proof, reverse direction**: "the address `inc(t, 0)` can be produced by exactly one allocator's tracked chain — namely t's own sub-allocator (since `inc(t, 0)` is, by TA5(c), the sibling-increment of t on its own chain ...)."

**Problem**: `t` is an *emission* of an allocator, not an allocator; `inc(t, 0)` is the next emission on the parent allocator A whose tracked chain contains `t`, not on "t's own sub-allocator" (t's sub-allocators are the children spawned beneath t, which produce `inc(t, k')` with `k' > 0`, not `inc(t, 0)`). The substance (GlobalUniqueness/T10a.6 confine `inc(t,0)` to A's chain) holds, but the naming inverts the allocator relationship the rest of the ASN sets up.

**Required**: Replace "t's own sub-allocator" with "the allocator A whose tracked chain contains t" (the parent allocator), consistently in both the forward and reverse directions.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
The fork composite (J4) leaves the new document's link subspace empty and explicitly defers any link-inheritance mechanism. This is correctly left to a future operations ASN — not an error here.

### Topic 2: Interior link withdrawal / tombstoning
K.μ⁻ admits only per-subspace suffix truncation under D-CTG★/D-MIN★, so withdrawing an interior link is not expressible. The ASN flags this in Open Questions; a separate withdrawal mechanism belongs in a future ASN.

META: (not applicable — the ASN remains squarely at the state/operation/invariant level; the findings are accretion and precision issues, not drift into implementation.)

VERDICT: REVISE
