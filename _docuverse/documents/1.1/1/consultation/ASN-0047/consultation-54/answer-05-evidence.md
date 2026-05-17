## Question 5 [evidence]

> Does `docreatenewversion` strictly require the source document to be a live granfilade entity (e.g., via `doretrievedocvspanfoo`) before issuing a version address, or can a version be allocated against an address that was never instantiated or has been removed?

## KB Synthesis

**Yes, `docreatenewversion` requires the source to be a live, open granfilade entity — but the check is deferred until after the version address is allocated.**

## Operation Sequence and Where the Liveness Check Falls

From [ST-VERSION-CREATE Finding 0032], the internal sequence is:
1. **Allocate** a new orgl under the source's address space via `createorglingranf`
2. **Retrieve** the source's vspanset via `doretrievedocvspanfoo`
3. **Copy** content via `docopyinternal`

The address allocation (step 1) uses the source ISA only as a hint for `findisatoinsertnonmolecule`. Per [SS-ADDRESS-ALLOC Finding 0021], that function searches for the highest existing address below the upper bound, falling back to the first-child convention (`hintisa.0.1`) if nothing is found. **This lookup does not verify the source has a live orgl** — it only searches the granfilade address tree.

The liveness requirement arrives at step 2. `doretrievedocvspanfoo` delegates to `retrievedocumentpartofvspanpm`, which reads the source document's root POOM node [SS-VSPAN-VS-VSPANSET Finding 0035, ST-VERSION-CREATE Finding 0043]. Per [SS-DOCUMENT-LIFECYCLE Finding 0027], operations that resolve V→I mappings require the document to be in the open list — `findorgl` must return TRUE. If the source is not open, step 2 fails.

This means: a version address can be allocated against a source that doesn't exist as a live entity, **but the operation will fail before completing**, leaving an allocated address with no content.

## "Never Instantiated" vs "Removed"

These are not symmetric cases:

- **Never instantiated:** No orgl exists at the source address. Address allocation may still succeed (first-child convention), but `doretrievedocvspanfoo` fails because there is no granfilade root node to read.

- **"Removed":** The Xanadu model has no true document deletion. Per [INV-MONOTONIC] and [FC-GRANF-ON-DELETE Findings 0061, 0068], granfilade addresses are permanent — deleting a version does not remove its address and does not affect subsequent allocation. A "removed" document in practice means the document was **closed** (not in the open list). Its address persists; its orgl is findable by `findorgl` only if it is open.

## Ownership and the Two Allocation Paths

[SS-VERSION-ADDRESS Finding 0068] adds a subtlety: ownership determines *where* the version address lands, not whether source liveness is checked.

- **User owns source:** `makehint(DOCUMENT, DOCUMENT, 0, isaptr, &hint)` — version allocated as child of source. Containment check is applied after `findpreviousisagr`.
- **User does not own source:** `makehint(ACCOUNT, DOCUMENT, 0, wheretoputit, &hint)` — version allocated under the creating user's account, bypassing the source's address space entirely.

In the unowned case, the address allocation doesn't even consult the source's address space directly, yet step 2 still requires the source document to be open for content retrieval.

## Summary

`docreatenewversion` requires the source to be an open, accessible granfilade entity **for the operation to complete**, even though the version address allocation happens first and does not itself enforce this. A source that was never instantiated or is currently closed will cause failure at `doretrievedocvspanfoo`. The precondition stated in [ST-VERSION-CREATE Finding 0032] — "the source document exists" — means the source must be open and readable, not merely that its address appears in the tumbler hierarchy.

---

## Code Exploration

Now I have everything I need. Let me synthesize the full answer.

---

## Does `docreatenewversion` Strictly Require a Live Granfilade Entity?

The short answer is **nuanced**: the source must exist structurally in the granfilade tree, but does **not** need to be "live" in the bert open-state sense — and critically, the new version address is **allocated before the source is validated**, creating a potential leak.

---

### The Execution Path

**`createnewversion` FEBE handler** — `fns.c` (calls `docreatenewversion` in a short-circuit chain):
```c
if (getcreatenewversion(taskptr, &originaldocisa)
 && docreatenewversion(taskptr, &originaldocisa, &originaldocisa, &newdocisa))
    putcreatenewversion(taskptr, &newdocisa);
else
    putrequestfailed(taskptr);
```

**`docreatenewversion`** — `do1.c:260–299`:
```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    /* ... build hint based on ownership ... */
    if (!createorglingranf(taskptr, granf, &hint, newisaptr)) {   // line 277: allocates new ISA
        return (FALSE);
    }
    if (!doretrievedocvspanfoo(taskptr, isaptr, &vspan)) {        // line 281: validates source
        return FALSE;   // ← source check happens AFTER allocation
    }
    /* ... copy content, open/close new version ... */
    return (TRUE);
}
```

---

### Finding 1: Version Address Allocated Before Source Validation

`createorglingranf` at **`do1.c:277`** inserts a new `GRANORGL` node into the granfilade for `newisaptr` via `createorglgr` → `findisatoinsertgr` → `insertseq` [`granf2.c:111–128`]:

```c
locinfo.infotype = GRANORGL;
locinfo.granstuff.orglstuff.orglptr = createenf(POOM);   // granf2.c:120
reserve((typecorecrum*)locinfo.granstuff.orglstuff.orglptr);
insertseq((typecuc*)fullcrumptr, isaptr, &locinfo);       // granf2.c:125
```

This allocation happens **before** any check that `isaptr` (the source) is valid. If the source check at `do1.c:281` subsequently fails, the new granfilade entry for `newisaptr` is stranded — there is no rollback.

---

### Finding 2: Source Validation Uses `NOBERTREQUIRED` — Not the Bert Table

`doretrievedocvspanfoo` [`do1.c:301–309`] — note the comment: `"this routine is a kluge not yet kluged"`:

```c
bool doretrievedocvspanfoo(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{
    return (
       findorgl(taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)   // line 307
    && retrievedocumentpartofvspanpm(taskptr, docorgl, vspanptr));
}
```

The `NOBERTREQUIRED` flag short-circuits `checkforopen` entirely [`bert.c:59–61`]:

```c
if (type == NOBERTREQUIRED) {
    return 1;   /* Random > 0 */
}
```

Contrast this with `doretrievedocvspan` [`do1.c:312–320`], which uses `READBERT` and therefore requires the document to actually be open. `docreatenewversion` uses the "foo" (kluged) variant, **bypassing the open-state check**.

---

### Finding 3: Structural Existence IS Required — Via `fetchorglgr`

Since `NOBERTREQUIRED` skips the bert check, `findorgl` [`granf1.c:39–40`] falls through to:

```c
*orglptr = fetchorglgr(taskptr, granfptr, isaptr);
return (*orglptr ? TRUE : FALSE);
```

`fetchorglgr` [`granf2.c:22–81`] enforces five structural checks:

| Line | Check | Failure result |
|------|-------|----------------|
| `granf2.c:31` | Address ≤ granfilade width bounds | returns NULL |
| `granf2.c:34` | `retrievecrums` can traverse to the address | returns NULL |
| `granf2.c:37` | Exact ISA match (`tumblereq` on `totaloffset`) | returns NULL, frees context |
| `granf2.c:51` | Node has `infotype == GRANORGL` (not a gap/other) | `gerror` or NULL |
| `granf2.c:62` | `orglptr` is non-NULL after load from disk | `gerror` or NULL |

The third check (`tumblereq` at `granf2.c:37`) is the pivotal one: if no node was ever inserted at that exact ISA address, the enfilade traversal returns a context whose `totaloffset` won't match, and `fetchorglgr` returns NULL. The source document must exist as a leaf in the granfilade.

---

### Finding 4: What Happens With a Never-Instantiated Source

If `isaptr` was never inserted in the granfilade:
1. `createorglingranf` succeeds — a new `GRANORGL` node for `newisaptr` is inserted at `do1.c:277`
2. `doretrievedocvspanfoo` fails — `fetchorglgr` returns NULL at `granf2.c:37–39`
3. `docreatenewversion` returns `FALSE` at `do1.c:282`
4. Caller sends `putrequestfailed` to client
5. The granfilade entry for `newisaptr` is **never cleaned up** — it exists as an empty, uninitialized `GRANORGL` node with a freshly allocated but content-free POOM enfilade

If `isaptr` was once valid but has been "removed" (which in udanax-green means a prior `deletevsplan` removed all content, or it was never fully closed), the outcome depends on whether the ISA leaf node still exists in the granfilade. If the leaf is structurally present but content-empty, `fetchorglgr` succeeds and returns a valid but empty orgl — `doretrievedocvspanfoo` may then succeed or fail depending on whether `retrievedocumentpartofvspanpm` tolerates an empty document.

---

### Summary

`docreatenewversion` does **not** require the source to be open (bert table is bypassed via `NOBERTREQUIRED`). It **does** require the source to exist as a structurally valid `GRANORGL` leaf in the granfilade — that check is enforced by `fetchorglgr`'s enfilade traversal at `granf2.c:34–40`.

The deeper problem is **ordering**: the new version ISA is allocated (`createorglingranf`, `do1.c:277`) before the source is validated (`doretrievedocvspanfoo`, `do1.c:281`). A non-existent source causes the operation to return failure, but the freshly allocated granfilade slot for the new version is leaked — permanently occupying an ISA address with an empty, unreachable `GRANORGL` node. There is no rollback path.
