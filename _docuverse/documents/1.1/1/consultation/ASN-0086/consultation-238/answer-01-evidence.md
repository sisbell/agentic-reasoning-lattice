## Question 1 [evidence]

> Does udanax-green's retraction mechanism constrain a retraction's target to an existing link address, or does it permit retracting an arbitrary (possibly never-allocated) tumbler/prefix?

## KB Synthesis

The KB contains no entries about a retraction mechanism. The operations documented cover INSERT, DELETE (DELETEVSPAN), REARRANGE, VCOPY, VERSION, CREATELINK, FINDLINKS, FOLLOWLINK, RETRIEVEENDSETS, and COMPARE-VERSIONS — but nothing named "retraction" or describing a mechanism that withdraws or supersedes a previously created link or assertion.

This question is not answerable from the KB as provided.

---

## Code Exploration

I now have everything needed for a complete answer. Here is the full analysis:

---

## Does udanax-green's retraction mechanism constrain its target to an existing link address?

### Primary Finding: No Retraction Operation Exists

Udanax-green implements **no retraction mechanism at all**. The authoritative opcode table in `backend/requests.h` defines 20 operations with no RETRACT, DELETELINK, or FORGETLINK entry:

```c
#define INSERT 0
#define RETRIEVEDOCVSPANSET 1
#define COPY 2
#define REARRANGE 3
#define RETRIEVEV 5
#define CREATENEWDOCUMENT 11
#define DELETEVSPAN 12
#define CREATENEWVERSION 13
#define FOLLOWLINK 18
#define CREATELINK 27
#define RETRIEVEENDSETS 28
#define FINDLINKSFROMTOTHREE 30
...
```
[`backend/requests.h:21-46`]

The dispatch table in `backend/init.c:42-76` assigns `nullfun` (which immediately returns `putrequestfailed`) to every slot not explicitly listed. No slot is assigned anything resembling link deletion.

A grep for `retract`, `deletelink`, `forgetlink`, and `removelink` (case-insensitive) across all `.c` and `.h` files in `backend/` returns **zero matches** — the only hit is `unlink(file)` in `xumain.c:152`, a standard POSIX filesystem call unrelated to Xanadu links.

### Links Are Permanent in the Data Model

The only link-related operations exposed by the FEBE protocol are:

| Opcode | Function | Purpose |
|--------|----------|---------|
| 27 — `CREATELINK` | `createlink()` [`fns.c:100`] | Creates a new link, allocates an address |
| 18 — `FOLLOWLINK` | `followlink()` [`fns.c:114`] | Reads a link's endpoints |

`DELETEVSPAN` (opcode 12) removes text content from a document's V-space but does not touch the link granfilade. Once `docreatelink()` [`do1.c:195`] writes a link into the granfilade and assigns it a tumbler address via `createorglingranf()`, there is no protocol path to remove or invalidate it.

### What the Architecture Would Enforce (If Retraction Were Added)

Although no retraction operation exists, the granfilade lookup infrastructure makes clear what any such operation *would* require. Every link read goes through this chain:

**`followlink()` → `dofollowlink()` → `link2sporglset()` → `findorgl()` → `fetchorglgr()`**

`fetchorglgr()` [`backend/granf2.c:22-81`] performs three sequential guards before returning a usable link pointer:

```c
// Guard 1 — bounds check [granf2.c:32]
if (tumblercmp (&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
    return (NULL);

// Guard 2 — crum context retrieval [granf2.c:34-35]
if ((context = retrievecrums ((typecuc*)fullcrumptr, address, WIDTH)) == NULL)
    return NULL;

// Guard 3 — EXACT address match [granf2.c:37-39]
if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return (NULL);
}
```

Guard 3 is the critical one. `retrievecrums()` [`retrie.c:15-31`] navigates the enfilade tree to the *containing* crum — i.e., the closest bracketing position — not necessarily an exact hit. The exact-match test `tumblereq()` immediately after is what rejects addresses that were never allocated. An arbitrary tumbler that was never written by `createorglingranf()` would fail guard 3 and `fetchorglgr()` would return `NULL`, causing the calling function to return `FALSE` and the FEBE handler to emit `putrequestfailed`.

The sister function `isaexistsgr()` [`granf2.c:244-253`] makes this pattern explicit:

```c
bool isaexistsgr(typecuc *crumptr, typeisa *isaptr)
{
  context = retrieve (crumptr, isaptr, WIDTH);   // line 249: nearest bracketing crum
  ret = tumblereq ((tumbler*)&context->totaloffset, isaptr); // line 250: exact match?
  contextfree (context);
  return (ret);
}
```

### Conclusion

**Retraction does not exist in udanax-green.** There is no FEBE opcode, no C function, and no data-path for it. Links, once created, are permanent in the backend's data model — neither the protocol nor the implementation provides any mechanism to remove, invalidate, or retract them.

If a retraction operation were to be grafted onto the system, the granfilade's exact-match lookup (`tumblereq` at `granf2.c:37-39`) would enforce that the target must be a previously allocated link address. An arbitrary or never-allocated tumbler prefix would fail the exact-match guard and the operation would return failure — the architecture admits no silent no-ops on phantom addresses.
