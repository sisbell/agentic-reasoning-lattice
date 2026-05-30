# Review of ASN-0043

## REVISE

### Issue 1: L11a discharges GlobalUniqueness's single-tree precondition with a per-document hypothesis that does not establish a common tree
**ASN-0043, L11a — LinkUniqueness**: "This is GlobalUniqueness (ASN-0034) instantiated at link addresses: its sole precondition is T10a-conformance of the events, and L1c (LinkAllocatorConformance) discharges precisely that — every `a ∈ dom(Σ.L)` is the terminus of a T10a-conforming chain."

**Problem**: GlobalUniqueness's precondition is not merely "the events conform to T10a"; it is that the events are distinct allocation events *within a single system conforming to T10a* — its proof inducts on **one** allocator tree, with the base case "sole root allocator" and the step routing pairs through a lowest common ancestor. L1c supplies, for each link address independently, a chain seeded at *its own* T4-valid document-level tumbler `s = home(a)`. For two links homed in different documents, L1c gives two chains from two different seeds and never asserts those seeds share a root or belong to one global allocator tree 𝒯. As written, L1c alone is consistent with each document's link chain being the root of a *separate* T10a tree — in which case GlobalUniqueness does not apply across the two links, and cross-document link distinctness is not established. The claim "its sole precondition is T10a-conformance of the events" understates what GlobalUniqueness requires.

**Required**: Connect the link chains to the one global tree. L9 already shows how: "By S7d on `Σ`, `d` is the terminus of a T10a-conforming allocator chain from 𝒯's root … T10a.4 propagates T4-validity." Invoke S7d (document tumblers are nodes of 𝒯) in L11a so that every link chain is a subtree of the single allocator tree, discharging GlobalUniqueness's single-tree precondition for cross-document pairs — not just per-chain T10a-conformance.

### Issue 2: L7's "Structurally." paragraph restates one claim four ways and closes with design commentary
**ASN-0043, L7 — DirectionalFlexibility, "Structurally." paragraph**: "not one of them predicates on which slot is source and which is target. They constrain slot identity solely up to positional distinctness — and a position carries no inherent orientation. L6 establishes that slots are positionally addressable, but that is sequence-position, not direction … The F/G labels in the standard triple `(F, G, Θ)` are nominal conveniences for prose …" followed by "The consequence: any system that determines a link's directionality from slot position alone … is misinterpreting the design."

**Problem**: The single load-bearing fact — no invariant predicates on direction — is stated four times in successive sentences, then re-stated a fifth time as the "consequence" paragraph, which is design exhortation ("is misinterpreting the design") rather than a property of the model. This is the essay-expansion the anti-bloat pass targets: the reader must skip restatements to reach the one assertion (the invariants quantify only over addresses, endset membership, and slot position).

**Required**: Reduce to the one assertion plus the Nelson quote; drop the redundant restatements and the "any system … is misinterpreting the design" commentary.

### Issue 3: Worked-example L12/L12a verifications are pure forward-deferral
**ASN-0043, Worked Example**: "*L12 (LinkImmutability).* L12 constrains state transitions, not individual states. In this single-state example, no transition is under consideration, so L12 is vacuously satisfied. Verified non-vacuously below across two transitions. ✓ (vacuous)" and the identical pattern for L12a.

**Problem**: Two entries in the verification list carry no object-level content — they announce vacuity and defer to the same downstream extension ("Verified non-vacuously below"). This is the flagged pattern of multiple slots deferring to one downstream location; the transition checks themselves appear later, so these two bullets add navigation noise, not verification.

**Required**: Drop the two vacuous bullets and verify L12/L12a only where they are non-vacuous (the four `Σ_i → Σ_{i+1}` transitions), or replace with a single one-line note that transition invariants are checked in the extension below.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace constant extending disjointness beyond the `s_C`-resident slice
The ASN scopes `dom(Σ.L) ∩ dom(Σ.C) = ∅` to the `s_C`-resident slice (L0a, L14, L14a) and lists the global version as an open question. Fixing a global content-subspace invariant is a strengthening of ASN-0036's content model, not a defect in this ASN's link claims.

VERDICT: REVISE
