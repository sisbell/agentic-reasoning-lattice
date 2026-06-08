## Question 1 [evidence]

> What does udanax-green's RETRIEVEENDSETS take as its content-region argument — a span/span-set (vspecset) that gets resolved to addresses, or an explicitly enumerated set of I-addresses?

## KB Synthesis

RETRIEVEENDSETS takes a **vspecset** (a set of V-address spans), not explicitly enumerated I-addresses.

From [SS-RETRIEVE-ENDSETS] (Finding 0035): "RETRIEVEENDSETS (opcode 28) takes a specset (V-spec of a content region) and returns three specsets simultaneously." The call chain is: `retrieveendsetsfromspanf()` **first converts the input specset to a sporglset** (V-to-I translation via `specset2sporglset()`), then uses the resulting I-addresses as the SPANRANGE restriction when searching the spanfilade.

From [INT-SPORGL-LINK-INDEX] (Finding 0035): "The specset input is converted to I-addresses (sporglset) for the SPANRANGE restriction, then each endset type is searched independently by restricting the ORGLRANGE dimension."

So the V→I conversion is internal to the operation — the caller supplies V-spans, and the operation resolves them to I-addresses before querying the spanfilade. This contrasts with FOLLOWLINK [SS-FOLLOWLINK], which takes a link ISA directly and reads the link orgl's stored I-addresses without any V-address input.

---

## Code Exploration

## RETRIEVEENDSETS Content-Region Parameter

**Short answer:** It takes a **`typespecset`** (a vspecset/span-set in V-address space), which the backend resolves to I-addresses internally. It is **not** an explicitly enumerated I-address set — that resolution happens server-side.

---

### Wire Format

`backend/get1fe.c:192–196`:
```c
bool getretrieveendsets(typetask *taskptr, typespecset *specsetptr)
{
    return (getspecset (taskptr, specsetptr));
}
```

It reads a `typespecset` off the wire — a linked list of union nodes (`backend/xanadu.h:78–89`):

```c
typedef struct structtypevspec {
    struct structtypevspec *next;
    typeitemid  itemid;     /* VSPECID=3 or ISPANID=1 */
    typeisa     docisa;
    typevspanset vspanset;
} typevspec;

typedef union {
    typevspec xxxvspec;
    typeispan xxxispan;
} typespec;
typedef typespec * typespecset;
```

Each node is tagged: either a **VSPECID** (document id + V-span set) or an **ISPANID** (raw I-address span).

---

### Call Chain

`backend/fns.c:350–362` → `backend/do1.c:369–374` → `backend/spanf1.c:190–235`:

```
retrieveendsets()         [fns.c:350]
  getretrieveendsets()    [get1fe.c:192]   ← reads typespecset
  doretrieveendsets()     [do1.c:369]
    retrieveendsetsfromspanf()  [spanf1.c:190]
      specset2sporglset()       [sporgl.c:14]  ← V→I resolution happens here
```

---

### The Resolution Step

`backend/sporgl.c:14–33` is where V-address specs become I-addresses:

```c
bool specset2sporglset(typetask *taskptr, typespecset specset,
                       typesporglset *sporglsetptr, int type)
{
    for (; specset; specset = ...) {
        if (itemid == ISPANID) {
            /* raw I-span: pass through as-is */
            *sporglsetptr = (typesporglset)specset;
        } else if (itemid == VSPECID) {
            /* V-spec: resolve via granfilade */
            vspanset2sporglset(taskptr,
                &((typevspec *)specset)->docisa,
                ((typevspec *)specset)->vspanset,
                sporglsetptr, type);
        }
    }
}
```

- **VSPECID nodes**: The backend calls `vspanset2sporglset()` which looks up the document's granfilade node (`docisa`) and walks the orgl tree to translate V-spans → I-address ranges.
- **ISPANID nodes**: Passed through directly — so the caller *can* supply raw I-addresses, but the normal usage path sends V-specs.

---

### Conclusion

RETRIEVEENDSETS takes a **`typespecset` — a vspecset in V-address space** (document id + V-spans), not a pre-enumerated I-address set. The V→I resolution is performed internally by `specset2sporglset()` at `sporgl.c:14`, via the granfilade/orgl tree lookup in `vspanset2sporglset()`. The wire protocol does permit ISPANID nodes (raw I-spans) as a degenerate case, but the canonical client argument is a VSPECID list — spans in the document's V-space.
