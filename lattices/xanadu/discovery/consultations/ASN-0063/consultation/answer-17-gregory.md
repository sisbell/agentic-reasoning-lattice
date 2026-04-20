## Question 17 [gregory]

> When a link's type endset references content at `1.0.2.x` in the global type namespace, is that type content created by a prior INSERT into a dedicated type document, or is there a separate type registration mechanism outside the normal document operations?

## KB Synthesis

The KB does not contain enough information to answer this fully.

What the KB does establish:

**Type content exists in a bootstrap document** [SS-LINK-ENDPOINT, Finding 0024]:
- Link types are stored as VSpec references to a type registry at addresses like `1.0.2.2` (JUMP), `1.0.2.3` (QUOTE), `1.0.2.6` (FOOTNOTE), `1.0.2.6.2` (MARGIN) in a "bootstrap document (doc 1)"
- The type hierarchy is encoded in the tumbler containment structure — MARGIN is nested under FOOTNOTE because `1.0.2.6.2` is contained within `1.0.2.6`
- The client (`febe/client.py`) constructs VSpecs referencing these addresses directly by address, not by any lookup or registration call

**What the KB does NOT say:**

The KB has no findings that describe *how* those `1.0.2.x` addresses were populated. There is no documented type registration opcode, no finding showing an INSERT into doc 1 producing type content, and no description of bootstrap/initialization procedures that pre-populate the type registry.

The bootstrap document is referenced only as a pre-existing entity whose type addresses the client hardcodes. Whether those addresses were written by normal INSERT operations during system initialization, by a special seeding procedure during installation, or by some other mechanism entirely — the KB is silent on this.

If you need to establish the mechanism, it would require examining the system initialization code (likely in `entexit.c` or similar startup paths) or the bootstrap document creation logic, which have not been covered by the findings in the KB.

---

## Code Exploration

Now I have everything I need. Here is the complete answer sourced directly from the C code.

---

## Answer: Link Type Registration in udanax-green

**There is no separate type registration mechanism.** The backend treats the type endset as an ordinary V-space reference into an ordinary document. Whether content exists at `1.0.2.x` depends entirely on whether a prior operation (INSERT, COPY, etc.) placed content there. Nothing in the backend pre-populates or registers type addresses.

---

### Execution path through `createlink`

**`fns.c:100-112`** — FEBE handler, no special handling of the type endset:
```c
void createlink(typetask *taskptr)
{
    typeisa docisa, linkisa;
    typespecset fromspecset, tospecset, threespecset;
    ...
    if (
       getcreatelink(taskptr, &docisa, &fromspecset, &tospecset, &threespecset)
    && docreatelink(taskptr, &docisa, fromspecset, tospecset, threespecset, &linkisa))
        putcreatelink(taskptr, &linkisa);
```

**`do1.c:195-221`** — `docreatelink`, the type endset is processed identically to FROM and TO:
```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset fromspecset, typespecset tospecset,
    typespecset threespecset, typeisa *linkisaptr)
{
    ...
    return (
         createorglingranf(taskptr, granf, &hint, linkisaptr)
      && tumbler2spanset(taskptr, linkisaptr, &ispanset)
      && findnextlinkvsa(taskptr, docisaptr, &linkvsa)
      && docopy(taskptr, docisaptr, &linkvsa, ispanset)
      && findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)  // line 213
      && specset2sporglset(taskptr, fromspecset, &fromsporglset, NOBERTREQUIRED)  // line 214
      && specset2sporglset(taskptr, tospecset,   &tosporglset,   NOBERTREQUIRED)  // line 215
      && specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED) // line 216
      && setlinkvsas(&fromvsa, &tovsa, &threevsa)
      && insertendsetsinorgl(...)
      && insertendsetsinspanf(...)
    );
}
```

All three endsets pass through exactly the same `specset2sporglset` call with `NOBERTREQUIRED`. There is no type-specific branch.

---

### How `specset2sporglset` resolves the type address

**`sporgl.c:14-33`** — iterates the specset items, dispatches VSpec items to `vspanset2sporglset`:
```c
bool specset2sporglset(typetask *taskptr, typespecset specset,
                       typesporglset *sporglsetptr, int type)
{
    for (; specset; specset = ...) {
        if (...itemid == VSPECID) {
            if (!(sporglsetptr = vspanset2sporglset(
                    taskptr,
                    &((typevspec *)specset)->docisa,   // the type document address
                    ((typevspec *)specset)->vspanset,  // the V-span within it (1.0.2.x)
                    sporglsetptr, type)))
                return (FALSE);
        }
    }
}
```

**`sporgl.c:35-65`** — `vspanset2sporglset` converts V-spans to I-spans (sporgls) by calling `findorgl` on the referenced document:
```c
typesporglset *vspanset2sporglset(typetask *taskptr, typeisa *docisa,
    typevspanset vspanset, typesporglset *sporglsetptr, int type)
{
    typeorgl orgl;
    ...
    if (!findorgl(taskptr, granf, docisa, &orgl, type)) {  // line 44
        return (NULL);                                      // FAILS if doc not found
    }
    for (; vspanset; vspanset = vspanset->next) {
        (void) vspanset2ispanset(taskptr, orgl, vspanset, &ispanset);  // V→I
        for (; ispanset; ispanset = ispanset->next) {
            // builds sporgl from I-coords
        }
    }
}
```

If `findorgl` returns NULL — because the type document doesn't exist in the granfilade — `vspanset2sporglset` returns NULL, `specset2sporglset` returns FALSE, and `docreatelink` fails. **The type document must already exist.**

---

### `NOBERTREQUIRED` bypasses open/close, not existence

**`granf1.c:17-41`** — `findorgl` with `NOBERTREQUIRED`:
```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr,
              typeorgl *orglptr, int type)
{
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {
        if (!isxumain) {    // in standalone mode, skip the error
            return FALSE;
        }
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);  // disk lookup
    return (*orglptr ? TRUE : FALSE);
}
```

**`bert.c:52-61`** — `checkforopen` with `NOBERTREQUIRED` short-circuits immediately:
```c
int checkforopen(tumbler *tp, int type, int connection)
{
    if (type == NOBERTREQUIRED) {
        return 1;    /* Random > 0 */
    }
    // ... bert table lookup ...
}
```

`NOBERTREQUIRED` skips the open/close protocol (the bert table) — the type document doesn't need to be explicitly OPENed. But it does not skip the disk lookup (`fetchorglgr`). The orgl must exist in the granfilade.

Additionally, `isxumain = TRUE` is set in **`xumain.c:23`** for the standalone backend, which means even if `checkforopen` returned a failure, the error path in `findorgl` is bypassed. Standalone mode is more permissive still — but `fetchorglgr` returning NULL will still propagate as failure.

---

### No initialization creates type documents

**`entexit.c:19-47`** — `initmagicktricks` initializes only the enfilade infrastructure:
```c
int initmagicktricks(void)
{
    initgrimreaper();
    initqueues();
    clear(&ZEROTUMBLERvar, sizeof(tumbler));
    if (initenffile()) {
        initkluge((typecuc**)&granf, (typecuc**)&spanf);   // restore existing enf
    } else {
        granf = (typegranf) createenf(GRAN);               // fresh granfilade
        spanf = (typespanf) createenf(SPAN);               // fresh spanfilade
    }
}
```

No type documents, no pre-populated addresses, no registration tables. The `init()` function in **`init.c:25-79`** only installs FEBE handler function pointers.

**`xumain.c:30-63`** — the full startup sequence:
```c
int main(void)
{
    processrcfile();
    init(0);
    inittask(&task);
    initmagicktricks();
    getaccount(&task, &task.account);
    for (;;) { xanadu(&task); }
}
```

Nothing here creates content at `1.0.2.x` or any type address.

---

### What happens if the content doesn't exist

If the type document's orgl exists but no content was ever inserted at V-coordinate `1.0.2.x`, then `vspanset2ispanset` returns an empty `ispanset`. The inner `for (; ispanset; ...)` loop in `vspanset2sporglset` never executes. `threesporglset` ends up NULL.

In `do1.c:219` (inside `insertendsetsinspanf`):
```c
if (threesporglset) {                                    // guarded by NULL check
    if (!insertspanf(..., threesporglset, LINKTHREESPAN)) { ... }
}
```

The type endset is silently omitted from the spanfilade index. The link is created but with no type entry. There is no error.

---

### Summary

| Question | Answer |
|---|---|
| Is there a separate type registration mechanism? | **No.** The backend has no such function. |
| How are types at `1.0.2.x` created? | By ordinary INSERT or COPY operations placing content at those V-coordinates in a type document. |
| Does `NOBERTREQUIRED` bypass document existence? | **No.** It bypasses the open/close (bert) protocol only. `fetchorglgr` still requires the orgl to exist on disk. |
| What if no content exists at `1.0.2.x`? | V→I conversion yields empty ispanset; type sporgl is silently dropped; link is created without a type index entry. |
| Is there startup initialization of type documents? | **No.** `initmagicktricks` and `init` create only enfilade infrastructure, never content. |

The `1.0.2.x` addresses are conventional — the client hardcodes them as well-known type coordinates in whatever type document it uses — but the backend has no knowledge of them. From the backend's perspective, a type endset is indistinguishable from a FROM or TO endset. It stores whatever V-span reference it is given, converting via V→I only if that content already exists.
