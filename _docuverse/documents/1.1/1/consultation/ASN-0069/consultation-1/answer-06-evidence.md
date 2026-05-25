## Question 6 [evidence]

> When `docreatenewversion` is invoked on a source whose content subspace is empty, does the operation report failure to the caller, produce a new version entity with an empty arrangement, or behave in some other observable way?

## KB Synthesis

## Versioning an Empty Content Subspace

The KB provides direct evidence on this question across several findings.

**Observable behavior: success, not failure.**

[EC-EMPTY-DOC] (Finding 0007) states explicitly: "Empty documents can be versioned. The resulting version is also empty and can have content added independently." The test `version_of_empty_document` confirms this. [ST-VERSION-CREATE] (Finding 0032) reinforces: "The precondition is simply that the source document exists (even empty documents can be versioned)."

**Internal mechanism:**

[ST-VERSION-CREATE] (Finding 0043) traces the call chain: `docreatenewversion` → `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm()`. This function reads the root crum's V-dimension displacement and width. For an empty text subspace, [SS-VSPAN-VS-VSPANSET] (Finding 0035) confirms: "Empty document: RETRIEVEDOCVSPAN returns zeros." The subsequent `docopyinternal` call receives a zero-width vspan and copies zero content.

Step 1 (address allocation via `createorglingranf`) always succeeds for a valid parent document, producing a child address per [SS-VERSION-ADDRESS] and [ST-ADDRESS-ALLOC].

**Postcondition:**

The new version entity exists at a child address of the source (for owned documents) with `references(version) = ∅`. [ST-VERSION-CREATE] (Finding 0032): "The postcondition is: `references(new_version) = references(source)` with the new version at a child address." When `references(source) = ∅`, the version starts empty.

**One caveat:**

[EC-EMPTY-DOC] (Finding 0058) notes that documents emptied by DELETE (versus never-filled) leave the enfilade tree in a structurally different state — taller with no bottom nodes — and that subsequent INSERT/VCOPY on such documents crashes (Bug 0019). Whether `docreatenewversion` on a delete-emptied source avoids this crash path (because the zero-width vspan may bypass `firstinsertionnd`) is not directly confirmed in the KB. The KB's `version_of_empty_document` test evidence most naturally corresponds to a never-filled document.

---

## Code Exploration

Now I have the complete picture. Let me compile the full answer.

---

## Answer: `docreatenewversion` on an Empty-Content Source

### Verdict

**The operation succeeds (returns TRUE, allocates a new version entity) and produces a new version with an empty content arrangement.** The content copy is silently bypassed via a zero-address guard deep in `insertpm`, but `docreatenewversion` discards `docopyinternal`'s return value and returns TRUE unconditionally.

---

### Code Trace

#### 1. Entry point: `fns.c:289` — `createnewversion`

```c
// fns.c:294-299
if (
   getcreatenewversion (taskptr, &originaldocisa)
&& docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))
      putcreatenewversion (taskptr, &newdocisa);
  else
      putrequestfailed (taskptr);
```

`createnewversion` calls `docreatenewversion` and, if it returns TRUE, calls `putcreatenewversion` to send the new document ISA to the client. If FALSE, it sends `requestfailed`.

---

#### 2. `docreatenewversion` — `do1.c:260`

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    ...
    if (!createorglingranf(taskptr, granf, &hint, newisaptr)) {
        return (FALSE);                        // [do1.c:277-279]
    }

    if (!doretrievedocvspanfoo(taskptr, isaptr, &vspan)) {
        return FALSE;                          // [do1.c:281-283]
    }

    vspec.next = NULL;
    vspec.itemid = VSPECID;
    movetumbler(isaptr, &vspec.docisa);
    vspec.vspanset = &vspan;

    addtoopen(newisaptr, user, TRUE, WRITEBERT);
    docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // [do1.c:293] RETURN VALUE DISCARDED
    logbertmodified(newisaptr, user);
    doclose(taskptr, newisaptr, user);

    return (TRUE);                             // [do1.c:298] unconditional
}
```

**Critical observation:** `docopyinternal`'s return value is not checked at `do1.c:293`. After the new entity is created and opened, the function returns TRUE regardless of whether the copy succeeded.

---

#### 3. `doretrievedocvspanfoo` — `do1.c:301`, called as `retrievedocumentpartofvspanpm` — `orglinks.c:155`

For an empty source document, the orgl was created by `createcruminternal`, which zeroes all fields:

```c
// credel.c:580-581
clear(&ptr->cdsp, sizeof(ptr->cdsp));
clear(&ptr->cwid, sizeof(ptr->cwid));
```

So `cdsp.dsas[V] = 0` (stream start) and `cwid.dsas[V] = 0` (width).

`retrievedocumentpartofvspanpm` always returns TRUE — it just copies whatever is in those fields:

```c
// orglinks.c:157-161
vspanptr->next = NULL;
vspanptr->itemid = VSPANID;
movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);  // → 0
movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);   // → 0
return (TRUE);
```

`doretrievedocvspanfoo` therefore returns TRUE with `vspan.stream = 0`, `vspan.width = 0`. There is **no empty-document guard here** — in contrast to `doretrievedocvspanset` (`do1.c:322`), which does call `isemptyorgl` and returns an explicit empty result.

---

#### 4. `docopyinternal` — `do1.c:66`

```c
bool docopyinternal(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    if (!specset2ispanset(taskptr, specset, &ispanset, NOBERTREQUIRED)) return FALSE;
    if (!findorgl(taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)) return FALSE;
    if (!acceptablevsa(vsaptr, docorgl)) return FALSE;   // always TRUE [do2.c:111-113]
    if (!asserttreeisok(docorgl)) return FALSE;
    if (!insertpm(taskptr, docisaptr, docorgl, vsaptr, ispanset)) return FALSE;  // ← fails here
    ...
}
```

**`specset2ispanset` returns TRUE with `ispanset = NULL`** because:
- The source doc is empty → `retrieverestricted` returns NULL (no crumbs)
- `span2spanset` returns `targspansetptr` unchanged (`orglinks.c:446-448`)
- `permute` returns `save` (non-null pointer to the NULL ispanset) (`orglinks.c:421`)
- `specset2ispanset` sees a non-NULL return and returns TRUE (`do2.c:34-45`)

**`insertpm` fires the zero-address guard** (`orglinks.c:86-91`):

```c
// orglinks.c:86-91
if (iszerotumbler (vsaptr)){
#ifndef DISTRIBUTION
    fprintf(stderr,"insertpm inserting at 0 ---punt zzzz?");
#endif
    return (FALSE);
}
```

`vsaptr = &vspan.stream = 0` → `iszerotumbler` is TRUE → `insertpm` returns FALSE.

`docopyinternal` returns FALSE at `do1.c:78`.

But — as established above — `docreatenewversion` at `do1.c:293` **does not check this return value**.

---

#### 5. Final result

| Step | Outcome | Code |
|------|---------|------|
| `createorglingranf` | Succeeds → new document entity allocated | `do1.c:277` |
| `doretrievedocvspanfoo` | Succeeds → vspan = (0, 0) | `do1.c:281`, `orglinks.c:155` |
| `addtoopen` | New version added to bert open table | `do1.c:292` |
| `docopyinternal` | **Returns FALSE** (vsaptr=0 kills `insertpm`) — **return value ignored** | `do1.c:293`, `orglinks.c:86-91` |
| `logbertmodified` | New version marked modified (prevents deletion on close) | `do1.c:295` |
| `doclose` | New version committed to storage | `do1.c:296` |
| `docreatenewversion` returns | **TRUE** | `do1.c:298` |
| Client receives | New version ISA via `putcreatenewversion` | `fns.c:297` |

---

### Summary

When `docreatenewversion` is called on a source whose content subspace is empty:

1. **A new version entity is successfully created** with its own document address. The operation does NOT report failure.
2. **The content copy silently fails** inside `docopyinternal` → `insertpm` because `vsaptr` (the source's content stream start) is zero. The `insertpm` guard at `orglinks.c:86-91` returns FALSE with a debug message `"insertpm inserting at 0 ---punt zzzz?"`, but this propagates only as far as `docopyinternal`'s return value.
3. **`docreatenewversion` discards `docopyinternal`'s return value** (`do1.c:293`) and returns TRUE unconditionally after the entity-creation and vspan-retrieval steps succeed.
4. **The new version has an empty content arrangement** — the copy was a no-op. This is semantically correct: a version of an empty document should itself be empty.
5. **The client receives success** and the new version's ISA address via `putcreatenewversion`.

The "kluge" note on `doretrievedocvspanfoo` (`do1.c:302`) is telling: unlike `doretrievedocvspanset` (which calls `isemptyorgl` and handles empty documents explicitly), `doretrievedocvspanfoo` blindly reads zero-valued fields and returns TRUE, leaving the zero-vsaptr problem to be caught silently downstream.
