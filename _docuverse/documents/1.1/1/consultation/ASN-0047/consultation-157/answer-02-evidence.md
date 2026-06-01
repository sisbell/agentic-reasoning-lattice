## Question 2 [evidence]

> After a document's text is fully deleted and new text is inserted, does udanax-green re-establish the same V-position depth for the text subspace, or can the re-populated text occupy a different depth than before?

## KB Synthesis

The KB does not fully support the scenario as posed — complete text deletion followed by re-insertion hits Bug 0019, which crashes the backend before any V-position can be assigned.

**Why re-insertion crashes after full deletion**

[EC-EMPTY-DOC] (Finding 0058) distinguishes two structurally different "empty" states:

- *Never-filled*: height-1 tree with one zero-width bottom node
- *After delete-everything*: taller tree, empty intermediate nodes, **zero bottom nodes**

When all text is removed, `deletend` calls `disown` + `subtreefree` on all bottom crums but creates no replacement. [ST-INSERT] (Finding 0064) confirms that `firstinsertionnd()` dereferences the left-most bottom crum via `findleftson()`, which returns NULL in this state — a null-pointer dereference (Bug 0019). The insert never reaches the V-position assignment step.

**What the KB does tell us about V-positions for surviving text**

When some text remains, new insertions always target 1.x positions ([FC-SUBSPACE], [SS-SUBSPACE-CONVENTION]). The two-blade knife in [SS-TWO-BLADE-KNIFE] hard-codes blade[1] = 2.1 for any insert at N.x, confining shifts to [1.x, 2.1). The assigned V-addresses (1.1, 1.2, …) are determined by the caller-specified insertion point, not by prior history.

**Tree height is irreversibly retained**

[SS-ENFILADE-TREE] (Finding 0058) establishes that `levelpull` is disabled — tree height is monotonically non-decreasing. Any re-inserted text would be mapped into a POOM tree at least as tall as the deleted tree. The V-address *format* (e.g., 1.1, 1.2) does not change with tree height; only internal node depth changes.

**Summary**: The KB does not document successful re-insertion into a fully-deleted document — that path crashes. For partial deletions, new text occupies the same 1.x V-address scheme as always, with the same two-digit tumbler format, but the enfilade tree retains whatever height it reached before deletion.

---

## Code Exploration

Now I have the full picture. Here is the complete answer:

---

## V-Position Depth After Full Delete and Re-Insert

### Short Answer

The server has **no mechanism to enforce V-position depth consistency on re-insert**. For the FEBE `INSERT` command, the V-address depth is entirely client-determined. In the test harness, the client always sends `Address(1,1)` (depth 2), so the same depth is re-established — but by client convention, not server logic. The `APPEND` code path does enforce a consistent starting depth, but it is not used by the FEBE `insert` command.

---

### How V-Addresses Are Assigned on INSERT

The FEBE `insert` handler at `fns.c:84-98`:

```c
void insert(typetask *taskptr)
{
  typeisa docisa, vsa;
  typetextset textset;
  ...
  (void) getinsert(taskptr, &docisa, &vsa, &textset);   // reads vsa from protocol
  putinsert(taskptr);
  if (!doinsert(taskptr, &docisa, &vsa, textset))       // stores at client-specified vsa
```

The V-address `vsa` is read directly from the wire via `gettumbler` [`get1fe.c:30`]:

```c
bool getinsert(typetask *taskptr, tumbler *docisaptr, tumbler *vsaptr, typetextset *textsetptr)
{
    return (
       gettumbler(taskptr, docisaptr)
    && gettumbler(taskptr, vsaptr)       // V-address comes from client
    && gettextset(taskptr, textsetptr));
}
```

The server validates with `acceptablevsa`, but that function unconditionally returns `TRUE` [`do2.c:110-113`]:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return(TRUE);
}
```

The server will accept any client-specified V-address, including a previously deleted one.

---

### How the V-Width Encodes Depth

Inside `insertpm` [`orglinks.c:113-117`]:

```c
movetumbler(vsaptr, &crumorigin.dsas[V]);
/*I'm suspissious of this shift <reg> 3/1/85 zzzz*/
shift = tumblerlength(vsaptr) - 1;
inc = tumblerintdiff(&lwidth, &zero);
tumblerincrement(&zero, shift, inc, &crumwidth.dsas[V]);
```

The V-width exponent is set to `shift = tumblerlength(vsaptr) - 1`. For `vsaptr = 1.1` (a 2-component tumbler), `tumblerlength` [`tumble.c:259-262`]:

```c
INT tumblerlength(tumbler *tumblerptr)
{
    return(nstories(tumblerptr) - tumblerptr->exp);
}
```

returns 2, so `shift = 1`. This means V-widths are encoded with exponent −1 (fractional tumbler units). If the same `1.1` address is re-used after a full delete, the same `shift = 1` applies — same depth encoding.

If a client were to re-insert at `1.1.1` (depth 3 tumbler), `shift` would be 2, and widths would be encoded with exponent −2 — a different scale than the original. The POOM would store content at a different depth level in V-space.

---

### What Happens After Full Deletion

`deletevspanpm` [`orglinks.c:145-152`]:

```c
bool deletevspanpm(typetask *taskptr, tumbler *docisaptr, typeorgl docorgl, typevspan *vspanptr)
{
    if (iszerotumbler(&vspanptr->width))
        return(FALSE);
    deletend((typecuc*)docorgl, &vspanptr->stream, &vspanptr->width, V);
    logbertmodified(docisaptr, user);
    return(TRUE);
}
```

After all text is deleted, the POOM enfilade's root `cwid` becomes zero (all content removed). The tree structure is NOT collapsed back because `levelpull` is permanently disabled [`genf.c:318-321`]:

```c
int levelpull(typecuc *fullcrumptr)
{
/*  typecuc *ptr; */
return(0);
/* ... entire collapse logic is dead code ... */
```

The tree retains its structural height, but its logical content width (root `cwid`) is zero.

---

### The APPEND Path (Not Used by FEBE INSERT)

Had the FEBE `INSERT` command gone through `appendpm` → `findvsatoappend` [`orglinks.c:29-49`], the server would have computed a fresh V-address automatically. For an empty document (`iszerolock` on root `cwid` returns TRUE):

```c
if (
   iszerolock((tumbler*)&ptr->cwid, widsize(POOM))
|| (tumblercmp(&grasp.dsas[V], &linkspacevstart) != LESS)) {
    tumblerincrement(vsaptr, 0, 1, vsaptr); /* no text in doc */
    tumblerincrement(vsaptr, 1, 1, vsaptr);
```

This always produces `vsaptr = 1.1` (depth 2), regardless of prior history. This would enforce the same starting depth. But this path is only exercised by `doappend` → `appendpm`; the FEBE `INSERT` command bypasses it entirely.

---

### Client Convention in the Test Harness

All test scenarios use `Address(1, 1)` as the starting V-address for first insertion:

```python
session.insert(opened, Address(1, 1), ["AAA"])   # allocation_independence.py:40
session.insert(doc_opened, Address(1, 1), ["Inserted text"])  # insert_docispan.py:27
```

Subsequent inserts use the returned `vspan.end()` as the next address — which is still a 2-component tumbler since it advances within the `1.x` subspace. After a full delete, if the same client sends `Address(1, 1)` again, the server will store the new text at depth 2 — the same as before.

---

### Conclusion

The re-inserted text occupies the **same V-position depth** as the original in practice, but for the following reasons:

| Mechanism | Enforces same depth? | Source |
|-----------|---------------------|--------|
| `acceptablevsa` | No — always returns TRUE | `do2.c:112` |
| `insertpm` shift | Follows depth of whatever `vsaptr` is sent | `orglinks.c:115` |
| `findvsatoappend` (APPEND path) | Yes — always returns `1.1` for empty doc | `orglinks.c:42-43` |
| FEBE INSERT path | No — uses client-provided V-address | `get1fe.c:30` |

For FEBE `INSERT`, the depth is preserved only because the test harness client re-uses `Address(1, 1)`. The server has no structural mechanism to prevent a client from re-inserting at a different depth (e.g., `Address(1, 1, 1)`), which would produce POOM entries with a different V-width exponent and place the text at a different depth in V-space. The `levelpull` being dead code means enfilade tree height never shrinks, but that is an internal structural detail irrelevant to the client-visible V-address depth.
