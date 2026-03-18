# ASN-0025 Formal Statements

*Source: ASN-0025-address-permanence.md (revised 2026-03-07) — Index: 2026-03-07 — Extracted: 2026-03-07*

## Definition — ISpaceContentFn

    Σ.ι : IAddr ⇸ Value

    where Value encompasses text bytes, structural entries (document and version orgls), and link data.

## Definition — AllocatedAddresses

    Σ.A = dom(Σ.ι)

## Definition — DocumentId

    DocId = IAddr

## Definition — DocumentSet

    Σ.D ⊆ Σ.A

## Definition — VSpaceMap

    Σ.v(d) : VPos ⇸ IAddr

## Definition — VPos

    VPos = {text, link} × ℕ⁺

    A V-position q = (S, x) pairs a subspace tag S with a positive ordinal x.
    tag(q) = S
    ord(q) = x
    text(q) ≡ tag(q) = text
    link(q) ≡ tag(q) = link

    Ordering: q < q' is defined only when tag(q) = tag(q'), and means ord(q) < ord(q').

## Definition — VPosShiftAdd

    q ⊕ [n] = (tag(q), ord(q) + n)

## Definition — VPosShiftSub

    q ⊖ [n] = (tag(q), ord(q) − n)

## Definition — NextTextPos

    next(d, Σ) = max({q ∈ dom(Σ.v(d)) : q is a text position}) ⊕ [1]
                 when text positions exist,
               = [1] (in text subspace context)
                 when none exist.

## Definition — NextLinkPos

    next_link(d, Σ) = max({q ∈ dom(Σ.v(d)) : q is a link position}) ⊕ [1]
                      when link positions exist,
                    = [1] (in link subspace context)
                      when none exist.

## Definition — VisibleInDoc

    visible(a, d, Σ) ≡ (E p : p ∈ dom(Σ.v(d)) : Σ.v(d)(p) = a)

## Definition — VisibleInSystem

    visible(a, Σ) ≡ (E d : d ∈ Σ.D : visible(a, d, Σ))

---

## J0 — VSpaceGrounded (INV, predicate(State))

    (A d : d ∈ Σ.D : rng(Σ.v(d)) ⊆ Σ.A)

## J1 — TextContiguity (INV, predicate(State))

    (A d : d ∈ Σ.D : {ord(q) : q ∈ dom(Σ.v(d)) ∧ q is a text position} = {1, ..., |text positions in d|})

    where the right-hand side is the empty set when the count is zero.

## J2 — LinkContiguity (INV, predicate(State))

    (A d : d ∈ Σ.D : {ord(q) : q ∈ dom(Σ.v(d)) ∧ q is a link position} = {1, ..., |link positions in d|})

    where the right-hand side is the empty set when the count is zero.

## P0 — ISpaceGrowth (INV, predicate(State, State))

    Σ.A ⊆ Σ'.A

## P1 — ContentImmutability (INV, predicate(State, State))

    (A a : a ∈ Σ.A : Σ'.ι(a) = Σ.ι(a))

## P2 — NoReuse (LEMMA, lemma)

Derived from P0 ∧ P1.

    (A i, j : 0 ≤ i ≤ j ∧ a ∈ Σᵢ.A : Σⱼ.ι(a) = Σᵢ.ι(a))

Proof sketch: By P0, a ∈ Σᵢ.A implies a ∈ Σᵢ₊₁.A. By P1, Σᵢ₊₁.ι(a) = Σᵢ.ι(a). Inductively, Σⱼ.ι(a) = Σᵢ.ι(a) for all j ≥ i.

## P6 — DocumentSetGrowth (INV, predicate(State, State))

    Σ.D ⊆ Σ'.D

## P3 — ISpaceNonExtension (FRAME, ensures)

Applies to DELETE, REARRANGE, COPY.

    Σ'.A = Σ.A ∧ Σ'.ι = Σ.ι

## UF — UniversalIFrame (FRAME, ensures)

Applies to every operation. Equivalent to P1 restated as a per-operation obligation.

    (A a : a ∈ Σ.A : Σ'.ι(a) = Σ.ι(a))

## UF-V — UniversalVFrame (FRAME, ensures)

Applies to every operation targeting document d.

    (A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.v(d') = Σ.v(d'))

For CREATE VERSION and CREATE DOCUMENT, the target is the newly created document d'; UF-V then covers all pre-existing documents in Σ.D.

## P4 — RearrangementContentInvariance (POST, ensures)

Applies to REARRANGE.

    (A a : a ∈ Σ.A : #{p ∈ dom(Σ'.v(d)) : Σ'.v(d)(p) = a}
                    = #{p ∈ dom(Σ.v(d))  : Σ.v(d)(p)  = a})

## Domain preservation — DomainPreservation (FRAME, ensures)

Applies to REARRANGE.

    dom(Σ'.v(d)) = dom(Σ.v(d))

## Exterior frame — ExteriorFrame (FRAME, ensures)

Applies to REARRANGE. Cut positions c₁ < c₂ < ... < cₖ are text-subspace V-positions; k ∈ {3, 4}.

    (A q : q ∈ dom(Σ.v(d)) ∧ q is a text position ∧ (q < c₁ ∨ q ≥ cₖ) : Σ'.v(d)(q) = Σ.v(d)(q))

## Link-subspace frame — LinkSubspaceFrame (FRAME, ensures)

Applies to REARRANGE.

    (A q : q ∈ dom(Σ.v(d)) ∧ q is a link position : Σ'.v(d)(q) = Σ.v(d)(q))

## P5 — TransclusionIdentity (POST, ensures)

Applies to COPY. S = (s₁, ..., sₘ) is the I-address sequence of the source span, where sᵢ = Σ.v(d_s)(qᵢ).

    (A a : a ∈ S : visible(a, d, Σ'))

## P7 — CreationBasedIdentity (LEMMA, lemma)

Derived from T9, T10, GlobalUniqueness, P3.

A *creation event* is a single invocation of an I-space-extending operation — INSERT, CREATE LINK, CREATE VERSION, or CREATE DOCUMENT. Each creation event allocates addresses within a single allocator's prefix.

    (a) Distinct creation events produce disjoint address sets.
        If events e₁ ≠ e₂, then Alloc(e₁) ∩ Alloc(e₂) = ∅.

    (b) A shared I-address traces to a single creation event.
        (A a : (E e₁, e₂ : a ∈ Alloc(e₁) ∧ a ∈ Alloc(e₂) : e₁ = e₂))

    Proof sketch: By T9 (forward allocation), successive allocations within one allocator are strictly monotonically increasing. By T10 (partition independence), allocators with distinct ownership prefixes produce non-overlapping addresses. By GlobalUniqueness (ASN-0001), no two distinct allocations anywhere in the system produce the same address.

    Corollary (independent creation): If two creation events occur under different ownership prefixes, their allocated addresses are disjoint.

    Corollary (transclusion preservation): COPY places existing I-addresses into a document's V-space without new allocation (P3: Σ'.A = Σ.A). Therefore fields() applied to any transcluded byte's I-address returns the originating document, not the document where it is currently viewed.

## P8 — ProvenanceNotLocation (INV, predicate(IAddr))

Type-level property. No component of the tumbler type IAddr encodes or constrains current physical storage location.

    (A a : a ∈ Σ.A : fields(a).node = originating_node(a))

    where fields(a).node records the node at which `a` was created (per T4), and this encoding is immutable by P1:

    (A a : a ∈ Σ.A : Σ'.ι(a) = Σ.ι(a))  [P1]

    The resolution mapping (IAddr → physical location) is not a component of a or of Σ.ι.
