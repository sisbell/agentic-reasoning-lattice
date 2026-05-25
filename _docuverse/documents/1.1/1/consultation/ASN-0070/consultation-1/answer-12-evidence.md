## Question 12 [evidence]

> What concrete data structure does the udanax-green follow-equivalent operation use to represent its V-position result?

## KB Synthesis

FOLLOWLINK returns a **SpecSet** — a sequence of VSpecs — as its V-position result.

Each VSpec in the result has three tumbler fields: `(doc: Tumbler, start: Tumbler, width: Tumbler)`. The `doc` field is the document ISA, `start` is the V-position within that document, and `width` is the span size [SS-SPECSET].

The conversion path is: link orgl I-addresses → sporgls (via `link2sporglset`) → VSpecs (via `linksporglset2specset` which queries the specified `homedoc`'s POOM). If an I-address has no POOM mapping in the queried document, it is silently dropped from the result — meaning the SpecSet can be empty even when the link exists [SS-FOLLOWLINK].

The returned SpecSet is the full original endpoint as stored at link creation time, not filtered by discovery context [SS-FOLLOW-LINK].

---

## Code Exploration

---

## V-Position Result Data Structure in `dofollow`

### Entry Point: `followlink()` [`fns.c:114–127`]

```c
void followlink(typetask *taskptr)
{
  typeisa linkisa;
  typespecset specset;        // ← the output
  INT whichend;
  bool getfollowlink(), dofollowlink();

    if (
       getfollowlink (taskptr, &linkisa, &whichend)
    && dofollowlink (taskptr, &linkisa, &specset, whichend)){
        putfollowlink (taskptr, specset);
      }else
        putrequestfailed (taskptr);
}
```

The FEBE handler `followlink` calls `dofollowlink()` and passes its result as `typespecset`.

---

### `dofollowlink()` [`do1.c:223–232`]

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr, &((typesporgl *)sporglset)->sporgladdress,
                              sporglset, specsetptr, NOBERTREQUIRED));
}
```

The function returns `bool` (success/failure) and fills `*specsetptr` with the V-position result. The concrete type is `typespecset`.

---

### The Type Hierarchy [`xanadu.h:65–89`]

**`typespecset`** is a pointer to a linked list of `typespec` unions:

```c
typedef typespec * typespecset;           // xanadu.h:89

typedef union {
    typevspec xxxvspec;                   // V-coordinate result
    typeispan xxxispan;                   // I-coordinate result
} typespec;                               // xanadu.h:85–88
```

Each node has a `typeitemid` discriminant (`xanadu.h:25–29`):
- `ISPANID = 1` → the union holds a raw I-span  
- `VSPECID = 3` → the union holds a V-spec

**`typevspec`** — the V-position node [`xanadu.h:78–83`]:

```c
typedef struct structtypevspec{
    struct structtypevspec *next;
    typeitemid  itemid;           // = VSPECID (3)
    typeisa     docisa;           // tumbler: which document
    typevspanset vspanset;        // linked list of V-spans
} typevspec;
```

**`typevspan`** — the actual V-span [`xanadu.h:65–74`]:

```c
typedef struct structtypespan{
    struct structtypespan *next;
    typeitemid  itemid;
    tumbler stream;               // start V-address (tumbler arithmetic)
    tumbler width;                // extent in V-space
} typespan;

typedef typespan typevspan;
typedef typevspan * typevspanset;  // linked list of V-spans
```

`typevspan` is **not a distinct struct** — it is a `typedef` alias for `typespan`, the same struct used for I-spans. The `itemid` field discriminates at runtime.

---

### Concrete Answer

The follow-equivalent operation (`dofollowlink`) represents its V-position result as:

> **`typespecset`** — a singly-linked list of `typespec` unions, where each VSPECID-tagged node is a **`typevspec`** containing:
> - `docisa` (`typeisa`/tumbler): the document identifier
> - `vspanset` (`typevspan *`): a linked list of V-spans, each holding a `stream` tumbler (start address) and `width` tumbler (extent)

The leaf type, `typevspan` (`= typespan`, `xanadu.h:73`), is the fundamental unit: two tumblers — `stream` and `width` — expressing a contiguous range of V-space addresses within a named document.
