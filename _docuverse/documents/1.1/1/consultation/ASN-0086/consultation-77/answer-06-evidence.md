## Question 6 [evidence]

> In ASN-0043's catalog, are L5 (EndsetSetSemantics), L6 (SlotDistinction), and L8 (TypeByAddress) stated as state invariants over `Σ.L` requiring preservation across transitions, or as definitional commitments / function definitions that hold wherever the link store is well-formed?

## KB Synthesis

I cannot access ASN-0043's text directly in this session. Here is what the KB evidence supports, with the honest epistemic status marked.

---

**From KB evidence: L5, L6, L8 are definitional commitments, not transition invariants**

**L5 EndsetSetSemantics**

`[SS-LINK-ENDPOINT]` Finding 0037 establishes that a link endset *is* a set of I-spans (sporgls) — this is a representational fact about what is stored in the endset field. The property characterizes the **type** of the endset slot. If a link record is well-formed, L5 holds by construction: there is no operation that could produce a well-formed link with V-span endsets and then need to "repair" L5. The property belongs to the well-formedness predicate over link records, not to the transition proof obligations.

**L6 SlotDistinction**

`[SS-LINK-ENDPOINT]` Finding 0005 grounds FROM/TO discoverability as a bidirectional index structure. SlotDistinction says the FROM/TO/THREE partition is part of the **shape** of a link object. Any operation that emits a link record emits one with three named slots — by construction. There is no post-hoc "slot distinction was disrupted and must be restored" scenario that a transition invariant would guard against. It defines what a link IS in this model.

**L8 TypeByAddress**

`[SS-LINK-ENDPOINT]` Finding 0024 gives the type field as a VSpec reference into the bootstrap document at `1.0.2.x`. TypeByAddress commits to the **representation** of the type field — an address into a fixed registry, not an enumeration constant. This is a structural fact about how type information is encoded. It holds wherever the link record is well-formed; it does not generate per-operation frame obligations.

---

**Why definitional and not invariant**

A state invariant over `Σ.L` generates a proof obligation of the form: for every operation `op`, if `I(Σ)` before, then `I(op(Σ))` after. That obligation is meaningful when the property can be *temporarily violated* mid-operation or when an operation's logic could plausibly produce a state where the property fails.

L5/L6/L8 are not that kind of property. They constrain the **record structure** of link objects — the type of the endset field, the named-slot decomposition, the encoding of the type address. Once the representation is fixed, any operation that handles link records at all either: (a) does not touch links, in which case the frame condition is trivial; or (b) constructs new link records, in which case the property holds by construction if the constructor is correct.

The `[SS-THREE-LAYER-MODEL]` entry corroborates this: it notes that link existence, discoverability, and containment are **independent predicates** — the layers are defined independently, not maintained against each other by invariant proofs. L5/L6/L8 belong to the definitional layer of that same architecture.

---

**Caveat**

I have not read ASN-0043's catalog entries for L5, L6, L8 in this session. The above is inference from KB evidence about what these properties describe. If ASN-0043 explicitly labels them as `Invariant:` blocks with `Preserved-by:` claims, that would override this inference — the spec author's framing is authoritative. If you have access to the actual catalog text, the heading type (`Invariant` vs. `Definition` vs. `Function`) is the definitive answer.

---

## Code Exploration

I've completed a thorough search. Let me formulate my answer based on what the source code actually shows.

---

## Answer

**Preliminary finding:** The document "ASN-0043" does not exist anywhere in this repository. The labels L5 (EndsetSetSemantics), L6 (SlotDistinction), and L8 (TypeByAddress) appear in no file under `backend/`, `knowledge-base/`, `findings/`, `docs/`, or `bugs/`. I cannot quote ASN-0043's actual phrasing. What follows is the answer derivable from the C source code alone.

---

### What the source code reveals about these three properties

#### L5 — EndsetSetSemantics: A link's endsets are sets of sporgls

**Code path:**

`do1.c:195–221` — `docreatelink` is the sole entry point for link creation. It calls:

```c
specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)   // [do1.c:214]
specset2sporglset(taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)   // [do1.c:215]
specset2sporglset(taskptr, threespecset,&threesporglset,NOBERTREQUIRED)   // [do1.c:216]
```

Each endset is typed `typesporglset` — a set, structurally. The insertion function:

```c
bool insertendsetsinorgl(typetask *taskptr, tumbler *linkisaptr, typeorgl link,
    tumbler *fromvsa, typesporglset fromsporglset,
    tumbler *tovsa,   typesporglset tosporglset,
    tumbler *threevsa, typesporglset threesporglset)    // [do2.c:130]
```

stores each slot's sporglset at a distinct V-address. The set cardinality is determined at creation time by how many disjoint I-address regions `specset2sporglset` produces. Once stored, the link orgl is never modified — there is no write path to an existing link's endsets other than the creation path.

**Character of the property:** The set-nature of each endset is encoded in the declared type `typesporglset`. It holds by construction at the moment `insertendsetsinorgl` is called. There is no code path that produces a link with non-set endsets. This is **not a preservation requirement**: because links are write-once (immutable after `insertendsetsinorgl`), there is no transition to preserve them across. The property is a **definitional commitment** — it characterizes what a well-formed link object IS, not a condition that operations must maintain.

---

#### L6 — SlotDistinction: FROM, TO, and TYPE occupy distinct V-addresses in the link orgl

**Code path:**

`do2.c:169–183` — `setlinkvsas` constructs three distinct V-addresses before the endsets are written:

```c
tumblerincrement(fromvsaptr, 0, 1, fromvsaptr);  // digit[0] = 1 → V-pos 0.1.1
tumblerincrement(fromvsaptr, 1, 1, fromvsaptr);

tumblerincrement(tovsaptr,   0, 2, tovsaptr);    // digit[0] = 2 → V-pos 0.2.1
tumblerincrement(tovsaptr,   1, 1, tovsaptr);

if (threevsaptr) {
    tumblerincrement(threevsaptr, 0, 3, threevsaptr);  // digit[0] = 3 → V-pos 0.3.1
    tumblerincrement(threevsaptr, 1, 1, threevsaptr);
}
```

These V-positions — `0.1.1`, `0.2.1`, `0.3.1` — are hardcoded constants that the endsets are inserted at via `insertpm`. The distinction between FROM (digit 0 = 1), TO (digit 0 = 2), and TYPE (digit 0 = 3) is purely a V-address convention, not a runtime-typed field.

Retrieval respects this: `dofollowlink` [`do1.c:223–232`] takes a `whichend` parameter (1, 2, or 3) that selects which V-position's sporglset to return via `link2sporglset`.

**Character of the property:** The slot partition is encoded in a fixed V-address assignment at link creation. No code path reassigns or merges slots after creation. The distinction is a **definitional commitment** — it defines the structure of a link orgl. It is not a safety invariant that transitions must prove they preserve, because neither `doinsert`, `docopy`, `dodeletevspan`, nor any operation touches the link orgl V-addresses after creation [`acceptablevsa` at `do2.c:110–113` unconditionally returns `TRUE`, confirming no runtime enforcement exists].

---

#### L8 — TypeByAddress: The link type is stored as a VSpec address

**Code path:**

The two-endset form `docreatestorylink` [`do1.c:162–193`] passes `NULL` for `threespecset`, `threesporglset`, `threevsa`. The three-endset form `docreatelink` [`do1.c:195–221`] accepts `threespecset` and converts it:

```c
specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)  // [do1.c:216]
```

The type IS a `specset` — a virtual address specification, normalized to a sporglset of I-addresses by `specset2sporglset`. It is stored at V-position `0.3.1` inside the link orgl, exactly as FROM and TO are stored at `0.1.1` and `0.2.1`. The type has no separate semantic field; it is structurally identical to an endpoint, distinguished only by V-address.

The knowledge base confirms the runtime consequence: type addresses point to the bootstrap document type registry at `1.0.2.x`, where FOOTNOTE is `1.0.2.6` and MARGIN is `1.0.2.6.2`. But `insertendsetsinorgl` stores the type sporglset at `0.3.1` with no type-registry validation — `acceptablevsa` would be the validation site but returns `TRUE` unconditionally [`do2.c:110–113`].

**Character of the property:** The type IS an address by construction — `threespecset` is a `typespecset` (a V-address specification), and the implementation makes no distinction between how it stores FROM, TO, and TYPE. The address-nature of the type is not a condition that operations must preserve; it is the definition of what a link's type field IS. This is a **definitional commitment**.

---

### Synthesis

All three properties — EndsetSetSemantics, SlotDistinction, TypeByAddress — have the same formal character when read from the C source: they are **definitional commitments**, not state invariants requiring preservation.

The distinction is sharp:

- A **state invariant** would take the form: "For all reachable Σ, P(Σ.L) holds, and for every transition Σ → Σ', if P(Σ.L) then P(Σ'.L)." This would require a proof that operations preserve P.

- A **definitional commitment** takes the form: "Any element of Σ.L, by its construction, satisfies P." Preservation is trivial because (a) links are write-once — `insertendsetsinorgl` writes and no subsequent operation writes to the same link orgl — and (b) the set-structure, V-address slot distinction, and address-representation of type are all encoded in what it means to be a link, not conditions layered on top.

The reason no preservation proof is needed for L5/L6/L8 is that link creation (`docreatelink`/`docreatestorylink`) is the only write path to the link orgl, and it mechanically instantiates all three properties. The link store Σ.L only grows (monotonic under `create_link`); existing elements are never mutated. Therefore L5, L6, and L8 hold for every element of Σ.L in every reachable state — not because operations are constrained to preserve them, but because the link type's definition entails them.

The genuine state invariant over Σ.L is **monotonicity**: `|Σ'.L| ≥ |Σ.L|`, which IS a preservation requirement. L5, L6, and L8 are more primitive than that — they characterize the shape of each element, not the growth of the set.

**Since ASN-0043 does not exist in this repository, I cannot confirm how that document states these properties. The answer above describes what the source code implies about their formal character, which is the only authoritative basis available here.**
