## Question 1 [evidence]

> When RETRIEVEDOCVSPANSET is called on an unallocated or nonexistent document id, what does the implementation do — return empty, signal an error, or fault?

## KB Synthesis

The KB does not contain a finding that directly tests or documents RETRIEVEDOCVSPANSET behavior on a nonexistent document ID.

The closest evidence available:

- **[SS-VSPAN-VS-VSPANSET]** (Finding 0035) notes that for an *existing but empty* document, RETRIEVEDOCVSPANSET returns NULL (empty set).
- **[PRE-RETRIEVE-CONTENTS]** / **[SS-DOCUMENT-LIFECYCLE]** (Finding 0027) describe the `findorgl` path: if a document exists in the granfilade but is not open, operations that resolve V→I mappings fail with a backend error. But RETRIEVEDOCVSPANSET uses `retrievevspansetpm` / `retrievedocumentpartofvspanpm` ([SS-DUAL-ENFILADE], Finding 0043) which reads the root crum directly — the KB does not document whether this path goes through `findorgl`.
- **[EC-ERROR-ABORT]** (Finding 0011) establishes that invariant violations abort via `qerror`, but whether a bad document ID triggers this vs. a clean error return is unspecified.

The question — crash, empty result, or error signal — is **not answerable from the KB as currently constituted**. A targeted finding probing RETRIEVEDOCVSPANSET with a never-allocated tumbler would be needed.

---

## Code Exploration

All key lines verified. Here is the complete trace.

---

## RETRIEVEDOCVSPANSET on a Nonexistent Document ID

**Answer: The backend signals an error to the client — it outputs `?` and does not crash.**

---

### Call Chain

**`fns.c:129–141`** — dispatcher `retrievedocvspanset`:

```c
void retrievedocvspanset(typetask *taskptr)
{
  typeisa docisa;
  typevspanset vspanset;
  bool getretrievedocvspanset(), doretrievedocvspanset();

    if (
       getretrievedocvspanset (taskptr, &docisa)
    && doretrievedocvspanset (taskptr, &docisa, &vspanset))
        putretrievedocvspanset (taskptr, &vspanset);
      else
        putrequestfailed (taskptr);
}
```

The pattern is: parse input → do operation → put result, or else put failure. If either side of the `&&` returns FALSE, `putrequestfailed` is called.

---

**`do1.c:322–336`** — `doretrievedocvspanset`:

```c
bool doretrievedocvspanset(typetask *taskptr, typeisa *docisaptr, typevspanset *vspansetptr)
{
  typeorgl docorgl;
  bool findorgl(), isemptyorgl(), retrievevspansetpm();

    if (!findorgl (taskptr, granf, docisaptr, &docorgl, READBERT))
        return FALSE;

    if (isemptyorgl (docorgl)) {
        *vspansetptr = NULL;  /* Empty document returns empty vspanset */
        return TRUE;
    }

    return retrievevspansetpm (taskptr, docorgl, vspansetptr);
}
```

The first guard at `do1.c:327` calls `findorgl` with access type `READBERT`. For a nonexistent document, this returns FALSE, and the function returns FALSE at `do1.c:328` without reaching the empty-check or retrieval.

---

**`granf1.c:17–41`** — `findorgl`:

```c
bool
findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{
  typeorgl fetchorglgr();
  int temp;

    if (/*backenddaemon &&*/(temp = checkforopen(isaptr, type, user)) <= 0) {
#ifndef DISTRIBUTION
        if (!isxumain) {
            fprintf(stderr,"orgl for ");
            dumptumbler(isaptr);
            fprintf(stderr," not open in findorgl temp = %d\n",temp);
            return FALSE;
            /*gerror("Temporary crash in findorgl\n");*/
            /* ECH ?? or should I simply return FALSE? */
        }
#else
        if (!isxumain) {
            *orglptr = NULL;
            return FALSE;
        }
#endif
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);
    return (*orglptr ? TRUE : FALSE);
}
```

Two code paths depending on the build:

- **Debug (`#ifndef DISTRIBUTION`)**: prints a diagnostic to `stderr` then returns FALSE. The commented-out `gerror(...)` and the `ECH ??` note are historical — an early design question about whether to crash vs. return FALSE. The decision was made to return FALSE.
- **Production (`#else`)**: silently sets `*orglptr = NULL` and returns FALSE.

In both cases `isxumain` is FALSE for a normal backend connection, so the return-FALSE path fires.

---

**`bert.c:52–87`** — `checkforopen`:

```c
/*  checkforopen
    Returns:  >0 for sufficiently open
            integer indicates type of open
          0 if open required
         -1 if new version should be made

    Open state -->
    type           Not Open          Open READ         Open WRITE
      |        !owned | owned    conn== |conn!=    conn== |conn!=
      v        -------+------   -------+-------   -------+-------
    READ          0   |   0     READ   |   0      WRITE  | -1
*/
int checkforopen(tumbler *tp, int type, int connection)
{
  conscell *p;
  bertentry *bert;
  int foundnonread = FALSE;

  if (type == NOBERTREQUIRED) { return 1; }

  for (p = berttable[hashoftumbler(tp)]; p && p->stuff; p = p->next) {
    bert = p->stuff;
    if (tumblereq(tp, &bert->documentid)) { ... }
  }

  if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {
    return 0;
  } else {
    return -1;
  }
}
```

For a nonexistent document:
- The hash-table loop at `bert.c:63` finds no matching `bertentry`
- `foundnonread` remains FALSE
- The condition at `bert.c:81` is `!FALSE && (READBERT == READBERT)` → TRUE → **returns 0**

The comment table confirms this: READBERT on a Not Open, !owned document → 0 ("open required"). The guard in `findorgl` at `granf1.c:22` is `temp <= 0`, so 0 triggers it.

---

**`put.c:248–251`** — `putrequestfailed`:

```c
int putrequestfailed(typetask *taskptr)
{
        fprintf (taskptr->outp,"?\n");
}
```

A single `?` character followed by newline is sent to the client output stream. This is the standard FEBE protocol error marker.

---

### Summary

| Step | Location | Outcome |
|------|----------|---------|
| `getretrievedocvspanset` reads the tumbler ID | `get1.c:82` | Returns TRUE — any tumbler is syntactically valid |
| `doretrievedocvspanset` calls `findorgl(…, READBERT)` | `do1.c:327` | Guard fires on FALSE return |
| `findorgl` calls `checkforopen`, gets 0 (open required) | `granf1.c:22` | `temp <= 0` triggers the failure branch |
| `checkforopen` finds no bert table entry | `bert.c:63–82` | Returns 0 for READBERT on unregistered document |
| `findorgl` returns FALSE (production: silently; debug: stderr diagnostic) | `granf1.c:33–35` | `*orglptr = NULL` |
| `doretrievedocvspanset` returns FALSE | `do1.c:328` | Short-circuits |
| Dispatcher calls `putrequestfailed` | `fns.c:140` | Outputs `?` to client |

**The backend does not fault.** There is a commented-out `gerror("Temporary crash in findorgl\n")` at `granf1.c:29` that shows a crash was considered during development — the `ECH ??` comment records that uncertainty — but the current code returns FALSE cleanly. **It also does not return empty results;** an empty vspanset (`NULL` with TRUE return) only occurs for a document that exists but is empty, via `do1.c:330–332`. A nonexistent document never reaches that branch.
