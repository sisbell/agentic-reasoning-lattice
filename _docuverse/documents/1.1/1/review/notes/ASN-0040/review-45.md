# Review of ASN-0040

## REVISE

### Issue 1: S0 invokes T10a.7 outside its stated contract
**ASN-0040, S0 (StreamOrdering)**: "ASN-0034's T10a.7 (EnumerationInjectivity) establishes that every such enumeration is strictly increasing… its proof rests only on TA5(a)… none of which appeal to T4-validity of the base."
**Problem**: T10a.7's stated precondition is "Allocator A *conforming to T10a*," and T10a's axiom requires the base satisfy T4. S0's precondition is only `p ∈ T, d ≥ 1` — `c₁ = inc(p, d)` need not be T4-valid. The proof reaches into T10a.7's *internal proof* ("rests only on TA5(a)…") rather than its *contract*. A foundation lemma must be used by its postcondition under its preconditions, not by re-litigating its proof skeleton.
**Required**: Either prove S0 directly from TA5(a) (per-step `inc(cₙ,0) > cₙ`) plus T1 transitivity/irreflexivity — the same three-line induction — or restrict S0's precondition to B6-valid `(p,d)` so T10a-conformance is genuine. (Note: B7's parallel use of T10a.1 is within contract, since T10a.1's precondition is only "allocator with base, siblings by inc(·,0)" — no T4 needed.)

### Issue 2: the sibling-stream length/sig invariant is re-derived five times
**ASN-0040, S(p,d) proof, S1 proof, B5a application, B6 necessity (b), B7 Case 3**: the micro-argument "c₁ has final value 1 so sig(c₁)=#p+d; each inc(·,0) advances sig by 1 preserving length, so sig(cₙ)=#p+d, hence position ≤#p is invariant" appears in full at least five separate places.
**Problem**: Each occurrence is correct, but the repetition is exactly the accretion the anti-bloat classifier targets — the same load-bearing fact is proven inline wherever it is needed instead of once. The S(p,d) postcondition already establishes `cₙ = [p₁,…,p_{#p},0,…,0,n]` with `#cₙ = #p+d`; everything downstream should cite it.
**Required**: Hoist "for all `n≥1`, `#cₙ = #p+d`, `sig(cₙ) = #p+d`, and `cₙᵢ = pᵢ` for `i ≤ #p`" into the S(p,d) contract (it nearly is) and have S1, B5a-application, B6, B7 cite it rather than re-derive.

### Issue 3: B10's preservation step over-claims contiguity it does not use
**ASN-0040, B10 inductive step**: "the sibling `a = inc(max(children(B,p,d)),0) = c_{m+1}`."
**Problem**: B10 needs only `a ∈ S(p,d)`, which follows because `max(children) ∈ S(p,d)` and `inc(·,0)` maps a stream element to its successor in the stream. Writing `= c_{m+1}` presupposes B1 (contiguity), and the doc's own dependency ordering establishes B1 *after* B10. The equality is gratuitous and creates an apparent forward dependency.
**Required**: State only `a = inc(cⱼ,0) = c_{j+1} ∈ S(p,d)` where `cⱼ = max(children)`; drop the `c_{m+1}` labeling, which is not needed and presumes B1.

### Issue 4: B4 carries implementation and future-concurrency essay prose
**ASN-0040, B4 (Atomic Baptism)**: "Gregory's implementation achieves the atomic-transition semantics through single-threaded dispatch… But B4 is a specification-level requirement… Any mechanism that exhibits one Σ-transition per baptism — locking, transactions, hardware serialization, single-threaded dispatch — satisfies B4." and "if the system later admits a model with concurrent operations, the serialization requirement collapses to…"
**Problem**: The mechanism enumeration and the conditional about a not-yet-existing concurrency model advance no reasoning about the present single-component state space. This is forward-looking essay in a definitional slot. (The one-line implementation witness is fine; the catalog and the hypothetical concurrency model are not.)
**Required**: Reduce to the abstract content — one Σ-edge per baptism, `next` evaluated against the precondition state — and drop the mechanism catalog and the speculative concurrency discussion (or move the latter to Open Questions, where a per-grain serialization question already lives).

### Issue 5: B0a carries scope-rationale and equivalence-justification meta-prose
**ASN-0040, B0a (Baptismal Closure)**: "B0a constrains only the depth arithmetic, not the authorization chain — whether p must itself be baptized…" and "Equivalently… The equivalence rests on the *State Space and Transitions* section's definition of transition: every `s → s'` is of the form `(s, op(s))`… so a partition of Σ… induces a partition of transitions."
**Problem**: The first sentence defers to authorization (out of scope) to explain what B0a does *not* do; the second restates B0a and then justifies *why the restatement is equivalent*. Neither advances the closure law. These are the "why the axiom is needed / restatement rationale" patterns.
**Required**: Keep the partition statement and its single-sentence consequence; drop the authorization-deferral sentence and the equivalence-justification (the restatement, if kept, needs no proof that it is a restatement).

### Issue 6: Bop proof justifies its own ordering to dodge circularity
**ASN-0040, Bop proof of well-definedness**: "These invariants are established, each by its own induction, in dependency order: B_fin… B10… B1… At the precondition state s of any reachable transition we may therefore cite each as already holding."
**Problem**: This is prose about document/proof ordering inserted to assure the reader the dependencies are acyclic — exactly the flagged "placed here to avoid circular dependency" pattern. The acyclicity is a fact about the proofs, not a step in this one.
**Required**: Drop the ordering paragraph; cite B_fin, B10, B1 as the established invariants they are. If the dependency graph genuinely needs documenting, the Properties Introduced table already carries the `from …` columns.

### Issue 7: B9 stacks three Nelson quotes making one point
**ASN-0040, B9 (Unbounded Extent)**: three separate Nelson quotations ("Each integer has no upper limit," "New items may be continually inserted…," "…all have possible descendants") each followed by "The word X carries the weight"–style gloss.
**Problem**: All three reinforce the single claim already captured by T0(a): components are unbounded. Two paragraphs saying the same thing in different words. One quote suffices to motivate; the rest is redundant essay.
**Required**: Keep one motivating quote; remove the duplicated commentary.

### Issue 8: B7 body precondition is redundant
**ASN-0040, B7 (Namespace Disjointness)**: "provided both parents satisfy T4 and both depths satisfy B6."
**Problem**: B6(i) already requires the parent satisfy T4, so "both parents satisfy T4" is subsumed by "both depths satisfy B6." Minor, but it is the kind of duplicated precondition the formal contract should not carry (the Formal Contract line correctly states only B6).
**Required**: State the precondition once as "both `(p,d)`, `(p',d')` satisfy B6."

## OUT_OF_SCOPE

### Topic 1: B3 (Ghost Validity) as a forward requirement on content
**Why out of scope**: Content storage is explicitly deferred. B3 does not define `Occupied` or any content operation — it states a one-way binding (`Occupied(t,s) ⟹ t ∈ s.B`) that future content ASNs must satisfy. This is appropriate boundary-setting rather than in-scope content specification, so it is correctly framed; no action needed beyond confirming it stays parametric (which it does).

### Topic 2: Parent-prerequisite / authorization chain
**Why out of scope**: The repeated "no parent-baptized prerequisite is imposed" notes in B0a and Bop touch the authorization model deferred to Tumbler Ownership. Leaving the prerequisite unmodeled here is correct; only the *explanatory* deferral prose (Issue 5) should be trimmed, not the design decision.

VERDICT: REVISE
