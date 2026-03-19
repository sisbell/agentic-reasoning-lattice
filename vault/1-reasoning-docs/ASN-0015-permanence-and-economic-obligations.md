# ASN-0015: Permanence and Economic Obligations

*2026-02-24*

We wish to understand whether the system's permanence invariants — address
irrevocability, content immutability, publication irrevocability — are
unconditional structural guarantees or are conditioned on the continued
payment of economic obligations. The question is forced by a tension
Nelson acknowledges but does not resolve: the system promises permanent
addresses and perpetual literature, yet requires that "all services must be
self-supporting" and that storage must be "economically self-sustaining"
[LM 4/5]. If someone stops paying, what breaks?

The tension is not a design flaw to be papered over. It is a genuine
collision between two non-negotiable principles, and we must formalize
both sides before we can state what the system guarantees at the boundary.
The investigation will reveal that the system's invariants stratify into
three tiers: unconditional structural guarantees that no economic event
can disturb, contractual obligations that publication creates toward third
parties, and contingent properties that depend on someone paying for
storage. The formal specification must distinguish these tiers explicitly,
because an implementation that conflates them — that treats content
accessibility as equivalent to address permanence — will either make
promises it cannot keep or break promises it should not break.


## State Components

We need a model that captures both the structural and economic dimensions
of the system. Let Σ denote the system state, containing at least:

**EΣ1 (content store).** Σ.ispace : IAddr ⇀ Content is the permanent,
append-only content store. We take as given:

- *Permanence*: dom(Σ.ispace) ⊆ dom(Σ'.ispace) for all subsequent Σ'.
- *Immutability*: Σ'.ispace(a) = Σ.ispace(a) for all a ∈ dom(Σ.ispace).

These are the properties established by the address permanence analysis.
We do not re-derive them; we ask whether economic events can violate them.

**EΣ2 (publication status).** Σ.pub : DocId → {private, published} records
whether each document has been published. We take as given that publication
is near-permanent:

    published(d) in Σ  ⟹  published(d) in Σ'
      for all subsequent Σ', subject to extraordinary due-process exceptions

**EΣ3 (economic status).** Σ.econ : OwnerId → EconStatus records the
economic standing of each content owner, where:

    EconStatus = {current, lapsed, abandoned}

- `current`: obligations are met — storage rental is paid.
- `lapsed`: obligations are unmet — payment has ceased, but the owner
  has not been unreachable for an implementation-defined grace period.
- `abandoned`: the owner is unreachable and has not paid for a duration
  exceeding the grace period.

The progression is monotonic with respect to non-payment:
current → lapsed → abandoned. Return to `current` is possible from
`lapsed` (by resuming payment) but the transition from `abandoned` back
to `current` is an implementation decision we do not constrain here.

**EΣ4 (accessibility).** Σ.accessible : IAddr → {accessible, withheld}
records whether content at a given I-space address is currently deliverable
to requestors. This is a new state component — one that the purely
structural analysis did not need, but that the economic analysis demands.
The distinction between "exists" and "can be served" is precisely where
the two principles collide.

We do not model a `destroyed` state. The append-only architecture
precludes destruction of I-space content. Content may be withheld; it
may not be annihilated.

**EΣ5 (identity encoding).** For every I-space address a ∈ dom(Σ.ispace),
the function creator(a) extracts the owner identity from the address
itself:

    creator(a) = (THE u : u ∈ Σ.accounts : prefix(u, a))

This is a structural derivation, not a lookup. The owner's account
address is a prefix of every I-space address allocated under that account.
We state it explicitly because it will be central to the permanence of
attribution and economic structures.

**EΣ6 (royalty structure).** Σ.royalty : IAddr → OwnerId records, for each
I-space address, the identity of the party to whom per-byte delivery
royalties are owed. By Nelson's design, this is derivable from the
address itself:

    Σ.royalty(a) = creator(a)    for all a ∈ dom(Σ.ispace)

Nelson states: "There is a royalty on every byte transmitted. This is
paid automatically by the user to the owner every time a fragment is
summoned" [LM 2/43]. The royalty relationship is not stored in a table
that could be corrupted or deleted — it is a consequence of the address
encoding.


## The Invariant Hierarchy

We are now in a position to state the central result: the system's
permanence guarantees stratify into three tiers, each with different
conditioning.


### Tier 1: Unconditional Structural Invariants

These properties are mathematical consequences of the addressing and
storage architecture. No economic event can violate them, because they do
not depend on any economic state component. They hold in every reachable
state Σ, regardless of Σ.econ.

**E0 (Address irrevocability — unconditional).** Once an address enters
the domain of ispace, it remains forever:

    (A a : a ∈ dom.ispace : a ∈ dom.ispace')

for every operation transforming Σ to Σ'. This is a property of the
addressing scheme — tumblers grow by forking, never by recycling. The
address `1.3.27.4` will always denote the content it was assigned to. An
economic event (non-payment, bankruptcy, death of the owner) cannot remove
an address from the tumbler space, because the tumbler space is a
mathematical structure, not a physical resource.

Nelson: "any address of any document in an ever-growing network may be
specified by a permanent tumbler address" [LM 4/19]. The word "permanent"
is not qualified by "while payment continues."

**E1 (Content immutability — unconditional).** Content at an allocated
address never changes:

    (A a : a ∈ dom.ispace : ispace'.a = ispace.a)

for every operation. The I-space store is write-once, append-only. Even
"deletion" does not destroy I-space content: "DELETED BYTES (not currently
addressable, awaiting historical backtrack functions, may remain included
in other versions)" [LM 4/9]. Content in I-space is a historical fact —
it was written, it persists, and no subsequent event (including
non-payment) can alter what was written.

**E2 (Identity permanence — unconditional).** The association between
content and its creator is permanent:

    (A a : a ∈ dom.ispace : creator(a) in Σ' = creator(a) in Σ)

This follows from E0 (the address survives) and the structural encoding
of identity in the address (EΣ5). The creator function extracts a prefix
of the immutable address; it cannot change unless the address itself
changes. Even if the creator's account lapses or is abandoned, the fact
that the content at address `a` was created by that account is encoded in
`a` and persists for the lifetime of the system.

Nelson: "You always know where you are, and can at once ascertain the home
document of any specific word or character" [LM 2/40].

**E3 (Economic structure permanence — unconditional).** The royalty
relationship between content and its creator survives all economic events:

    (A a : a ∈ dom.ispace : Σ'.royalty(a) = Σ.royalty(a))

for every operation. This follows from E2 and the derivation
Σ.royalty(a) = creator(a) (EΣ6). Because the royalty claim is encoded in
the address, not in a mutable database record, it cannot be "severed"
by non-payment. If the content at address `a` is ever delivered to a
reader in any future state, the system knows who is owed the royalty —
the information is in the address itself.

This is a powerful guarantee. It means that even if content goes dark for
a period (withheld due to non-payment), and is later restored to
accessibility (by some party resuming payment, by the Author's Fund
absorbing cost, by declining storage prices making it trivially cheap to
maintain), the economic relationships are perfectly preserved. No
"reconnection" of royalty structures is needed. The address remembers.

**E4 (Non-destruction — unconditional).** No operation destroys I-space
content:

    (A op : op ∈ Operations : dom(Σ.ispace) ⊆ dom(Σ'.ispace))

This is a restatement of E0 in the language of operations rather than
states. We state it separately because the economic context introduces a
temptation: when no one is paying for storage, an implementation might be
tempted to "garbage collect" unpaid content. E4 says this is forbidden.
Content may be withheld; it may not be destroyed.

The architectural basis is the append-only storage model: "Instead,
suppose we create an append-only storage system" [LM 2/14]. An
append-only store has no delete operation. This is not a policy choice
(like "we choose not to delete") but an architectural constraint (the
store does not support the operation).

We collect the unconditional invariants:

    E-STRUCT = E0 ∧ E1 ∧ E2 ∧ E3 ∧ E4

E-STRUCT holds in every reachable state. It is not conditioned on any
economic state component. The proof obligation for any operation is:

    {E-STRUCT} op {E-STRUCT}

regardless of Σ.econ.


### Tier 2: Publication Obligations to Third Parties

Publication creates obligations that go beyond the structural invariants.
When an author publishes, other users may link to, transclude, and build
upon the published content. These third-party dependencies create
permanence obligations that are independent of the author's economic
status.

The obligations arise from three sources:

First, publication is a contractual commitment. Nelson describes
publication as "a solemn event, to be undertaken cautiously" involving
"something very like a credit-card triplicate slip" [LM 2/42–44]. The
publication contract includes the provision: "I agree that anyone may link
and window to my document" [LM 2/45]. This is a binding agreement, not
a revocable preference.

Second, others' links are their property. A link is homed in its
creator's document, not in its target: "A link need not point anywhere in
its home document. Its home document indicates who owns it, and not what
it points to" [LM 4/12]. If Alice links to Bob's published content, that
link is Alice's property at Alice's address. Bob's failure to pay storage
would damage Alice's property — her link would point to inaccessible
content.

Third, transclusion creates structural dependency. A document that
transcludes another's content does not hold a copy; it holds references
that must be resolved at retrieval time: "all other bytes are obtained by
front-end or back-end requests to their home locations" [LM 4/11]. If the
home location becomes inaccessible, the transcluding document is
structurally incomplete.

We formalize these obligations.

**E5 (Publication irrevocability — unconditional on author intent,
including economic failure).** Once a document is published, its published
status is not revoked by any economic event affecting its author:

    published(d) ∧ Σ.econ(owner(d)) ∈ {lapsed, abandoned}
      ⟹  published(d) in Σ'

Nelson: "It is in the common interest that a thing once published stay
published, as in the world of paper. Other readers and users will come to
depend on its accessibility. Consequently its author may not withdraw it
except by lengthy due process" [LM 2/43]. Non-payment is not "lengthy
due process." It is a breach of the publication contract, not an exercise
of a withdrawal right.

**E6 (Third-party link validity).** Links created by third parties to
published content remain valid regardless of the content owner's economic
status:

    (A link ∈ Σ.links, a ∈ endsets(link).iaddrs :
      a ∈ dom(Σ.ispace) ∧ published(home(a))
      ⟹  a ∈ dom(Σ'.ispace) ∧ endsets'(link).iaddrs = endsets(link).iaddrs)

The link's endset I-addresses are structural (they point to permanent
I-space addresses). They cannot be invalidated by economic events because
they are governed by E0 (address irrevocability). The link's *resolution*
— whether following the link returns content or an error — is a separate
question (addressed in Tier 3).

But the link itself — as an assertion of connection — is permanent. The
system can always answer "yes, this link exists and points to address
`a`" even if it must add "but the content at `a` is currently withheld."

**E7 (Transclusion structural integrity).** When document d₂ transcludes
content from published document d₁, and d₁'s owner's economic status
changes, the transclusion relationship is preserved:

    (A d₂, a : (E p : Σ.poom(d₂).p = a) ∧ published(home_doc(a))
      ⟹  (E p' : Σ'.poom(d₂).p' = a))

The transcluding document's arrangement mapping is unaffected by the
transcluded content's owner's economic status. This follows from the
cross-document isolation property: no operation on d₁ (including economic
state changes to d₁'s owner) modifies d₂'s V-space mapping.

However, the *completeness* of d₂'s retrieval depends on d₁'s content
being accessible. If d₁'s content is withheld, d₂ has a gap — its
arrangement maps positions to I-addresses, but the content behind those
I-addresses cannot be delivered. The arrangement is intact; the delivery
is impaired.

**E8 (Version history preservation).** The version history of a published
document survives its owner's economic failure:

    (A d : published(d) :
      version_graph(d) in Σ' = version_graph(d) in Σ)

where version_graph(d) is the DAG of version relationships. Nelson's
design treats version history as fundamental to what a document IS: "A
document is really an evolving ONGOING BRAID" [LM 2/14]. The version
graph is encoded in the tumbler address structure (versions are
sub-addresses of their sources) and in the I-space content they share.
Both are unconditional (Tier 1). The version graph cannot be damaged by
economic events because its existence is structural, not economic.

We collect the publication obligations:

    E-PUB = E5 ∧ E6 ∧ E7 ∧ E8

E-PUB constrains the system's behavior toward published content. Unlike
E-STRUCT, which is self-enforcing (the architecture makes violation
impossible), E-PUB requires institutional enforcement — someone must
ensure that published content remains accessible even when its owner
defaults. The obligation is clear; the funding mechanism is not.


### Tier 3: Contingent Accessibility

We now arrive at the property that Nelson leaves unresolved: whether
content at a valid, permanent, immutable I-space address is actually
*deliverable* to a requestor. This is where the economic model enters.

**E9 (Accessibility contingency).** The accessibility of content is
conditioned on economic status, subject to the constraints of E-PUB:

    Σ.accessible(a) may transition from accessible to withheld
      only if Σ.econ(owner(a)) ∈ {lapsed, abandoned}

Content whose owner's obligations are `current` is accessible. Content
whose owner's obligations have `lapsed` or are `abandoned` *may* become
inaccessible — but only in the weak sense of being withheld, never in
the strong sense of being destroyed (by E4).

The transition to `withheld` is further constrained for published content.
E5 says publication status is not revoked. But publication status without
accessibility is hollow. The tension is real:

- Nelson says published content "must remain on the network" [LM 2/43].
- Nelson says "all services must be self-supporting" [LM 4/5].
- Someone must pay for storage.
- If no one pays, the content cannot be served — not because the system
  chooses to punish the defaulter, but because servers require electricity
  and disk requires rental.

We formalize what we can, and mark what we cannot.

**E10 (Withheld is not destroyed).** A withheld state is structurally
distinct from a destroyed state:

    Σ.accessible(a) = withheld  ⟹
      a ∈ dom(Σ.ispace)                        — address still valid
      ∧ Σ.ispace(a) = Σ₀.ispace(a)            — content unchanged since allocation
      ∧ creator(a) = creator₀(a)               — identity preserved
      ∧ Σ.royalty(a) = Σ₀.royalty(a)           — economic structure preserved

where Σ₀ is the state at the time of original allocation. Every Tier 1
invariant holds for withheld content. Withholding affects delivery, not
existence.

Nelson's architecture already has a precedent: "DELETED BYTES (not
currently addressable, awaiting historical backtrack functions, may remain
included in other versions)" [LM 4/9]. Deleted bytes exist but are not
served through the current V-space mapping. Withheld-for-non-payment
bytes exist but are not served through the delivery layer. The I-space
status is identical in both cases — the content is there, the address is
valid, the content is immutable. Only the accessibility differs.

The system also already handles temporary inaccessibility as a normal
condition: "It is a truism that 'computer networks are always broken.'
Meaning that on the average some nodes are disconnected or not working"
[LM 4/75]. The BEBE protocol routes around unavailable servers. A payment
lapse that makes content temporarily unreachable is operationally no
different from a server being down — the content exists somewhere, it
simply cannot be delivered right now.

**E11 (Recoverability).** Content that is withheld can be restored to
accessible status without data loss:

    Σ.accessible(a) = withheld ∧ Σ'.accessible(a) = accessible
      ⟹  Σ'.ispace(a) = Σ.ispace(a)

Recovery delivers the original content, not a reconstruction. This is a
consequence of E1 (content immutability) and E4 (non-destruction): the
content was never modified or destroyed, so recovery is simply a change
in the delivery policy, not a data restoration.

This property has practical significance. It means the system can offer
a "resume payment and recover everything" guarantee to lapsed owners, and
a "content can be re-lit by any party willing to pay" mechanism for
abandoned content.


## The Published/Private Distinction

The three tiers interact differently depending on whether content is
published or private. We must formalize this distinction because it
determines the strength of the accessibility guarantee.

**E12 (Published content: strong accessibility obligation).** For
published content whose owner's economic status has lapsed or been
abandoned, the system owes a preservation obligation to third parties:

    published(d) ∧ Σ.econ(owner(d)) ∈ {lapsed, abandoned}
      ⟹  the system must seek to maintain Σ.accessible(a) = accessible
          for all a ∈ img(Σ.poom(d))

We write "must seek to maintain" because the obligation is clear but the
funding mechanism is not. Nelson provides several mechanisms that push
toward preservation:

1. **Distributed replication.** Content is replicated across vendors:
   "Material is moved between servers for... redundancy and backup
   purposes" [LM 4/71]. Backup copies at other vendors may remain
   accessible even when the home vendor's payment relationship breaks.

2. **Vendor transition obligations.** "Upon notice of cancellation,
   Storage Vendor will arrange for the orderly transition of all
   customer-stored materials to other Xanadu locations" [LM 5/16]. Content
   migrates; it does not vanish.

3. **Royalty feedback.** Popular content generates delivery revenue that
   may offset storage costs: "There is a royalty on every byte transmitted"
   [LM 2/43]. If enough readers access the content, the delivery charges
   flowing through the system may sustain its storage.

4. **The Author's Fund.** A surcharge on public domain byte delivery
   accumulates into an escrow account for "the charitable funding of
   worthy causes within the network" [LM 5/12]. Whether this extends to
   preserving orphaned published content is unspecified, but "worthy
   purposes" is suggestively broad.

5. **Declining storage costs.** Nelson designed the system anticipating
   that digital storage would become radically cheaper over time. The
   long-term cost of maintaining a published document approaches zero
   even if the author's payments stop.

None of these mechanisms is individually sufficient. Together, they
represent a design philosophy: the economic model should be designed so
that published content's permanence is de facto achievable, even though
the specification does not guarantee it de jure.

**E13 (Private content: weak accessibility obligation).** For private
(unpublished) content whose owner's economic status has lapsed or been
abandoned, the system owes no third-party accessibility obligation:

    ¬published(d) ∧ Σ.econ(owner(d)) ∈ {lapsed, abandoned}
      ⟹  Σ'.accessible(a) = withheld    is permitted
          for all a ∈ img(Σ.poom(d))

Private content has no third-party dependents. No one else has linked to
it (or should not have — private content is not universally accessible).
No one else has transcluded it. The owner is the sole stakeholder.

Even so, the Tier 1 invariants hold. The content is not destroyed (E4).
The address remains valid (E0). The creator identity is preserved (E2).
The economic structure survives (E3). If the owner returns and resumes
payment, their content is recoverable (E11).

The distinction between published and private is sharp:

    published(d)   ⟹  third-party obligations exist     (E12)
    ¬published(d)  ⟹  no third-party obligations exist   (E13)

Publication is the act that creates social obligations. Without it, the
owner's relationship to the system is bilateral — owner and storage
vendor. With it, the relationship becomes multilateral — owner, vendor,
and every user who has linked to or transcluded the content.


## The Ghost State

We must account for the case where content has never been stored at an
address. Nelson describes ghost elements:

> "While servers, accounts and documents logically occupy positions on
> the developing tumbler line, no specific element need be stored in
> tumbler-space to correspond to them. Hence we may call them ghost
> elements." [LM 4/23]

A ghost element is an address that is valid but empty — it has never had
content stored at it. This is distinct from both `accessible` and
`withheld`:

- `accessible`: content exists and can be delivered.
- `withheld`: content exists but cannot currently be delivered.
- `ghost`: no content has ever been stored.

**E14 (Ghost distinction).** For any address a:

    a ∉ dom(Σ.ispace)  ⟹  a is ghost (no content to withhold or deliver)
    a ∈ dom(Σ.ispace)  ⟹  Σ.accessible(a) ∈ {accessible, withheld}

Ghosts are not the result of economic failure. They are positions in the
address space that have not yet been populated — or that were reserved
structurally (as document or account placeholders) and may never be
populated. The distinction matters because a link to a ghost element is
not "broken by non-payment" — it was never "connected" in the content
sense. Ghost elements are "virtually present in tumbler-space, since
links may be made to them which embrace all the contents below them"
[LM 4/23].

When content transitions from `accessible` to `withheld` due to
non-payment, the address does NOT become a ghost. It remains in
dom(Σ.ispace). The content is there. It is simply not being served.
An implementation must be able to distinguish these three states, because
the appropriate response to a query differs:

- Ghost: "No content has ever been stored at this address."
- Withheld: "Content exists at this address but is currently unavailable."
- Accessible: "Here is the content."

This three-way distinction is not merely informational. It determines
what the system may promise about the future. A ghost address might
eventually receive content. A withheld address will deliver its original
content if payment resumes (E11). Only for a ghost address is it true
that there is nothing to restore.


## Worked Example: The Cascade

We verify the properties against a scenario that exercises the
published/private distinction and the three tiers.

*Setup.* Alice (account `1.0.2`) publishes document d₁ containing text
"The fundamental theorem..." at I-addresses i₁, i₂, ..., iₙ. Bob
(account `1.0.3`) creates document d₂ that transcludes Alice's text
and adds commentary. Carol (account `1.0.4`) creates link L₁, homed in
her document d₃, with an endset pointing to i₁...iₙ in d₁.

All three users are in good standing: Σ.econ(`1.0.2`) = current,
Σ.econ(`1.0.3`) = current, Σ.econ(`1.0.4`) = current.

*Event: Alice stops paying.*

Σ'.econ(`1.0.2`) = lapsed.

What must the system guarantee?

**Tier 1 checks (E-STRUCT):**

- E0: All I-addresses i₁...iₙ remain in dom(Σ'.ispace). ✓
  (Address irrevocability is unconditional.)
- E1: Σ'.ispace(iₖ) = Σ.ispace(iₖ) for all k. ✓
  (Content immutability is unconditional.)
- E2: creator(iₖ) = `1.0.2` in Σ' as in Σ. ✓
  (Identity is structural.)
- E3: Σ'.royalty(iₖ) = `1.0.2` for all k. ✓
  (Royalty structure is structural.)
- E4: dom(Σ.ispace) ⊆ dom(Σ'.ispace). ✓
  (Non-destruction is unconditional.)

All Tier 1 invariants hold. Alice's non-payment changes nothing about the
existence, content, attribution, or economic structure of her bytes.

**Tier 2 checks (E-PUB):**

- E5: published(d₁) in Σ'. ✓
  (Publication is not revoked by non-payment.)
- E6: Carol's link L₁ remains valid — its endset I-addresses are
  unchanged. ✓ (Links reference I-space, which is unconditional.)
- E7: Bob's transclusion arrangement is preserved —
  Σ'.poom(d₂) = Σ.poom(d₂). ✓
  (Cross-document isolation; Alice's economic status does not modify
  Bob's V-space mapping.)
- E8: The version history of d₁ is preserved. ✓
  (Version structure is encoded in addresses and I-space sharing.)

All Tier 2 invariants hold. The publication obligations to Bob and Carol
are intact.

**Tier 3 checks (accessibility):**

Here the tension emerges. Alice is not paying. The system may transition
her content to withheld:

    Σ'.accessible(iₖ) = withheld    for k = 1..n    (permitted by E9)

But E12 says the system must seek to maintain accessibility for published
content. The available mechanisms:

- If Alice's content is replicated at other vendors (BEBE protocol),
  those copies may remain accessible. The withheld state applies to
  Alice's *home server*, not necessarily to all replicas.
- If Alice's content generates delivery revenue (it is being read), the
  royalties may offset storage costs.
- The vendor's transition obligation (LM 5/16) may trigger migration to
  another vendor willing to absorb the content.

*Consequence for Bob's document:* If i₁...iₙ become withheld, Bob's
document d₂ has a gap. His arrangement mapping still references those
I-addresses, but retrieval of d₂ cannot deliver the transcluded bytes.
Bob's own content (his commentary) remains fully accessible — it is at
different I-addresses, under Bob's own account, with Bob's economic
status `current`. The damage is partial: the transcluded portion is
impaired, but the structure (which bytes are transcluded, from where,
under whose authorship) is fully preserved.

*Consequence for Carol's link:* Carol's link L₁ remains valid (E6). If
she traverses it and the target content is withheld, she learns that
"content exists at these addresses but is currently unavailable" —
not "these addresses are invalid" or "this content never existed."

*Event: Alice resumes payment.*

Σ''.econ(`1.0.2`) = current. By E11 (recoverability):

    Σ''.accessible(iₖ) = accessible    for k = 1..n
    Σ''.ispace(iₖ) = Σ.ispace(iₖ)    (original content, unchanged)

Bob's document is whole again. Carol's link resolves to content again.
The royalty structure is intact — every byte delivered to readers during
and after the lapse generates the correct royalty for Alice. No
"reconnection" was needed; the address never forgot who owned it.


## The Fundamental Theorem

We can now state the central result precisely.

**Theorem E-STRAT (Invariant Stratification).** The system's permanence
guarantees stratify into three tiers with decreasing conditionality:

*Tier 1 — Unconditional (E-STRUCT = E0 ∧ E1 ∧ E2 ∧ E3 ∧ E4):*

    {E-STRUCT} op {E-STRUCT}    for all operations op, regardless of Σ.econ

Address irrevocability, content immutability, identity permanence,
economic structure permanence, and non-destruction hold in every reachable
state without exception. No economic event can violate them.

*Proof sketch.* E0–E4 depend only on properties of the tumbler address
space (mathematical), the append-only storage model (architectural), and
the derivability of identity and royalty from addresses (structural).
None of these depend on Σ.econ. The proof obligation reduces to showing
that no operation — including any operation triggered by economic state
changes — modifies dom(Σ.ispace), Σ.ispace(a) for existing a, or the
prefix structure of addresses. The append-only architecture provides this:
there is no "delete from I-space" operation.  ∎

*Tier 2 — Obligatory for published content (E-PUB = E5 ∧ E6 ∧ E7 ∧ E8):*

    published(d)  ⟹  the system must preserve E-PUB for d
      regardless of Σ.econ(owner(d))

Publication creates obligations to third parties that are independent of
the author's payment status. These obligations are enforced by the
publication contract, the vendor transition protocol, and the distributed
replication architecture. The funding mechanism for honoring these
obligations when the author defaults is incompletely specified.

*Tier 3 — Contingent (E9, E10, E11):*

    Σ.accessible(a) depends on Σ.econ(creator(a))
      subject to the constraints of Tier 1 (never destroy)
      and Tier 2 (seek to preserve published content)

Accessibility is the only permanence property that is genuinely contingent
on economics. And even this contingency is constrained: withholding is
permitted, destruction is not; and for published content, the system must
seek alternatives to withholding.


## The Unresolved Gap

We have now formalized what the system guarantees and what it does not.
The gap between Tier 2 (obligation) and Tier 3 (contingency) is the
specification's acknowledged incompleteness. Nelson states two principles
that, in the limit, conflict:

    "It is in the common interest that a thing once published
     stay published" [LM 2/43]

    "ALL SERVICES MUST BE SELF-SUPPORTING" [LM 4/5]

When no one pays for published content's storage, one of these principles
must yield. Nelson does not say which. The specification provides
mechanisms that *delay* the conflict (replication, vendor obligations, the
Author's Fund, royalty feedback) but does not resolve it for the case
where all mechanisms are exhausted.

We characterize the gap precisely:

**E-GAP (The permanence funding problem).** For published content whose
owner has abandoned economic obligations and whose delivery revenue does
not cover storage costs:

    published(d) ∧ Σ.econ(owner(d)) = abandoned
    ∧ revenue(d) < storage_cost(d)
    ⟹  ???

The system owes a preservation obligation (E12) but has no specified
funding source. This is an open problem in the specification — not a
defect in our formalization, but a faithful representation of a tension
Nelson identified and did not resolve.

Nelson's own assessment of the intent is clear:

> "I designed a system where addresses are permanent and literature is
> preserved. The self-supporting requirement was a practical necessity —
> someone must pay for the disk. But the deeper principle is that
> published content enters the permanent record of human civilization."

And: "A system designed for 'deep rock and deep space' does not delete
published content because a monthly payment was missed."

The resolution, when it comes, must satisfy:
- E-STRUCT is inviolable (no destruction, no address reuse)
- E-PUB creates a genuine obligation (not a "best effort")
- The funding mechanism must be self-sustaining (no indefinite subsidy)

These three constraints are jointly satisfiable only if the long-term
cost of storage decreases faster than the accumulation of orphaned
content. Nelson appears to have been betting on this — and given the
historical trajectory of storage costs, the bet may be sound. But the
specification does not prove it.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| EΣ1 | Σ.ispace : IAddr ⇀ Content — permanent, append-only content store | introduced |
| EΣ2 | Σ.pub : DocId → {private, published} — publication status | introduced |
| EΣ3 | Σ.econ : OwnerId → EconStatus where EconStatus = {current, lapsed, abandoned} | introduced |
| EΣ4 | Σ.accessible : IAddr → {accessible, withheld} — content deliverability status | introduced |
| EΣ5 | creator(a) = (THE u : u ∈ Σ.accounts : prefix(u, a)) — identity derived from address | introduced |
| EΣ6 | Σ.royalty(a) = creator(a) — royalty claim derived from address | introduced |
| E0 | Address irrevocability is unconditional: a ∈ dom.ispace ⟹ a ∈ dom.ispace' regardless of Σ.econ | introduced |
| E1 | Content immutability is unconditional: ispace'.a = ispace.a regardless of Σ.econ | introduced |
| E2 | Identity permanence is unconditional: creator(a) is invariant regardless of Σ.econ | introduced |
| E3 | Economic structure permanence is unconditional: Σ.royalty(a) is invariant regardless of Σ.econ | introduced |
| E4 | Non-destruction is unconditional: no operation removes content from I-space | introduced |
| E-STRUCT | E0 ∧ E1 ∧ E2 ∧ E3 ∧ E4 — the unconditional structural invariant | introduced |
| E5 | Publication irrevocability: published status is not revoked by economic failure | introduced |
| E6 | Third-party link validity: links to published content remain valid regardless of owner's economic status | introduced |
| E7 | Transclusion structural integrity: transclusion arrangements survive owner's economic failure | introduced |
| E8 | Version history preservation: version graph of published documents survives owner's economic failure | introduced |
| E-PUB | E5 ∧ E6 ∧ E7 ∧ E8 — publication obligations to third parties | introduced |
| E9 | Accessibility contingency: content may transition to withheld only when owner's econ ∈ {lapsed, abandoned} | introduced |
| E10 | Withheld ≠ destroyed: all Tier 1 invariants hold for withheld content | introduced |
| E11 | Recoverability: withheld content can be restored to accessible without data loss | introduced |
| E12 | Published content: strong accessibility obligation — system must seek to maintain accessibility | introduced |
| E13 | Private content: weak accessibility obligation — withholding is permitted | introduced |
| E14 | Ghost distinction: address not in dom.ispace is ghost; address in dom.ispace is accessible or withheld | introduced |
| E-STRAT | Invariant Stratification Theorem: permanence guarantees form three tiers with decreasing conditionality | introduced |
| E-GAP | The permanence funding problem: published, abandoned, revenue-negative content has unspecified funding | introduced |


## Open Questions

What minimum grace period must the system guarantee between economic lapse and content withholding — is immediate withholding on first missed payment consistent with the publication obligation?

Must the system provide a mechanism for third parties (linkers, transcluders) to assume storage costs for content whose original owner has defaulted?

What must the system guarantee about the discoverability of withheld content — must search indexes and link traversal reveal that content exists but is withheld, or may the system treat withheld content as invisible?

Can the Author's Fund or a similar collective mechanism be formally specified as a funding source for orphaned published content, and if so, what governance invariants must it satisfy?

Must the system guarantee that the transition from `lapsed` to `abandoned` is reversible — can an abandoned owner reclaim their content and economic relationships?

What must the system guarantee about partial withholding — if a document contains both owner-original and transcluded content, must the transcluded portions (owned by a different, paying party) remain accessible when the document owner defaults?

Does the vendor transition obligation (LM 5/16) create a sufficient backstop for published content permanence, or must the specification provide additional mechanisms beyond vendor-to-vendor migration?

What upper bound, if any, must the system place on the duration of the withheld state before some resolution (restoration, migration, or collective preservation) is required?
