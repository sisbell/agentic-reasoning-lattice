## Question 17 [evidence]

> Can a single RETRIEVECONTENTS SpecSet span multiple documents, and if so does it honor FC-DOC-ISOLATION by reading each target document's POOM independently?

## KB Synthesis

Yes on both counts, with an important nuance.

**Multi-document SpecSets are supported**

[SS-SPECSET] states explicitly: "A SpecSet can contain VSpecs referencing different documents and non-contiguous regions within the same document... The cross-document capability means SpecSet operations are not scoped to a single document." The VSpec ordering is preserved in the result — content is concatenated in SpecSet order regardless of which documents the spans come from [INV-SPECSET-ORDER].

**FC-DOC-ISOLATION is honored at the POOM-read layer**

The `doretrievev` call chain is: `specset → specset2ispanset → findorgl (per document) → I-spans → ispanset2vstuffset` [PRE-RETRIEVE-CONTENTS, Finding 0010]. The `findorgl` call is invoked separately for each document orgl referenced in the SpecSet. Each document has its own POOM tree, so V→I resolution is isolated per document — reading document A's POOM cannot affect document B's POOM [SS-POOM-MUTABILITY].

**The permascroll lookup is global**

After per-document V→I conversion, all collected I-spans are passed together to `ispanset2vstuffset(granf, ...)`, which is a single global permascroll lookup. This is not a violation of FC-DOC-ISOLATION because the permascroll (granfilade) is read-only and append-only [INV-IADDR-IMMUTABILITY]; no document's content can be mutated by the lookup.

**Preconditions that apply across all referenced documents**

Two preconditions must hold for every document in the SpecSet:

1. **Open-doc requirement**: Every referenced document must be in the session's open-doc set. If any document is closed, `findorgl` returns FALSE and the operation fails [PRE-RETRIEVE-CONTENTS, Finding 0027].
2. **Subspace requirement**: All V-addresses must be in the text subspace (1.x). If any VSpec in any document resolves to a link-subspace position, the resulting link-orgl ISA is passed to the permascroll lookup, producing garbage or NULL silently [PRE-RETRIEVE-CONTENTS, Finding 0010; PRE-VCOPY].

---

## Code Exploration

All key lines are verified. Here is the complete answer.

---

## Can a Single RETRIEVECONTENTS SpecSet Span Multiple Documents?

**Yes.** And FC-DOC-ISOLATION is honored at the **POOM level** but **not** at the crum-level homedoc filter. Here is the full trace.

---

### 1. Entry Point — `fns.c:175–187`

```c
void retrievev(typetask *taskptr)
{
    typespecset specset;
    typevstuffset vstuffset;
    bool getretrievev(), doretrievev();

    if (getretrievev(taskptr, &specset)
     && doretrievev(taskptr, specset, &vstuffset))
        putretrievev(taskptr, &vstuffset);
    else
        putrequestfailed(taskptr);
}
```

`retrievev` is the RETRIEVECONTENTS handler. It passes the entire SpecSet — unmodified — to `doretrievev`, which delegates to `specset2ispanset`.

---

### 2. Multi-Document Loop — `do2.c:14–46`

```c
bool specset2ispanset(typetask *taskptr, typespec *specset,
                      typeispanset *ispansetptr, int type)
{
    typeorgl docorgl;
    ...
    *ispansetptr = NULL;
    for (; specset; specset = (typespec *)((typeitemheader *)specset)->next) {  // :23 — iterate every item
        if (((typeitemheader *)specset)->itemid == ISPANID) {
            ...
        } else if (((typeitemheader *)specset)->itemid == VSPECID) {
            if (iszerotumbler(&((typevspec *)specset)->docisa))   // :28
                qerror("retrieve called with docisa 0\n");
            if (!(
              findorgl(taskptr, granf, &((typevspec *)specset)->docisa, &docorgl, type)  // :35
           && (ispansetptr = vspanset2ispanset(taskptr, docorgl,             // :36
                ((typevspec *)specset)->vspanset, ispansetptr))))
                return (FALSE);
        }
    }
    return (TRUE);
}
```

**A SpecSet is a linked list of items.** Each `VSPECID` item carries its own `docisa` (document tumbler). The loop processes them one at a time:

- **do2.c:35** — `findorgl()` is called **per VSPEC**, passing that VSPEC's `docisa`. This is where document access control fires.
- **do2.c:36** — `vspanset2ispanset()` is called with the POOM (`docorgl`) returned for **that specific document**. A different document's POOM is never touched here.

A SpecSet with three VSPECs pointing to three different documents will call `findorgl()` three times with three different `docisa` values.

---

### 3. Document Access Control — `granf1.c:17–41`

```c
bool findorgl(typetask *taskptr, typegranf granfptr,
              typeisa *isaptr, typeorgl *orglptr, int type)
{
    int temp;
    if ((temp = checkforopen(isaptr, type, user)) <= 0) {  // :22 — BERT check
        if (!isxumain) { ...; return FALSE; }
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);  // :39 — fetch this document's POOM
    return (*orglptr ? TRUE : FALSE);
}
```

- **granf1.c:22** — `checkforopen()` enforces that the caller has the document open (the BERT access model). This runs **per document**, per VSPEC.
- **granf1.c:39** — `fetchorglgr()` retrieves that document's enfilade root. Each document gets its own `orgl`.

---

### 4. V→I Coordinate Translation — `orglinks.c:397–454`

```c
typeispanset *vspanset2ispanset(..., typeorgl orgl, typevspanset vspanptr, ...)
{
    return permute(taskptr, orgl, vspanptr, V, ispansetptr, I);  // :401
}
```

`permute` iterates each vspan in the set (`orglinks.c:414`) and calls `span2spanset` for each one, passing the same single-document `orgl`.

```c
typespanset *span2spanset(typetask *taskptr, typeorgl orgl, ...)
{
    context = retrieverestricted(
        (typecuc*)orgl, restrictionspanptr, restrictionindex,
        (typespan*)NULL, targindex,
        (typeisa*)NULL);   // :435 — docisaptr is always NULL here
    ...
}
```

**Critical: `orglinks.c:435` passes `(typeisa*)NULL` as `docisaptr`.** This is the only call site for `retrieverestricted` in the V→I path.

---

### 5. The Homedoc Guard — `retrie.c:56–85` and `retrie.c:270–304`

```c
typecontext *retrieverestricted(..., typeisa *docisaptr)
{
    ...
    if (docisaptr) {
        movetumbler(docisaptr, &info.homedoc);  // :78
        infoptr = &info;
    } else {
        infoptr = NULL;                          // :81 — fired every time from RETRIEVEV
    }
    temp = retrieveinarea(..., (typebottomcruminfo*)infoptr);
    return(temp);
}
```

Because `docisaptr` is NULL, `infoptr` is always NULL during RETRIEVECONTENTS. That null propagates into `crumqualifies2d`:

```c
bool crumqualifies2d(..., type2dbottomcruminfo *infoptr)
{
    if ((crumptr->height == 0) && infoptr            // :274 — guard on infoptr
     && !tumblereq(&infoptr->homedoc,
                   &(((type2dcbc *)crumptr)->c2dinfo.homedoc))) {
        return (FALSE);  // homedoc mismatch — reject crum
    }
    ...
}
```

**`retrie.c:274`: the `infoptr &&` guard means the homedoc filter is completely bypassed when `infoptr` is NULL.** This filter is never active during a normal RETRIEVECONTENTS call.

---

## Summary

| Question | Answer | Evidence |
|---|---|---|
| Can a SpecSet span multiple documents? | **Yes** | `do2.c:23` — the loop iterates every VSPEC; each carries its own `docisa` |
| Is each document's POOM read independently? | **Yes** | `do2.c:35–36` — `findorgl()` + `vspanset2ispanset()` called per-VSPEC with that doc's tumbler |
| Is the BERT access check applied per document? | **Yes** | `granf1.c:22` — `checkforopen()` fires for every document in the loop |
| Is the crum-level `homedoc` filter active? | **No** | `orglinks.c:435` passes `NULL` → `retrie.c:81` sets `infoptr=NULL` → `retrie.c:274` skips the filter |

**FC-DOC-ISOLATION is honored at the organizational (POOM) level**: each document's enfilade is fetched and queried independently, gated by `checkforopen`. It is **not** enforced at the crum-leaf level via the `homedoc` field — that guard code exists in `crumqualifies2d` but is structurally dormant during RETRIEVECONTENTS because the call chain never supplies a non-NULL `docisaptr`. The isolation is structural (each POOM is one document) rather than filter-based (comparing `homedoc` tumblers per crum).
