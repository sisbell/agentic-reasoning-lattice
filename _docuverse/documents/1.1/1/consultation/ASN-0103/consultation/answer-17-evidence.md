## Question 17 [evidence]

> After creation, is the new document automatically registered in BERT as open with WRITEBERT access for the creating connection, or must the caller issue a separate open?

## KB Synthesis

Not answerable from the KB.

The KB covers BERT's state structure ([SS-BERT]), the `checkforopen` access matrix ([PRE-OPEN-DOC]), and the fact that documents have an explicit open/closed lifecycle ([SS-DOCUMENT-LIFECYCLE]). It also documents that CREATENEWVERSION is atomic — it allocates a new orgl and copies content in a single call ([ST-VERSION-CREATE]).

However, no finding describes what happens to BERT state *at* document creation. The KB records neither that creation auto-registers a WRITEBERT entry nor that it leaves the new document in a closed/unregistered state requiring a separate open. The closest hint is [PRE-OPEN-DOC]'s rule that a "WRITE request on an owned document that is not open → 0 (need to open)," but that speaks to opening pre-existing documents, not the post-creation state.

To answer this definitively, the relevant code path would be `docreatenewversion` or `docreatedocument` in `do1.c`, and the `addtoopen`/`bert.c` interaction immediately after orgl allocation — neither of which appears in the KB findings.

---

## Code Exploration

Now I have the complete picture. Let me compile the full answer.

---

## Answer: BERT Registration After Document Creation

**The short answer:** Neither `createnewdocument` nor `createnewversion` (as standalone FEBE commands) leaves the new document registered in BERT for the creating connection. The caller must issue a separate `open`. The one exception is `open` with `BERTMODECOPY` mode, which creates a new version *and* registers it atomically.

---

### Path 1: `createnewdocument` FEBE command

`fns.c:276-286` dispatches to `docreatenewdocument` at `do1.c:234-241`:

```c
bool docreatenewdocument(typetask *taskptr, typeisa *isaptr)
{
  typehint hint;
  bool createorglingranf();

    makehint (ACCOUNT, DOCUMENT, 0, &taskptr->account, &hint);
    return (createorglingranf (taskptr, granf, &hint, isaptr));
}
```

This calls only `createorglingranf` — no `addtoopen`, no BERT registration whatsoever. The document is allocated and returns its ISA, but the connection is not recorded as having it open. **A separate `open` is required.**

---

### Path 2: `createnewversion` FEBE command

`fns.c:289-300` dispatches to `docreatenewversion` at `do1.c:260-299`. The critical section:

```c
/* Skip doopen ownership check - we just created this document so we own it.
   Add directly to bert table instead. */
addtoopen(newisaptr, user, TRUE, WRITEBERT);     // [do1.c:292]
docopyinternal(taskptr, newisaptr, &vspan.stream, &vspec);
/* Mark as modified so removefromopen doesn't delete the newly created version */
logbertmodified(newisaptr, user);                // [do1.c:295]
doclose(taskptr, newisaptr, user);               // [do1.c:296]
```

The sequence is deliberate:

1. `addtoopen` at `do1.c:292` — opens the new version with `WRITEBERT` *internally*, solely to authorize `docopyinternal` to write into it.
2. `logbertmodified` at `do1.c:295` — marks the entry `modified = TRUE`. This is load-bearing: `removefromopen` at `bert.c:173` checks `bert->created && !bert->modified`; if both true it calls `deleteversion`. The `logbertmodified` call prevents the newly populated document from being deleted when it is closed.
3. `doclose` at `do1.c:296` → `removefromopen` at `bert.c:154` — removes the entry from the BERT hash table entirely.

By the time `docreatenewversion` returns to its FEBE caller at `fns.c:296`, the new document is **not in BERT**. The FEBE `createnewversion` handler never calls `addtoopen`. **A separate `open` is required.**

---

### The One Exception: `doopen` with `BERTMODECOPY`

`bert.c:273-277`:

```c
if (mode == BERTMODECOPY) {
    docreatenewversion(taskptr, tp, &taskptr->account, newtp);
    addtoopen(newtp, connection, TRUE, type);    // [bert.c:275]
    return 1;
}
```

Here the `open` command itself calls `docreatenewversion` (which does its internal open/copy/close cycle), then **immediately calls `addtoopen` again** for the requesting connection. This is the only code path where creation and BERT registration are atomic from the connection's perspective.

---

### Summary Table

| Operation | BERT state after return |
|---|---|
| `createnewdocument` FEBE → `docreatenewdocument` (`do1.c:234`) | Not registered; caller needs `open` |
| `createnewversion` FEBE → `docreatenewversion` (`do1.c:260`) | Internal open/close cycle leaves nothing in BERT; caller needs `open` |
| `open(BERTMODECOPY)` FEBE → `doopen` (`bert.c:264`) | New version is registered with the requested type (`READBERT` or `WRITEBERT`) for the connection |

The design is intentional: bare creation is a pure allocation operation. BERT registration is a separate concern handled explicitly by the `open` protocol command. The internal open in `docreatenewversion` is an implementation detail that authorizes the content-copy, not a grant of access to the caller.
