# Review of ASN-0075

## REVISE

### Issue 1: D-IDENT "Link survival" overstates where link spans anchor
**ASN-0075, Identity Preservation (D-IDENT), "Link survival" bullet**: "every link in `dom(L)` references content via endsets — each endset is a set of spans (Shared Vocabulary), and each span is anchored at an I-address start in `dom(C)`."

**Problem**: This is a false universal. Per the Shared Vocabulary, an endset references Istream addresses generally, and a span's start tumbler may be a link address (`dom(L)`) — link-to-link references are permitted. So "each span is anchored at an I-address start in `dom(C)`" does not hold for every span of every link. The load-bearing point (the content address `a` survives, and any span anchored at `a` continues to reference `a`) is correct, but the blanket claim about *all* spans is wrong.

**Required**: Qualify the statement to the spans that actually anchor at `a`: "a span anchored at the content address `a` continues to reference the same `a`," dropping the universal assertion that every link span starts in `dom(C)`.

### Issue 2: Foundation predicate `Element` renamed to `IsElement`
**ASN-0075, Foundation Recap**: "where `T_elem = {a ∈ T : IsElement(a)} ⊆ T`."

**Problem**: ASN-0047 (foundation) defines this set as `T_elem = {a ∈ T : Element(a)}`, using the predicate `Element(·)` (also used in `Σ.E`'s `¬Element(e)` clause and K.ρ's level constraint). ASN-0075 reintroduces the same concept under a new name `IsElement(·)`. Per the self-containment standard, an ASN should use the foundation's notation rather than reinvent it; the rename invites drift between the two predicates.

**Required**: Use `Element(a)` as defined in ASN-0047, or drop the restated definition entirely and cite the foundation's `T_elem`.

## OUT_OF_SCOPE

### Topic 1: Restoration operation mechanics
**Why out of scope**: The "Composability with Restoration" section correctly limits itself to noting that the output *form* makes restoration possible without specifying any restoration transition. A restoration operation is genuinely new territory for a later ASN, not a gap in this one.

### Topic 2: Three-document and concurrent-snapshot generalizations
**Why out of scope**: The Open Questions on multi-document witness structure and concurrent-transition consistency models are future ASN material; their absence is not an error here.

VERDICT: REVISE
