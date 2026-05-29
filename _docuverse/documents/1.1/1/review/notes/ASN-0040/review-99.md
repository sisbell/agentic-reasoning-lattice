# Review of ASN-0040

## REVISE

### Issue 1: S(p,d), S0, and B7 reinvent foundation allocator-domain results

**ASN-0040, S(p,d) / S0 / B7**: `S(p, d) = c₁, c₂, …` with `c₁ = inc(p, d)`, `cₙ₊₁ = inc(cₙ, 0)`; S0 proves the stream strictly increasing; B7 proves `S(p, d) ∩ S(p', d') = ∅`.

**Problem**: `S(p, d)` is, by construction, the domain of the child allocator spawned from `p` at depth `d`: base `inc(p, d)` followed by the `inc(·, 0)` chain — exactly the foundation's `dom(A) = {tₙ : tₙ₊₁ = inc(tₙ, 0)}` (T10a). Consequently:
- **S0** ("the sibling stream is strictly increasing") is precisely T10a.7 (EnumerationInjectivity), which already states the enumeration `n ↦ tₙ` is strictly increasing under T1. S0's proof (TA5(a) + T1 transitivity/irreflexivity) re-derives T10a.7 verbatim without citing it.
- **B7** ("distinct namespaces have disjoint streams") is T10a.6 (DomainDisjointness) for distinct allocators. The length-split / equal-parent / unequal-parent case analysis re-derives the foundation result.

The Depends lists for S0 and B7 cite only TA5/T1/T3/T4 primitives, never T10a.6, T10a.7, or GlobalUniqueness. The reviewer standard is explicit: an ASN should use the foundation, not reinvent notation it already defines.

**Required**: Either (a) state that `S(p, d)` is the foundation child-allocator domain and discharge S0 from T10a.7 and B7 from T10a.6 (after the small argument that distinct B6-valid `(p, d)` yield distinct allocators — the aliasing observation already in the B6(i) paragraph), or (b) if the standalone re-derivation is deliberate because `S(p, d)` is defined over *arbitrary* T4 parents rather than disciplined-tree allocators, say so explicitly and justify why the foundation results do not apply directly. Right now the relationship is silent and the proofs duplicate verified foundation work.

### Issue 2: B3 depends on an undefined predicate via a dangling pointer

**ASN-0040, B3 (Ghost Validity)**: "Let `Occupied : T × 𝒮 → {⊤, ⊥}` (introduced elsewhere) denote 'the address t carries content in state s'."

**Problem**: `Occupied` is not defined in this ASN, and content storage is explicitly out of scope. "(introduced elsewhere)" is a forward reference to no specific location — it is exactly the kind of dangling deferral the anti-bloat pass is meant to surface. Moreover, unlike B1/B10/B_fin, B3 carries no preservation discharge: no operation in this ASN sets `Occupied`, so the invariant is neither established nor preserved here — it is a constraint imposed on out-of-scope future operations.

**Required**: Drop "(introduced elsewhere)". Declare `Occupied` as an explicit abstract predicate parameter of the baptism model (a constraint on any future content-storage operation), and state plainly that B3 is an *introduced* constraint with no preservation obligation in this ASN. Do not point at an unnamed future location.

### Issue 3: Forward-reference accretion around Bop

**ASN-0040, B0a / B0 / B4 / Bop**: B0a defines baptismal operations as "the operation specified by Bop below; its action on the registry is the one Bop fixes"; B0's proof restates "`op(s).B = s.B ∪ {next(s.B, p, d)}`"; B4 restates the "read the high water mark / compute next / commit `s.B ∪ {next…}`" content; Bop then states the same postcondition again.

**Problem**: The single fact "baptism adds `next(s.B, p, d)` to the registry" is written four times (B0a, B0 proof, B4, Bop), three of them as forward deferrals to `Bop below`. This is the "multiple paragraphs defer to the same downstream location" pattern, compounded by the operation being defined last while the registry-mutation rule is needed first.

**Required**: State the registry-mutation rule once (at Bop, or hoisted to B0a) and have the other sites cite it by label without re-quoting the postcondition. Either define `baptize` before B0a or have B0a reference it purely by name.

### Issue 4: B4 contains self-describing meta-prose

**ASN-0040, B4 (Atomic Baptism)**: "The baptism-specific content is that the operation's three internal steps … collapse onto that one edge: no transition interposes between the read and the commit."

**Problem**: "The baptism-specific content is that…" narrates what the property contributes rather than stating the guarantee. The substantive claim is "read-hwm, compute-next, and commit occur on one `→` edge." The framing clause is meta-prose around an axiom.

**Required**: Reduce B4 to the guarantee itself; drop the "baptism-specific content is that" scaffolding.

## OUT_OF_SCOPE

### Topic 1: Cross-replica / divergent-path baptism uniqueness
B8 is honestly scoped to *co-reachable* (single-path) acts, and the divergent-path case (two paths each reading `hwm = m` and both producing `c_{m+1}`) is correctly listed as an open question. No revision needed — flagging only to confirm the limitation is deliberate and correctly bounded, not an omission.

VERDICT: REVISE
