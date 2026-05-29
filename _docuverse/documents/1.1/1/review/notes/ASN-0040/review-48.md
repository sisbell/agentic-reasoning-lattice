# Review of ASN-0040

## REVISE

### Issue 1: B8's postcondition is stronger than the proof establishes
**ASN-0040, B8 (Global Uniqueness), Case 1**: "*Two acts on incomparable branches share no reachable descendant; their outputs are never jointly observed, and the collision question does not arise.*"
**Problem**: The contract postcondition is unconditional — `(A a, b : produced by distinct baptismal acts : a ≠ b)`. But the proof admits that two `baptize(p, d)` edges leaving the same precondition state on incomparable branches both compute `c_{m+1}` and therefore *do* produce the same address. The proof rescues the claim only by silently restricting attention to acts lying on one transition path ("jointly observed"). The postcondition as written is false for incomparable-branch acts; the saving restriction lives in prose, not in the contract.
**Required**: Scope the B8 statement and contract to co-reachable acts (acts comparable on some path `s_init →* s`), or define "baptismal act" so branch-duplicated edges are identified. State the restriction in the postcondition, not the proof body.

### Issue 2: B7 applies T10a.6 to arbitrary B6 pairs without realizing them in one conforming tree
**ASN-0040, B7 (Namespace Disjointness), proof**: "*Distinct B6-valid pairs name distinct allocators… T10a.6 (DomainDisjointness) gives dom(A_{p,d}) ∩ dom(A_{p',d'}) = ∅.*"
**Problem**: T10a.6's precondition is "X and Y distinct allocators conforming to T10a," and its proof splits on *ancestor–descendant vs. non-ancestor–descendant* — relations defined only within a single conforming allocator tree. B6 requires only that `p` satisfy T4; it does not require `p` to arise as a domain element of any allocator, nor that two unrelated B6-valid parents `p, p'` and their spawns form one T10a-conforming tree. The identification `S(p, d) = dom(A_{p,d})` and the appeal to T10a.6 therefore presuppose a tree that is never constructed. For prefix-unrelated `p, p'` the disjointness is a pure arithmetic fact (via S1 + T1/PrefixOrderingExtension) that the proof never derives directly.
**Required**: Either establish that every B6-valid `(p, d)` is realized as an allocator in one T10a-conforming tree (and that the at-most-once / parentage constraints hold), or prove `S(p, d) ∩ S(p', d') = ∅` directly from S1 and the prefix structure, independent of T10a.6's tree framing.

### Issue 3: B6 necessity forward-references B8, which depends on B6
**ASN-0040, B6 necessity, sub-case (b), d = 1**: "*collapsing B8 (Global Uniqueness) by allowing two distinct baptisms… to deliver the same address.*"
**Problem**: B6 appears before B8 in the document. B8's proof depends on B7, and B7 depends on B6 (sufficiency). Using B8's conclusion to justify B6's necessity is a forward citation into a result that transitively rests on B6 — a circular citation chain in the prose. The necessity direction is also used by no downstream proof (all consumers use B6 sufficiency), so the dependency is gratuitous.
**Required**: Replace the appeal to "collapsing B8" with the self-contained fact already available: by S2, `S(p, 1) = S(p', 2)` for the T4-valid `(p', 2)`, so admitting `(p, 1)` produces a stream identical to a distinct B6-valid namespace. State this directly rather than routing through a later theorem.

### Issue 4: Bop frame statement triplicated with repeated component inventory
**ASN-0040, Bop**: the paragraph "*The frame condition's scope is essential. With respect to s.B, baptism is precise…*", the Formal Contract *Frame:* line, and the Properties table Bop row all repeat the same content and the same enumeration "*content, links, arrangement, ASN-0034's Act and nₛ*."
**Problem**: This is the anti-bloat pattern — the same "we modify only s.B, nothing else" claim stated three times, twice with an explicit use-site inventory of components this ASN does not touch. Two of the three carry no information the FRAME line does not.
**Required**: State the frame once (the contract *Frame:* line) and drop the prose paragraph and the table-row restatement, or compress the table row to "modifies only s.B."

### Issue 5: Repeated downstream deferral to the activation-discipline ASN
**ASN-0040, "Relationship to ASN-0034's allocated set" (stated twice) and Open Questions**: "*Whether allocated(s) ⊆ s.B holds is left to the activation-discipline ASN…*" / "*Non-emptiness… is forced externally (see Relationship to ASN-0034's allocated set above)*" / the matching Open Question.
**Problem**: Three locations defer the same `allocated(s) ⊆ s.B` question to the same future ASN — the "multiple paragraphs deferring to the same downstream location" accretion pattern. The cross-pointers ("see … above") add navigation overhead without advancing reasoning.
**Required**: Keep the single Open Questions entry; remove the in-body deferral paragraphs or reduce them to one sentence at the point `s.B` is introduced.

## OUT_OF_SCOPE

### Topic 1: B3 (Occupied predicate / content placement)
**Why out of scope**: B3 introduces `Occupied : T × 𝒮 → {⊤, ⊥}` and constrains where content may live. Content storage and retrieval are explicitly deferred (Tumbler content/I-space ASN). The ghost-element *concept* is core to baptism and belongs here, but the formal `Occupied` predicate and its placement constraint are content-storage claims; framing them as a "forward requirement" is acceptable, but the formal obligation should be owned by the content ASN, not asserted as a contract here.

VERDICT: REVISE
