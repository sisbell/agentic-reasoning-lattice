# Review of ASN-0077

## REVISE

### Issue 1: V-span operation's behavior over link subspace is undefined

**ASN-0077, "The operation" (SHOWORIGIN over a content reference)**: Precondition (iii) "`V_{u₁}(d) ≠ ∅`" permits `u₁ ∈ {s_C, s_L}`; the postcondition is `origins_V(Σ, d, σ) = { origin(M(d)(v)) : v ∈ ⟦σ⟧ ∩ dom(M(d)) }`.

**Problem**: When `u₁ = s_L`, by S3★ (foundation ASN-0047), `M(d)(v) ∈ dom(L)`. But S7 of foundation ASN-0036 (the ASN's stated source for `origin`) defines `origin` only on `dom(C)`. The postcondition expression `origin(M(d)(v))` is therefore either undefined or implicitly extended. CL-OWN in foundation ASN-0047 uses `origin` on link addresses (yielding trivial result `d`), suggesting an implicit structural-projection extension, but ASN-0077 does not acknowledge this. The edge cases section addresses the I-span cross-subspace case (Open Question 1) but does not address V-span over link subspace.

**Required**: Either add a precondition `u₁ = s_C` to restrict SHOWORIGIN_V to content subspace, or explicitly extend `origin` to `dom(L)` via the structural projection `N(·).0.U(·).0.D(·)` and note that by CL-OWN the link-subspace V-span case trivially yields `{d}`.

### Issue 2: Singleton I-span proof relies on the wrong premise

**ASN-0077, "Edge cases" (Singleton I-span)**: "the next tumbler exceeding `a` in the same parent is by construction `a ⊕ ℓ`, so `⟦σ_a⟧ ∩ dom(C) = {a}` (assuming no other allocated address sits at that exact position, which is impossible by S4 — distinct allocation events have distinct addresses)."

**Problem**: `⟦σ_a⟧` contains `a` and the entire subtree of `a` (any extension of `a` lies between `a` and its next sibling by T1 case (ii)). The reason no other allocated address lies in `⟦σ_a⟧ ∩ dom(C)` is not S4 (which forbids two distinct allocation events producing the same address) but S7b (foundation ASN-0036), which restricts `dom(C)` to addresses with `zeros = 3`: any proper extension of an element-level `a` has `zeros > 3` and so cannot be in `dom(C)`. The cited S4 addresses a different question.

**Required**: Replace the S4 appeal with S7b: `⟦σ_a⟧` contains `a`'s entire subtree, but every descendant has `zeros > 3` and cannot be in `dom(C)` per S7b. Hence `⟦σ_a⟧ ∩ dom(C) = {a}`.

### Issue 3: D(Σ) notation is undefined

**ASN-0077, "The operation" (SHOWORIGIN over a content reference)**: Precondition (i) says "`d ∈ D(Σ)` (the source document has an arrangement defined in the ambient state Σ)".

**Problem**: `D(Σ)` is used without prior definition in this ASN. Foundation ASN-0047 defines `Σ.E_doc` as the set of documents in `Σ.E` satisfying `IsDocument(e)`. The introduction of a new symbol without definition (or alignment with foundation terminology) is a hand-wave at the precondition level.

**Required**: Use `d ∈ Σ.E_doc` consistent with foundation ASN-0047, or explicitly define `D(Σ)` in this ASN.

### Issue 4: Empty-restriction edge case argument is hand-wavy

**ASN-0077, "Edge cases" (Empty-restriction within a non-empty document)**: "well-formedness requires every depth-`m` position in the span's range to be in `dom(M(d))` (precondition (vi)). Since `reach(σ) > u` by TA-strict and at least one depth-`m` position lies between them (the position `u` itself), this case does not arise when precondition (vi) is interpreted nontrivially."

**Problem**: The "interpreted nontrivially" phrasing obscures the derivation. The actual argument: by TA-strict (ASN-0034), `u = start(σ) ∈ ⟦σ⟧`; by precondition (v), `#u = m`; so `u` is a depth-`m` position in `⟦σ⟧`. Precondition (vi) then gives `u ∈ dom(M(d))`. Hence `u ∈ ⟦σ⟧ ∩ dom(M(d))`, so the intersection is non-empty. The structural reason for non-emptiness should be stated explicitly rather than hidden in "interpretation".

**Required**: Replace the "nontrivial interpretation" prose with the explicit derivation showing `u ∈ ⟦σ⟧ ∩ dom(M(d))` via TA-strict and precondition (vi).

### Issue 5: O5 derivation conflates address-as-value with address-as-state

**ASN-0077, O5 derivation**: "(2) The address `a` is a fixed tumbler — a sequence of natural-number components. No transition rewrites the components of an existing address; only `dom(C)` (the set of allocated addresses) and `C` (the mapping from addresses to values) can change. The address-as-tumbler is invariant by construction."

**Problem**: A tumbler is a value (T0 of ASN-0034), not state. State transitions never "rewrite" values — they update mappings between values. The claim "address-as-tumbler is invariant by construction" is vacuous: values don't change because they aren't state. Step (2) is a framing distraction; the actual mathematical content of the proof lies in steps (3) and (4).

**Required**: Rewrite O5's derivation: by O3, `origin` is a pure projection of the component sequence of its argument; evaluating the same pure function on the same value yields the same result in any state; hence `origin'(a) = origin(a)`. Cite P0 only to justify that the hypothesis `a ∈ dom(Σ'.C)` is consistent with `a ∈ dom(Σ.C)`.

## OUT_OF_SCOPE

None — all topics deferred (link-subspace I-spans, transitive provenance chains, native vs transcluded distinction, byte-fetch unreachability, historical containment via `Σ.R`, intra-document sharing reporting) are explicitly noted in the ASN's Open Questions section.

VERDICT: REVISE
