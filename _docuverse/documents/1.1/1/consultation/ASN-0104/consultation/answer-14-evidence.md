## Question 14 [evidence]

> Does a read against an I-address that still exists in the granfilade but is no longer referenced by any POOM (a deleted-but-permanent fragment per FC-GRANFILADE-PERMANENT) return its original bytes if addressed by I-address directly?

## KB Synthesis

## Direct I-Address Retrieval After POOM Deletion

**Yes, the bytes remain structurally present and internally accessible — but no FEBE-exposed operation retrieves them by raw I-address when no POOM maps them.**

### The Bytes Are Permanently There

[INV-IADDR-IMMUTABILITY] (Findings 0030, 0031, 0064) establishes the core guarantee: the granfilade is append-only. `inserttextingranf` allocates I-addresses permanently; no operation deallocates them. DELETE frees only the POOM bottom crums that *reference* I-addresses — the granfilade entry is untouched.

[FC-GRANF-ON-DELETE] (Finding 0061) confirms: DELETE modifies only the spanfilade/POOM, leaving granfilade state identical. The I-address `i` with its associated bytes persists regardless of how many POOMs have dropped their `v → i` mappings.

### The Internal Path Exists

[SS-GRANF-OPERATIONS] (Finding 0012) documents `ispanset2vstuffset()` as a granfilade primitive: given an I-span set, return the corresponding content bytes. This function queries the granfilade tree directly by I-address with no POOM involvement. Internally, it *would* return the original bytes for any permanently-allocated I-address.

### But No FEBE Operation Exposes This

[PRE-RETRIEVE-CONTENTS] (Findings 0010, 0027) makes the constraint explicit: the standard `RETRIEVE_CONTENTS` path is `doretrievev` → `specset2ispanset` (V→I via document POOM) → `ispanset2vstuffset` (I→bytes). The V→I step calls `findorgl`, which requires the document to be open and the I-address to be currently mapped in that document's POOM. No FEBE opcode takes a raw I-address and returns bytes.

[SS-FOLLOWLINK] (Finding 0048) / [INV-ITOV-FILTERING] show the same pattern: even link-following resolves I-addresses through a document's POOM, and silently drops any I-address with no current POOM mapping.

### The Documented Recovery Path

[ST-COPY] (Finding 0064) is explicit: the only documented mechanism for identity-preserving restoration after DELETE is `VCOPY` from a document that still has those I-addresses mapped — typically a version created before the deletion. `INSERT` of the same text allocates *fresh* I-addresses; it does not recover the originals.

### Summary

| Layer | Bytes present? | Accessible via FEBE? |
|-------|---------------|----------------------|
| Granfilade | Yes, permanently | Only if some POOM maps the I-address |
| POOM (deleted doc) | Mapping gone | No |
| Standard RETRIEVE | Requires open doc + POOM entry | Fails if mapping absent |
| `ispanset2vstuffset` | Would succeed internally | Not exposed as a FEBE opcode |

The KB does not document any FEBE operation that bypasses the document-POOM requirement to retrieve bytes directly by I-address. The design intent appears to be that permanent I-addresses enable *reconstitution via transclusion* (copying them into a new document), not direct I-address reads.

---

## Code Exploration

The permission prompt will appear separately. Here is the full answer:

---

## Answer: Does a Direct I-Address Read Return the Original Bytes?

**Yes.** A deleted-but-permanent granfilade fragment returns its original bytes when addressed by I-address directly. This holds at every layer: the delete path never touches the granfilade, the retrieval path searches it purely by I-address, and the FEBE wire protocol explicitly supports raw I-span reads.

---

### The Two-Layer Architecture

There are two separate enfilades. The **granfilade** (`granf`) stores text at I-addresses (WIDTH dimension) and is permanent. The **POOM** (`orgl`, one per document) maps V-addresses to I-addresses. Delete only affects the POOM. They are fully independent.

---

### 1. Delete touches only the POOM

`dodeletevspan` [`do1.c:158-167`]:
```c
bool dodeletevspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, WRITEBERT)
    && deletevspanpm (taskptr, docisaptr, docorgl, vspanptr));
}
```

`deletevspanpm` [`orglinks.c:145-152`]:
```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return (FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return (TRUE);
}
```

`deletend` [`edit.c:31-76`] receives `docorgl` — the document's POOM — and frees the crums holding V→I mappings. **The global granfilade (`granf`) is never passed to `deletend`.** There is no `deleteseq` call on `granf` anywhere in this chain.

---

### 2. Granfilade retrieval searches by I-address, no POOM check

`ispan2vstuffset` [`granf2.c:286-317`] calls `retrieveinspan` on `granf`:

```c
context = retrieveinspan((typecuc*)fullcrumptr, &lowerbound, &upperbound, WIDTH);
```

`retrieveinspan` [`retrie.c:112-136`] dispatches to `findcbcinspanseq` [`retrie.c:307-329`]:

```c
int findcbcinspanseq(typecorecrum *crumptr, typewid *offsetptr,
                     tumbler *spanstart, tumbler *spanend, typecontext **headptr)
{
    for (; crumptr; crumptr = getrightbro(crumptr)) {
        if (!crumintersectsspanseq(crumptr, (tumbler*)&localoffset, spanstart, spanend)) {
            dspadd(&localoffset, &crumptr->cwid, &localoffset, (INT)crumptr->cenftype);
            continue;
        }
        if (crumptr->height == 0) {
            context = makecontextfromcbc((typecbc*)crumptr, offsetptr);
            oncontextlistseq(headptr, context);
        } else {
            findcbcinspanseq(findleftson((typecuc*)crumptr), ...);
        }
    }
}
```

**No POOM check anywhere.** The gran tree is searched by I-address range (`crumintersectsspanseq` compares WIDTH values). If a `GRANTEXT` crum exists at I-address X, it is found and returned — regardless of whether any POOM currently maps to it.

---

### 3. The FEBE wire protocol supports raw I-span reads

`specset2ispanset` [`do2.c:23-26`]:
```c
if (((typeitemheader *)specset)->itemid == ISPANID) {
    *ispansetptr = (typeispanset)specset;   // Pass-through: no POOM lookup
    ispansetptr = ...;
}
```

An `ISPANID` item bypasses `findorgl` and `vspanset2ispanset` entirely and goes straight to `ispan2vstuffset` → `retrieveinspan` on `granf`.

`getspecset` in the FEBE front-end [`get2fe.c:147-180`] creates `ISPANID` items when the wire uses flag character `'s'` (`SPANFLAG`):
```c
if (c == SPANFLAG) {
    specset = (typespecset)taskalloc(taskptr, sizeof(typespan));
    if (!getspan(taskptr, specset, ISPANID))   // itemid = ISPANID
        return(FALSE);
}
```

So `retrieve_contents` (command 5) accepts two specset entry types:
- `'v'` (`VSPECFLAG`): document ISA + V-spans → POOM lookup → I-spans → granfilade
- `'s'` (`SPANFLAG`): raw I-spans → granfilade **directly**, POOM not consulted

With `'s'`, a caller who knows the I-address of deleted content can retrieve its bytes without any open document or POOM state. The backend code fully supports this.

**Caveat**: The Python `client.py` `SpecSet` class only creates `VSPECID` items (via `VSpec`). There is no Python API for raw I-spans. A client must speak the wire protocol directly.

---

### Summary

| Layer | What happens on delete | What remains |
|-------|----------------------|--------------|
| **POOM** (`docorgl`) | `deletend` prunes the V→I mapping crums [`edit.c:31-76`] | Mapping is gone |
| **Granfilade** (`granf`) | Nothing — never touched | `GRANTEXT` crum at I-address X persists forever |
| **Wire protocol** | Not involved | `'s'` flag in a specset reads granfilade directly by I-address [`get2fe.c:147-180`] |

The POOM is a view over the permascroll. Deleting from the view does not delete from the scroll. FC-GRANFILADE-PERMANENT is confirmed at the code level: there is no granfilade delete operation, and `findcbcinspanseq` will faithfully return deleted content to anyone who still knows its I-address.

The finding has been written to `findings/0079-granfilade-direct-iaddress-read.md` (pending your write permission approval).
