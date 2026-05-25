# Review of ASN-0075

## REVISE

### Issue 1: D-DISCR composite-boundary notation is internally inconsistent

**ASN-0075, §Why the Provenance Relation Is Load-Bearing**:

History 1 is written:
```
Σ_0  →* K.δ(d)
     →* K.δ(d')
     →* K.α(a, d)
     →* K.μ⁺(d,  v  ↦ a);  K.ρ(a, d)
     ...
```

History 2 mirrors this with K.α(a, d) on its own "→*" arrow.

**Problem**: Each "→*" arrow appears to denote a separate composite, consistent with ASN-0047's ValidComposite★ definition. Under that reading, "K.α(a, d)" alone is a composite. But J0 (AllocationRequiresPlacement) requires that any composite producing `a ∈ dom(C') \ dom(C)` place `a` in some document's arrangement at the composite's end. K.α's frame leaves M unchanged, so J0 fails for a standalone-K.α composite — making the chain invalid as a sequence of valid composites.

The worked example (Setup section) uses a different convention: K.α, K.μ⁺, K.ρ are bundled on one line with semicolons (one composite arrow). The two sections are notationally inconsistent. For the D-DISCR proof to go through, K.α must be bundled with the immediately-following K.μ⁺/K.ρ, but this bundling is invisible at the notation level.

**Required**: Either re-format Histories 1 and 2 so that K.α(a, d), K.μ⁺(d/d', v ↦ a), and K.ρ(a, d/d') share a single "→*" arrow (matching the worked example), or add a paragraph at the start of D-DISCR explicitly fixing the convention — line breaks are visual separators, composite groupings are determined by coupling requirements. Without this, the validity of each history as a sequence of valid composites under ValidComposite★ is not visible to the reader, and D-DISCR's argument leans on an unstated bundling assumption.

### Issue 2: "Informationally equivalent to R" in D-DISCR's necessity claim is informal

**ASN-0075, §Why the Provenance Relation Is Load-Bearing and Claims Introduced table**: "any conforming implementation must maintain state information equivalent to R" / "any system supporting SHOWDELETIONS must maintain a state component informationally equivalent to R".

**Problem**: D-DISCR's proof establishes only that `(C, M)` alone is insufficient — two reachable states with identical `(C, M)` differ in their DELETED/NEVER_INCLUDED classification. The leap from this negative result to "must maintain R or equivalent" requires a precise notion of equivalence. The current text leaves "informationally equivalent" unspecified, weakening the necessity claim: a reader cannot tell whether the obligation is to maintain R exactly, a graph of historical arrangements, per-document inclusion sets, or some weaker projection.

**Required**: Sharpen the necessity statement. A concrete formulation: "any system supporting SHOWDELETIONS must maintain state components C* such that, for every reachable Σ and every (a, d) with a ∈ dom(C) and d ∈ E_doc, consulting (C, M, C*) at Σ determines whether (a, d) is DELETED or NEVER_INCLUDED." This makes the obligation about predicate disambiguation rather than about R's specific form, while still being formally crisp.

### Issue 3: D-IDENT's derived consequences cite vague "foundation invariants"

**ASN-0075, §Identity Preservation**: "Link survival. By foundation invariants on link endsets, links attach to I-addresses. If a is in dom(L)'s endsets..."

**Problem**: "Foundation invariants on link endsets" is not a specific citation. Each of D-IDENT's three derived consequences (link survival, transclusion integrity, origin attribution) should name the invariant being invoked. Origin attribution cites S7 (ASN-0036) explicitly; the other two do not. This makes one-third of the derivation rigorous and two-thirds gestural.

**Required**: Cite specific invariants for each consequence:
- Link survival → ASN-0047 L3 (NEndsetStructure) together with the L definition (link store maps to endset tuples whose entries are spans over I-addresses); P3 (ArrangementMutabilityOnly) preserves L across all transitions.
- Transclusion integrity → ASN-0036 S2 (ArrangementFunctionality) and S3★ (ASN-0047, GeneralizedReferentialIntegrity) — arrangements reference I-addresses by tumbler identity; S0/P0 (ContentImmutability/ContentPermanence) prevents tampering with the referenced values.
- Origin attribution → ASN-0036 S7 (already cited correctly).

This converts the derivation from "the property holds because of unspecified foundation facts" into a verifiable chain.

### Issue 4: K.α-uniformity argument cites GlobalUniqueness for a property GlobalUniqueness does not establish

**ASN-0075, §Why the Provenance Relation Is Load-Bearing**: "By K.α's first-emission rule (`{a' ∈ dom(C) : origin(a') = d} = ∅` initially), the allocated address is determinately `a = [d.0.s_C.1]`. By GlobalUniqueness (ASN-0034) applied to identical allocator firings, the same address value `a` appears in both histories."

**Problem**: GlobalUniqueness (ASN-0034) states that *distinct* allocation events in a single system trace produce *distinct* addresses. It does not state that identical first-emission firings across two different histories produce the same address. The property at work here is the *determinism* of K.α's first-emission rule — the value `[d.0.s_C.1]` is fixed by the rule once `d` is fixed — not GlobalUniqueness.

**Required**: Replace the GlobalUniqueness citation with a direct appeal to the K.α first-emission rule's determinism. The argument is just: K.α's first-emission rule determines the allocated address as a function of d alone; both histories pass the same d to the first-emission predicate; therefore the rule yields the same value in both. No cross-history uniqueness theorem is needed.

## OUT_OF_SCOPE

None. The ASN's stated open questions all belong to future ASNs (n-way comparison, concurrency, link-subspace deletion analysis, restoration mechanics) and are correctly framed as open.

VERDICT: REVISE
