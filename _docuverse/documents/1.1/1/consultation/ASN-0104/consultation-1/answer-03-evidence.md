## Question 3 [evidence]

> When RETRIEVEV is given a V-spec whose document is unallocated or not open, does the implementation return an empty/⊥ result or reject the request as a precondition failure?

## KB Synthesis

Two distinct failure cases apply here, both resulting in error responses rather than empty/⊥ results.

**Not-open document:** `doretrievev` calls `specset2ispanset`, which calls `findorgl(..., READBERT)` for each referenced document orgl. If the document is not in the session's open list, `findorgl` returns FALSE and the operation produces a backend error ("error response from back-end"). The backend log records: `orgl for <addr> not open in findorgl temp = 0`. This is a hard failure, not a graceful empty return. [PRE-RETRIEVE-CONTENTS]

**Unallocated document:** An unallocated document can never be in the open list, so it fails the same `findorgl` check by the same mechanism. Additionally, [PRE-SPECSET] notes that `specset2sporglset()` checks that the referenced document exists — a distinct validation path used in link operations, but the open-list check comes first for RETRIEVEV. Either way, the result is an error response.

**Summary:** RETRIEVEV rejects both cases as precondition failures (error responses), not empty/⊥. The precondition `∀ doc ∈ specset.referenced_documents : doc ∈ open_docs(session)` must hold, and the implementation enforces it by failing rather than returning empty content. [PRE-RETRIEVE-CONTENTS, SS-DOCUMENT-LIFECYCLE]

---

## Code Exploration

I have everything I need. Here is the complete answer.

---

## RETRIEVEV: Behavior on Unallocated or Unopened Document

**Short answer:** Both cases — document not open and document not allocated — result in a **precondition failure** (`putrequestfailed`), never an empty/⊥ result. The two cases fail at different points in the call chain, but neither produces a graceful empty response.

---

### Call Path

```
retrievev()           [fns.c:175]
  doretrievev()       [do1.c:338]
    specset2ispanset(..., READBERT) [do2.c:14]
      findorgl(..., READBERT)       [granf1.c:17]
        checkforopen()              [bert.c:52]
        fetchorglgr()               [granf2.c:22]
```

---

### Case 1 — Zero docisa (malformed spec)

`specset2ispanset` [do2.c:28–33] checks first:

```c
if (iszerotumbler (&((typevspec *)specset)->docisa))
#ifndef DISTRIBUTION
    qerror ("retrieve called with docisa 0\n");
#else
    gerror("");
#endif
```

This is a fatal call — `qerror`/`gerror` — before any access check. The process aborts in distribution mode.

---

### Case 2 — Document not open

`findorgl` [granf1.c:22] immediately calls `checkforopen(isaptr, READBERT, user)`.

`checkforopen` [bert.c:52–87] scans the bert hash table. For a document with no entry, `foundnonread` stays false, and because `type == READBERT` the function returns **0** [bert.c:81]:

```c
if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
} else {
    return -1;
}
```

Back in `findorgl` [granf1.c:22], `temp == 0` satisfies `<= 0`. With `isxumain == false` (FEBE daemon mode):

```c
if (!isxumain) {
    *orglptr = NULL;
    return FALSE;      // [granf1.c:35]
}
```

`findorgl` returns FALSE. `specset2ispanset` returns FALSE [do2.c:37]. `doretrievev` returns FALSE [do1.c:343–345]. `retrievev` calls `putrequestfailed` [fns.c:185–186].

> **Note on `isxumain`:** When the backend runs as the standalone Xanadu main process (`isxumain == true`), the open check is *bypassed* and the code falls through to `fetchorglgr`. This is the old single-user path. In FEBE daemon mode, `isxumain` is false and the bert gate is enforced.

---

### Case 3 — Document not allocated in granfilade

If `checkforopen` returns > 0 (e.g., `isxumain == true`, or the document is genuinely open by this connection), execution falls through to `fetchorglgr` [granf1.c:39].

`fetchorglgr` [granf2.c:22–81] has three distinct NULL-return paths for a missing/unallocated document:

```c
// [granf2.c:31] Address beyond the granfilade's extent:
if (tumblercmp (&((typecuc*)fullcrumptr)->cwid.dsas[WIDTH], address) == LESS)
    return (NULL);

// [granf2.c:34–35] retrievecrums finds nothing:
if ((context = retrievecrums ((typecuc*)fullcrumptr, address, WIDTH)) == NULL)
    return NULL;

// [granf2.c:37–40] Retrieved position doesn't match the address exactly:
if (!tumblereq((tumbler*)&context->totaloffset, address)) {
    crumcontextfree(context);
    return (NULL);
}
```

Back in `findorgl` [granf1.c:39–40]:

```c
*orglptr = fetchorglgr(taskptr, granfptr, isaptr);
return (*orglptr ? TRUE : FALSE);
```

`fetchorglgr` returned NULL → `findorgl` returns FALSE → propagates to `putrequestfailed` [fns.c:186] exactly as in Case 2.

---

### Summary Table

| Condition | Where it fails | Result |
|---|---|---|
| `docisa` is zero tumbler | `specset2ispanset` [do2.c:28] | Fatal `gerror` / abort |
| Document not open (daemon mode) | `findorgl` [granf1.c:35] via `checkforopen` returning 0 | `putrequestfailed` |
| Document not open (main mode) | Falls through to `fetchorglgr` → NULL | `putrequestfailed` |
| Document not allocated in granfilade | `fetchorglgr` [granf2.c:31–40] returns NULL | `putrequestfailed` |

**There is no code path in `doretrievev` → `specset2ispanset` → `findorgl` that returns an empty vstuffset in response to a missing or unopened document.** The empty vstuffset result (`*vstuffsetptr = NULL`, `return TRUE`) only occurs in `ispanset2vstuffset` [granf1.c:66] when the translated ispanset is itself empty — i.e., the document *was* found and opened but contains no content at the requested V-positions. That is the ⊥/empty case; it is never reached for an unopened or unallocated document.
