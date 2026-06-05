## Question 19 [evidence]

> Does this operation require the link's home document to be open under BERT (PRE-DOCUMENT-OPEN / `findorgl`), and does it succeed for an orphaned link whose endpoint content is undiscoverable via `find_links`?

## KB Synthesis

The question concerns FOLLOWLINK (the operation most directly characterized by home-document involvement and orphan behavior in the KB).

**BERT / open-document requirement: No.**

FOLLOWLINK uses two sequential steps [SS-FOLLOWLINK, Finding 0048]:

1. `link2sporglset()` — reads the link orgl from the granfilade via `retrieverestricted()`. This is a direct I-space lookup; no BERT table check and no `findorgl()` call against the home document's orgl occur here.
2. `linksporglset2specset()` — converts stored I-addresses to V-addresses by probing the specified `homedoc`'s POOM. If an I-address has no current V-position mapping, `retrieverestricted` returns NULL and the address is silently dropped; the operation still returns successfully.

This contrasts sharply with `retrieve_contents`, which routes through `specset2ispanset` → `findorgl`, explicitly requiring the target document to be open [PRE-RETRIEVE-CONTENTS]. FOLLOWLINK explicitly does not: "follow_link — reads link orgl endpoint spans, returns SpecSet — no target document handle needed" [INT-LINK-FOLLOW-LIFECYCLE].

**Orphaned link behavior: Succeeds, returning empty.**

[PRE-FOLLOWLINK] states: "There is no precondition requiring that endset I-addresses be currently referenced in any POOM. The operation succeeds even when all endset I-addresses are unreferenced, returning an empty result rather than an error."

[EC-GHOST-LINK] confirms with the direct test case: "Content deleted from all documents → FOLLOWLINK(L, TO, any) returns `[]`, operation succeeds." [INV-LINK-PERMANENCE] generalizes this: FOLLOWLINK succeeds for source, target, and type endpoints regardless of V-stream state, because link orgls are permanent in I-space.

**Summary:**

| Condition | Result |
|-----------|--------|
| Home doc not in BERT open-list | Succeeds (no BERT check on link orgl path) |
| Endpoint content deleted from all documents | Succeeds, returns `[]` |
| Endpoint content partially deleted | Succeeds, returns surviving V-spans only |

---

## Code Exploration

I have all the source I need. Let me now compile the full analysis.

---

## Answer

### The Operation in Question

The question concerns two operations: **`followlink` / `dofollowlink`** (following a link to retrieve its endpoint specsets) and, by contrast, **`docreatelink`** which places the link into its home document. Both are traced below.

---

### Part 1: Does the Operation Require the Link's Home Document to Be Open Under BERT?

#### `findorgl` — the BERT gatekeeper (`granf1.c:17–41`)

Every document access goes through `findorgl`, which calls `checkforopen`:

```c
if (/*backenddaemon &&*/(temp = checkforopen(isaptr, type, user)) <= 0) {
    if (!isxumain) {
        *orglptr = NULL;
        return FALSE;
    }
}
```
[`granf1.c:22–38`]

The `/*backenddaemon &&*/` is commented out — meaning the BERT check is unconditional, not gated by daemon mode. `checkforopen` returns `> 0` only if the document is sufficiently open; `<= 0` blocks access. The single exception: `type == NOBERTREQUIRED` causes `checkforopen` to immediately return `1` (`bert.c:59–61`), bypassing every check.

---

#### `docreatelink` — home document **requires WRITEBERT** (`do1.c:195–221`)

The critical call chain:

```c
// do1.c:212
&& docopy (taskptr, docisaptr, &linkvsa, ispanset)
```

`docopy` immediately calls:

```c
// do1.c:55
&& findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
```

This is a hard gate. If the home document is not open for write, `findorgl` returns `FALSE`, and `docopy` — and therefore `docreatelink` — fails. **The home document must be open under BERT for WRITE before `docreatelink` succeeds.**

Note the contrasting situation for the link's own orgl in the same function:

```c
// do1.c:213
&& findorgl (taskptr, granf, linkisaptr, &link,/*WRITEBERT ECH 7-1*/NOBERTREQUIRED)
```

The inline comment `/*WRITEBERT ECH 7-1*/` records that this was deliberately changed from `WRITEBERT` to `NOBERTREQUIRED`. The link's own orgl does **not** require a BERT open — only the home document does.

---

#### `dofollowlink` — **no BERT requirement at all** (`do1.c:223–232`)

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
  typesporglset sporglset;
  bool link2sporglset(), linksporglset2specset();

    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (taskptr,&((typesporgl *)sporglset)->sporgladdress, sporglset, specsetptr,
                              /* ECH 6-29 READBERT */NOBERTREQUIRED));
}
```

Both calls pass `NOBERTREQUIRED`. The comment `/* ECH 6-29 READBERT */` on the second call records that this too was deliberately relaxed from `READBERT`. The calls delegate to:

- **`link2sporglset` (`sporgl.c:77`)**: `findorgl(taskptr, granf, linkisa, &orgl, NOBERTREQUIRED)` — link ISA lookup bypasses BERT entirely.
- **`linksporglset2specset` → `sporglset2vspanset` (`sporgl.c:152`)**: `(void) findorgl(taskptr, granf, homedoc, &orgl, NOBERTREQUIRED)` — the home document lookup is also NOBERTREQUIRED, and the return value is discarded with `(void)`.

**`dofollowlink` does not require the link's home document to be open under BERT.** Neither the link's ISA document nor the endpoint's home document needs a prior `PRE-DOCUMENT-OPEN`.

---

### Part 2: Does `dofollowlink` Succeed for an Orphaned Link Undiscoverable via `find_links`?

#### How `find_links` discovers links (`spanf1.c:56–103`)

`dofindlinksfromtothree` → `findlinksfromtothreesp` queries the **spanfilade**:

1. Converts query V-specs to I-spans via `specset2sporglset` (which calls `findorgl` on the source documents).
2. Calls `sporglset2linkset` → `sporglset2linksetinrange` → `retrieverestricted((typecuc*)spanf, ...)` — a direct spanfilade range query.

The spanfilade is populated at link creation time by `insertendsetsinspanf` (`do2.c:116–128`), which calls `insertspanf` for each endpoint, inserting `(ORGLRANGE=link_ISA, SPANRANGE=endpoint_I-span)` pairs. **A link is discoverable via `find_links` only if these spanfilade entries exist.**

#### How `dofollowlink` retrieves endpoints (`sporgl.c:67–95`)

`link2sporglset` reads from the **link's own orgl** (granfilade node), not from the spanfilade:

```c
// sporgl.c:77
if (!findorgl (taskptr, granf, linkisa, &orgl, type)) {
    return (FALSE);
}
// sporgl.c:83
if (context = retrieverestricted((typecuc*)orgl, &vspan, V, (typespan*)NULL, I, (typeisa*)NULL)) {
    for (c = context; c; c = c->nextcontext) {
        contextintosporgl((type2dcontext*)c, (tumbler*)NULL, sporglptr, I);
        ...
    }
    return (TRUE);
}
```

The endpoint data is retrieved directly from the link's orgl via `retrieverestricted` on `orgl` — the link's own granfilade node. The spanfilade is never consulted.

This data was stored at creation time by `insertendsetsinorgl` (`do2.c:130–149`), which calls `insertpm` to embed the endpoint sporglsets into the link's orgl — a separate write from `insertendsetsinspanf`.

#### The Architectural Separation

The system maintains **two independent indices** for link endpoint data:

| Structure | Populated by | Queried by |
|-----------|-------------|------------|
| Link's orgl (granfilade) | `insertendsetsinorgl` | `dofollowlink` via `link2sporglset` |
| Spanfilade | `insertendsetsinspanf` | `find_links` via `sporglset2linkset` |

These are written in sequence at `docreatelink:218–219`:
```c
// do1.c:218–219
&& insertendsetsinorgl (taskptr, linkisaptr, link, &fromvsa, fromsporglset, &tovsa, tosporglset, &threevsa, threesporglset)
&& insertendsetsinspanf (taskptr, spanf, linkisaptr, fromsporglset, tosporglset, threesporglset)
```

They are logically coupled but physically separate. If spanfilade entries are missing (incomplete creation, corruption, or deliberate omission), the link's orgl still retains its endpoint data.

#### Conclusion for Orphaned Link

**Yes, `dofollowlink` succeeds for an orphaned link whose endpoints are undiscoverable via `find_links`**, subject to one condition: the **link's orgl must exist in the granfilade** (so `fetchorglgr` returns non-NULL at `granf1.c:39`). If the orgl exists with valid endpoint sporglsets, `dofollowlink` returns those endpoints regardless of spanfilade state.

The V-span reconstruction (`linksporglset2specset` → `sporglset2vspanset` → `ispan2vspanset`) requires the endpoint home documents' orgls to exist in the granfilade. The call at `sporgl.c:152` discards its return value with `(void)`, meaning a missing home doc is silently tolerated — though this risks passing a garbage `orgl` pointer to `ispan2vspanset`, which is a potential crash in that edge case.

---

### Summary

| Operation | Home doc BERT required? | Succeeds when spanfilade-undiscoverable? |
|-----------|------------------------|------------------------------------------|
| `docreatelink` | **Yes — WRITEBERT** [`do1.c:55`] | N/A (creation, not lookup) |
| `dofollowlink` | **No — NOBERTREQUIRED** [`do1.c:229–230`] | **Yes**, reads link orgl directly [`sporgl.c:83`] |
| `find_links` (`dofindlinksfromtothree`) | No | N/A (the query itself) |

The deliberate `/*WRITEBERT ECH 7-1*/NOBERTREQUIRED` and `/* ECH 6-29 READBERT */NOBERTREQUIRED` annotations in the source record that these BERT relaxations were intentional design decisions, not oversights.
