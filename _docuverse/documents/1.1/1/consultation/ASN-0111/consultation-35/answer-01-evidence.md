## Question 1 [evidence]

> When the udanax-green back end receives a request to retrieve a link's endsets for an address with no allocated link, does it return a distinguished error/failure response to the front end, or does it treat the request as a protocol violation outside the operation's contract?

## KB Synthesis

The KB gives a partial but not complete answer to this question.

**What the KB establishes:**

[PRE-FOLLOWLINK] (Finding 0048) states directly:

> FOLLOWLINK requires: (1) the link ISA must reference an existing link orgl — if `findorgl()` returns FALSE, the operation fails.

The code reference cited is `backend/sporgl.c:76-78` where `link2sporglset()` returns FALSE when the link orgl is not found.

So the back end detects the absence of a link at the given address. The precondition is that the link exists; violating it causes the operation to "fail."

**What the KB does not establish:**

The KB does not document what FEBE response is sent when `findorgl()` returns FALSE for a non-existent link. The distinction you're asking about — distinguished error response vs. silent empty return — is not answered.

The closest analogy is [EC-RESPONSE-BEFORE-CHECK] (Finding 0050), which shows that for *mutation* operations (INSERT, DELETEVSPAN), the back end sends a success response *before* calling `doXXX`, so internal failures like a failed BERT check are silently swallowed. However, FOLLOWLINK is a query operation, and the cited pattern in Finding 0050 explicitly notes that `createlink` — also a query-influenced operation — follows the *correct* pattern (checks success before sending response).

[EC-GHOST-LINK] (Finding 0048) is informative by contrast: when the link *does* exist but its endset I-addresses have no POOM mappings, FOLLOWLINK "still succeeds" and returns `[]` with `works: true`. This is an empty-result success, not an error. But that case satisfies the precondition (link orgl exists); the question asks about the precondition-failing case.

**Summary:**

The KB establishes that a non-existent link ISA violates FOLLOWLINK's precondition and causes an internal failure at `findorgl()`. It does not document whether the back end then sends a `putrequestfailed` response, returns an empty success, crashes, or silently does nothing. This is a gap in the KB — no finding tested or reported FOLLOWLINK behavior specifically for an unallocated address.

---

## Code Exploration

I have all the information needed. Here is the full answer.

---

## Answer

**The backend returns a distinguished failure response (`'?'`) to the front end. It does not treat the request as a protocol violation.**

---

### Execution Path: `retrieveendsets`

The relevant FEBE top-level handler is `retrieveendsets` (`fns.c:350-362`):

```c
void retrieveendsets(typetask *taskptr)
{
  typespecset specset, fromset, toset, threeset;
  ...
    if (
       getretrieveendsets (taskptr, &specset)
    && doretrieveendsets (taskptr, specset, &fromset, &toset, &threeset)){
        putretrieveendsets (taskptr, fromset, toset, threeset);
     }else
        putrequestfailed (taskptr);          // <-- failure path
}
```

Every operation in `fns.c` follows this idiom: `get...() && do...()` → success response or `putrequestfailed`. The `else` branch is the in-contract failure path, not an assertion or abort.

---

### Failure Propagation Down the Stack

**`doretrieveendsets`** (`do1.c:369-374`) is a thin wrapper:

```c
bool doretrieveendsets(typetask *taskptr, typespecset specset, ...)
{
    return retrieveendsetsfromspanf(taskptr, specset, fromsetptr, tosetptr, threesetptr);
}
```

**`retrieveendsetsfromspanf`** (`spanf1.c:190-235`) immediately calls:

```c
if (!(specset2sporglset (taskptr, specset, &sporglset, NOBERTREQUIRED)
    && retrievesporglsetinrange(...)
    && linksporglset2specset(...))) {
        return (FALSE);                       // propagated upward
}
```

**`specset2sporglset`** (`sporgl.c:14-33`) calls `vspanset2sporglset` for each VSPEC item:

```c
if (!(sporglsetptr = vspanset2sporglset(taskptr, &docisa, vspanset, sporglsetptr, type))){
    return (FALSE);
}
```

**`vspanset2sporglset`** (`sporgl.c:35-65`) calls `findorgl` as its first act:

```c
if (!findorgl (taskptr, granf, docisa, &orgl, type)){
    return (NULL);               // causes specset2sporglset to return FALSE
}
```

---

### The Gate: `findorgl`

**`findorgl`** (`granf1.c:17-41`):

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        if (!isxumain) { return FALSE; }
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

Since all endset retrieval calls pass `NOBERTREQUIRED` (`common.h:165` → value `0`), the bert access-control check is completely bypassed. **`checkforopen`** (`bert.c:59-61`) short-circuits immediately:

```c
if (type == NOBERTREQUIRED) {
    return 1;   /* Random > 0 */
}
```

Control falls straight to **`fetchorglgr`** (`granf2.c:22-81`), which traverses the granfilade:

```c
if (tumblercmp(&fullcrumptr->cwid.dsas[WIDTH], address) == LESS)
    return (NULL);                           // address out of range

if ((context = retrievecrums(fullcrumptr, address, WIDTH)) == NULL)
    return NULL;                             // no crum found

if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return (NULL);                           // exact-match test failed
}
```

When no link is allocated at the given address, every path through `fetchorglgr` returns `NULL`. Consequently `findorgl` returns `FALSE` at `granf1.c:40`.

---

### The Same Holds for `followlink`

**`dofollowlink`** (`do1.c:223-232`) takes the analogous path via `link2sporglset`:

```c
bool dofollowlink(typetask *taskptr, typeisa *linkisaptr, typespecset *specsetptr, INT whichend)
{
    return (
       link2sporglset (taskptr, linkisaptr, &sporglset, whichend, NOBERTREQUIRED)
    && linksporglset2specset (...));
}
```

**`link2sporglset`** (`sporgl.c:67-95`) calls `findorgl` identically:

```c
if (!findorgl (taskptr, granf, linkisa, &orgl, type)){
    return (FALSE);
}
```

Same failure chain; `followlink` (`fns.c:114-127`) also terminates in `putrequestfailed`.

---

### What `putrequestfailed` Sends

**`putrequestfailed`** (`putfe.c:364-368`):

```c
int putrequestfailed(typetask *taskptr)
{
/*gerror("putrequestfailed \n");*/
    xuputc (FAILFLAG, taskptr->outp);
}
```

`FAILFLAG` is defined at `putfe.c:29`:

```c
#define FAILFLAG '?'
```

A single ASCII `?` byte is written to the output stream. This is the protocol's designated failure sentinel — the same byte emitted for every failed operation across all operation types in `fns.c`. The commented-out `gerror` shows the authors once considered treating this as a hard error but chose not to: it is a soft, protocol-level failure reply.

---

### Summary

| Layer | File : Line | Action on missing link |
|---|---|---|
| `retrieveendsets` / `followlink` | `fns.c:350`, `fns.c:114` | Calls `putrequestfailed` on `FALSE` return |
| `doretrieveendsets` / `dofollowlink` | `do1.c:369`, `do1.c:223` | Returns `FALSE` |
| `retrieveendsetsfromspanf` / `link2sporglset` | `spanf1.c:222`, `sporgl.c:77` | Returns `FALSE` on `findorgl` failure |
| `findorgl` | `granf1.c:40` | Returns `FALSE` when `fetchorglgr` → `NULL` |
| `fetchorglgr` | `granf2.c:31–39` | Returns `NULL`: address out of range or no exact match in granfilade |
| `putrequestfailed` | `putfe.c:367` | Writes `FAILFLAG` (`'?'`) to output stream |

**Conclusion:** A request to retrieve endsets for an unallocated link address is handled within the operation's contract. The backend returns the standard `'?'` failure byte — a distinguished, protocol-level error response — not a crash, hang, or protocol violation.
