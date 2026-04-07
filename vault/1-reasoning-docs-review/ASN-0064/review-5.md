# Review of ASN-0064

## REVISE

### Issue 1: F1 uses "partitions" but the per-block I-contributions may overlap or merge
**ASN-0064, From Positions to Identity**: "the set resolve(d, ⟦σ_V⟧) partitions into at most m contiguous I-address runs, one per block whose V-extent intersects ⟦σ_V⟧"
**Problem**: With self-transclusion, two blocks can share I-extents. Consider β₁ = ([1,1], a, 2) and β₂ = ([1,3], a, 2) in the same canonical decomposition — M14 (ASN-0058) confirms these coexist since the merge I-adjacency condition a = a + 2 fails. If the V-span covers both blocks, each contributes {a, a+1}, and the resolved set is {a, a+1} — one run from two blocks, not a partition. Separately, two blocks can be I-adjacent without being V-adjacent (e.g., β₁ = ([1,1], a, 2) and β₃ = ([1,5], a+2, 1) — they are not merged since V-adjacency fails). Their I-contributions {a, a+1} and {a+2} merge into one contiguous run. The upper bound of m is correct, but the word "partitions" implies disjoint decomposition and "one per block" implies a bijection — neither holds under self-transclusion or I-adjacent non-V-adjacent blocks.
**Required**: Replace "partitions into at most m contiguous I-address runs, one per block" with "is the union of at most m contiguous I-address runs" (or "decomposes into at most m maximal contiguous runs"). Add a note that self-transclusion and I-adjacency across distinct blocks may reduce the count below m.

### Issue 2: Variable ℓ used for both link addresses and span widths
**ASN-0064, throughout**: Link addresses are denoted ℓ (e.g., "ℓ ∈ dom(Σ.L)"), while the overlap definition and F3 proof quantify over "(s, ℓ) ∈ e" where ℓ is a span width — the standard convention from all foundation ASNs (T12, S4, etc.). The collision appears in the same sections: the satisfaction predicate introduces ℓ as a link address, then the overlap expansion introduces ℓ as a span width. Foundation ASN-0043 avoids this by using `a` for link addresses throughout (e.g., "(A a ∈ dom(Σ.L) ...)"). A secondary collision: `resolve_spec({(d₁, Σ₁), ..., (dₖ, Σₖ)})` uses Σᵢ for V-span-sets, colliding with Σ for system state — the ASN itself uses the clearer Σ_V earlier.
**Required**: Rename the link-address variable to avoid collision with span widths — either `a` (matching ASN-0043's convention) or another letter that doesn't shadow foundation notation. Replace Σᵢ in resolve_spec with Σ_Vᵢ or a distinct name.

## OUT_OF_SCOPE

### Topic 1: Integration of Σ.L into formal system state
**Why out of scope**: ASN-0047 defines Σ = (C, E, M, R). The link store Σ.L (ASN-0043) is not yet part of this tuple. A link-creation transition (analogous to K.α for content) would extend the state and establish LinkEntityCoherence as a theorem rather than an assumption. This is new territory — the assumption is correctly marked and correctly used.

### Topic 2: Link store finiteness
**Why out of scope**: No foundation establishes that dom(Σ.L) is finite at every reachable state (paralleling S8-fin for arrangements). This follows informally from finite transition history but has no formal statement. The gap is inherited from ASN-0043, not introduced here.

VERDICT: REVISE
