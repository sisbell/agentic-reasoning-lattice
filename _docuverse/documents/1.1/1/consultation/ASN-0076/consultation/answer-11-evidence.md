## Question 11 [evidence]

> When a link is created via `docreatelink`, is there any field in the link orgl structure reserved for a "supersedes" or "previous version" pointer that could record a relationship to a prior link?

## KB Synthesis

Not answerable from the KB.

The KB consistently describes the link orgl as having exactly three endsets: FROM/source (`LINKFROMSPAN=1`), TO/target (`LINKTOSPAN=2`), and THREE/type (`LINKTHREESPAN=3`) [SS-DUAL-ENFILADE Finding 0038, INT-SPORGL-LINK-INDEX Finding 0035]. The formal type is given as `Link = { source: VSpan, target: VSpan, type: Tumbler }` [SS-LINK-ENDPOINT Finding 0028].

No KB entry mentions a fourth field, supersedes pointer, or prior-link reference anywhere in the link orgl structure. The link creation path (`docreatelink`: allocate orgl → copy ISA to 2.x → index three endsets in spanf) [ST-CREATE-LINK Finding 0012] is fully described without such a field, and link permanence is stated unconditionally — links are created but never modified [INV-LINK-PERMANENCE].

Whether the orgl struct definition in the C source has unused or reserved fields beyond the three documented endsets is not covered by the KB.

---

## Code Exploration

I now have a complete picture. Here is the full answer:

---

## Does the link orgl structure have a "supersedes" / "previous version" pointer?

**No. There is no such field anywhere in the link orgl structure or the sporgl structure that holds link endpoint data.**

---

### The type definitions

`typeorgl` is defined in `backend/xanadu.h:17` as a bare `INT *` alias — a temporary placeholder, not a struct:

```c
#define typeorgl  INT *   /* temp -- INT for alignment */
```

The actual storage unit for link endpoint data is `typesporgl`, defined in `backend/xanadu.h:115–121`:

```c
typedef struct structsporgl{
    struct structsporgl *next;
    typeitemid      itemid;
    tumbler sporglorigin;
    tumbler sporglwidth;
    typeisa sporgladdress;
} typesporgl;
```

Its five fields are:
- `next` — linked-list pointer to next sporgl in the set
- `itemid` — type tag (SPORGLID)
- `sporglorigin` — tumbler marking the span's position within the link's orgl
- `sporglwidth` — tumbler marking the span's width
- `sporgladdress` — the ISA (document address) of the linked content

There is no `supersedes`, `prevlink`, `priorversion`, or any version-chain pointer.

The in-memory orgl cache structure (`backend/wisp.h:81–84`) is equally minimal:

```c
struct structorgl {
    struct structcuc *orglptr;
    typediskloafptr diskorglptr;
};
```

Just a core-memory pointer and a disk pointer. Nothing for versioning.

---

### Tracing `docreatelink`

`backend/do1.c:195–221` shows the complete link-creation path:

```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset fromspecset, typespecset tospecset,
    typespecset threespecset, typeisa *linkisaptr)
{
  typehint hint;
  tumbler linkvsa, fromvsa, tovsa, threevsa;
  typespanset ispanset;
  typesporglset fromsporglset, tosporglset, threesporglset;
  typeorgl link;
  ...
  makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
  return (
       createorglingranf(taskptr, granf, &hint, linkisaptr)   // allocate a new orgl
    && tumbler2spanset(taskptr, linkisaptr, &ispanset)
    && findnextlinkvsa(taskptr, docisaptr, &linkvsa)
    && docopy(taskptr, docisaptr, &linkvsa, ispanset)
    && findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
    && specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)
    && specset2sporglset(taskptr, tospecset, &tosporglset, NOBERTREQUIRED)
    && specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)
    && setlinkvsas(&fromvsa, &tovsa, &threevsa)
    && insertendsetsinorgl(taskptr, linkisaptr, link,
           &fromvsa, fromsporglset,
           &tovsa,   tosporglset,
           &threevsa, threesporglset)
    && insertendsetsinspanf(taskptr, spanf, linkisaptr,
           fromsporglset, tosporglset, threesporglset)
  );
}
```

`insertendsetsinorgl` (`backend/do2.c:130–148`) calls `insertpm` up to three times — once per endpoint set (from, to, three). Each call inserts a sporgl (span+address pair) into the orgl at the specified VSA position. The entire operation carries:

1. The link's ISA address (`linkisaptr`)
2. The three endpoint sporgl sets (from, to, three), each containing `sporgladdress` pointers to content spans

No supersedes pointer is written. No prior-link ISA is threaded in. No version metadata is attached.

---

### Exhaustive search result

A full-text search across all `backend/*.c` and `backend/*.h` for `supersede`, `prevlink`, `prior.link`, `previous.link`, `version.ptr`, and `link.chain` returns **zero matches** in link-related code. The only `supersede` hit is a comment in `backend/NOTES:82` reading "mostly superseded: by standard lib stuff" — unrelated to data structures.

---

### Conclusion

The link orgl structure — as implemented — stores only the three endpoint sporgl sets (from, to, three) indexed by VSA positions within the link's tumbler address space. **There is no reserved field, no pointer slot, no placeholder, and no commented-out stub for a "supersedes" or "previous version" relationship.** If link versioning were desired, it would have to be implemented entirely outside the orgl: either as a separate document-level version chain (the tumbler version chain machinery exists in `common.h` for content), or as a convention encoded in link content, but the orgl data structure itself carries no trace of it.
