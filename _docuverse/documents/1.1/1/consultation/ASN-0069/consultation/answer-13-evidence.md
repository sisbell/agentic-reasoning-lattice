## Question 13 [evidence]

> If the source document is empty (no text, no links), or contains only link-subspace entries, what does CREATENEWVERSION produce — an empty version, a no-op, or an error?

## KB Synthesis

## CREATENEWVERSION on Empty or Links-Only Source

**Result: produces an empty version document — not a no-op, not an error.**

### For a completely empty source

[EC-EMPTY-DOC] (Finding 0007) states this explicitly: "Even empty documents can be versioned (the resulting version has an empty reference set)." The precondition for CREATENEWVERSION is simply that the source document exists — no minimum content requirement. Postcondition: `references(version) = ∅`.

### For a links-only source

[ST-VERSION-CREATE] (Finding 0043) is the decisive entry. `CREATENEWVERSION` retrieves the source vspan via `doretrievedocvspanfoo` → `retrievedocumentpartofvspanpm`, which reads only `cdsp.dsas[V]` and `cwid.dsas[V]` — the text subspace displacement and width. The link subspace (internal V-position `2.x`) lies structurally *before* the text displacement start and is outside the returned vspan. This is described explicitly: "The link subspace occupies V-positions before the document's recorded displacement."

For a links-only document, the text width is zero. `docopyinternal` is called with a zero-width vspan, copies nothing, and the version is created with an empty text subspace. The link subspace is not copied.

[FC-SUBSPACE] (Finding 0043) confirms the frame condition: "CREATENEWVERSION preserves the source document's link subspace unchanged while copying the text subspace to the version... The version receives a new, empty link subspace."

### What DOES happen in both cases

[ST-ADDRESS-ALLOC] still runs: a fresh document address is allocated under the source (owned) or under the creating account (unowned), per [SS-VERSION-ADDRESS] Finding 0068. The operation succeeds and returns a valid document address.

### Caveat: the resulting empty version

[EC-EMPTY-DOC] (Finding 0058) warns that a version produced from an empty source is in the "never-filled" state (height-1 tree, one zero-width bottom node). This is structurally distinct from a document emptied by DELETE, and importantly is safe for subsequent INSERT — unlike the delete-everything case which triggers Bug 0019.

---

## Code Exploration

I now have a complete picture. Here is my full analysis:

---

## What CREATENEWVERSION Produces for an Empty or Link-Only Source Document

### Short Answer

**It produces a new empty version in all cases.** No error, no no-op. The new ISA is allocated and returned, but its content is always empty — the copy step fails silently and its failure is deliberately ignored.

---

### Code Trace

#### Entry: `fns.c:289–300` — `createnewversion`

```c
void createnewversion(typetask *taskptr)
{
  typeisa originaldocisa, newdocisa;
  if (
     getcreatenewversion (taskptr, &originaldocisa)
  && docreatenewversion (taskptr, &originaldocisa, &originaldocisa, &newdocisa))
      putcreatenewversion (taskptr, &newdocisa);
    else
      putrequestfailed (taskptr);
}
```

The only question is whether `docreatenewversion` returns TRUE.

---

#### Core Logic: `do1.c:260–299` — `docreatenewversion`

```c
bool docreatenewversion(typetask *taskptr, typeisa *isaptr, typeisa *wheretoputit, typeisa *newisaptr)
{
    // [do1.c:270] ownership check → hint
    if (tumbleraccounteq(isaptr, wheretoputit) && isthisusersdocument(isaptr))
        makehint (DOCUMENT, DOCUMENT, 0, isaptr, &hint);
    else
        makehint (ACCOUNT, DOCUMENT, 0, wheretoputit, &hint);

    // [do1.c:277] Allocate new granfilade slot
    if (!createorglingranf(taskptr, granf, &hint, newisaptr))
        return (FALSE);

    // [do1.c:281] Retrieve source doc's V-span
    if (!doretrievedocvspanfoo (taskptr, isaptr, &vspan))
        return FALSE;

    vspec.next = NULL;
    vspec.itemid = VSPECID;
    movetumbler(isaptr, &vspec.docisa);
    vspec.vspanset = &vspan;

    // [do1.c:292] Add new doc to bert table
    addtoopen(newisaptr, user, TRUE, WRITEBERT);

    // [do1.c:293] *** RETURN VALUE DISCARDED ***
    docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);

    // [do1.c:295] Mark modified → prevents deleteversion on close
    logbertmodified(newisaptr, user);
    doclose(taskptr, newisaptr, user);

    return (TRUE);  // Always succeeds after createorglingranf
}
```

The function always returns `TRUE` once `createorglingranf` succeeds. The result of `docopyinternal` at `do1.c:293` is **discarded** — this is the load-bearing fact.

---

#### Step 1: `doretrievedocvspanfoo` — `do1.c:301–309`

```c
bool doretrievedocvspanfoo(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{ /* this routine is a kluge not yet kluged*/
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)
    && retrievedocumentpartofvspanpm (taskptr, docorgl, vspanptr) );
}
```

It calls `retrievedocumentpartofvspanpm` [orglinks.c:155–162]:

```c
bool retrievedocumentpartofvspanpm(typetask *taskptr, typeorgl orgl, typevspan *vspanptr)
{ /* this is a kluge*/
    vspanptr->next = NULL;
    vspanptr->itemid = VSPANID;
    movetumbler (&((typecuc *) orgl)->cdsp.dsas[V], &vspanptr->stream);
    movetumbler (&((typecuc *) orgl)->cwid.dsas[V], &vspanptr->width);
    return (TRUE);
}
```

**This always returns TRUE.** It reads the raw V-axis fields from the root POOM crum.

**For an empty document:** `isemptyorgl` [orglinks.c:539–544] shows that empty means both `cwid` and `cdsp` are zero. So:
- `vspan.stream` = 0
- `vspan.width` = 0

**For a link-subspace-only document:** Link entries are inserted at V-positions ≥ 2.1 (via `findnextlinkvsa` [do2.c:151–167] which sets `firstlink` to `tumblerincrement(0, 2) + tumblerincrement(1, 1)`). The root POOM crum's `cdsp.dsas[V]` is still 0 (root displacement), while `cwid.dsas[V]` covers the link span. So:
- `vspan.stream` = 0
- `vspan.width` = non-zero (link span width)

In both cases: **`vspan.stream` = 0.**

---

#### Step 2: `docopyinternal` — `do1.c:66–82`

```c
bool docopyinternal(typetask *taskptr, typeisa *docisaptr, tumbler *vsaptr, typespecset specset)
{
    if (!specset2ispanset (...)) return FALSE;     // [do1.c:74]
    if (!findorgl (...)) return FALSE;              // [do1.c:75]
    if (!acceptablevsa (vsaptr, docorgl)) return FALSE;  // [do1.c:76]
    if (!asserttreeisok(docorgl)) return FALSE;    // [do1.c:77]
    if (!insertpm (..., vsaptr, ispanset)) return FALSE; // [do1.c:78]
    if (!insertspanf (...)) return FALSE;           // [do1.c:79]
    return TRUE;
}
```

Called with `vsaptr = &vspan.stream` = 0.

**`acceptablevsa` is a stub** [do2.c:110–113]:

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);
}
```

Always TRUE. Never validates anything.

**`insertpm` [orglinks.c:86–91] explicitly rejects vsaptr=0:**

```c
if (iszerotumbler (vsaptr)){
#ifndef DISTRIBUTION
    fprintf(stderr,"insertpm inserting at 0 ---punt zzzz?");
#endif
    return (FALSE);
}
```

`docopyinternal` returns `FALSE` at `do1.c:78`.

But at `do1.c:293`, this return value is discarded:
```c
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);  // result thrown away
```

---

#### Step 3: `logbertmodified` preserves the new version — `do1.c:295`, `bert.c:97–109`

`addtoopen` [bert.c:128–151] was called with `created=TRUE, modified=FALSE`. Then `logbertmodified` [bert.c:97–109] sets `modified=TRUE`.

In `removefromopen` [bert.c:172–175]:
```c
status = bert->created && !bert->modified;
if (status) {
    deleteversion(tp);
}
```

Because `modified=TRUE`, `status = TRUE && !TRUE = FALSE`. `deleteversion` is **not called**. The new version survives.

---

### Summary Table

| Source State | `vspan.stream` | `insertpm` result | `docopyinternal` return | New version created? | Content transferred? | Return to client |
|---|---|---|---|---|---|---|
| Empty (no text, no links) | 0 | FALSE (vsaptr=0) | FALSE | **Yes** | **No** | New ISA |
| Link-subspace only (V ≥ 2.1) | 0 | FALSE (vsaptr=0) | FALSE | **Yes** | **No** | New ISA |

---

### Design Intent

The comment at `do1.c:290–295` documents the intent explicitly:

```c
/* Skip doopen ownership check - we just created this document so we own it.
   Add directly to bert table instead. */
addtoopen(newisaptr, user, TRUE, WRITEBERT);
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
/* Mark as modified so removefromopen doesn't delete the newly created version */
logbertmodified(newisaptr, user);
```

The design is: **always create the version slot; mark it modified so it's never garbage-collected; discard copy failures silently.** This is a deliberate "create the slot regardless" policy.

The remark at `doretrievedocvspanfoo` — `"this routine is a kluge not yet kluged"` [do1.c:302] — and at `retrievedocumentpartofvspanpm` — `"this is a kluge"` [orglinks.c:156] — confirm these are provisional implementations where the zero-stream-origin problem was known but not addressed. The `insertpm` debug print `"insertpm inserting at 0 ---punt zzzz?"` [orglinks.c:88] reinforces this.

---

### Conclusion

**CREATENEWVERSION on an empty document or a link-subspace-only document:**
- **Not a no-op** — a new granfilade slot with a fresh ISA is allocated.
- **Not an error** — the protocol sends back `putcreatenewversion` with the new ISA, not `putrequestfailed`.
- **Produces a new empty version** — `docopyinternal` fails silently (vsaptr=0 guard in `insertpm`), its return is discarded, and the empty new version is preserved by the modified-flag mechanism.

The link-subspace content is never copied into the new version. The new version is structurally identical to a freshly created document. The client receives a valid new ISA and has no indication that no content was transferred.
