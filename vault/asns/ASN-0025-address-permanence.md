# ASN-0025: Address Permanence

*2026-03-07*

We are looking for the invariant that captures address permanence — the guarantee that once content receives an address, the meaning of that address is fixed for all subsequent states of the system. ASN-0001 states this compactly as T8: if tumbler `a` is assigned to content `c`, then `a` remains assigned to `c` in every later state. Here we unfold that guarantee into its full operational meaning: which operations may extend the address space, which may not alter it, and what structural consequences flow from the separation this forces.

## The Forced Separation

We want two properties simultaneously.

First, *permanent citation*: an address given to content today must resolve to that same content indefinitely. Links, attributions, royalty accounting, and transclusion all depend on this. Nelson states the requirement plainly: "any address of any document in an ever-growing network may be specified by a permanent tumbler address" [LM 4/19].

Second, *free editing*: users insert, delete, and rearrange content without constraint. Editing must not require coordination with anyone who has cited the document.

These conflict. Suppose addresses are positions in a sequential byte stream. An INSERT of `n` bytes at position `p` shifts every byte after `p` to a position `n` higher. A citation to position `p + 1` before the insertion now resolves to the newly inserted content — not to the original byte, which has moved to `p + n + 1`. Every insertion invalidates every subsequent citation. Under a positional scheme, permanent citation and free editing are mutually exclusive.

The resolution is forced: the system must maintain two kinds of address. One — the *I-address* — names content by identity, permanently. The other — the *V-position* — names content by its current arrangement in a document, transiently. These are distinct address spaces with opposite durability properties. I-addresses are permanent and immutable. V-positions are ephemeral and shift freely with editing. Nelson confirms: "The address of a byte in its native document is of no concern to the user or to the front end; indeed, it may be constantly changing" [LM 4/11].

This is not a design preference. It is a logical necessity. Any system that must provide both permanent citation and free editing is obligated to distinguish identity from position. T11 from ASN-0001 records this: permanence properties apply exclusively to I-space; editing shifts apply exclusively to V-space.


## State Model

We define the system state Σ with three components.

**I-space** (identity space). The I-space content function maps I-addresses to values:

    Σ.ι : IAddr ⇸ Value

where Value encompasses text bytes, structural entries (document and version orgls), and link data. The permanence arguments require only that Value is a type with decidable equality — no operation inspects or depends on the codomain beyond preserving it. We write Σ.A for dom(Σ.ι) — the set of currently allocated I-addresses. Each I-address is a tumbler satisfying T4 (hierarchical parsing) from ASN-0001; the `fields()` function extracts the originating node, user, and document from any I-address.

**Documents.** Σ.D is the set of existing document identifiers. For each d ∈ Σ.D, the document's *V-space* is a finite mapping from virtual positions to I-addresses:

    Σ.v(d) : VPos ⇸ IAddr

This mapping represents the document's current arrangement — what a user sees, in the order they see it. V-positions are tumblers in the document's virtual subspace; they shift with every editing operation.

**Well-formedness.** Every V-space entry must refer to allocated content:

    J0: (A d : d ∈ Σ.D : rng(Σ.v(d)) ⊆ Σ.A)

No document may reference an I-address that does not exist in I-space.


## The Permanence Invariant

For any state transition Σ → Σ' caused by any operation:

**P0 (I-Space Growth).** No operation shrinks I-space.

    Σ.A ⊆ Σ'.A

**P1 (Content Immutability).** No operation alters content at an existing I-address.

    (A a : a ∈ Σ.A : Σ'.ι(a) = Σ.ι(a))

P0 says the domain of Σ.ι only grows. P1 says the values at existing domain points are frozen. Together: I-space is append-only and write-once. The only way Σ'.ι may differ from Σ.ι is by having entries at new addresses in Σ'.A \ Σ.A.

From P0 ∧ P1 we derive immediately:

**P2 (No Reuse).** No I-address is ever assigned to different content.

Suppose a ∈ Σᵢ.A with Σᵢ.ι(a) = c. By P0, a ∈ Σᵢ₊₁.A. By P1, Σᵢ₊₁.ι(a) = c. Inductively, Σⱼ.ι(a) = c for all j ≥ i. Address `a` can never denote anything other than `c`.

    (A i, j : 0 ≤ i ≤ j ∧ a ∈ Σᵢ.A : Σⱼ.ι(a) = Σᵢ.ι(a))

This is T8 from ASN-0001, now derived operationally. T8 is the historical statement ("if ever assigned, stays assigned"). P0 ∧ P1 are the step-wise conditions that each operation must satisfy to maintain T8.


## Visibility and Indestructibility

Content in I-space is permanent. But content in a *document* — visible to a user — is not. We need to distinguish these.

Content at I-address `a` is *visible in document d* when some V-position maps to it:

    visible(a, d, Σ) ≡ (E p : p ∈ dom(Σ.v(d)) : Σ.v(d)(p) = a)

Content is *visible in the system* when it is visible in at least one document:

    visible(a, Σ) ≡ (E d : d ∈ Σ.D : visible(a, d, Σ))

What users call "deletion" is the removal of visibility from a single document. Content removed from every document's V-space enters the state Nelson labels "DELETED BYTES (not currently addressable, awaiting historical backtrack functions, may remain included in other versions)" [LM 4/9].

Indestructibility follows from P0: no operation shrinks I-space, so deletion modifies visibility, not existence.

**P3 (I-Space Non-Extension).** DELETE, REARRANGE, and COPY leave I-space entirely unchanged:

    Σ'.A = Σ.A ∧ Σ'.ι = Σ.ι

Among the seven operations defined here, INSERT, CREATE LINK, CREATE VERSION, and CREATE DOCUMENT are the ones that extend Σ.A with fresh addresses; all four satisfy P0 ∧ P1 (they add new entries without modifying existing ones).

The state ¬visible(a, Σ) — content allocated but invisible everywhere — is permitted. The state a ∉ Σ'.A for any a that was once in Σ.A is forbidden by P0. Thus "content at this address no longer exists anywhere in the system" is architecturally impossible. Nelson confirms: "the owner of a document may delete bytes from the owner's current version, but those bytes remain in all other documents where they have been included" [LM 4/11]. Even when no other document includes them, the bytes persist in I-space — the only question about content after deletion is not *whether* it exists (always yes) but *where* it is visible (that changes with editing).


## Operations Under Permanence

We now examine each operation's effect on Σ.ι and Σ.v. Two universal frame conditions apply to every operation.

**UF (Universal I-Frame).** Every operation preserves all existing I-space content:

    (A a : a ∈ Σ.A : Σ'.ι(a) = Σ.ι(a))

This is P1 restated as a per-operation obligation.

**UF-V (Universal V-Frame).** Every operation targeting document d leaves all other documents' V-spaces unchanged:

    (A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.v(d') = Σ.v(d'))

These two frame conditions, together with the specific postconditions below, characterize each operation's effect.


### INSERT

INSERT places new content β = β₁...βₙ into document d at V-position p.

**Preconditions.** d ∈ Σ.D; p is a valid insertion position in dom(Σ.v(d)) ∪ {next}; β is a non-empty byte sequence (n ≥ 1).

**I-space effect.** Fresh I-addresses are allocated for the new content. Let B = {b₁, ..., bₙ} be these addresses:

    Σ'.A = Σ.A ∪ B  where  B ∩ Σ.A = ∅
    (A i : 1 ≤ i ≤ n : Σ'.ι(bᵢ) = βᵢ)

Freshness (B ∩ Σ.A = ∅) is guaranteed by T9 (forward allocation): new addresses are strictly greater than all existing ones under T1. The new addresses are monotonically ordered: i < j ⟹ bᵢ < bⱼ.

**V-space effect on d.** The new content maps at positions starting at p. All V-positions at or beyond p shift forward by width n. The I-addresses of the shifted entries are unchanged — only their V-positions move. Per TA7a from ASN-0001, the shift arithmetic operates within the text subspace of V-space. Per TA7b, positions in other subspaces (e.g., links at element prefix 2.x) are unaffected.

**Verification of P0 ∧ P1.** P0: Σ.A ⊆ Σ.A ∪ B = Σ'.A. P1: for a ∈ Σ.A, since a ∉ B (freshness), the extension to B does not touch Σ.ι(a). Both hold.

**J0 preservation.** The new V-entries map positions to addresses in B. Since B ⊆ Σ'.A, these are allocated. Shifted V-entries retain their original I-addresses, which are in Σ.A ⊆ Σ'.A. J0 holds.

Gregory confirms the mechanism: `inserttextgr` calls `findisatoinsertgr` to compute the next available I-address as max+1, then `insertseq` creates a new bottom crum storing the content bytes. The V-space shift in `makegappm` applies `tumbleradd` exclusively to `dsas[V]`; the I-dimension `dsas[I]` is never an operand of any arithmetic in the shift path (Q13). The dimensional isolation is structural per TA8.


### DELETE

DELETE removes a V-span from document d.

**Preconditions.** d ∈ Σ.D; the target span exists in dom(Σ.v(d)).

**I-space effect.** None.

    Σ'.A = Σ.A  ∧  Σ'.ι = Σ.ι

**V-space effect on d.** The mappings in the deleted span are removed. Subsequent V-positions shift backward to close the gap. The I-addresses of shifted entries remain unchanged.

**J0 preservation.** Remaining V-entries retain their original I-addresses, all in Σ.A = Σ'.A. J0 holds.

Gregory confirms: `dodeletevspan` calls `deletevspanpm`, which operates solely on the POOM — the V→I mapping tree. No function in the delete path touches the granfilade (Q11). The `strongsub` exponent guard ensures that V-positions in higher subspaces (links at 2.x) are not affected by text deletion — the guard fires and the crum field is literally untouched through pointer aliasing (Q16). This is the implementation mechanism behind TA7b.


### REARRANGE

REARRANGE permutes content within document d.

**Preconditions.** d ∈ Σ.D; the source and target spans are valid in dom(Σ.v(d)).

**I-space effect.** None.

    Σ'.A = Σ.A  ∧  Σ'.ι = Σ.ι

**V-space effect on d.** V-positions change, but the multiset of I-addresses is preserved:

**P4 (Rearrangement Content Invariance).**

    (A a : a ∈ Σ.A : #{p ∈ dom(Σ'.v(d)) : Σ'.v(d)(p) = a}
                    = #{p ∈ dom(Σ.v(d))  : Σ.v(d)(p)  = a})

No I-address gains or loses visibility in d through rearrangement; only the V-positions change.

**J0 preservation.** The multiset of I-addresses is unchanged (P4), so rng(Σ'.v(d)) = rng(Σ.v(d)) ⊆ Σ.A = Σ'.A. J0 holds.

Gregory notes a subtlety: when `slicecbcpm` splits a POOM bottom crum that straddles a cut boundary, the I-displacement and I-width of the resulting halves are recomputed through exact integer tumbler arithmetic. The move step (phase 2) does not touch I-fields at all; the reconstruction occurs only at slice boundaries and relies on an unverified assumption that V-width equals I-width in POOM bottom crums (Q14).


### COPY (Transclusion)

COPY places content into document d by reference to existing I-space content at V-position p. This is the transclusion primitive.

**Preconditions.** d ∈ Σ.D; the source I-addresses S ⊆ Σ.A; p is a valid insertion position in dom(Σ.v(d)) ∪ {next}. The precondition S ⊆ Σ.A is essential — COPY references existing content, not yet-to-be-allocated content.

**I-space effect.** None. No new I-addresses are allocated. No content is duplicated.

    Σ'.A = Σ.A  ∧  Σ'.ι = Σ.ι

**V-space effect on d.** New V-positions map to *the same I-addresses* as the source content. Existing V-positions at or beyond p shift forward by the width of the transcluded span; their I-address mappings are unchanged — the shift is structurally parallel to INSERT. If the source span in document d' covers I-addresses S ⊆ Σ.A, then after COPY:

**P5 (Transclusion Identity).**

    (A a : a ∈ S : visible(a, d, Σ'))

The "copy" is virtual — a V-space reference to existing I-space content, not a duplication. Nelson: "Bytes native elsewhere have an ordinal position in the byte stream just as if they were native to the document. Non-native byte-spans are called inclusions or virtual copies" [LM 4/11]. Combined with UF-V, the source I-addresses remain visible in d' as well. Both documents see the same content through the same I-addresses.

**J0 preservation.** The new V-entries map to addresses in S ⊆ Σ.A = Σ'.A. Shifted V-entries retain their original I-addresses, also in Σ.A. J0 holds.

Gregory confirms: when copied I-addresses are contiguous with an existing POOM entry, `isanextensionnd` extends the entry's width without touching its I-displacement. The displacement is preserved identically; only the width grows (Q18).


### CREATE VERSION

Creating a new version produces a new document d' whose V-space initially mirrors document d.

**Preconditions.** d ∈ Σ.D.

**I-space effect.** CREATE VERSION allocates a fresh document address for the new version's orgl (structural entry). Let `o` be this address:

    Σ'.A = Σ.A ∪ {o}  where  o ∉ Σ.A

Gregory confirms: `docreatenewversion` calls `createorglingranf`, which allocates a GRANORGL entry via `findisatoinsertnonmolecule`. For the user's own document, the orgl address is structurally subordinate to the source (e.g., document `1.1.0.1.0.1` yields version address `1.1.0.1.0.1.0.1`). For another user's document, the orgl is allocated in the creating user's account namespace, mirroring `docreatenewdocument`. In both cases, the new version shares the original's *content* I-addresses — `docopyinternal` copies existing I-addresses via `insertpm` without allocating new content entries.

**V-space effect.** A new document d' appears in Σ'.D with initial V-space mapping to the same I-addresses as Σ.v(d). The two V-spaces are thenceforth independent — this follows from UF-V: since every editing operation targets a single document, UF-V guarantees Σ'.v(d') = Σ.v(d') for all d' ≠ d. No separate property is required.

**Verification of P0 ∧ P1.** P0: Σ.A ⊆ Σ.A ∪ {o} = Σ'.A. P1: o ∉ Σ.A, so the extension does not touch Σ.ι at existing addresses. Both hold.

**J0 preservation.** Σ'.v(d') mirrors Σ.v(d), so rng(Σ'.v(d')) = rng(Σ.v(d)) ⊆ Σ.A ⊆ Σ'.A by J0 for d and P0. J0 holds for d'. For d itself, Σ'.v(d) = Σ.v(d) (the original is unchanged), so J0 for d is inherited.

Gregory provides detailed evidence for structural independence: `docreatenewversion` allocates a fresh POOM root via `createenf(POOM)`, then populates it with new crums via `insertpm`. Each crum is freshly heap-allocated by `createcrum` → `eallocwithtag`. All I-address data is copied by value through `movetumbler` (a C struct assignment). No pointer aliasing exists between the original and new document's POOM trees (Q17). In-place mutation of either tree cannot affect the other.


### CREATE LINK

Creating a link allocates new I-space content in the link subspace and places it in a specific document's V-space.

**Preconditions.** h ∈ Σ.D (the *home document* — where the link resides); the endsets reference valid I-addresses (all endpoint addresses ⊆ Σ.A). Nelson requires the home document to be specified explicitly: "The document must be specified because that determines the actual residence of the link — since a document may contain a link between two other documents" [LM 4/63]. The home document determines ownership, not destination: "A link need not point anywhere in its home document" [LM 4/12].

**I-space effect.** A new I-address `l` is allocated in the link subspace (element field 0.2.x), disjoint from text content (0.1.x) by T7 (subspace disjointness):

    Σ'.A = Σ.A ∪ {l}  where  l ∉ Σ.A

**V-space effect on h.** The link is placed at the next available position in h's link subspace (element prefix 2.x). Existing V-entries in h are unchanged — link entries are appended sequentially in creation order and are not subject to the V-position shifts that text editing produces. Per TA7b, this insertion in the link subspace does not affect text positions in h. Per UF-V, no other document's V-space is modified.

Gregory confirms: `docreatelink` calls `findnextlinkvsa` on the home document to compute the V-position, then `docopy` to insert the link's I-address into that document's POOM at V-address 2.x. The first link goes to 2.1; subsequent links append at the end of the 2.x extent. Endpoint documents receive no POOM modifications — only the home document is written (Q15).

**Verification of P0 ∧ P1.** P0: Σ.A ⊆ Σ.A ∪ {l} = Σ'.A. P1: l ∉ Σ.A, so the extension does not touch Σ.ι at existing addresses. Both hold.

**J0 preservation.** The new V-entry in h maps a position in the 2.x subspace to l ∈ Σ'.A. Existing V-entries in h retain their original I-addresses, all in Σ.A ⊆ Σ'.A. J0 holds unconditionally.

**Frame condition on text I-space.** The link allocation does not affect the text allocator. Gregory confirms: `findisatoinsertmolecule` uses `atomtype` to bound its search — text searches below `docisa.0.2`, links search below `docisa.0.3`. The two subspaces are invisible to each other's allocators (Q15).


### CREATE DOCUMENT

CREATE DOCUMENT allocates a fresh document with no source.

**Preconditions.** The creating user's account address exists in Σ.

**I-space effect.** A fresh document address `o` is allocated in the creating user's account namespace:

    Σ'.A = Σ.A ∪ {o}  where  o ∉ Σ.A

Gregory confirms: `docreatenewdocument` calls `createorglingranf`, which dispatches to `findisatoinsertnonmolecule`. This allocates exactly one GRANORGL entry — the document's orgl address — computed as max+1 under the user's account prefix (e.g., `account.0.1` for the first document, `account.0.N` for the Nth). No content atoms are allocated; no DOCISPAN entries are created.

**V-space effect.** A new document d appears in Σ'.D with an empty V-space:

    dom(Σ'.v(d)) = ∅

The POOM enfilade is initialized by `createenf(POOM)` with a bare root whose width is zero (`cwid.dsas[V] = 0`). No content exists until a subsequent INSERT.

**Verification of P0 ∧ P1.** P0: Σ.A ⊆ Σ.A ∪ {o} = Σ'.A. P1: o ∉ Σ.A, so the extension does not touch Σ.ι at existing addresses. Both hold.

**J0 preservation.** dom(Σ'.v(d)) = ∅, so rng(Σ'.v(d)) = ∅ ⊆ Σ'.A. J0 holds vacuously.

Note that CREATE DOCUMENT is not a special case of CREATE VERSION. CREATE VERSION requires d ∈ Σ.D — an existing source document whose V-space is mirrored. CREATE DOCUMENT has no source; the new document's V-space is empty.


### Worked Example: INSERT

We verify the invariants against a concrete scenario. Let document d have V-space:

    Σ.v(d) = {1 ↦ a₁, 2 ↦ a₂, 3 ↦ a₃}

where Σ.A = {a₁, a₂, a₃} with Σ.ι(a₁) = 'H', Σ.ι(a₂) = 'i', Σ.ι(a₃) = '!'. INSERT byte 'X' at V-position 2 in d. A fresh I-address b₁ is allocated with b₁ ∉ Σ.A.

After the operation:

    Σ'.A = {a₁, a₂, a₃, b₁}
    Σ'.ι = Σ.ι ∪ {b₁ ↦ 'X'}
    Σ'.v(d) = {1 ↦ a₁, 2 ↦ b₁, 3 ↦ a₂, 4 ↦ a₃}

Verification:

- **P0:** Σ.A = {a₁, a₂, a₃} ⊆ {a₁, a₂, a₃, b₁} = Σ'.A.
- **P1:** Σ'.ι(a₁) = 'H' = Σ.ι(a₁); Σ'.ι(a₂) = 'i' = Σ.ι(a₂); Σ'.ι(a₃) = '!' = Σ.ι(a₃). No existing mapping changed.
- **J0:** rng(Σ'.v(d)) = {a₁, b₁, a₂, a₃} ⊆ {a₁, a₂, a₃, b₁} = Σ'.A.
- **V-shift:** Positions 2, 3 shifted to 3, 4; their I-addresses (a₂, a₃) unchanged.

Content at a₁ ('H') remains at V-position 1. The newly inserted 'X' at b₁ occupies V-position 2. The original content at a₂ ('i') and a₃ ('!') shifted from positions 2, 3 to positions 3, 4 — their I-addresses and content values are undisturbed. The document reads "HXi!" at positions 1–4, but the permanent I-address of each original byte is unchanged.


## Content Identity

The permanence invariant ensures that an I-address always refers to the same content. But we must also ask: when do two pieces of content share the same I-address?

**P7 (Creation-Based Identity).** Content identity is determined by *creation*, not by *value*. We derive this from existing machinery rather than assert it independently.

A *creation event* is a single invocation of an I-space-extending operation — INSERT, CREATE LINK, CREATE VERSION, or CREATE DOCUMENT. Each creation event allocates addresses within a single allocator's prefix.

*Distinct creation events produce distinct addresses.* By T9 (forward allocation), successive allocations within one allocator are strictly monotonically increasing. By T10 (partition independence), allocators with distinct ownership prefixes produce non-overlapping addresses. By GlobalUniqueness (ASN-0001), no two distinct allocations anywhere in the system produce the same address. Therefore if two creation events are distinct, their allocated address sets are disjoint.

*A shared I-address traces to a single creation event.* This is the contrapositive: if addresses coincide, the allocations are not distinct.

Two consequences follow.

*Independent creation produces distinct addresses.* If two users independently type identical text, the resulting bytes receive different I-addresses — the allocations occur under different ownership prefixes (T4 guarantees different document fields), so T10 yields disjoint addresses. The content is textually identical but structurally unrelated.

*Transclusion preserves the original address.* When COPY places content from document d' into document d, no new I-addresses are allocated (P3: COPY leaves I-space unchanged). The copied bytes retain the I-addresses of their origin in d'. The `fields()` function applied to any transcluded byte's I-address returns the home document — the document where the byte was originally created, not the document where it is currently viewed.

Nelson makes attribution a structural consequence: "You always know where you are, and can at once ascertain the home document of any specific word or character" [LM 2/40]. This is not metadata attached to content — it is an intrinsic property of the I-address itself, computable by `fields()` as defined in ASN-0001. By P1, the encoding never changes.

The creation-based identity principle means that content equality (Σ.ι(a) = Σ.ι(b)) does not imply address equality (a = b). Nor does address inequality imply content inequality. The I-address is a *provenance* identifier: it records where, when, and by whom a byte was created.


## Structural Consequences

The invariants P0–P5, P7, and the frame conditions UF/UF-V, composed, provide four system-level guarantees.

**Link survivability.** The state model Σ does not model link internal structure — the representation of endsets and their reference targets belongs to a future link ASN. We observe, however, that Nelson's design requires link endpoints to reference I-space addresses: "links between bytes can survive deletions, insertions and rearrangements, if anything is left at each end" [LM 4/43]. Gregory confirms this: `insertendsetsinspanf` indexes endpoint I-addresses, not V-positions, in the spanfilade. If link endsets reference I-space addresses — as both the design intent and the implementation indicate — then P0 ∧ P1 guarantee survivability: those I-addresses are permanent (P0) and their content immutable (P1), so no editing operation (which modifies only V-space, or extends I-space without altering existing entries) can cause a link's endpoint to refer to different content. The derivation is conditional on the premise that endsets reference I-space; formalizing that premise is the link ASN's responsibility.

**Attribution.** By T4, the I-address structurally encodes the originating document via `fields()`. By P1, this encoding is immutable — the I-address itself never changes. By P7, only the original creation event produces that I-address. Attribution of content to its originating document is therefore permanent, structural, and unforgeable — it follows from the address type (T4), content immutability (P1), and creation uniqueness (P7), without requiring any additional attribution mechanism in Σ.

**Correspondence.** Versions share I-space content (by CREATE VERSION). The system identifies matching parts across versions by shared I-addresses — not by textual comparison. This requires P0 (shared addresses persist across all subsequent states) and CREATE VERSION's V-space mirroring postcondition (rng(Σ'.v(d')) = rng(Σ.v(d)) at creation). Nelson: "a facility that holds multiple versions of the same material... can show you, word for word, what parts of two versions are the same" [LM 2/20].

**Transclusion integrity.** COPY shares I-addresses across documents. By P1, every document referencing the same I-address sees the same byte value. Divergence is impossible: Σ.ι is a function, so two lookups of the same argument yield the same result. There is no mechanism by which transcluded content could become stale, outdated, or inconsistent with its source.


## Location Transparency

**P8 (Provenance, Not Location).** No component of the tumbler type IAddr encodes or constrains current physical storage location. The node field, extracted by `fields()` per T4, records the *originating node* — where the content was created — not where it currently resides. By P1, this provenance encoding is immutable: the node field at creation time is the node field for all subsequent states.

This is a property of the type definition. The tumbler `1.1.0.1.0.1.0.42` records that the content was created at node 1, by user 1, in document 1, at element position 42. No field records current hosting location. Resolution — mapping an I-address to a physical location — is the system's responsibility, not the address's burden.

Nelson specifies the operational consequence through the BEBE protocol: "The contents can slosh back and forth dynamically" [LM 4/72]. Content migrates between servers "for more rapid access to final material," "for rebalance in keeping with demand," and "for redundancy and backup purposes" [LM 4/71]. In the abstract model, Σ.ι maps I-addresses to values with no notion of physical location. A conforming implementation may store content wherever it wishes, so long as the mapping Σ.ι is maintained.


## Implementation Evidence: The Provenance Witness

The implementation maintains a secondary index — the spanfilade — that records which documents have incorporated which I-address ranges. This index independently witnesses the permanence guarantee at the implementation level. The spanfilade is not part of the abstract state model Σ; the observations below are implementation evidence, not model properties.

**Provenance Monotonicity.** Spanfilade DOCISPAN entries are append-only. No operation removes or modifies an existing entry.

DOCISPAN entries record (ISpan → DocId) — I-address ranges, not V-positions. They are therefore immune to all V-space mutations. Gregory confirms: no `deletespanf` or `modifyspanf` function exists in the implementation. REARRANGE and DELETE call no spanfilade function. Only INSERT and COPY add new entries (Q19).

The consequence: even after content is deleted from every document's V-space, the DOCISPAN entries testify that the content once belonged to those documents. The spanfilade is a permanent provenance record, consistent with P0 (content persists in I-space) and P3 (deletion is V-space only). Whether the abstract specification requires such a provenance index — and if so, what state component it demands — remains an open question.


## Implementation Commentary: The Durability Boundary

The abstract specification requires P0 ∧ P1 for every state transition Σ → Σ'. A conforming implementation providing operation-level durability (e.g., through write-ahead logging) satisfies this directly. The following documents a known limitation of one implementation, not a property of the abstract model.

The udanax-green implementation maintains I-space in memory and flushes to disk only at checkpoints: session exit, idle periods, or signal handling. If the process terminates between an INSERT (which allocates an I-address in memory) and the next disk flush, the allocation is lost. On restart, the I-address allocator — which computes max(current tree) + 1 — produces the same address for new, different content (Q12).

In effect, P0 and P1 hold unconditionally over the sequence of *committed* (durably persisted) states. Between commit points, they hold within a session but may be violated across a crash boundary.

Gregory's evidence is precise: `findisatoinsertmolecule` computes addresses from the current in-memory tree. `writeenfilades()` is the only function that persists to disk, called on clean exit or idle. There is no write-ahead log, no per-operation fsync, no crash recovery protocol (Q12). Within a session, run-to-completion scheduling guarantees that no other session observes an incomplete INSERT — the I-address and its content bytes are atomically present together in the in-memory state (Q20). Across a crash, only committed state survives.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| Σ.ι | ι : IAddr ⇸ Value — I-space content function (Value covers bytes, orgls, link data) | introduced |
| Σ.A | A = dom(ι) — set of allocated I-addresses | introduced |
| Σ.v | v : DocId → (VPos ⇸ IAddr) — per-document V-space mappings | introduced |
| J0 | (A d ∈ Σ.D : rng(Σ.v(d)) ⊆ Σ.A) — V-space references only allocated content | introduced |
| P0 | Σ.A ⊆ Σ'.A — I-space only grows | introduced |
| P1 | (A a ∈ Σ.A : Σ'.ι(a) = Σ.ι(a)) — existing content immutable | introduced |
| P2 | No I-address ever reassigned to different content (from P0 ∧ P1) | derived (from P0 ∧ P1) |
| P3 | DELETE, REARRANGE, COPY leave I-space unchanged: Σ'.A = Σ.A ∧ Σ'.ι = Σ.ι | introduced |
| P4 | REARRANGE preserves the multiset of visible I-addresses per document | introduced |
| P5 | COPY makes source I-addresses visible in target without new allocation | introduced |
| P7 | Content identity determined by creation event, not byte value | derived (from T9, T10, GlobalUniqueness, P3) |
| P8 | No component of IAddr encodes current physical location; node field records originating provenance | introduced |
| UF | Every operation preserves existing I-space content (= P1 per-operation) | introduced |
| UF-V | Every operation on document d leaves Σ.v(d') unchanged for d' ≠ d | introduced |


## Open Questions

- Must the system provide a mechanism (historical backtrack) to make invisible content visible again, or is mere existence in I-space sufficient for the permanence guarantee?
- What constraints does P0 impose on storage reclamation — may a conforming implementation garbage-collect I-space content that is invisible in all documents and unreachable by any link?
- Must the permanence guarantee extend across administrative boundaries such as server decommissioning or vendor transitions?
- What durability granularity must a conforming implementation provide — is session-level commit sufficient, or must each operation be individually durable?
- Does the creation-based identity principle (P7) apply to link content with the same force as to text content?
- If content becomes invisible in all documents, must links pointing to those I-addresses still resolve, and what does resolution mean for invisible content?
- Must the system distinguish between content that was never visible in a given document and content that was once visible but has been deleted from that document?
