## Question 1 [evidence]

> Does udanax-green's `docreatenewversion` (or equivalent) permit the source document operand to be uninstantiated in the registry, or does it always require the source to exist in allocated state?

## KB Synthesis

Based on the KB, `docreatenewversion` **always requires the source document to exist in allocated state**.

The operation's internal call chain makes this mandatory:

1. `docreatenewversion` calls `doretrievedocvspanfoo` to retrieve the source document's V-span [ST-VERSION-CREATE, Finding 0032; ST-VERSION, Finding 0077]
2. `doretrievedocvspanfoo` delegates to `retrievedocumentpartofvspanpm`, which reads `cdsp.dsas[V]` and `cwid.dsas[V]` from the source document's root crum [ST-VERSION-CREATE, Finding 0043]
3. This requires the source orgl to be present and findable in the granfilade

The document lifecycle model requires a document to be open (in the open list) for orgl-based operations to succeed; `findorgl` returns FALSE if not, causing the operation to fail [SS-DOCUMENT-LIFECYCLE].

The only relaxation: the source may be **empty** (never-filled). Finding 0007 in [ST-VERSION-CREATE] explicitly states "even empty documents can be versioned (the resulting version has an empty reference set)." The postcondition for that case is `references(version) = ∅`.

An uninstantiated source — one with no orgl in the granfilade — is not addressable by `doretrievedocvspanfoo` and would fail at the V-span retrieval step. The KB contains no finding describing a successful version of a non-existent source document.

---

## Code Exploration

I now have a complete trace. Here is my full answer.

---

## Does `docreatenewversion` require the source document to exist in allocated state?

**Yes — the source must exist in the granfilade. But it does NOT need to be open in the bert (registry) table.**

---

### Full Execution Path

**FEBE entry point — `fns.c:289–300`**

```c
void createnewversion(typetask *taskptr) {
    if (   getcreatenewversion(taskptr, &originaldocisa)
        && docreatenewversion(taskptr, &originaldocisa, &originaldocisa, &newdocisa))
        putcreatenewversion(taskptr, &newdocisa);
    else
        putrequestfailed(taskptr);
}
```

`getcreatenewversion` (`get1.c:76–80`) calls `getisa` → `gettumbler` — it only parses a tumbler address off the wire. There is **no existence check here**. Any well-formed tumbler is accepted.

---

**`docreatenewversion` — `do1.c:260–299`**

The function has two sequential guard points:

**Guard 1 — create the new destination document** (`do1.c:277–279`):
```c
if (!createorglingranf(taskptr, granf, &hint, newisaptr)) {
    return (FALSE);
}
```
This allocates a new orgl in the granfilade for the destination. If this fails, return immediately.

**Guard 2 — retrieve the source document's vspan** (`do1.c:281–283`):
```c
if (!doretrievedocvspanfoo(taskptr, isaptr, &vspan)) {
    return FALSE;
}
```
This retrieves the source document's address range. If the source does not exist, this returns `FALSE` and the whole function returns `FALSE`.

Note the ordering hazard: Guard 1 runs **before** Guard 2. If the source doesn't exist, a new orphaned destination orgl has already been allocated in the granfilade before the failure is detected (it is never added to bert, never modified, never closed).

---

**`doretrievedocvspanfoo` — `do1.c:301–309`**

```c
return (
    findorgl(taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)
 && retrievedocumentpartofvspanpm(taskptr, docorgl, vspanptr));
```

The critical argument is `NOBERTREQUIRED`. This flag bypasses the bert open-state check entirely.

---

**`findorgl` — `granf1.c:17–41`**

```c
if ((temp = checkforopen(isaptr, type, user)) <= 0) {
    ...
    return FALSE;
}
*orglptr = fetchorglgr(taskptr, granfptr, isaptr);
return (*orglptr ? TRUE : FALSE);
```

With `type == NOBERTREQUIRED`, `checkforopen` at `bert.c:59–61` immediately returns 1:
```c
if (type == NOBERTREQUIRED) {
    return 1;   /* Random > 0 */
}
```
The bert table is never consulted. Then `fetchorglgr` is called to locate the source in the granfilade.

---

**`fetchorglgr` — `granf2.c:22–81`**

This is the hard existence check:

```c
// granf2.c:31 — address beyond tree width → NULL
if (tumblercmp(&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
    return (NULL);

// granf2.c:34 — crum not found in tree → NULL
if ((context = retrievecrums((typecuc*)fullcrumptr, address, WIDTH)) == NULL)
    return NULL;

// granf2.c:37–40 — found a crum, but it's not at this exact address → NULL
if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return (NULL);
}
```

If the source ISA is not found exactly in the granfilade, `fetchorglgr` returns `NULL`. `findorgl` then returns `FALSE` (`granf1.c:40`), `doretrievedocvspanfoo` returns `FALSE` (`do1.c:307`), and `docreatenewversion` returns `FALSE` (`do1.c:282`), which triggers `putrequestfailed` (`fns.c:299`).

---

### Summary

| Requirement | Enforced? | Where |
|---|---|---|
| Source ISA must be parseable as a tumbler | Yes | `get1.c:76–80` (wire parse) |
| Source must be open in bert table | **No** | `NOBERTREQUIRED` at `do1.c:307` bypasses `bert.c:59–61` |
| Source must exist in the granfilade | **Yes** | `fetchorglgr` null-checks at `granf2.c:31`, `34`, `37–40` |

The function **does not require the source to be in open/registered state**, but it **does unconditionally require the source to exist as an allocated granfilade entry**. An uninstantiated ISA — a tumbler that was never the subject of a prior `createorglingranf` call — will cause `fetchorglgr` to return `NULL`, propagate failure up through `doretrievedocvspanfoo` → `docreatenewversion`, and result in `putrequestfailed` at the FEBE layer. There is no code path permitting the source to be absent.
