## Question 5 [evidence]

> Does udanax-green ever actually allocate a link with both F and G empty (only Θ populated), or is the absence of a runtime guard in `acceptablevsa`/`docreatelink` simply unreachable in practice?

## KB Synthesis

The KB does not contain enough evidence to answer definitively, but here is what it does establish:

**What the KB says:**

[PRE-ZERO-WIDTH] documents that `create_link` with **zero-width** endpoints crashes (Bug 0017). This is a minimum-width precondition, not a guard on empty specsets — NOSPECS and a zero-width VSpec are not shown to be equivalent in the KB.

[PRE-LINK-CREATE] states the full structural precondition as: "source content exists AND target content exists AND both endpoint widths >= 1 AND home_doc is valid." Both F and G must be present and non-empty.

[ST-LINK-CREATE] (Finding 0037) describes `domakelink` as converting V-spans via `vspanset2sporglset` → one sporgl per contiguous I-address region. If F and G are NOSPECS, there is nothing for `vspanset2sporglset` to process; the KB does not document what happens in that case.

[SS-LINK-ENDPOINT] (Finding 0012) shows `docreatelink` writes to all three endsets via `insertendsetsinspanf`. Whether passing empty FROM and TO sets causes a crash, a no-op insert, or a valid degenerate link is not in the KB.

**Conclusion:** The KB documents that zero-width endpoints crash and that both F and G are structurally required, but it does not cover whether NOSPECS for both F and G is reachable in practice or what `docreatelink` does in that case. This is not answerable from the KB as given.

---

## Code Exploration

I now have everything needed for a complete, cited answer. Let me compile it.

---

## Answer: Can udanax-green allocate a link with only Θ populated (F and G empty)?

**Yes. The code path is fully reachable, not dead code.** Here is the complete trace.

---

### 1. Protocol layer permits empty endpoint specsets

`getcreatelink` in both CLI and FE paths unconditionally calls `getspecset` for all three endpoints with no validation:

```
get1.c:46-61   (interactive / CLI)
get1fe.c:75-84 (FEBE protocol path)
```

`get1fe.c:75-84`:
```c
bool getcreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset *fromspecsetptr, typespecset *tospecsetptr, typespecset *threespecsetptr)
{
    logstuff = TRUE;
    fprintf(interfaceinput, "%d~", CREATELINK);
    return (
       gettumbler(taskptr, docisaptr)
    && getspecset(taskptr, fromspecsetptr)
    && getspecset(taskptr, tospecsetptr)
    && getspecset(taskptr, threespecsetptr));
}
```

`getspecset` at `get2.c:162-176` explicitly permits a NULL specset:

```c
if (!any) {
    *specsetptr = NULL;
    return (TRUE);   // get2.c:174-175
}
```

The protocol boundary does not enforce that any endpoint be non-empty. A client can legitimately send F=empty, G=empty, Θ=populated.

---

### 2. `acceptablevsa` is a pure stub

```c
bool acceptablevsa(tumbler *vsaptr, typeorgl orglptr)
{
    return (TRUE);   // do2.c:111-112
}
```

This function is called during `docopy` (`do1.c:56`) to validate the VSA before insertion. It performs no checks. Every VSA is always acceptable.

---

### 3. `docreatelink` has no guard against empty endpoint specsets

`do1.c:195-221`:
```c
bool docreatelink(typetask *taskptr, typeisa *docisaptr,
    typespecset fromspecset, typespecset tospecset, typespecset threespecset,
    typeisa *linkisaptr)
{
    ...
    makehint(DOCUMENT, ATOM, LINKATOM, docisaptr, &hint);
    return (
         createorglingranf(taskptr, granf, &hint, linkisaptr)  // link created HERE
      && tumbler2spanset(taskptr, linkisaptr, &ispanset)
      && findnextlinkvsa(taskptr, docisaptr, &linkvsa)
      && docopy(taskptr, docisaptr, &linkvsa, ispanset)
      && findorgl(taskptr, granf, linkisaptr, &link, NOBERTREQUIRED)
      && specset2sporglset(taskptr, fromspecset,  &fromsporglset,  NOBERTREQUIRED)  // line 214
      && specset2sporglset(taskptr, tospecset,    &tosporglset,    NOBERTREQUIRED)  // line 215
      && specset2sporglset(taskptr, threespecset, &threesporglset, NOBERTREQUIRED)  // line 216
      && setlinkvsas(&fromvsa, &tovsa, &threevsa)
      && insertendsetsinorgl(...)
      && insertendsetsinspanf(...)
    );
}
```

**`createorglingranf` at line 209 runs before any endpoint validation.** The link ISA is committed to granf before any of the endpoint operations run.

---

### 4. `specset2sporglset` silently accepts NULL and returns NULL

`sporgl.c:14-33`:
```c
bool specset2sporglset(typetask *taskptr, typespecset specset,
    typesporglset *sporglsetptr, int type)
{
    *sporglsetptr = NULL;
    for (; specset; specset = ...) {  // loop doesn't execute if specset == NULL
        ...
    }
    *sporglsetptr = NULL;
    return (TRUE);   // sporgl.c:32 — succeeds with NULL sporglset output
}
```

When `fromspecset` or `tospecset` is NULL, this returns TRUE with `fromsporglset = NULL` and `tosporglset = NULL`. The chain continues.

---

### 5. `insertendsetsinorgl` calls `insertpm` unconditionally for F and G

`do2.c:130-149`:
```c
bool insertendsetsinorgl(typetask *taskptr, tumbler *linkisaptr, typeorgl link,
    tumbler *fromvsa, typesporglset fromsporglset,
    tumbler *tovsa,  typesporglset tosporglset,
    tumbler *threevsa, typesporglset threesporglset)
{
    if (!( insertpm(taskptr, linkisaptr, link, fromvsa, fromsporglset)   // ALWAYS called
        && insertpm(taskptr, linkisaptr, link, tovsa, tosporglset))) {   // ALWAYS called
            return (FALSE);
    }
    if (threevsa && threesporglset) {                                    // GUARDED
        if (!insertpm(taskptr, linkisaptr, link, threevsa, threesporglset))
            return (FALSE);
    } else {
#ifndef DISTRIBUTION
        fprintf(stderr, "leaving INSERTENDSETSINORGL 4\n");             // do2.c:142
        fprintf(stderr, " threevsa ptr= %x threesporglset ptr = %x\n",
                threevsa, threesporglset);                               // do2.c:143
        dumptumbler(threevsa);
#endif
    }
    return (TRUE);
}
```

F and G are **unguarded**. Only Θ checks `threevsa && threesporglset` before calling `insertpm`. This means if Θ is non-empty (both `threevsa` and `threesporglset` non-NULL), the debug else-branch at line 142 is **not** triggered.

---

### 6. `insertpm` with NULL sporglset is a silent no-op

`orglinks.c:75-134`:
```c
bool insertpm(typetask *taskptr, tumbler *orglisa, typeorgl orgl,
    tumbler *vsaptr, typesporglset sporglset)
{
    if (iszerotumbler(vsaptr)) {           // orglinks.c:86 — would return FALSE
        return (FALSE);
    }
    ...
    logbertmodified(orglisa, user);        // orglinks.c:99 — called even with NULL sporglset
    for (; sporglset; sporglset = ...) {   // orglinks.c:100 — loop doesn't execute
        ...
    }
    return (TRUE);                         // orglinks.c:133 — succeeds
}
```

The only guard that could reject the call is `iszerotumbler(vsaptr)`. But `setlinkvsas` (`do2.c:169-183`) sets:
- `fromvsa = 0.1.1` (non-zero)
- `tovsa = 0.2.1` (non-zero)
- `threevsa = 0.3.1` (non-zero)

None of these are zero tumblers. The check never triggers. With NULL sporglset, `insertpm` calls `logbertmodified` (marking the link as modified in the bert table), skips the loop body entirely, and returns TRUE.

---

### 7. `insertendsetsinspanf` similarly no-ops for F and G

`do2.c:116-128`:
```c
bool insertendsetsinspanf(typetask *taskptr, typespanf spanfptr, typeisa *linkisaptr,
    typesporglset fromsporglset, typesporglset tosporglset, typesporglset threesporglset)
{
    if (!(
        insertspanf(taskptr, spanfptr, linkisaptr, fromsporglset, LINKFROMSPAN)   // unguarded
        && insertspanf(taskptr, spanfptr, linkisaptr, tosporglset,  LINKTOSPAN))) // unguarded
            return (FALSE);
    if (threesporglset) {                                                          // guarded
        if (!insertspanf(taskptr, spanfptr, linkisaptr, threesporglset, LINKTHREESPAN))
            return (FALSE);
    }
    return (TRUE);
}
```

`insertspanf` with NULL sporglset (`spanf1.c:15-54`):
```c
for (; sporglset; sporglset = ...) {  // spanf1.c:25 — loop doesn't execute
    ...
}
return (TRUE);   // spanf1.c:53
```

Again: silent no-op, returns TRUE.

---

### Complete call trace for F=∅, G=∅, Θ=non-empty

| Step | Call | Result |
|------|------|--------|
| `fns.c:106-108` | `getcreatelink` | Accepts ∅ for F and G |
| `do1.c:209` | `createorglingranf` | **Link ISA committed to granf** |
| `do1.c:214` | `specset2sporglset(∅)` → `fromsporglset=NULL` | TRUE |
| `do1.c:215` | `specset2sporglset(∅)` → `tosporglset=NULL` | TRUE |
| `do1.c:216` | `specset2sporglset(Θ)` → `threesporglset≠NULL` | TRUE |
| `do1.c:217` | `setlinkvsas(0.1.1, 0.2.1, 0.3.1)` | Non-zero VSAs set |
| `do2.c:132` | `insertpm(link, 0.1.1, NULL)` | No-op (loop skipped), TRUE |
| `do2.c:133` | `insertpm(link, 0.2.1, NULL)` | No-op (loop skipped), TRUE |
| `do2.c:136` | `if (threevsa && threesporglset)` | TRUE, branch taken |
| `do2.c:137` | `insertpm(link, 0.3.1, threesporglset)` | **Θ written to POOM** |
| `do2.c:119` | `insertspanf(link, NULL, LINKFROMSPAN)` | No-op, TRUE |
| `do2.c:120` | `insertspanf(link, NULL, LINKTOSPAN)` | No-op, TRUE |
| `do2.c:122` | `if (threesporglset)` | TRUE, branch taken |
| `do2.c:123` | `insertspanf(link, threesporglset, LINKTHREESPAN)` | **Θ indexed in spanf** |

---

### Conclusion

A link with only Θ populated is **fully allocated and fully committed**. It is not unreachable. The absence of a runtime guard in `acceptablevsa` (`do2.c:110-113` — a pure stub returning TRUE) and in `docreatelink` (`do1.c:195-221`) is not "dead" — it is simply absent. Any client that sends CREATELINK with empty F and G specsets will receive a valid link ISA. The resulting link:

- Exists in **granf** as a LINKATOM object
- Has its ISA copied into the **home document's POOM** at the next available link VSA
- Has **Θ endpoints written** into its own POOM at VSA 0.3.1
- Has **Θ indexed** in the global **spanfilade** as LINKTHREESPAN
- Has **nothing** at LINKFROMSPAN or LINKTOSPAN in the spanfilade

Such a link is structurally opaque to `followlink` for endpoints 1 (F) and 2 (G): `dofollowlink` → `link2sporglset` (`sporgl.c:67-95`) would look up the POOM at V-position `0.whichend` and find no context, returning FALSE. Only following endpoint 3 would succeed. The link exists but is half-blind by design — or by omission.
