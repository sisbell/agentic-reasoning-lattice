## Question 17 [gregory]

> The type namespace lives at `1.0.2.x` in the global address space — what structure do type tumblers have, how are new types created, and is there a base set of built-in types that the system assumes?

## KB Synthesis

## Type Namespace Structure and Built-in Types

### Type Tumbler Structure

Type tumblers are VSpec references into a type registry embedded in the bootstrap document at address prefix `1.0.2.*`. [SS-LINK-ENDPOINT Finding 0024]

The known type addresses follow a hierarchical containment structure:

| Type | Address | Structural interpretation |
|------|---------|--------------------------|
| JUMP | `1.0.2.2` | version.0.types.2 |
| QUOTE | `1.0.2.3` | version.0.types.3 |
| FOOTNOTE | `1.0.2.6` | version.0.types.6 |
| MARGIN | `1.0.2.6.2` | version.0.types.6.subtype.2 |

The addresses `1.0.2.2`, `1.0.2.3`, `1.0.2.6` are first-level types under the type namespace. `1.0.2.6.2` (MARGIN) is a subtype — it is tumbler-contained within `1.0.2.6` (FOOTNOTE), enabling range-based subtype queries: any search for links of type `1.0.2.6` will match MARGIN links because `1.0.2.6.2` falls within the span `[1.0.2.6, 1.0.2.7)`. [SS-LINK-ENDPOINT Finding 0024, SS-TUMBLER-CONTAINMENT]

A link's type field is structurally `link.type : VSpec` where `VSpec.docid = bootstrap_doc ∧ VSpec.spans ⊆ addresses(1.0.2.*)`. Types are content references participating in the same address and identity system as all other content — they are not enums or flags. [SS-LINK-ENDPOINT Finding 0024]

### Built-in Base Set

The KB documents exactly four types from the client implementation (`QUOTE_TYPE`, `MARGIN_TYPE`, and by extension JUMP and FOOTNOTE from the address table). These are the types that `febe/client.py` constructs as VSpec objects against the bootstrap document. Whether positions `1.0.2.1`, `1.0.2.4`, `1.0.2.5`, etc. are reserved, occupied by undocumented types, or available, is **not answerable from the KB**.

### Type Creation

**Not answerable from the KB.** The KB does not document the mechanism by which new type addresses are created or registered. What is known is:

1. Type addresses exist in the bootstrap document's address space [SS-LINK-ENDPOINT Finding 0024]
2. Address allocation in general is via `findisatoinsertnonmolecule` — query-and-increment under a parent address [SS-ADDRESS-ALLOC Finding 0021]
3. Type containment (subtyping) is implicit in tumbler prefix matching, so creating a subtype of FOOTNOTE would mean allocating an address under `1.0.2.6` [SS-TUMBLER-CONTAINMENT]

Whether type creation is a privileged bootstrap-document operation, a special FEBE opcode, or simply a content insert into the type namespace is not documented in the KB.

---

## Code Exploration

Now I have everything I need. Let me synthesize the complete answer.

---

## Type Tumblers, Creation, and Built-in Types in udanax-green

### The Short Answer: `1.0.2.x` Does Not Exist in This Backend

After a full search of the source, **no such address range** is defined, initialized, or referenced anywhere in the C code. The premise that "the type namespace lives at `1.0.2.x`" comes from Xanadu conceptual specification documents, not from anything implemented in udanax-green. The backend has no "type registry" stored in the global address space at all.

What follows is what the code actually says.

---

### 1. What Structure Do Type Tumblers Have?

#### Tumbler Data Structure

Defined in `backend/common.h:59-65`:

```c
typedef struct structtumbler {
    humber xvartumbler;       /* variable-length form (unused in practice) */
    char varandnotfixed;      /* flag for variable form */
    char sign;                /* 1 if negative, otherwise 0 */
    short exp;                /* exponent, always <= 0; counts leading-zero fields */
    tdigit mantissa[NPLACES]; /* NPLACES = 16, unsigned 32-bit integers */
} tumbler;
```

`tdigit` is `UINT` (`common.h:57`). `NPLACES` was `11` originally, expanded to 16 to support deeper version chains (`common.h:53`).

#### Dot Notation

The `puttumbler` function (`backend/put.c:26-46`) prints tumblers as:

```c
for (i = tumblerptr->exp; i < 0; ++i)
    fprintf(outfile, "0.");             // leading zero fields from exp
for (i = 0; i <= place; ++i) {
    putnum(outfile, tumblerptr->mantissa[i]);
    if (i < place) putc('.', outfile);  // dot-separated mantissa
}
```

So `{exp=-0, mantissa={1,1,0,1,...}}` prints as `1.1.0.1`.

#### Four-Field Global Address Structure

Per `docs/tumbler-technical.md`, full addresses have four fields separated by `.0.`:

```
Node.0.User.0.Document.0.Element
```

Example: `1.1.0.2.0.1` = Node `1.1`, User `2`, first Document `1`. There are at most three zeros (field separators) in an address tumbler.

The only hardcoded addresses in the source:
- `backend/be.c:37`: `tumbler defaultaccount = {0,0,0,0, 1,1,0,1,0,0,0,0}; /* 1.1.0.1 */` — Node `1.1`, User `1`
- `backend/socketbe.c:35`: `tumbler defaultaccount = {0,0,0,0, 1,1,0,14,0};` — Node `1.1`, User `14`
- `backend/do1.c:86`: `tumbler fivetumbler = {0,0,0,0,500,0,...}` — a debug constant

There is no `1.0.2` anywhere.

---

### 2. How Are New Types Created?

**There is no mechanism to create new types in udanax-green.** The type system is hardcoded as compile-time constants. What the backend calls "types" are:

#### Level 1: The `typehint` Hierarchy (Object Creation)

Defined in `backend/xanadu.h:140-153`:

```c
#define NODE      1
#define ACCOUNT   2
#define DOCUMENT  3
#define ATOM      4
#define TEXTATOM  1   /* atom types */
#define LINKATOM  2

typedef struct {
    INT supertype;   /* NODE=1, ACCOUNT=2, DOCUMENT=3 */
    INT subtype;     /* ACCOUNT=2, DOCUMENT=3, ATOM=4 */
    INT atomtype;    /* 0=none, TEXTATOM=1, LINKATOM=2 */
    typeisa hintisa; /* parent address */
} typehint;
```

These are validated in `backend/do2.c:86-108` (`validhint`). The constraints are:
- `supertype ∈ {NODE, ACCOUNT, DOCUMENT}` (1–3)
- `subtype ∈ {ACCOUNT, DOCUMENT, ATOM}` (2–4)
- `subtype >= supertype` and `(subtype - supertype) <= 1`
- `(subtype == ATOM) == !atomtype`

The `makehint` call at `backend/do1.c:239` for document creation:
```c
makehint(ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
```

And at `backend/do1.c:251` for node creation:
```c
makehint(NODE, NODE, 0, &isa, &hint);
```

**New "type" addresses cannot be created** — only new instances of the four fixed types.

#### Level 2: Item Type Tags (In-Memory)

Defined in `backend/xanadu.h:26-33`:
```c
#define TEXTID    0
#define ISPANID   1
#define VSPANID   2
#define VSPECID   3
#define NODEID    4
#define ADDRESSID 5
#define SPORGLID  6
```

These are the `typeitemid` field in every in-memory struct (e.g., `typetext`, `typespan`, `typeaddress`). They are type tags in the C sense — not stored in the address space.

#### Level 3: Spanfilade Span Types

Defined in `backend/xanadu.h:36-39`:
```c
#define LINKFROMSPAN    1
#define LINKTOSPAN      2
#define LINKTHREESPAN   3
#define DOCISPAN        4
```

Used in `backend/spanf1.c` to identify what kind of span is being inserted into the spanfilade.

---

### 3. Is There a Base Set of Built-in Types?

Yes — the entire type system is built-in and fixed. Here is the complete inventory:

| Category | Name | Value | Where Defined |
|----------|------|-------|---------------|
| Object hierarchy | `NODE` | 1 | `xanadu.h:140` |
| Object hierarchy | `ACCOUNT` | 2 | `xanadu.h:141` |
| Object hierarchy | `DOCUMENT` | 3 | `xanadu.h:142` |
| Object hierarchy | `ATOM` | 4 | `xanadu.h:143` |
| Atom subtypes | `TEXTATOM` | 1 | `xanadu.h:145` |
| Atom subtypes | `LINKATOM` | 2 | `xanadu.h:146` |
| V-space subspaces | link subspace | `0.x` | `do1.c:393` |
| V-space subspaces | text subspace | `1.x+` | `do1.c:395` |
| Span types | `LINKFROMSPAN` | 1 | `xanadu.h:36` |
| Span types | `LINKTOSPAN` | 2 | `xanadu.h:37` |
| Span types | `LINKTHREESPAN` | 3 | `xanadu.h:38` |
| Span types | `DOCISPAN` | 4 | `xanadu.h:39` |

The system also requires at initialization:
- A valid `account` tumbler in `taskptr->account` (set in `be.c:88`)
- A `granf` (granfilade) and `spanf` (spanfilade) initialized via `inittask` (`task.c:15`)

---

### Why `1.0.2.x` Doesn't Appear

With the four-field format `Node.0.User.0.Document.0.Element`, the address `1.0.2.x` would mean Node=`1`, User=`2.x`. This is a structurally valid account address (same format as the real account `1.1.0.1` = Node=`1.1`, User=`1`). But:

1. No such account is created or referenced anywhere in the source
2. The backend stores no data about types in any granfilade entry — types are purely in-memory constants
3. All type-dispatching logic uses C `#define` constants and the `typehint.supertype/subtype/atomtype` fields, not address lookups

If the Xanadu conceptual design designated `1.0.2.x` as a type registry, **udanax-green never implemented it**. The backend's type system is a flat four-level hierarchy (`NODE > ACCOUNT > DOCUMENT > ATOM`) with two atom subtypes, all hardcoded in `xanadu.h` and validated in `do2.c:validhint`.
