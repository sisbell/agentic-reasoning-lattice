## Question 17 [evidence]

> Does FINDDOCSCONTAINING enforce BERT/open-document gating on the returned documents (filtering out documents the caller cannot read), or does it return all matching document IDs regardless of access?

## KB Synthesis

The KB does not contain a finding that directly tests or confirms whether FINDDOCSCONTAINING filters results by BERT access level or open-document status. That specific question is not answerable from the KB alone.

However, the KB provides strong architectural evidence that it does **not** apply such filtering:

**FINDDOCSCONTAINING queries the spanf, not through `findorgl`.**

[SS-DOCUMENT-LIFECYCLE] (Finding 0027b) explicitly partitions operations into two classes:
> Operations that work through I-address lookup (e.g., `find_links` via span-f) **do not require the referenced document to be open**. Operations that resolve V→I mappings within a specific document orgl (e.g., `retrieve_contents` via `findorgl`) **do require it to be open.**

[SS-BERT] (Finding 0014) establishes that BERT gating happens inside `findorgl`/`checkforopen`. FINDDOCSCONTAINING is implemented as `finddocscontainingsp` — a pure spanf query [SS-DOCISPAN], [SS-SPANF-OPERATIONS] — which never calls `findorgl`.

[FC-CONTENT-SPANF-ISOLATION] (Finding 0012) further confirms that spanf operations are structurally isolated from the granf/orgl machinery where BERT lives.

**Conclusion:** Based on KB architecture, FINDDOCSCONTAINING returns all matching document ISAs from the spanf index with no BERT or open-document filtering. A caller discovering a document via FINDDOCSCONTAINING would still need to open it (and satisfy BERT preconditions) before `retrieve_contents` on that document would succeed.

---

## Code Exploration

Now I have complete, verified citations. Here is the full answer.

---

## Does FINDDOCSCONTAINING Enforce BERT/Open-Document Gating?

**No. FINDDOCSCONTAINING explicitly bypasses access control and returns all matching document IDs regardless of whether the caller has any open-document relationship with them.**

---

### Full Execution Path

**1. FEBE handler — `backend/fns.c:20-29`**

```c
void finddocscontaining(typetask *taskptr)
{
  ...
  if (   getfinddocscontaining (taskptr, &specset)
      && dofinddocscontaining (taskptr, specset, &addressset))
          putfinddocscontaining (taskptr, (typeitemset)addressset);
}
```

The handler calls `dofinddocscontaining`. No access check here.

---

**2. Core dispatch — `backend/do1.c:15-23`**

```c
bool dofinddocscontaining(typetask *taskptr, typespecset specset, typelinkset *addresssetptr)
{
  typeispanset ispanset;
  bool specset2ispanset(), finddocscontainingsp();

    return (
       specset2ispanset (taskptr, specset, &ispanset, NOBERTREQUIRED)   // line 21
    && finddocscontainingsp (taskptr, ispanset, addresssetptr));         // line 22
}
```

The critical flag is `NOBERTREQUIRED` passed to `specset2ispanset`. This value is defined at `backend/common.h:165`:

```c
#define NOBERTREQUIRED 0
```

---

**3. The gating function — `backend/granf1.c:16-41`**

`specset2ispanset` internally calls `findorgl`, which is the single chokepoint where BERT is checked:

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
  int temp;
    if (/*backenddaemon &&*/(temp = checkforopen(isaptr, type, user)) <= 0) {
        // ACCESS DENIED — returns FALSE
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);   // line 39
    return (*orglptr ? TRUE : FALSE);
}
```

`findorgl` calls `checkforopen` and only proceeds if the return value is `> 0`. With `type == NOBERTREQUIRED`, see what `checkforopen` does.

---

**4. The bypass — `backend/bert.c:52-61`**

```c
int checkforopen(tumbler *tp, int type, int connection)
{
  ...
  if (type == NOBERTREQUIRED) {
    return 1;   /* Random > 0 */     // line 60
  }
  // ... actual BERT table lookup only reached when type != NOBERTREQUIRED
}
```

When `type == NOBERTREQUIRED`, `checkforopen` returns `1` immediately — without consulting the BERT table at all. The condition in `findorgl` (`<= 0`) is false, so the denial path is skipped and the document's orgl is fetched unconditionally.

---

**5. Result collection — `backend/spanf1.c:151-188`**

`finddocscontainingsp` iterates all matching ispans, retrieves every document ID from the spanfilade via `retrieverestricted`, and appends them to the result set. There is **no per-document access check** in this loop — it adds every document it finds:

```c
for (; ispanset; ispanset = ispanset->next) {
    context = retrieverestricted(...);
    for (c = context; c; c = c->nextcontext) {
        movetumbler (&c->totaloffset.dsas[ORGLRANGE], &docid);
        beheadtumbler (&docid, &document.address);
        if (isinlinklist(*headptr, &document.address))
            continue;                          // dedup only, no auth check
        ...
        addresssetptr = onitemlist(...);
    }
}
```

---

### Conclusion

**FINDDOCSCONTAINING does not enforce BERT gating.** The access control gate (`checkforopen` in `granf1.c:22`) is present in the code path, but it is deliberately bypassed by passing `NOBERTREQUIRED` at `do1.c:21`. `checkforopen` short-circuits at `bert.c:59-60` and returns success without touching the BERT table. The subsequent `finddocscontainingsp` at `spanf1.c:151-188` performs no additional per-document authorization checks.

This appears intentional: the commented-out `/*backenddaemon &&*/` guard in `granf1.c:22` suggests the access-control path was once gated on a daemon mode flag, and the overall design treats `NOBERTREQUIRED` as a first-class bypass mechanism used uniformly across query operations (`do1.c:21, 54, 74, 75`). A caller can discover the existence of any document whose content matches the search spec, regardless of whether they have opened it for reading or writing.
