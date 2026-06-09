# Review of ASN-0120

## REVISE

### Issue 1: "content addresses have `#E = 2`" is the load-bearing fact, but only `#E ≥ 2` is cited

**ASN-0120, "What the endset arguments name..." (ML1/ML2 derivation)**: "The extra coverage points — the tumblers lying in a resolved address's subtree but strictly below it — are never content: every content address sits on a sub-allocator chain `A_C(d)` with element-field depth `#E = 2` (ASN-0093, C1b and ChainDiscipline), whereas a proper descendant of such an address has `#E ≥ 3`, so it lies on no content chain and is not in `dom(Σ.C)`."

**Problem**: The exclusion of descendants from `dom(Σ.C)` requires that *every* content address has `#E = 2` *exactly*. The cited C1b (ContentElementFieldDepth, ASN-0093) gives only `#E(a) ≥ 2`. With `#E ≥ 2` alone, a content address could have `#E = 3`, and then a `#E = 3` descendant of a resolved address could be content — breaking `coverage(e_j) ∩ dom(Σ.C) = ρ(R_j, Σ)` (ML1, ML2). The exact value `#E = 2` follows from FirstEmission (`[d.0.s_C.1]` has `#E = 2`), ChainDiscipline (`inc(·, 0)` preserves length, TA5(c)), and ChainMembershipForOrigin (every `dom(C)` entry lies on some `A_C(d)`) — none of which is C1b. This same exact bound silently underwrites ML8's survivability framing: it is what guarantees no *future*-allocated content can enter a recorded endset's coverage surplus, so that `coverage(e_j) ∩ dom(Σ''.C) = ρ(R_j, Σ)` persists across later states.

**Required**: Cite FirstEmission + ChainDiscipline + ChainMembershipForOrigin (ASN-0093) for the exact `#E = 2`, and state explicitly that this exactness is what keeps both the creation-state equality (ML1/ML2) and its persistence under later K.α allocation (ML8) intact.

### Issue 2: ML6 claims MAKELINK can create L9-ghost types, but `ρ`-resolution forbids it

**ASN-0120, "Three endsets..." (ML6) and Claims table**: "So the type may even reference a region where nothing is stored (a ghost type, L9), because what the system records and compares is the address, not its content." / Claims table ML6: "type-by-address admits ghost types."

**Problem**: The type argument is resolved by the same procedure as from/to (ML3): `ρ(R₃, Σ) ⊆ dom(Σ.C)`, and ML6 itself *requires* `ρ(R₃, Σ) ≠ ∅`. So the type endset's *resolved* addresses are always active content in `dom(Σ.C)`. MAKELINK therefore structurally **cannot** produce an L9 ghost type — L9 (TypeGhostPermission) is precisely a type endset whose referenced address lies *outside* `dom(Σ.C) ∪ dom(Σ.L)`. The only "unstored" tumblers in `coverage(e₃)` are the subtree-surplus descendants, which are an artifact of the unit-span representation, not an L9-permitted ghost reference. The claim as written contradicts the operation's own resolution constraint and precondition.

**Required**: Either drop the L9-ghost claim for MAKELINK, or restate it precisely: MAKELINK's type always resolves to stored content; the only unstored addresses in the type's coverage are surplus descendants, and MAKELINK does not exercise L9's general ghost-type permission (which would require a type reference the operation cannot mint via `ρ`).

## OUT_OF_SCOPE

### Topic 1: Endset-internal run ordering, empty from/to semantics, link-subspace endsets, no-document discoverability
**Why out of scope**: These are correctly deferred in Open Questions — ordering observability, empty non-type endset meaning, links-pointing-at-links, and orphan/resurrection conditions are each new territory, not defects in the present coordinate-conversion specification.

VERDICT: REVISE
