## Question 17 [evidence]

> Does RETRIEVEDOCVSPAN require the document to be in the caller's open-document list (BERT-gated via findorgl), and does it fail silently returning nothing if the document is not open?

## KB Synthesis

The KB provides partial but not complete coverage of this question.

**What the KB establishes:**

RETRIEVEDOCVSPAN (opcode 14) reads the raw root node's V-dimension displacement and width via `retrievevspanpm()` at `orglinks.c:165-172` — described as "no processing, no subspace awareness," just a raw root copy [SS-VSPAN-VS-VSPANSET, Finding 0035].

On the general open-document requirement, [SS-DOCUMENT-LIFECYCLE] distinguishes two operation classes: those that work through I-address lookup (span-f queries, `find_links`) which do NOT require the document to be open, versus those that resolve V→I mappings within a specific document orgl via `findorgl` (e.g., `retrieve_contents`) which DO require it. [PRE-RETRIEVE-CONTENTS] confirms `retrieve_contents` fails with a backend error when the target document is closed.

**What the KB does not answer:**

The KB does not explicitly state whether `retrievevspanpm()` calls `findorgl` internally or accesses the enfilade tree through a different path. RETRIEVEDOCVSPAN does need to access the document orgl's root node, which suggests orgl access, but the KB contains no direct evidence about its behavior when the document is closed — whether it errors, fails silently, or succeeds without an open requirement.

This is not answerable from the KB as written. The code at `orglinks.c:165-172` would need to be inspected directly.

---

## Code Exploration

I have all the information needed. Here is the complete, fully-cited answer.

---

## Does RETRIEVEDOCVSPAN require the document to be open?

**Yes — unambiguously.** `doretrievedocvspan` calls `findorgl` with `READBERT`, which invokes `checkforopen`, which checks the `berttable[]` open-document list. If the document is not open by the caller's connection, `findorgl` returns `FALSE` and the handler sends `"?\n"` (not silence — but no span data).

---

### The full call chain, with exact citations

#### 1. `fns.c:303–314` — FEBE handler `retrievedocvspan`

```c
void retrievedocvspan(typetask *taskptr)       /* fns.c:303 */
{
  typeisa docisa;
  typevspan vspan;
  bool getretrievedocvspan(), doretrievedocvspan();

    if (
       getretrievedocvspan (taskptr, &docisa)  /* fns.c:310 */
    && doretrievedocvspan (taskptr, &docisa, &vspan))  /* fns.c:311 */
        putretrievedocvspan (taskptr, &vspan); /* fns.c:312 — success */
      else
        putrequestfailed (taskptr);            /* fns.c:314 — failure */
}
```

Short-circuit AND: if `doretrievedocvspan` returns `FALSE`, the else branch fires.

---

#### 2. `do1.c:312–320` — `doretrievedocvspan`

```c
bool doretrievedocvspan(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{                                                       /* do1.c:312 */
  typeorgl docorgl;
  bool findorgl(), retrievevspanpm();

    return
       findorgl (taskptr, granf, docisaptr, &docorgl, READBERT)  /* do1.c:318 */
    && retrievevspanpm (taskptr, docorgl, vspanptr);             /* do1.c:319 */
}
```

`READBERT = 1` [common.h:166]. The `READBERT` flag is what triggers the BERT gate inside `findorgl`.

---

#### 3. `granf1.c:16–41` — `findorgl` (the BERT gate)

```c
bool findorgl(typetask *taskptr, typegranf granfptr, typeisa *isaptr, typeorgl *orglptr, int type)
{                                                                 /* granf1.c:17 */
  typeorgl fetchorglgr();
  int temp;

    if (/*backenddaemon &&*/(temp = checkforopen(isaptr, type, user)) <= 0) {  /* granf1.c:22 */
#ifndef DISTRIBUTION
        if (!isxumain) {
            fprintf(stderr,"orgl for ");
            dumptumbler(isaptr);
            fprintf(stderr," not open in findorgl temp = %d\n",temp);
            return FALSE;                /* granf1.c:28 — debug build */
        }
#else
        if (!isxumain) {
            *orglptr = NULL;             /* granf1.c:34 */
            return FALSE;                /* granf1.c:35 — distribution build */
        }
#endif
    }
    *orglptr = fetchorglgr(taskptr, granfptr, isaptr);  /* granf1.c:39 */
    return (*orglptr ? TRUE : FALSE);                   /* granf1.c:40 */
}
```

**Guard:** if `checkforopen` returns `<= 0`, and the caller is not the internal daemon (`isxumain`), then `findorgl` returns `FALSE` without ever calling `fetchorglgr`. The `backenddaemon &&` prefix is commented out, meaning the BERT check always fires.

---

#### 4. `bert.c:52–87` — `checkforopen`: what actually gates on the open list

```c
int checkforopen(tumbler *tp, int type, int connection)  /* bert.c:52 */
{
  conscell *p;
  bertentry *bert;
  int foundnonread = FALSE;

  if (type == NOBERTREQUIRED) {           /* bert.c:59 */
    return 1;	/* Random > 0 */           /* bert.c:60 — bypasses all BERT checks */
  }

  for (p = berttable[hashoftumbler(tp)]; p && p->stuff; p = p->next) {  /* bert.c:63 */
    bert = p->stuff;
    if (tumblereq(tp, &bert->documentid)) {
      if (connection == bert->connection) {          /* bert.c:66 — must be THIS connection */
        switch (bert->type) {
          case READBERT:
            return (type == READBERT) ? READBERT : -1;  /* bert.c:69 — passes for READBERT */
          case WRITEBERT:
            return WRITEBERT;                           /* bert.c:71 — also passes */
        }
      } else {
          if (bert->type != READBERT) {
            foundnonread = TRUE;                        /* bert.c:75 — doc open WRITE by other */
          }
      }
    }
  }

  if (!foundnonread && (type == READBERT || isthisusersdocument(tp))) {  /* bert.c:81 */
    return 0;    /* "open required" — still fails the <= 0 guard */      /* bert.c:82 */
  } else {
    return -1;   /* "new version needed" — also fails */                 /* bert.c:84 */
  }
}
```

The `berttable[]` is a hash table [bert.c:29] of `bertentry` structs, each recording `connection`, `documentid`, and `type` [bert.c:13–19].

The comment block at `bert.c:37–50` summarizes all return values in a table:

```
type=READ, Not Open (!owned or owned) → 0        ← fails guard (<=0)
type=READ, Open READ, same connection → READBERT  ← passes guard (>0)
type=READ, Open READ, diff connection → 0         ← fails guard
type=READ, Open WRITE, same connection → WRITEBERT ← passes guard (>0)
type=READ, Open WRITE, diff connection → -1       ← fails guard
```

Key implication: even if the document is open for READ by *another* connection, `checkforopen` returns `0` — which still fails the `<= 0` guard. Only the **caller's own connection** opening the document passes.

---

#### 5. `put.c:248–251` — what `putrequestfailed` actually sends

```c
int putrequestfailed(typetask *taskptr)  /* put.c:248 */
{
    fprintf (taskptr->outp,"?\n");       /* put.c:250 */
}
```

The caller receives `"?\n"` — **not silence**. But there is no span data whatsoever.

---

### Contrast: the "kluge" internal variant bypasses BERT

`doretrievedocvspanfoo` [do1.c:301–309] exists for internal use (called by `docreatenewversion` at do1.c:281):

```c
bool doretrievedocvspanfoo(typetask *taskptr, typeisa *docisaptr, typevspan *vspanptr)
{/* this routine is a kluge not yet kluged*/             /* do1.c:301 */
    return (
       findorgl (taskptr, granf, docisaptr, &docorgl, NOBERTREQUIRED)  /* do1.c:307 */
    && retrievedocumentpartofvspanpm (taskptr, docorgl, vspanptr) );
}
```

`NOBERTREQUIRED = 0` [common.h:165] causes `checkforopen` to immediately return `1` [bert.c:59–60], bypassing the entire BERT table lookup. This internal path is not accessible through the FEBE interface.

---

### Summary

| Question | Answer |
|---|---|
| Does RETRIEVEDOCVSPAN require the document to be in the caller's open-document list? | **Yes.** `doretrievedocvspan` passes `READBERT` to `findorgl` [do1.c:318], which calls `checkforopen` [granf1.c:22], which checks `berttable[]` [bert.c:63]. |
| Must it be THIS connection's open, not another connection's? | **Yes.** [bert.c:66] `connection == bert->connection` — another connection's open returns `0` (guard trips). |
| Does it fail silently? | **Not silently** — `putrequestfailed` sends `"?\n"` [put.c:250]. But no span data is returned. |
| Is there a bypass path? | **Yes, internal only.** `doretrievedocvspanfoo` uses `NOBERTREQUIRED` [do1.c:307], bypassing BERT entirely. Not reachable via FEBE. |
