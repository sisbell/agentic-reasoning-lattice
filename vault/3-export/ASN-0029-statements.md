# ASN-0029 Formal Statements

*Source: ASN-0029-document-ontology.md (revised 2026-03-11) — Index: 2026-03-11 — Extracted: 2026-03-11*

## Definition — AccountAddr

    AccountAddr = {a ∈ T : zeros(a) = 1}

Precisely the tumblers of the form `N.0.U` — node and user fields with no document or element fields.

## Definition — AccountPrefix

    account(d) = max≼ {a ∈ AccountAddr : a ≼ d}

where `≼` is the prefix relation from ASN-0001. Pure function of the address value; consults no mutable state.

## Definition — Actor

    actor(op) = the account address on whose behalf operation op is performed

## Definition — HomeDocument

    home(a) = max≼ {d' : zeros(d') = 2 ∧ d' ≼ a}

## Definition — DocumentLevelPrefix (≺)

    d_s ≺ d_v  iff  d_s ≼ d_v ∧ d_s ≠ d_v ∧ zeros(d_s) = zeros(d_v) = 2

## Definition — SameAllocator

    same_allocator(d₁, d₂)  iff
        (both are root documents under the same account)
        ∨ parent(d₁) = parent(d₂)

---

## AccountAddr — ValidAccountAddr (INV, predicate(Tumbler))

    AccountAddr = {a ∈ T : zeros(a) = 1}

## account — AccountPrefix (INV, function(DocId): Tumbler)

    account(d) = max≼ {a ∈ AccountAddr : a ≼ d}

---

## D0 — EmptyCreation (POST, ensures)

    pre:  a ∈ AccountAddr ∧ actor(op) = a
    post ∧ frame:
      (E d : d ∉ Σ.D ∧ d ∈ Σ'.D ∧ account(d) = a :
           |Σ'.V(d)| = 0 ∧ Σ'.pub(d) = private
         ∧ parent(d) undefined
         ∧ (A d' : d' ∈ Σ.D ∧ account(d') = a : d' < d)
         ∧ Σ'.D = Σ.D ∪ {d} ∧ Σ'.I = Σ.I
         ∧ (A d' : d' ∈ Σ.D : Σ'.V(d') = Σ.V(d') ∧ Σ'.pub(d') = Σ.pub(d')))

The existential scopes over both postcondition and frame.

---

## D1 — DocumentAllocation (INV, predicate(DocId, DocId))

Two allocator kinds per account:
- *Root allocator* for account `a`: produces root documents (single-component document field). First invocation: `inc(a, 2)` (T10a child creation, `k' = 2`). Subsequent: `inc(·, 0)` (sibling stream).
- *Child allocator* for document `d_s`: produces children via `inc(d_s, 1)` (T10a child stream, `k' = 1`).

    (A d₁, d₂ : same_allocator(d₁, d₂) ∧ allocated_before(d₁, d₂) : d₁ < d₂)

---

## D2 — DocumentPermanence (INV, predicate(State, State))

    [d ∈ Σ.D ⟹ d ∈ Σ'.D]

for every state transition Σ → Σ'.

---

## D3 — StructuralOwnership (INV, predicate(DocId))

    account(d) is computable from d's tumbler address alone, without consulting any mutable state.

By T6 (DecidableContainment, ASN-0001), whether two documents share the same owner is decidable from their addresses.

---

## D4 — OwnershipPermanence (LEMMA, lemma)

Derived from D2 and D3.

    account(d) in Σ = account(d) in Σ'

for all state transitions.

---

## D5 — OwnershipRights (INV, predicate(State, DocId))

For document `d` with owner `account(d)`:

    (a) content modification: only the owner may alter Σ.V(d)
    (b) outgoing links: only the owner may create or remove links stored in d
    (c) visibility (when private): only the owner and designated associates may access d
    (d) address subdivision: only the owner may allocate new tumblers extending d's prefix

Design requirement on correct participants, not a mechanically enforced invariant.

---

## D6 — IdentityByAddress (INV, predicate(DocId, DocId))

    d₁ = d₂  ⟺  fields(d₁) = fields(d₂)

---

## D7 — OriginTraceability (INV, function(IAddr): DocId)

    home(Σ.V(d)(p)) = max≼ {d' : zeros(d') = 2 ∧ d' ≼ Σ.V(d)(p)}

for any position `p` in any document `d`. The `max≼` is necessary: a versioned document has multiple prefixes with `zeros = 2`. Since `fields()` uniquely decomposes any I-address (T4, HierarchicalParsing), the set has a well-defined maximum.

---

## D7a — DocumentScopedAllocation (POST, ensures)

INSERT on document `d` allocates fresh I-addresses under `d`'s tumbler prefix, with the element-field separator immediately following `d`:

    (A a ∈ fresh : d ≼ a ∧ a_{#d+1} = 0 ∧ zeros(a) = 3)

where `fresh` is the set of newly allocated I-addresses per P9 (FreshPositions, ASN-0026). Each fresh address has the form `d.0.E₁...Eδ` with all `Eᵢ > 0` and `δ ≥ 1`.

---

## D7b — HomeDocumentMembership (LEMMA, lemma)

Derived from D7a, P2, D2.

    (A d ∈ Σ.D, p : 1 ≤ p ≤ n_d : home(Σ.V(d)(p)) ∈ Σ.D)

---

## D8 — InclusionNonDestruction (LEMMA, lemma)

Derived from P7 (CrossDocVIndependent, ASN-0026).

    [target(COPY) = d₂ ∧ d₁ ≠ d₂ ⟹ Σ'.V(d₁) = Σ.V(d₁)]

---

## D9 — EditIsolation (LEMMA, lemma)

Derived from P7 (CrossDocVIndependent, ASN-0026).

    [op modifies Σ.V(d₁) ∧ d₁ ≠ d₂ ⟹ Σ'.V(d₂) = Σ.V(d₂)]

---

## Σ.pub — PublicationStatus (INV, State field)

    Σ.pub : Σ.D → {private, published, privashed}

State extension; `private`, `published`, `privashed` are the three publication states.

---

## D10 — PublicationMonotonicity (INV, predicate(State, State))

    [Σ.pub(d) = published ⟹ Σ'.pub(d) = published]

for every state transition Σ → Σ'. Unconditional over all protocol operations.

---

## D10-ext — PublicationFrame (FRAME, ensures)

For any ASN-0026 operation (INSERT, DELETE, COPY, REARRANGE):

    (A d : d ∈ Σ.D : Σ'.pub(d) = Σ.pub(d))

---

## D10a — PublishOperation (POST, ensures)

    pre:  d ∈ Σ.D ∧ account(d) = actor(op) ∧ Σ.pub(d) = private ∧ status ∈ {published, privashed}
    post: Σ'.pub(d) = status
    frame: Σ'.D = Σ.D ∧ Σ'.I = Σ.I ∧ Σ'.V(d) = Σ.V(d)
         ∧ (A d' : d' ∈ Σ.D ∧ d' ≠ d : Σ'.V(d') = Σ.V(d') ∧ Σ'.pub(d') = Σ.pub(d'))

---

## D11 — PublicationSurrender (INV, predicate(State, DocId))

    Σ.pub(d) = published ⟹
        (a) any session may read d
        (b) any session may create links into d (incoming links)
        (c) any session may transclude from d (quotation)
        (d) withdrawal requires extraordinary process

---

## D12 — VersionCreation (POST, ensures)

    pre:  d_s ∈ Σ.D ∧ a_req = actor(op)
        ∧ (Σ.pub(d_s) ∈ {published, privashed} ∨ account(d_s) = a_req)
    post:
    (a) d_v ∉ Σ.D ∧ d_v ∈ Σ'.D
    (b) |Σ'.V(d_v)| = |Σ.V(d_s)|
    (c) (A p : 1 ≤ p ≤ |Σ.V(d_s)| : Σ'.V(d_v)(p) = Σ.V(d_s)(p))
    (d) Σ'.V(d_s) = Σ.V(d_s)
    (e) Σ'.I = Σ.I
    (f) Σ'.pub(d_v) = private
    (g₁) account(d_s) = a_req ⟹ (A d' : d' ∈ Σ.D ∧ parent(d') = d_s : d' < d_v)
    (g₂) account(d_s) ≠ a_req ⟹ (A d' : d' ∈ Σ.D ∧ account(d') = a_req : d' < d_v)
    frame: Σ'.D = Σ.D ∪ {d_v}
         ∧ (A d' : d' ∈ Σ.D : Σ'.V(d') = Σ.V(d') ∧ Σ'.pub(d') = Σ.pub(d'))

---

## D13 — VersionPlacement (POST, ensures)

For CREATENEWVERSION(d_s, a_req) creating d_v:

    account(d_s) = a_req  ⟹  parent(d_v) = d_s
    account(d_s) ≠ a_req  ⟹  account(d_v) = a_req ∧ parent(d_v) undefined

Own-account allocation: `inc(d_s, 1)` (T10a, `k' = 1`), preserving `zeros(d_v) = 2`. Cross-account: root allocator for `a_req`.

---

## D14 — VersionForest (INV, predicate(State))

    parent(d) = max≼ {d' ∈ Σ.D : d' ≺ d}
        (partial — undefined when {d' ∈ Σ.D : d' ≺ d} = ∅)

where `d_s ≺ d_v  iff  d_s ≼ d_v ∧ d_s ≠ d_v ∧ zeros(d_s) = zeros(d_v) = 2`.

The covering relation of `≺` restricted to `Σ.D` forms a forest. Membership invariant:

    (A d : d ∈ Σ.D ∧ parent(d) defined : parent(d) ∈ Σ.D)

---

## D14a — DocFieldWellFormed (INV, predicate(DocId))

    (A d ∈ Σ.D : let (N, U, D) = fields(d) : #D ≥ 1 ∧ (A i : 1 ≤ i ≤ #D : Dᵢ > 0))

---

## D15 — OwnerExclusiveModification (INV, predicate(State, DocId))

    [op modifies Σ.V(d)  ⟹  account(d) = actor(op)]

Design requirement on correct participants.

---

## D16 — NonOwnerForking (INV, predicate(State, DocId))

    account(d) ≠ actor(op)
    ∧ op requests modification of d
    ∧ (Σ.pub(d) ∈ {published, privashed})
    ⟹ system applies CREATENEWVERSION(d, actor(op)) with account(d_v) = actor(op)

---

## D17 — ContentBasedDiscovery (POST, ensures)

Each `(s, l) ∈ S` is well-formed per T12 (SpanWellDefined): `l > 0`, ensuring `s ⊕ l` is defined by TA0.

    FINDDOCSCONTAINING(S) =
        {d ∈ Σ.D : (E p : 1 ≤ p ≤ n_d :
                       (E (s,l) ∈ S : s ≤ Σ.V(d)(p) < s ⊕ l))}
    frame: Σ' = Σ
